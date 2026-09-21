#!/usr/bin/env python3
"""Pindarian Pyramids - build, install, package and release in one command.

    python manage.py install          build, validate, and install into Foundry
    python manage.py package          build, validate, and write dist/
    python manage.py release 2.4.2    bump the version, build, package, tag, publish
    python manage.py watch            rebuild and reinstall whenever source changes

Run it from the `project/` directory.

Why this exists
---------------
Copying a built module over an existing install does not work for Foundry
compendium packs. Foundry opens each pack read-write and leaves `.ldb`, `LOG`,
`LOCK` and `MANIFEST-*` files behind. If those survive an update, LevelDB can
replay the *old* manifest and serve stale content, which looks exactly like the
build having silently failed. `install` therefore removes the module directory
before copying, and refuses to touch a directory that is not ours.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent
BUILD = ROOT / "build" / "pindarian-pyramids"
DIST = ROOT / "dist"
MODULE_ID = "pindarian-pyramids"
REPOSITORY = "macv0223/pindarian-pyramids"

# Files shipped inside the zip. Everything is at the archive root: a wrapper
# folder of the same name is wrong and Foundry will reject it.
SHIPPED = ("assets", "packs", "source", "styles", "module.json", "README.md", "LICENSE.md", "CHANGELOG.md")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def run(*command: str) -> None:
    result = subprocess.run(command, cwd=PROJECT)
    if result.returncode:
        sys.exit(result.returncode)


def current_version() -> str:
    text = (PROJECT / "build_module.py").read_text(encoding="utf-8")
    match = re.search(r'^VERSION = "([^"]+)"', text, re.M)
    if not match:
        sys.exit("Could not find VERSION in build_module.py")
    return match.group(1)


def build() -> str:
    """Build and validate. Returns the version that was built."""
    run(sys.executable, "build_module.py")
    run(sys.executable, "validate_module.py")
    return current_version()


def foundry_data_dir(override: str | None = None) -> Path:
    """Locate the Foundry user data directory.

    Order: --data, then $FOUNDRY_DATA, then the platform default.
    """
    explicit = override or os.environ.get("FOUNDRY_DATA")
    if explicit:
        path = Path(explicit).expanduser()
        # A typo here would otherwise install into a brand new tree and look
        # like a success, so insist the directory exists and looks like Foundry.
        if not path.is_dir():
            sys.exit(f"{path} does not exist.")
        if not any((path / name).is_dir() for name in ("modules", "systems", "worlds")):
            sys.exit(
                f"{path} does not look like a Foundry data directory.\n"
                "It should be the folder containing modules/, systems/ and worlds/."
            )
        return path

    system = platform.system()
    candidates: list[Path] = []
    if system == "Windows":
        local = os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local"))
        candidates.append(Path(local) / "FoundryVTT/Data")
    elif system == "Darwin":
        candidates.append(Path.home() / "Library/Application Support/FoundryVTT/Data")
    else:
        candidates.append(Path.home() / ".local/share/FoundryVTT/Data")
        candidates.append(Path.home() / "foundrydata/Data")
    candidates.append(Path.home() / "FoundryVTT/Data")

    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    sys.exit(
        "Could not find your Foundry data directory. Pass it explicitly:\n"
        "  python manage.py install --data \"/path/to/FoundryVTT/Data\"\n"
        "or set FOUNDRY_DATA once and forget about it."
    )


def is_our_module(target: Path) -> bool:
    """Only ever delete a directory that is this module."""
    manifest = target / "module.json"
    if not manifest.is_file():
        return False
    try:
        return json.loads(manifest.read_text(encoding="utf-8")).get("id") == MODULE_ID
    except (json.JSONDecodeError, OSError):
        return False


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def cmd_install(args: argparse.Namespace) -> None:
    version = build() if not args.no_build else current_version()
    data = foundry_data_dir(args.data)
    target = data / "modules" / MODULE_ID

    if target.exists():
        if not is_our_module(target):
            sys.exit(
                f"{target} exists but is not {MODULE_ID}. Refusing to delete it.\n"
                "Move it aside and run this again."
            )
        # Full removal, not an overwrite: see the note at the top of this file.
        shutil.rmtree(target)
        action = "Updated"
    else:
        action = "Installed"

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(BUILD, target)

    size = sum(path.stat().st_size for path in target.rglob("*") if path.is_file())
    print(f"{action} {MODULE_ID} {version} -> {target}  ({size / 1_048_576:.0f} MB)")
    print("Restart Foundry, or return to Setup and re-enter your world, to pick it up.")


def cmd_package(args: argparse.Namespace) -> None:
    version = build() if not args.no_build else current_version()
    DIST.mkdir(exist_ok=True)
    archive = DIST / f"{MODULE_ID}.zip"
    manifest = DIST / "module.json"

    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for entry in SHIPPED:
            source = BUILD / entry
            if source.is_dir():
                for path in sorted(source.rglob("*")):
                    if path.is_file():
                        bundle.write(path, path.relative_to(BUILD))
            elif source.is_file():
                bundle.write(source, source.name)
            else:
                print(f"  warning: {entry} not found in the build, skipping")
    shutil.copy2(BUILD / "module.json", manifest)

    print(f"Packaged {MODULE_ID} {version}")
    print(f"  {archive}  ({archive.stat().st_size / 1_048_576:.0f} MB)")
    print(f"  {manifest}")
    print("\nAttach BOTH files to the release, with exactly these names, and mark it Latest.")


def bump_version(new: str) -> None:
    """Rewrite VERSION and the validator's pin together."""
    if not re.fullmatch(r"\d+\.\d+\.\d+", new):
        sys.exit(f"'{new}' is not a version number like 2.4.2")
    old = current_version()

    build_file = PROJECT / "build_module.py"
    text = build_file.read_text(encoding="utf-8")
    text = text.replace(f'VERSION = "{old}"', f'VERSION = "{new}"', 1)
    build_file.write_text(text, encoding="utf-8")

    validator = PROJECT / "validate_module.py"
    text = validator.read_text(encoding="utf-8")
    text = text.replace(f'== "{old}"', f'== "{new}"', 1)
    validator.write_text(text, encoding="utf-8")
    print(f"Version {old} -> {new}")


def cmd_release(args: argparse.Namespace) -> None:
    if args.version:
        bump_version(args.version)
    version = current_version()

    if not (PROJECT / "build_module.py").read_text(encoding="utf-8").count(f"\n## {version}\n"):
        print(f"  warning: CHANGELOG has no '## {version}' section yet")

    cmd_package(argparse.Namespace(no_build=False))

    tag = f"v{version}"
    if args.dry_run:
        print(f"\nDry run. To publish:\n  gh release create {tag} ...")
        return

    if not shutil.which("gh"):
        print(
            "\nGitHub CLI not found. Publish manually:\n"
            f"  1. Create a release tagged {tag} on {REPOSITORY}\n"
            f"  2. Attach dist/{MODULE_ID}.zip and dist/module.json\n"
            "  3. Mark it Latest"
        )
        return

    notes = f"Pindarian Pyramids {version}. See CHANGELOG.md for the full list of changes."
    run("gh", "release", "create", tag,
        str(DIST / f"{MODULE_ID}.zip"), str(DIST / "module.json"),
        "--repo", REPOSITORY, "--title", f"Pindarian Pyramids {version}",
        "--notes", notes, "--latest")
    print(f"\nPublished {tag} to {REPOSITORY}")


def cmd_watch(args: argparse.Namespace) -> None:
    watched = [PROJECT / "build_module.py", PROJECT / "pindarian_content.py", PROJECT / "source"]

    def fingerprint() -> dict[str, float]:
        stamps: dict[str, float] = {}
        for entry in watched:
            paths = entry.rglob("*") if entry.is_dir() else [entry]
            for path in paths:
                if path.is_file():
                    stamps[str(path)] = path.stat().st_mtime
        return stamps

    print("Watching source, build_module.py and pindarian_content.py. Ctrl-C to stop.")
    last = fingerprint()
    while True:
        try:
            time.sleep(1.5)
            now = fingerprint()
            if now != last:
                last = now
                print("\n--- change detected ---")
                try:
                    cmd_install(argparse.Namespace(no_build=False, data=args.data))
                except SystemExit as stop:
                    if stop.code:
                        print("build failed; still watching")
        except KeyboardInterrupt:
            print("\nStopped.")
            return


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    subcommands = parser.add_subparsers(dest="command", required=True)

    install = subcommands.add_parser("install", help="build and install into Foundry")
    install.add_argument("--data", help="Foundry user data directory")
    install.add_argument("--no-build", action="store_true", help="install the existing build")
    install.set_defaults(func=cmd_install)

    package = subcommands.add_parser("package", help="build and write dist/ for a release")
    package.add_argument("--no-build", action="store_true", help="package the existing build")
    package.set_defaults(func=cmd_package)

    release = subcommands.add_parser("release", help="bump, package and publish")
    release.add_argument("version", nargs="?", help="new version, e.g. 2.4.2")
    release.add_argument("--dry-run", action="store_true", help="stop before publishing")
    release.set_defaults(func=cmd_release)

    watch = subcommands.add_parser("watch", help="reinstall on every source change")
    watch.add_argument("--data", help="Foundry user data directory")
    watch.set_defaults(func=cmd_watch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
