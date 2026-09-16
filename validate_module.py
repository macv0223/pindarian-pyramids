#!/usr/bin/env python3
"""Validate the built Pindarian Pyramids Foundry module and its LevelDB logs."""

from __future__ import annotations

import json
import re
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE = ROOT.parent / "build/pindarian-pyramids"


def varint(data: bytes, pos: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while True:
        byte = data[pos]
        pos += 1
        value |= (byte & 0x7F) << shift
        if byte < 0x80:
            return value, pos
        shift += 7


def crc32c(data: bytes) -> int:
    crc = 0xFFFFFFFF
    polynomial = 0x82F63B78
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (polynomial if crc & 1 else 0)
    return crc ^ 0xFFFFFFFF


def masked_crc32c(data: bytes) -> int:
    crc = crc32c(data)
    return (((crc >> 15) | ((crc << 17) & 0xFFFFFFFF)) + 0xA282EAD8) & 0xFFFFFFFF


def logical_records(path: Path) -> list[bytes]:
    raw = path.read_bytes()
    pos = 0
    result = []
    current = bytearray()
    while pos + 7 <= len(raw):
        room = 32768 - (pos % 32768)
        if room < 7:
            pos += room
            continue
        checksum, length, record_type = struct.unpack_from("<IHB", raw, pos)
        pos += 7
        if length == 0 and record_type == 0:
            pos += 32768 - (pos % 32768)
            continue
        payload = raw[pos:pos + length]
        pos += length
        assert checksum == masked_crc32c(bytes([record_type]) + payload), f"Bad checksum: {path}"
        if record_type == 1:
            result.append(payload)
        elif record_type == 2:
            current = bytearray(payload)
        elif record_type == 3:
            current.extend(payload)
        elif record_type == 4:
            current.extend(payload)
            result.append(bytes(current))
            current = bytearray()
        else:
            raise AssertionError(f"Unknown LevelDB record type {record_type}: {path}")
    return result


def decode_pack(name: str) -> list[tuple[str, dict]]:
    rows = []
    path = MODULE / "packs" / name / "000003.log"
    for batch in logical_records(path):
        _sequence, count = struct.unpack_from("<QI", batch, 0)
        pos = 12
        for _ in range(count):
            tag = batch[pos]
            pos += 1
            assert tag == 1, f"Unexpected delete record in {name}"
            length, pos = varint(batch, pos)
            key = batch[pos:pos + length].decode()
            pos += length
            length, pos = varint(batch, pos)
            value = json.loads(batch[pos:pos + length])
            pos += length
            rows.append((key, value))
        assert pos == len(batch), f"Trailing data in {name}"
    return rows


def module_asset(path: str) -> Path:
    prefix = "modules/pindarian-pyramids/"
    assert path.startswith(prefix), f"Unexpected asset path: {path}"
    return MODULE / path[len(prefix):]


def main() -> None:
    manifest = json.loads((MODULE / "module.json").read_text(encoding="utf-8"))
    assert manifest["id"] == "pindarian-pyramids"
    assert manifest["version"] == "2.3.1"
    assert manifest["compatibility"] == {"minimum": "14", "verified": "14", "maximum": "14"}
    system_compatibility = manifest["relationships"]["systems"][0]["compatibility"]
    assert system_compatibility == {"minimum": "5.3.3", "verified": "5.3.3"}
    assert {pack["name"] for pack in manifest["packs"]} == {"lore", "relics", "guardians", "scenes", "legions", "spells", "bestiary"}
    assert all("macv0223/pindarian-pyramids" in manifest[field] for field in ("url", "manifest", "download", "readme"))

    lore = decode_pack("lore")
    item_rows = decode_pack("relics")
    actor_rows = decode_pack("guardians")
    scenes = decode_pack("scenes")

    journal_parents = [(key, value) for key, value in lore if key.startswith("!journal!")]
    journal_pages = [(key, value) for key, value in lore if key.startswith("!journal.pages!")]
    assert len(journal_parents) == 12
    assert len(journal_pages) == 149
    items = [(key, value) for key, value in item_rows if key.startswith("!items!")]
    item_effects = [(key, value) for key, value in item_rows if key.startswith("!items.effects!")]
    actors = [(key, value) for key, value in actor_rows if key.startswith("!actors!")]
    actor_items = [(key, value) for key, value in actor_rows if key.startswith("!actors.items!")]
    assert len(items) == 16
    assert len(item_effects) == 7
    assert len(actors) == 9
    assert len(actor_items) == 145
    assert len(scenes) == 11

    for key, page in journal_pages:
        assert page["_id"] in key
        assert len(page["text"]["content"]) > 500
        assert "<img " in page["text"]["content"]
        assert page["image"] == {} and page["src"] is None
        image_match = __import__("re").search(r'<img src="([^"]+)"', page["text"]["content"])
        assert image_match and module_asset(image_match.group(1)).is_file()

    for key, item in items:
        assert key.startswith("!items!") and item["_id"] in key
        assert module_asset(item["img"]).is_file()
        assert len(item["system"]["description"]["value"]) > 500
        assert len(item["system"]["activities"]) >= 3
        for activity in item["system"]["activities"].values():
            if activity["uses"]["max"]:
                assert any(target["type"] == "activityUses" for target in activity["consumption"]["targets"])

    fivefold = next(value for _key, value in items if value["name"] == "Fivefold Scale")
    assert len(fivefold["system"]["activities"]) == 9
    assert fivefold["system"]["uses"]["max"] == "3"

    for key, actor in actors:
        assert key.startswith("!actors!") and actor["_id"] in key
        assert module_asset(actor["img"]).is_file()
        assert actor["prototypeToken"]["texture"]["src"] == actor["img"]
        assert len(actor["system"]["details"]["biography"]["value"]) > 300
        assert actor["system"]["attributes"]["ac"]["flat"] >= 17
        assert actor["system"]["attributes"]["hp"]["max"] >= 130
        assert len({ability["value"] for ability in actor["system"]["abilities"].values()}) > 1

    for key, actor_item in actor_items:
        assert key.startswith("!actors.items!") and actor_item["_id"] in key
        assert len(actor_item["system"]["activities"]) <= 1
        if actor_item["type"] == "spell" and not actor_item["system"]["activities"]:
            continue  # prepared spells on a sheet are reference entries
        activity = next(iter(actor_item["system"]["activities"].values()))
        if activity["uses"]["max"]:
            assert any(target["type"] == "activityUses" for target in activity["consumption"]["targets"])

    for key, scene in scenes:
        assert key.startswith("!scenes!") and scene["_id"] in key
        assert module_asset(scene["background"]["src"]).is_file()
        assert scene["width"] > 0 and scene["height"] > 0

    # Every image path referenced by any document must resolve to a real file.
    missing = set()
    for rows in (lore, item_rows, actor_rows, scenes):
        for _key, doc in rows:
            for path in re.findall(r'modules/pindarian-pyramids/assets/[^"\'<>)\\\\ ]+', json.dumps(doc)):
                if not module_asset(path).is_file():
                    missing.add(path)
    assert not missing, f"missing art files: {sorted(missing)[:5]}"

    generated = list((MODULE / "assets/art").rglob("*.webp"))
    maps = list((MODULE / "assets/maps").glob("*.jpg"))
    assert len(generated) == 286
    assert len(maps) == 2

    print("Pindarian Pyramids validation passed")
    print(f"  Journals: {len(journal_parents)} ({len(journal_pages)} populated pages)")
    print(f"  Actors: {len(actors)} ({len(actor_items)} embedded actions/features)")
    print(f"  Items: {len(items)}")
    print(f"  Scenes: {len(scenes)}")
    print(f"  Item effects: {len(item_effects)}")
    print(f"  Generated art: {len(generated)}")
    print(f"  Supplied maps: {len(maps)}")


if __name__ == "__main__":
    main()
