#!/usr/bin/env python3
"""Build the Pindarian Pyramids Foundry VTT module from the supplied source files."""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import struct
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "source"
ASSET_ROOT = ROOT / "assets"
MAP_ROOT = ROOT / "reference-maps"
TEMPLATE_PACK = ROOT / "pack-template"
OUTPUT = ROOT.parent / "build/pindarian-pyramids"

REPOSITORY = "https://github.com/macv0223/pindarian-pyramids"
VERSION = "2.3.1"
MODULE_ID = "pindarian-pyramids"

SOURCES = {
    "The Nine Pyramids of Pindar": INPUT / "the-nine-pyramids-of-pindar.md",
    "The Nine Pindarian Demon Relics": INPUT / "the-nine-pindarian-demon-relics.md",
    "The Mimic Relics of the Pyramids": INPUT / "the-mimic-relics-of-the-pyramids.md",
    "Astra: Pyramid of the Sun - Site Guide": INPUT / "astra-site-guide.md",
    "Khar'Zhul: Pyramid of the Empty Table - Site Guide": INPUT / "kharzhul-site-guide.md",
    "Ilyr-Ameul: Pyramid of Two Truths - Site Guide": INPUT / "ilyrameul-site-guide.md",
    "Gor-Mazaal: Pyramid of the Wandering Path - Site Guide": INPUT / "gormazaal-site-guide.md",
    "Myr'Velora: Pyramid of the Thousand Gardens - Site Guide": INPUT / "myrvelora-site-guide.md",
    "Thaal-Uluun: Pyramid of Unmaking - Site Guide": INPUT / "thaaluluun-site-guide.md",
    "Nar'Vael: Black Sun Pyramid - Site Guide": INPUT / "narvael-site-guide.md",
    "Khal'Vethar: Pyramid of the Final Vigil - Site Guide": INPUT / "khalvethar-site-guide.md",
    "Vhal'Kathar: Pyramid of the Last Breath - Site Guide": INPUT / "vhalkathar-site-guide.md",
}

# Expanded per-pyramid site guides. These are keyed-area documents: one page per
# "## " heading, rather than the "# " sectioning the original three journals use.
SITE_GUIDE_ART = {
    "Astra: Pyramid of the Sun - Site Guide": "astra.webp",
    "Khar'Zhul: Pyramid of the Empty Table - Site Guide": "kharzhul.webp",
    "Ilyr-Ameul: Pyramid of Two Truths - Site Guide": "ilyrameul.webp",
    "Gor-Mazaal: Pyramid of the Wandering Path - Site Guide": "gormazaal.webp",
    "Myr'Velora: Pyramid of the Thousand Gardens - Site Guide": "myrvelora.webp",
    "Thaal-Uluun: Pyramid of Unmaking - Site Guide": "thaaluluun.webp",
    "Nar'Vael: Black Sun Pyramid - Site Guide": "narvael.webp",
    "Khal'Vethar: Pyramid of the Final Vigil - Site Guide": "khalvethar.webp",
    "Vhal'Kathar: Pyramid of the Last Breath - Site Guide": "vhalkathar.webp",
}

from pindarian_content import BESTIARY, BOSSES, LEGIONS, SPELL_TRADITIONS

DEMON_RELICS = [
    ("The Velvet Ruin", "greatsword", "artifact", "velvet-ruin.webp"),
    ("Feastchain", "flail", "artifact", "feastchain.webp"),
    ("Gravewake", "mace", "artifact", "gravewake.webp"),
    ("The Two That Are One", "spear", "artifact", "two-that-are-one.webp"),
    ("The Labyrinth's Answer", "greataxe", "artifact", "labyrinths-answer.webp"),
    ("The Bride of Rot", "sickle", "artifact", "bride-of-rot.webp"),
    ("Mercy of Dissolution", "whip", "artifact", "mercy-of-dissolution.webp"),
    ("The Honest Lie", "rapier", "artifact", "honest-lie.webp"),
    ("Winter's Grudge", "maul", "artifact", "winters-grudge.webp"),
]

MIMIC_RELICS = [
    ("Tongue of the Last Wyrm", "greatsword", "rare", "tongue-last-wyrm.webp"),
    ("The Berry Bad Idea", "longbow", "rare", "berry-bad-idea.webp"),
    ("The Kindly Anatomist", "sickle", "rare", "kindly-anatomist.webp"),
    ("Everyone's Invited", "quarterstaff", "rare", "everyones-invited.webp"),
    ("The Seam Ripper", "rapier", "rare", "seam-ripper.webp"),
    ("The Unchosen", "", "rare", "unchosen.webp"),
]

GUARDIANS = [
    ("High Priestess Seryth Vael - The Last Dawn", "Astra - Pyramid of the Sun", "Seryth Vael", "seryth-vael.webp"),
    ("General Rhakkar Sol - The Starved Lion", "Khar'zhul - Pyramid of the Empty Table", "General Rhakkar", "rhakkar-sol.webp"),
    ("Kathandar, Elder Dragonlord", "Vhal'kathar - Pyramid of the Last Breath", "Kathandar", "kathandar.webp"),
    ("Vaelis, the Concordant Twin", "Ilyr-Ameul - Pyramid of Two Truths", "The Guardians", "vaelis.webp"),
    ("Vaelith, the Concordant Twin", "Ilyr-Ameul - Pyramid of Two Truths", "The Guardians", "vaelith.webp"),
    ("Marshal Korveth Anor - The Blind Cartographer", "Gor-Mazaal - Pyramid of the Wandering Path", "Korveth", "korveth-anor.webp"),
    ("Nymara Thess - Keeper of the Last Garden", "Myr'velora - Pyramid of the Thousand Gardens", "Nymara", "nymara-thess.webp"),
    ("Aul Tareth - The Man Who Refused to Melt", "Thaal-Uluun - Pyramid of Unmaking", "Aul Tareth", "aul-tareth.webp"),
    ("High Scribe Irio Venn - Keeper of the Unaltered Word", "Nar'vael - The Black Sun Pyramid", "Irio Venn", "irio-venn.webp"),
    ("Hestra Vaun - Last Marshal of Pindaria", "Khal'vethar - Pyramid of the Final Vigil", "Hestra", "hestra-vaun.webp"),
]

LOCATION_ART = {
    "I - Astra: Pyramid of the Sun": "astra.webp",
    "II - Khar'zhul: Pyramid of the Empty Table": "kharzhul.webp",
    "III - Vhal'kathar: Pyramid of the Last Breath": "vhalkathar.webp",
    "IV - Ilyr-Ameul: Pyramid of Two Truths": "ilyrameul.webp",
    "V - Gor-Mazaal: Pyramid of the Wandering Path": "gormazaal.webp",
    "VI - Myr'velora: Pyramid of the Thousand Gardens": "myrvelora.webp",
    "VII - Thaal-Uluun: Pyramid of Unmaking": "thaaluluun.webp",
    "VIII - Nar'vael: The Black Sun Pyramid": "narvael.webp",
    "IX - Khal'vethar: Pyramid of the Final Vigil": "khalvethar.webp",
}

RELIC_ART = {name: filename for name, _base, _rarity, filename in DEMON_RELICS + MIMIC_RELICS}

EXTRA_DAMAGE = {
    "The Velvet Ruin": [(1, 8, "psychic")],
    "Feastchain": [(1, 8, "piercing")],
    "Gravewake": [(2, 6, "necrotic")],
    "Aameul's Fury": [(2, 6, "psychic")],
    "The Labyrinth's Answer": [(1, 8, "force")],
    "The Bride of Rot": [(1, 8, "poison")],
    "Mercy of Dissolution": [(2, 6, "acid")],
    "The Honest Lie": [(1, 8, "psychic")],
    "Winter's Grudge": [(1, 8, "cold")],
}

ITEM_FEATURES = {
    "The Velvet Ruin": [
        {"name": "Beautiful Violence", "kind": "save", "activation": "special", "save": "wis", "dc": 18, "range": 5},
        {"name": "Sixfold Temptation", "activation": "action", "range": 60, "consume_item": True},
        {"name": "Kiss of the Dark Prince", "kind": "save", "activation": "special", "save": "wis", "dc": 18, "range": 5, "uses": "1", "recovery": "lr"},
    ],
    "Feastchain": [
        {"name": "Rampage", "activation": "bonus", "range": 0},
        {"name": "Smell Weakness", "activation": "special", "range": 30},
        {"name": "Feast of Yeenoghu", "activation": "bonus", "duration": (1, "minute"), "uses": "1", "recovery": "lr"},
    ],
    "Gravewake": [
        {"name": "Remember the Dead", "activation": "action", "range": 30},
        {"name": "Death Knell", "kind": "heal", "activation": "special", "healing": (2, 8, "healing")},
        {"name": "Wake the Fallen", "activation": "action", "range": 30, "consume_item": True, "duration": (1, "minute")},
        {"name": "Black Communion", "activation": "action", "range": 10, "uses": "1", "recovery": "day"},
    ],
    "The Two That Are One": [
        {"name": "Opposite Blade", "kind": "attack", "activation": "bonus", "range": 5, "damage": [(1, 6, "piercing")]},
        {"name": "Divided Mind", "activation": "special"},
        {"name": "Aameul's Fury", "kind": "damage", "activation": "special", "damage": [(2, 6, "psychic")]},
        {"name": "Hethradiah's Cunning", "activation": "reaction", "range": 10},
        {"name": "Gaze of the Prince", "kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 19, "uses": "1", "recovery": "lr", "duration": (1, "minute")},
    ],
    "The Labyrinth's Answer": [
        {"name": "Perfect Direction", "activation": "special"},
        {"name": "Gore Through", "kind": "save", "activation": "special", "range": 5, "save": "str", "dc": 18, "damage": [(3, 8, "slashing")]},
        {"name": "The Maze Moves", "activation": "bonus", "range": 60, "uses": "3", "recovery": "lr"},
        {"name": "Endless Labyrinth", "activation": "action", "range": 60, "uses": "1", "recovery": "lr"},
    ],
    "The Bride of Rot": [
        {"name": "Bloom in the Wound", "kind": "damage", "activation": "special", "damage": [(2, 6, "necrotic")]},
        {"name": "Mycelial Communion", "activation": "special", "range": 60},
        {"name": "Beautiful Decay", "kind": "damage", "activation": "special", "range": 10, "damage": [(2, 8, "poison")]},
        {"name": "Queen's Garden", "kind": "save", "activation": "action", "save": "con", "dc": 18, "template": ("radius", 30), "duration": (1, "minute"), "uses": "1", "recovery": "lr"},
    ],
    "Mercy of Dissolution": [
        {"name": "Dissolve Armour", "activation": "special", "range": 5},
        {"name": "Liquefy", "activation": "reaction", "uses": "@prof", "recovery": "lr"},
        {"name": "Slime Passage", "activation": "action", "duration": (1, "minute")},
        {"name": "Dissolution", "kind": "save", "activation": "special", "save": "con", "dc": 19, "damage": [(10, 6, "acid")], "uses": "1", "recovery": "lr"},
    ],
    "The Honest Lie": [
        {"name": "False Wound", "kind": "save", "activation": "special", "save": "wis", "dc": 18, "damage": [(2, 8, "psychic")]},
        {"name": "Liar's Step", "activation": "bonus", "range": 30, "uses": "3", "recovery": "lr"},
        {"name": "Rewrite the Scene", "activation": "reaction", "range": 60, "uses": "1", "recovery": "lr"},
        {"name": "Major Image", "activation": "action", "range": 120},
        {"name": "Mislead", "activation": "action", "uses": "1", "recovery": "lr"},
    ],
    "Winter's Grudge": [
        {"name": "Giant's Wrath", "activation": "special"},
        {"name": "Break Them", "kind": "save", "activation": "special", "save": "str", "dc": 18, "range": 5, "damage": [(2, 6, "bludgeoning")]},
        {"name": "Rage of the Glacier", "kind": "damage", "activation": "reaction", "damage": [(3, 8, "cold")]},
        {"name": "Avalanche", "kind": "save", "activation": "action", "save": "str", "dc": 19, "template": ("radius", 30), "damage": [(8, 8, "bludgeoning"), (8, 8, "cold")], "uses": "1", "recovery": "lr"},
    ],
    "Tongue of the Last Wyrm": [
        {"name": "Taste of Blood", "kind": "damage", "activation": "special", "damage": [(1, 6, "acid")]},
        {"name": "Tongue Lash", "kind": "save", "activation": "bonus", "save": "str", "dc": 14, "range": 15, "uses": "@prof", "recovery": "day"},
        {"name": "Feed Me", "kind": "heal", "activation": "special", "healing": (1, 1, "temphp"), "formula": "@prof"},
    ],
    "The Berry Bad Idea": [
        {"name": "Tactical Genius", "activation": "special", "range": 150},
        {"name": "Goodberry Ammunition", "kind": "heal", "activation": "bonus", "range": 150, "healing": (1, 6, "healing"), "formula": "@prof"},
        {"name": "I Meant To Do That", "activation": "special", "uses": "1", "recovery": "day"},
    ],
    "The Kindly Anatomist": [
        {"name": "Harvest Anatomy", "activation": "reaction", "range": 30},
        {"name": "Experimental Graft", "activation": "special", "duration": (1, "hour"), "uses": "1", "recovery": "lr"},
        {"name": "Surgical Precision", "kind": "damage", "activation": "special", "damage": [(1, 4, "necrotic")]},
    ],
    "Everyone's Invited": [
        {"name": "Amorphous Weapon", "activation": "special"},
        {"name": "Join Us", "activation": "special", "range": 5},
        {"name": "Family Support", "activation": "reaction", "range": 10, "uses": "@prof", "recovery": "lr"},
        {"name": "Puddle Mode", "activation": "action", "template": ("square", 10), "duration": (None, "perm")},
    ],
    "The Seam Ripper": [
        {"name": "Loose Thread", "kind": "save", "activation": "special", "save": "str", "dc": 14, "range": 10, "uses": "@prof", "recovery": "lr"},
        {"name": "Stitch It Closed", "kind": "heal", "activation": "bonus", "range": 5, "healing": (2, 6, "healing"), "formula": "@prof", "uses": "1", "recovery": "day"},
        {"name": "Patchwork Escape", "activation": "reaction", "range": 10, "uses": "1", "recovery": "sr"},
    ],
    "The Unchosen": [
        {"name": "Learning You", "activation": "special"},
        {"name": "Adaptive Relic", "activation": "special", "uses": "1", "recovery": "lr"},
    ],
}

GUARDIAN_BLOCKS = {
    "High Priestess Seryth Vael - The Last Dawn": {
        "ac": 19, "hp": 195, "formula": "26d8 + 78", "cr": 13,
        "abilities": [12, 18, 16, 19, 22, 20], "saves": ["dex", "wis", "cha"], "skills": {"ins": 2, "per": 2, "rel": 2},
        "actions": [
            {"name": "Multiattack", "description": "Seryth makes two Solar Scepter attacks.", "activation": "action"},
            {"name": "Solar Scepter", "description": "Melee Weapon Attack. The scepter strikes with disciplined sunlight.", "kind": "attack", "activation": "action", "range": 10, "ability": "wis", "damage": [(2, 8, "bludgeoning"), (4, 8, "radiant")]},
            {"name": "Mirror Verdict", "description": "One creature sees the desire it would damn the world to possess.", "kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 18, "damage": [(5, 10, "psychic")]},
            {"name": "Refuse Temptation", "description": "Seryth adds 5 to her AC against one attack that would hit her.", "activation": "reaction", "condition": "Seryth is hit by an attack."},
        ],
    },
    "General Rhakkar Sol - The Starved Lion": {
        "ac": 18, "hp": 210, "formula": "28d8 + 84", "cr": 12,
        "abilities": [22, 14, 17, 15, 19, 16], "saves": ["str", "con", "wis"], "skills": {"ath": 2, "ins": 1, "sur": 2},
        "actions": [
            {"name": "Multiattack", "description": "Rhakkar makes two Starved Glaive attacks.", "activation": "action"},
            {"name": "Starved Glaive", "description": "Melee Weapon Attack with the reach of a patient predator.", "kind": "attack", "activation": "action", "range": 10, "ability": "str", "damage": [(2, 10, "slashing"), (2, 8, "necrotic")]},
            {"name": "Hunger Without Cruelty", "description": "Allies of Rhakkar in the aura gain temporary hit points; enemies must master their hunger or become frightened.", "kind": "save", "activation": "action", "template": ("radius", 30), "save": "wis", "dc": 18, "uses": "1", "recovery": "day"},
            {"name": "Predator's Advance", "description": "Rhakkar moves up to half his speed without provoking opportunity attacks, then makes one Starved Glaive attack.", "activation": "bonus"},
        ],
    },
    "Kathandar, Elder Dragonlord": {
        "ac": 21, "hp": 285, "formula": "30d10 + 120", "cr": 17,
        "abilities": [24, 12, 19, 22, 18, 21], "saves": ["str", "con", "int", "wis"], "skills": {"arc": 2, "his": 2, "ins": 1, "prc": 2},
        "actions": [
            {"name": "Multiattack", "description": "Kathandar makes one Bite attack and two Claw attacks.", "activation": "action"},
            {"name": "Bite", "description": "Melee Weapon Attack with a deathless dragon's jaws.", "kind": "attack", "activation": "action", "range": 10, "ability": "str", "damage": [(2, 10, "piercing"), (3, 8, "necrotic")]},
            {"name": "Claw", "description": "Melee Weapon Attack.", "kind": "attack", "activation": "action", "range": 5, "ability": "str", "damage": [(2, 8, "slashing")]},
            {"name": "Breath of the Last Archive", "description": "Kathandar exhales a storm of names and grave-cold power in a 60-foot cone.", "kind": "save", "activation": "action", "save": "con", "dc": 20, "template": ("cone", 60), "damage": [(10, 8, "necrotic")], "on_save": "half", "uses": "1", "recovery": "day"},
        ],
    },
    "Vaelis, the Concordant Twin": {
        "ac": 18, "hp": 136, "formula": "21d8 + 42", "cr": 10,
        "abilities": [16, 20, 15, 18, 17, 18], "saves": ["dex", "int", "wis"], "skills": {"acr": 2, "ins": 2, "prc": 1},
        "actions": [
            {"name": "Multiattack", "description": "Vaelis makes two Concordant Blade attacks.", "activation": "action"},
            {"name": "Concordant Blade", "description": "Melee Weapon Attack carrying the fire half of one divided truth.", "kind": "attack", "activation": "action", "range": 5, "ability": "dex", "damage": [(2, 8, "slashing"), (2, 6, "fire")]},
            {"name": "Contradictory Command", "description": "The target receives two incompatible commands and is stunned until the end of its next turn on a failed save.", "kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 17},
            {"name": "Shared Soul", "description": "Vaelis halves damage dealt to Vaelith or another chosen ally within 30 feet, taking the remainder.", "activation": "reaction", "range": 30},
        ],
    },
    "Vaelith, the Concordant Twin": {
        "ac": 18, "hp": 136, "formula": "21d8 + 42", "cr": 10,
        "abilities": [18, 18, 15, 20, 16, 17], "saves": ["str", "int", "cha"], "skills": {"arc": 2, "dec": 2, "ins": 1},
        "actions": [
            {"name": "Multiattack", "description": "Vaelith makes two Concordant Blade attacks.", "activation": "action"},
            {"name": "Concordant Blade", "description": "Melee Weapon Attack carrying the water-cold half of one divided truth.", "kind": "attack", "activation": "action", "range": 5, "ability": "str", "damage": [(2, 8, "slashing"), (2, 6, "cold")]},
            {"name": "Reverse the Premise", "description": "The target's successful action becomes a contradiction; on a failed save it has disadvantage on attacks and saves until the end of its next turn.", "kind": "save", "activation": "reaction", "range": 60, "save": "int", "dc": 17},
            {"name": "Shared Soul", "description": "Vaelith halves damage dealt to Vaelis or another chosen ally within 30 feet, taking the remainder.", "activation": "reaction", "range": 30},
        ],
    },
    "Marshal Korveth Anor - The Blind Cartographer": {
        "ac": 19, "hp": 190, "formula": "20d10 + 80", "cr": 13,
        "abilities": [20, 18, 18, 20, 21, 14], "saves": ["dex", "int", "wis"], "skills": {"inv": 2, "prc": 2, "sur": 2},
        "actions": [
            {"name": "Multiattack", "description": "Korveth makes two Cartographer's Axe attacks.", "activation": "action"},
            {"name": "Cartographer's Axe", "description": "Melee Weapon Attack that cuts the route as readily as the target.", "kind": "attack", "activation": "action", "range": 5, "ability": "str", "damage": [(2, 12, "slashing"), (2, 8, "force")]},
            {"name": "North Is Down", "description": "Korveth rotates local gravity in a 20-foot cube.", "kind": "save", "activation": "action", "range": 90, "save": "dex", "dc": 18, "template": ("cube", 20), "damage": [(6, 8, "force")], "on_save": "half"},
            {"name": "Fold Corridor", "description": "Korveth teleports up to 60 feet and may bring one willing creature within 5 feet.", "activation": "bonus", "range": 60},
        ],
    },
    "Nymara Thess - Keeper of the Last Garden": {
        "ac": 18, "hp": 180, "formula": "24d8 + 72", "cr": 12,
        "abilities": [14, 16, 17, 19, 22, 18], "saves": ["con", "wis", "cha"], "skills": {"med": 2, "nat": 2, "ins": 1},
        "actions": [
            {"name": "Multiattack", "description": "Nymara makes two Garden Sickle attacks.", "activation": "action"},
            {"name": "Garden Sickle", "description": "Melee Weapon Attack carrying carefully tended rot.", "kind": "attack", "activation": "action", "range": 5, "ability": "wis", "damage": [(2, 6, "slashing"), (3, 8, "poison")]},
            {"name": "Beautiful Decay", "description": "Spores erupt in a 20-foot radius; enemies are poisoned and allies regain vitality.", "kind": "save", "activation": "action", "template": ("radius", 20), "save": "con", "dc": 18, "damage": [(5, 8, "poison")], "on_save": "half", "uses": "1", "recovery": "day"},
            {"name": "Symbiotic Restoration", "description": "One creature within 30 feet regains 4d8 + 6 hit points.", "kind": "heal", "activation": "bonus", "range": 30, "healing": (4, 8, "healing"), "formula": "6", "uses": "3", "recovery": "day"},
        ],
    },
    "Aul Tareth - The Man Who Refused to Melt": {
        "ac": 17, "hp": 220, "formula": "21d10 + 105", "cr": 12,
        "abilities": [21, 14, 20, 16, 20, 13], "saves": ["str", "con", "wis"], "skills": {"ath": 2, "ins": 1, "prc": 1},
        "actions": [
            {"name": "Multiattack", "description": "Aul makes two Dissolving Fist attacks.", "activation": "action"},
            {"name": "Dissolving Fist", "description": "Melee Weapon Attack with an acidic, half-liquid arm.", "kind": "attack", "activation": "action", "range": 10, "ability": "str", "damage": [(2, 10, "bludgeoning"), (3, 8, "acid")]},
            {"name": "Unmaking Wave", "description": "A 30-foot cone of dissolving force strips form from matter.", "kind": "save", "activation": "action", "template": ("cone", 30), "save": "dex", "dc": 18, "damage": [(8, 8, "acid")], "on_save": "half", "uses": "1", "recovery": "day"},
            {"name": "Liquefy", "description": "Aul gains resistance to one instance of bludgeoning, piercing, or slashing damage and moves up to 10 feet.", "activation": "reaction"},
        ],
    },
    "High Scribe Irio Venn - Keeper of the Unaltered Word": {
        "ac": 18, "hp": 170, "formula": "20d8 + 80", "cr": 13,
        "abilities": [10, 18, 18, 24, 20, 19], "saves": ["dex", "int", "wis"], "skills": {"arc": 2, "his": 2, "ins": 2, "inv": 2},
        "actions": [
            {"name": "Multiattack", "description": "Irio makes two Unaltered Word attacks.", "activation": "action"},
            {"name": "Unaltered Word", "description": "Ranged Spell Attack. A precisely spoken truth cuts through the target's self-deception.", "kind": "attack", "activation": "action", "range": 120, "ability": "int", "attack_type": "ranged", "damage": [(4, 10, "psychic")]},
            {"name": "One Truth in Every Lie", "description": "Creatures in a 30-foot cone must identify the truth or become confused until the end of their next turn.", "kind": "save", "activation": "action", "template": ("cone", 30), "save": "wis", "dc": 19, "damage": [(6, 8, "psychic")], "on_save": "half"},
            {"name": "Exact Correction", "description": "Irio forces a d20 roll made within 60 feet to be rerolled and chooses which result stands.", "activation": "reaction", "range": 60, "uses": "3", "recovery": "day"},
        ],
    },
    "Hestra Vaun - Last Marshal of Pindaria": {
        "ac": 21, "hp": 245, "formula": "26d10 + 104", "cr": 15,
        "abilities": [24, 14, 19, 17, 20, 21], "saves": ["str", "con", "wis", "cha"], "skills": {"ath": 2, "ins": 2, "itm": 2, "per": 1},
        "actions": [
            {"name": "Multiattack", "description": "Hestra makes three Vigil Maul attacks.", "activation": "action"},
            {"name": "Vigil Maul", "description": "Melee Weapon Attack driven by remembered grievances.", "kind": "attack", "activation": "action", "range": 5, "ability": "str", "damage": [(2, 6, "bludgeoning"), (3, 8, "cold")]},
            {"name": "The March", "description": "Spectral ranks advance through a 60-foot line.", "kind": "save", "activation": "action", "template": ("line", 60), "save": "str", "dc": 19, "damage": [(8, 8, "bludgeoning"), (8, 8, "cold")], "on_save": "half", "uses": "1", "recovery": "day"},
            {"name": "Retaliatory Mark", "description": "When damaged, Hestra marks the attacker. Her next Vigil Maul hit against it deals 3d8 additional cold damage.", "kind": "damage", "activation": "reaction", "range": 60, "damage": [(3, 8, "cold")]},
        ],
    },
}

BASE_WEAPONS = {
    "greatsword": (2, 6, "slashing", "martialM"),
    "flail": (1, 8, "bludgeoning", "martialM"),
    "mace": (1, 6, "bludgeoning", "simpleM"),
    "spear": (1, 6, "piercing", "simpleM"),
    "greataxe": (1, 12, "slashing", "martialM"),
    "sickle": (1, 4, "slashing", "simpleM"),
    "whip": (1, 4, "slashing", "martialM"),
    "rapier": (1, 8, "piercing", "martialM"),
    "maul": (2, 6, "bludgeoning", "martialM"),
    "longbow": (1, 8, "piercing", "martialR"),
    "quarterstaff": (1, 6, "bludgeoning", "simpleM"),
    "": (1, 6, "", "simpleM"),
}


def identifier(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def foundry_id(value: str) -> str:
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    number = int.from_bytes(hashlib.sha256(value.encode()).digest()[:12], "big")
    chars = []
    for _ in range(16):
        number, remainder = divmod(number, len(alphabet))
        chars.append(alphabet[remainder])
    return "".join(chars)


def markdown_to_html(markdown: str) -> str:
    proc = subprocess.run(
        ["pandoc", "--from=gfm", "--to=html5"],
        input=markdown,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout.strip()


def trim_preface(markdown: str, title: str) -> str:
    marker = f"# {title}"
    pos = markdown.find(marker)
    return markdown[pos:] if pos >= 0 else markdown


def split_h1(markdown: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^# (?!#)(.+?)\s*$", markdown))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        title = re.sub(r"[*`]", "", match.group(1)).strip()
        sections.append((title, markdown[match.start():end].strip()))
    return sections


def split_h2(markdown: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^## (?!#)(.+?)\s*$", markdown))
    if not matches:
        return split_h1(markdown)
    preamble = markdown[: matches[0].start()].strip()
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        title = re.sub(r"[*`]", "", match.group(1)).strip()
        body = markdown[match.start():end].strip()
        if index == 0 and preamble:
            body = f"{preamble}\n\n{body}"
        sections.append((title, body))
    return sections


def split_between(markdown: str, markers: list[tuple[str, str]], tail: tuple[str, str] | None = None) -> list[tuple[str, str]]:
    located = []
    for page_title, pattern in markers:
        match = re.search(pattern, markdown, flags=re.MULTILINE)
        if not match:
            raise ValueError(f"Missing journal marker: {page_title}")
        located.append((page_title, match.start()))
    sections = []
    if located[0][1] > 0:
        intro = markdown[:located[0][1]].strip()
        intro = re.sub(r"(?s)^.*?(?=^#{1,3} )", "", intro, count=1, flags=re.MULTILINE)
        if intro:
            sections.append(("Overview", intro))
    for index, (page_title, start) in enumerate(located):
        end = located[index + 1][1] if index + 1 < len(located) else len(markdown)
        if tail:
            tail_match = re.search(tail[1], markdown[start:end], flags=re.MULTILINE)
            if tail_match:
                split_at = start + tail_match.start()
                sections.append((page_title, markdown[start:split_at].strip()))
                sections.append((tail[0], markdown[split_at:end].strip()))
                continue
        sections.append((page_title, markdown[start:end].strip()))
    return sections


def journal_sections(name: str, markdown: str) -> list[tuple[str, str]]:
    if name in SITE_GUIDE_ART:
        return split_h2(markdown)
    if name == "The Nine Pyramids of Pindar":
        markers = [
            ("I - Astra: Pyramid of the Sun", r"^# I .+ ASTRA\s*$"),
            ("II - Khar'zhul: Pyramid of the Empty Table", r"^# II .+ KHAR'ZHUL\s*$"),
            ("III - Vhal'kathar: Pyramid of the Last Breath", r"^# III .+ VHAL'KATHAR\s*$"),
            ("IV - Ilyr-Ameul: Pyramid of Two Truths", r"^# IV .+ ILYR-AMEUL\s*$"),
            ("V - Gor-Mazaal: Pyramid of the Wandering Path", r"^# V .+ GOR-MAZAAL\s*$"),
            ("VI - Myr'velora: Pyramid of the Thousand Gardens", r"^# VI .+ MYR'VELORA\s*$"),
            ("VII - Thaal-Uluun: Pyramid of Unmaking", r"^# VII .+ THAAL-ULUUN\s*$"),
            ("VIII - Nar'vael: The Black Sun Pyramid", r"^# VIII .+ NAR'VAEL\s*$"),
            ("IX - Khal'vethar: Pyramid of the Final Vigil", r"^# IX .+ KHAL'VETHAR\s*$"),
            ("Pindarian Physiology", r"^# Pindarian Physiology\s*$"),
        ]
        return split_between(markdown, markers, ("The Ninefold Network", r"^# THE NINE AT A GLANCE\s*$"))
    if name == "The Nine Pindarian Demon Relics":
        markers = [(title, rf"^# {number}\. .+$") for number, (title, *_rest) in enumerate(DEMON_RELICS, 1)]
        return split_between(markdown, markers, ("Why the Pindarians Had Them", r"^# Why the Pindarians Had Them\s*$"))
    if name == "The Mimic Relics of the Pyramids":
        markers = [(title, rf"^# {number}\. .+$") for number, (title, *_rest) in enumerate(MIMIC_RELICS, 1)]
        return split_between(markdown, markers, ("Placement and Awakening", r"^# How I Would Place Them in the Pyramids\s*$"))
    return split_h1(markdown)


def extract_relic(markdown: str, title: str, all_titles: list[str]) -> str:
    start_match = re.search(rf"(?m)^# {re.escape(title)}\s*$", markdown)
    if not start_match:
        raise ValueError(f"Missing relic section: {title}")
    starts = []
    for other in all_titles:
        match = re.search(rf"(?m)^# {re.escape(other)}\s*$", markdown)
        if match and match.start() > start_match.start():
            starts.append(match.start())
    for closing in ("# Why the Pindarians Had Them", "# How I Would Place Them in the Pyramids"):
        match = re.search(rf"(?m)^{re.escape(closing)}\s*$", markdown)
        if match and match.start() > start_match.start():
            starts.append(match.start())
    next_number = re.search(r"(?m)^# \d+\. .+$", markdown[start_match.end():])
    if next_number:
        starts.append(start_match.end() + next_number.start())
    end = min(starts) if starts else len(markdown)
    return markdown[start_match.start():end].strip()


def extract_subsection(markdown: str, heading: str) -> str:
    match = re.search(rf"(?m)^## {re.escape(heading)}\s*$", markdown)
    if not match:
        raise ValueError(f"Missing guardian subsection: {heading}")
    next_heading = re.search(r"(?m)^#{1,2} ", markdown[match.end():])
    end = match.end() + next_heading.start() if next_heading else len(markdown)
    return markdown[match.start():end].strip()


def stats() -> dict:
    return {
        "systemId": "dnd5e",
        "systemVersion": "5.3.3",
        "coreVersion": "14.365",
        "createdTime": 1789330560000,
        "modifiedTime": 1789330560000,
        "lastModifiedBy": "pindarianpyramids",
    }


def recovery(period: str | None) -> list[dict]:
    if not period:
        return []
    return [{"period": period, "type": "recoverAll", "formula": ""}]


def damage_parts(parts: list[tuple[int, int, str]]) -> list[dict]:
    return [
        {
            "number": number,
            "denomination": denomination,
            "bonus": "",
            "types": [damage_type],
            "custom": {"enabled": False, "formula": ""},
            "scaling": {"mode": "", "number": 1, "formula": ""},
        }
        for number, denomination, damage_type in parts
    ]


def feature_description(markdown: str, name: str) -> str:
    match = re.search(rf"(?m)^###? {re.escape(name)}\s*$", markdown)
    if not match:
        return f"<p>See the full item description for {html.escape(name)}.</p>"
    following = re.search(r"(?m)^###? ", markdown[match.end():])
    end = match.end() + following.start() if following else len(markdown)
    return markdown_to_html(markdown[match.start():end].strip())


def activity_common(item_name: str, feature: dict, item_id: str, sort: int) -> dict:
    name = feature["name"]
    activity_id = foundry_id(f"activity:{item_name}:{name}")
    template_type, template_size = feature.get("template", ("", ""))
    duration_value, duration_units = feature.get("duration", ("", "inst"))
    consume_item = feature.get("consume_item", False)
    consumption = []
    if consume_item:
        consumption.append(
            {
                "type": "itemUses",
                "target": "",
                "value": "1",
                "scaling": {"mode": "", "number": None},
            }
        )
    if feature.get("uses") or feature.get("recharge"):
        consumption.append(
            {
                "type": "activityUses",
                "target": "",
                "value": "1",
                "scaling": {"mode": "", "number": None},
            }
        )
    return {
        "_id": activity_id,
        "type": feature.get("kind", "utility"),
        "name": name,
        "img": "",
        "sort": sort,
        "activation": {
            "type": feature.get("activation", "special"),
            "value": None,
            "override": False,
            "condition": feature.get("condition", ""),
        },
        "consumption": {
            "scaling": {"allowed": False, "max": ""},
            "spellSlot": False,
            "targets": consumption,
        },
        "description": {"chatFlavor": feature.get("chat", "")},
        "duration": {
            "units": duration_units,
            "value": "" if duration_value is None else str(duration_value),
            "special": "",
            "concentration": False,
            "override": False,
        },
        "effects": [],
        "range": {
            "units": "self" if not feature.get("range") else "ft",
            "value": None if not feature.get("range") else str(feature["range"]),
            "special": "",
            "override": False,
        },
        "target": {
            "template": {
                "count": "",
                "contiguous": False,
                "type": template_type,
                "size": "" if template_size == "" else str(template_size),
                "width": "",
                "height": "",
                "units": "ft" if template_type else "",
            },
            "affects": {
                "count": feature.get("targets", "1"),
                "type": feature.get("target_type", "creature"),
                "choice": feature.get("choice", False),
                "special": "",
            },
            "override": False,
            "prompt": True,
        },
        "uses": {
            "spent": 0,
            "max": "1" if feature.get("recharge") else feature.get("uses", ""),
            "recovery": (
                [{"period": "recharge", "type": "recoverAll", "formula": str(feature["recharge"])}]
                if feature.get("recharge")
                else recovery(feature.get("recovery"))
            ),
        },
    }


def activity_from_feature(item_name: str, item_id: str, feature: dict, sort: int) -> dict:
    activity = activity_common(item_name, feature, item_id, sort)
    kind = activity["type"]
    parts = damage_parts(feature.get("damage", []))
    if kind == "attack":
        activity["attack"] = {
            "ability": feature.get("ability", ""),
            "bonus": "",
            "critical": {"threshold": None},
            "flat": False,
            "type": {"value": feature.get("attack_type", "melee"), "classification": "weapon"},
        }
        activity["damage"] = {
            "critical": {"allow": True, "bonus": ""},
            "includeBase": feature.get("include_base", False),
            "parts": parts,
        }
    elif kind == "save":
        activity["damage"] = {"onSave": feature.get("on_save", "none"), "parts": parts}
        activity["save"] = {
            "ability": [feature.get("save", "wis")],
            "dc": {"calculation": "flat", "formula": str(feature.get("dc", 10))},
        }
    elif kind == "damage":
        activity["damage"] = {
            "critical": {"allow": False, "bonus": ""},
            "parts": parts,
        }
    elif kind == "heal":
        number, denomination, healing_type = feature.get("healing", (1, 1, "healing"))
        activity["healing"] = {
            "number": number,
            "denomination": denomination,
            "bonus": feature.get("formula", ""),
            "types": [healing_type],
            "custom": {"enabled": False, "formula": ""},
            "scaling": {"mode": "", "number": 1, "formula": ""},
        }
    return activity


def weapon_attack_activity(name: str, base_item: str) -> dict:
    number, denomination, damage_type, weapon_type = BASE_WEAPONS[base_item]
    if name == "Feastchain":
        number, denomination = 2, 8
    feature = {
        "name": "Weapon Attack",
        "kind": "attack",
        "activation": "action",
        "range": 150 if weapon_type.endswith("R") else 5,
        "attack_type": "ranged" if weapon_type.endswith("R") else "melee",
        "include_base": True,
        "damage": EXTRA_DAMAGE.get(name, []),
    }
    return activity_from_feature(name, foundry_id(f"item:{name}"), feature, 0)


def effect_record(
    parent_collection: str,
    parent_id: str,
    name: str,
    icon: str,
    changes: list[dict],
    *,
    disabled: bool = True,
    transfer: bool = True,
) -> tuple[bytes, bytes]:
    effect_id = foundry_id(f"effect:{parent_collection}:{parent_id}:{name}")
    effect = {
        "_id": effect_id,
        "name": name,
        "img": icon,
        "type": "base",
        "system": {},
        "changes": changes,
        "disabled": disabled,
        "duration": {
            "startTime": None,
            "seconds": None,
            "combat": None,
            "rounds": None,
            "turns": None,
            "startRound": None,
            "startTurn": None,
        },
        "description": "",
        "origin": None,
        "tint": "#ffffff",
        "transfer": transfer,
        "statuses": [],
        "sort": 0,
        "flags": {"dnd5e": {"type": "enchantment"}},
    }
    key = f"!{parent_collection}.effects!{parent_id}.{effect_id}".encode()
    return key, json.dumps(effect, separators=(",", ":")).encode()



# ---------------------------------------------------------------------------
# Art resolution.
#
# Art is matched to content by slug. Every lookup goes through these helpers so
# that a missing file degrades to the module cover rather than a broken path,
# and so that build-time reporting can list exactly what is unmatched.
# ---------------------------------------------------------------------------

MODULE_COVER = "branding/module-cover.webp"


def art_slug(text: str) -> str:
    """Slug used by the art files: lowercase, non-alphanumerics to hyphens."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)


def _art_index(folder: str) -> dict[str, str]:
    directory = ASSET_ROOT / folder
    if not directory.is_dir():
        return {}
    return {path.stem: f"{folder}/{path.name}" for path in sorted(directory.glob("*.webp"))}


ART_INDEX: dict[str, dict[str, str]] = {}
ART_USED: set[str] = set()
ART_MISSES: list[tuple[str, str]] = []


def art_path(folder: str, *candidates: str, fallback: str = MODULE_COVER) -> str:
    """Resolve the first candidate slug that has a file in `folder`."""
    index = ART_INDEX.setdefault(folder, _art_index(folder))
    for candidate in candidates:
        if not candidate:
            continue
        slug = art_slug(candidate)
        if slug in index:
            ART_USED.add(index[slug])
            return f"modules/{MODULE_ID}/assets/art/{index[slug]}"
    wanted = next((c for c in candidates if c), "")
    ART_MISSES.append((folder, wanted))
    return f"modules/{MODULE_ID}/assets/art/{fallback}"


ACTOR_ART_ALIASES = {
    "General Rhakkar Sol - The Starved Lion": "rhakkar-sol",
    "Marshal Korveth Anor - The Blind Cartographer": "korveth-anor",
    "Nymara Thess - Keeper of the Last Garden": "nymara-thess",
    "Aul Tareth - The Man Who Refused to Melt": "aul-tareth",
    "High Scribe Irio Venn - Keeper of the Unaltered Word": "irio-venn",
    "Hestra Vaun - Last Marshal of Pindaria": "hestra-vaun",
    "Kathandar, Elder Dragonlord": "kathandar",
    "Vaelis, the Concordant Twin": "vaelis",
    "Vaelith, the Concordant Twin": "vaelith",
    "Ivresse, Saharim Custodian": "ivresse-saharim-custodian",
    "Ssarveth Kol, First Voice": "ssarveth-kol-first-voice",
    "Vhaskar Corr, the Winged Shadow": "vhaskar-corr-the-winged-shadow",
    "Vhessara, the Devouring Queen": "vhessara-the-devouring-queen",
    "Vael'Shaar Reality Architect": "vael-shaar-reality-architect",
}


CONTEXT_ART = {
    "Astra": "locations/astra.webp",
    "Khar'Zhul": "locations/kharzhul.webp",
    "Vhal'Kathar": "locations/vhalkathar.webp",
    "Ilyr-Ameul": "locations/ilyrameul.webp",
    "Gor-Mazaal": "locations/gormazaal.webp",
    "Myr'Velora": "locations/myrvelora.webp",
    "Thaal-Uluun": "locations/thaaluluun.webp",
    "Nar'Vael": "locations/narvael.webp",
    "Khal'Vethar": "locations/khalvethar.webp",
}


def context_fallback(context: str | None) -> str:
    for key, filename in CONTEXT_ART.items():
        if context and key.lower() in context.lower():
            return filename
    return MODULE_COVER


def actor_art(name: str, *extra: str, fallback: str = MODULE_COVER) -> str:
    """Actor portraits, tried longest-name-first then trimmed of subtitles."""
    trimmed = re.split(r"\s+[-,]\s+", name)[0]
    first = name.split(",")[0]
    alias = ACTOR_ART_ALIASES.get(name)
    return art_path("actors", alias, name, *extra, trimmed, first, fallback=fallback)


def spell_art(name: str) -> str:
    return art_path("spells", name)


def journal_page_art(journal: str, index: int, title: str) -> str:
    """assets/art/journals/<journal-slug>--<NNN>-<page-slug>.webp"""
    return art_path("journals", f"{art_slug(journal)}--{index:03d}-{art_slug(title)}")


def journal_page_image(name: str, title: str, index: int) -> str:
    """Per-page art first, then the page's subject, then the journal's own art."""
    index_map = ART_INDEX.setdefault("journals", _art_index("journals"))
    # Art is filed under the journal's subject, without the " - Site Guide" suffix.
    stems = {art_slug(name), art_slug(re.sub(r"\s*-\s*Site Guide$", "", name))}
    for stem in stems:
        slug = f"{stem}--{index:03d}-{art_slug(title)}"
        if slug in index_map:
            ART_USED.add(index_map[slug])
            return f"modules/{MODULE_ID}/assets/art/{index_map[slug]}"
    slug = f"{art_slug(name)}--{index:03d}-{art_slug(title)}"
    if title in LOCATION_ART:
        ART_USED.add(f"locations/{LOCATION_ART[title]}")
        return f"modules/{MODULE_ID}/assets/art/locations/{LOCATION_ART[title]}"
    if title in RELIC_ART:
        ART_USED.add(f"items/{RELIC_ART[title]}")
        return f"modules/{MODULE_ID}/assets/art/items/{RELIC_ART[title]}"
    if name in SITE_GUIDE_ART:
        ART_USED.add(f"locations/{SITE_GUIDE_ART[name]}")
        return f"modules/{MODULE_ID}/assets/art/locations/{SITE_GUIDE_ART[name]}"
    ART_MISSES.append(("journals", slug))
    return f"modules/{MODULE_ID}/assets/art/branding/module-cover.webp"


def journal_records(name: str, markdown: str) -> list[tuple[bytes, bytes]]:
    journal_id = foundry_id(f"journal:{name}")
    sections = journal_sections(name, trim_preface(markdown, name))
    page_ids = [foundry_id(f"page:{name}:{title}:{i}") for i, (title, _) in enumerate(sections)]
    journal = {
        "_id": journal_id,
        "name": name,
        "folder": None,
        "sort": 100000,
        "ownership": {"default": 0},
        "flags": {},
        "_stats": stats(),
    }
    records = [(f"!journal!{journal_id}".encode(), json.dumps(journal, separators=(",", ":")).encode())]
    for sort, ((title, body), page_id) in enumerate(zip(sections, page_ids), 1):
        image_path = journal_page_image(name, title, sort)
        content = (
            f'<div class="pindarian-pyramids"><figure class="pindarian-splash">'
            f'<img src="{html.escape(image_path)}" alt="{html.escape(title)}">'
            f'<figcaption>{html.escape(title)}</figcaption></figure>{markdown_to_html(body)}</div>'
        )
        page = {
            "_id": page_id,
            "name": title,
            "type": "text",
            "title": {"show": True, "level": 1},
            "image": {},
            "text": {"format": 1, "content": content, "markdown": ""},
            "video": {"controls": True, "volume": 0.5},
            "src": None,
            "system": {},
            "sort": sort * 100000,
            "ownership": {"default": -1},
            "flags": {"pindarian-pyramids": {"source": name}},
            "_stats": stats(),
        }
        key = f"!journal.pages!{journal_id}.{page_id}".encode()
        records.append((key, json.dumps(page, separators=(",", ":")).encode()))
    return records


def item_records(name: str, base_item: str, rarity: str, icon: str, body: str, category: str) -> list[tuple[bytes, bytes]]:
    item_id = foundry_id(f"item:{name}")
    icon = art_path("items", Path(icon).stem)
    number, die, damage_type, weapon_type = BASE_WEAPONS[base_item]
    properties = ["mgc"]
    if base_item in {"greatsword", "greataxe", "maul"}:
        properties.extend(["hvy", "two"])
    if base_item in {"rapier", "whip"}:
        properties.append("fin")
    if name == "The Velvet Ruin":
        properties.append("fin")
    if name == "The Two That Are One":
        properties.append("ver")
    if base_item == "longbow":
        properties.extend(["amm", "hvy", "two"])
    activities = {weapon_attack_activity(name, base_item)["_id"]: weapon_attack_activity(name, base_item)}
    for sort, raw_feature in enumerate(ITEM_FEATURES[name], 1):
        feature = dict(raw_feature)
        feature["chat"] = feature_description(body, feature["name"])
        activity = activity_from_feature(name, item_id, feature, sort * 100000)
        activities[activity["_id"]] = activity

    base_number, base_die, base_type, _weapon_type = BASE_WEAPONS[base_item]
    if name == "Feastchain":
        base_number, base_die = 2, 8
    system = {
        "description": {"value": f'<div class="pindarian-pyramids">{markdown_to_html(body)}</div>', "chat": ""},
        "source": {"custom": "Pacts & Polyhedrals", "book": "Pindarian Pyramids", "page": "", "license": "", "revision": 1, "rules": "2024"},
        "identified": True,
        "unidentified": {"description": "", "name": "Unidentified Relic"},
        "quantity": 1,
        "weight": {"value": 0, "units": "lb"},
        "price": {"value": 0, "denomination": "gp"},
        "rarity": rarity,
        "attunement": "required",
        "attuned": False,
        "equipped": False,
        "cover": None,
        "range": {"value": 5 if weapon_type.endswith("M") else 150, "long": None if weapon_type.endswith("M") else 600, "units": "ft", "reach": None},
        "damage": {
            "base": {"number": base_number, "denomination": base_die, "bonus": "", "types": [base_type] if base_type else [], "custom": {"enabled": False, "formula": ""}, "scaling": {"mode": "", "number": 1, "formula": ""}},
            "versatile": {"number": None, "denomination": None, "bonus": "", "types": [], "custom": {"enabled": False, "formula": ""}, "scaling": {"mode": "", "number": None, "formula": ""}},
        },
        "type": {"value": weapon_type, "baseItem": base_item},
        "properties": properties,
        "proficient": None,
        "activities": activities,
        "uses": {
            "spent": 0,
            "max": "6" if name == "The Velvet Ruin" else ("3" if name == "Gravewake" else ""),
            "recovery": ([{"period": "day", "type": "formula", "formula": "1d4 + 2"}] if name == "The Velvet Ruin" else []),
        },
        "magicalBonus": 3 if rarity == "artifact" else 1,
        "ability": "wis" if name == "The Kindly Anatomist" else "",
        "attack": {"bonus": "", "flat": False},
        "identifier": identifier(name),
    }
    item = {
        "_id": item_id,
        "name": name,
        "type": "weapon",
        "img": icon,
        "system": system,
        "effects": [],
        "folder": None,
        "sort": 100000,
        "ownership": {"default": 0},
        "flags": {"pindarian-pyramids": {"category": category}},
        "_stats": stats(),
    }
    records = [(f"!items!{item_id}".encode(), json.dumps(item, separators=(",", ":")).encode())]
    if name == "Winter's Grudge":
        records.append(effect_record("items", item_id, "Giant's Wrath - Strength 23", icon, [{"key": "system.abilities.str.value", "mode": 4, "value": "23", "priority": 20}], disabled=False))
    return records


def fivefold_scale_records(markdown: str) -> list[tuple[bytes, bytes]]:
    name = "Fivefold Scale"
    item_id = foundry_id(f"item:{name}")
    icon = art_path("items", "fivefold-scale")
    effect_ids = {
        damage_type: foundry_id(f"effect:items:{item_id}:Fivefold Resilience - {damage_type.title()}")
        for damage_type in ("acid", "cold", "fire", "lightning", "poison")
    }
    features = [
        {"name": "We Stand as Many", "activation": "reaction", "range": 30, "consume_item": True, "condition": "A creature you can see within 30 feet fails a saving throw."},
        {"name": "Fivefold Resilience - Acid", "activation": "special"},
        {"name": "Fivefold Resilience - Cold", "activation": "special"},
        {"name": "Fivefold Resilience - Fire", "activation": "special"},
        {"name": "Fivefold Resilience - Lightning", "activation": "special"},
        {"name": "Fivefold Resilience - Poison", "activation": "special"},
        {"name": "Sixth Light", "activation": "special", "range": 30},
        {"name": "Many Stand as One", "activation": "special", "range": 30},
        {"name": "Draconic Concord", "activation": "special"},
    ]
    activities = {}
    for sort, raw_feature in enumerate(features):
        feature = dict(raw_feature)
        source_heading = "Fivefold Resilience" if feature["name"].startswith("Fivefold Resilience") else feature["name"]
        feature["chat"] = feature_description(markdown, source_heading)
        activity = activity_from_feature(name, item_id, feature, sort * 100000)
        if feature["name"].startswith("Fivefold Resilience"):
            damage_type = feature["name"].rsplit(" ", 1)[-1].lower()
            activity["effects"] = [
                {
                    "_id": effect_ids[damage_type],
                    "level": {"min": None, "max": None},
                    "riders": {"effect": [], "item": []},
                }
            ]
        activities[activity["_id"]] = activity
    system = {
        "description": {"value": f'<div class="pindarian-pyramids">{markdown_to_html(markdown)}</div>', "chat": ""},
        "identifier": "fivefold-scale",
        "source": {"book": "Pindarian Pyramids", "page": "", "custom": "Pacts & Polyhedrals", "license": "", "revision": 1, "rules": "2024"},
        "quantity": 1,
        "weight": {"value": 1, "units": "lb"},
        "price": {"value": 0, "denomination": "gp"},
        "rarity": "veryRare",
        "identified": True,
        "activities": activities,
        "uses": {"spent": 0, "max": "3", "recovery": [{"period": "day", "type": "recoverAll", "formula": ""}]},
        "type": {"value": "wondrous", "baseItem": ""},
        "properties": ["mgc"],
        "magicalBonus": None,
        "attuned": False,
        "attunement": "required",
        "equipped": False,
        "armor": {"value": None, "dex": None, "magicalBonus": None},
        "strength": None,
        "stealth": False,
    }
    item = {
        "_id": item_id,
        "name": name,
        "type": "equipment",
        "img": icon,
        "folder": None,
        "sort": 1600000,
        "system": system,
        "effects": [],
        "ownership": {"default": 0},
        "flags": {"pindarian-pyramids": {"category": "Story Relic", "state": "Dormant"}},
        "_stats": stats(),
    }
    records = [(f"!items!{item_id}".encode(), json.dumps(item, separators=(",", ":")).encode())]
    for damage_type, effect_id in effect_ids.items():
        effect = {
            "_id": effect_id,
            "name": f"Fivefold Resilience - {damage_type.title()}",
            "img": icon,
            "type": "base",
            "system": {},
            "changes": [{"key": "system.traits.dr.value", "mode": 2, "value": damage_type, "priority": 20}],
            "disabled": True,
            "duration": {"startTime": None, "seconds": None, "combat": None, "rounds": None, "turns": None, "startRound": None, "startTurn": None},
            "description": f"Enable after a long rest to select {damage_type} resistance. Disable the other Fivefold Resilience effects.",
            "origin": None,
            "tint": "#ffffff",
            "transfer": True,
            "statuses": [],
            "sort": 0,
            "flags": {"dnd5e": {"type": "enchantment"}},
        }
        key = f"!items.effects!{item_id}.{effect_id}".encode()
        records.append((key, json.dumps(effect, separators=(",", ":")).encode()))
    records.append(
        effect_record(
            "items",
            item_id,
            "Draconic Concord - Language",
            icon,
            [{"key": "system.traits.languages.value", "mode": 2, "value": "draconic", "priority": 20}],
            disabled=False,
        )
    )
    return records


def actor_record(name: str, location: str, body: str, icon: str) -> tuple[bytes, bytes]:
    actor_id = foundry_id(f"actor:{name}")
    icon = f"modules/{MODULE_ID}/assets/art/actors/{icon}"
    biography = (
        f'<div class="pindarian-pyramids"><p><em>Saharim guardian of {html.escape(location)}.</em></p>'
        '<p><strong>Rules note.</strong> This source provides characterization and encounter guidance, '
        'but no combat stat block. The actor is therefore configured as a narrative NPC for the GM to '
        'adapt to the party.</p>'
        f'{markdown_to_html(body)}</div>'
    )
    abilities = {
        ability: {"value": 10, "proficient": 0, "max": None, "bonuses": {"check": "", "save": ""}}
        for ability in ("str", "dex", "con", "int", "wis", "cha")
    }
    actor = {
        "_id": actor_id,
        "name": name,
        "type": "npc",
        "img": icon,
        "folder": None,
        "sort": 100000,
        "prototypeToken": {
            "name": name,
            "displayName": 20,
            "actorLink": False,
            "width": 1,
            "height": 1,
            "texture": {"src": icon, "scaleX": 1, "scaleY": 1, "offsetX": 0, "offsetY": 0, "rotation": 0, "tint": "#ffffff"},
            "sight": {"enabled": True, "range": 0},
            "disposition": 0,
            "displayBars": 40,
            "bar1": {"attribute": "attributes.hp"},
            "bar2": {"attribute": None},
        },
        "system": {
            "abilities": abilities,
            "attributes": {
                "ac": {"flat": 10, "calc": "flat", "formula": ""},
                "hp": {"value": 1, "max": 1, "temp": 0, "tempmax": 0, "formula": ""},
                "init": {"ability": "", "bonus": "", "roll": {"min": None, "max": None, "mode": 0}},
                "movement": {"burrow": 0, "climb": 0, "fly": 0, "swim": 0, "walk": 30, "units": "ft", "hover": False},
                "senses": {"darkvision": 0, "blindsight": 0, "tremorsense": 0, "truesight": 0, "units": "ft", "special": ""},
                "spellcasting": "",
            },
            "details": {
                "biography": {"value": biography, "public": ""},
                "alignment": "",
                "race": None,
                "type": {"value": "custom", "subtype": "", "swarm": "", "custom": "Saharim"},
                "environment": location,
                "cr": 0,
                "spellLevel": 0,
                "source": {"book": "Pindarian Pyramids", "page": "", "custom": "Pacts & Polyhedrals", "license": "", "revision": 1, "rules": "2024"},
            },
            "traits": {
                "size": "med",
                "di": {"value": [], "bypasses": [], "custom": ""},
                "dr": {"value": [], "bypasses": [], "custom": ""},
                "dv": {"value": [], "bypasses": [], "custom": ""},
                "ci": {"value": [], "custom": ""},
                "languages": {"value": [], "custom": "Pindarian languages"},
            },
            "skills": {},
            "tools": {},
            "spells": {},
            "resources": {"legact": {"value": 0, "max": 0}, "legres": {"value": 0, "max": 0}, "lair": {"value": False, "initiative": None}},
            "bonuses": {},
        },
        "effects": [],
        "ownership": {"default": 0},
        "flags": {"pindarian-pyramids": {"category": "Saharim Guardian", "narrativeActor": True}},
        "_stats": stats(),
    }
    return f"!actors!{actor_id}".encode(), json.dumps(actor, separators=(",", ":")).encode()


def actor_action_record(actor_id: str, actor_name: str, icon: str, spec: dict, sort: int) -> tuple[bytes, bytes]:
    item_id = foundry_id(f"actor-item:{actor_name}:{spec['name']}")
    feature = dict(spec)
    feature["chat"] = f"<p>{html.escape(spec['description'])}</p>"
    activity = activity_from_feature(actor_name, item_id, feature, 0)
    activity_id = activity["_id"]
    item_type = "weapon" if spec.get("kind") == "attack" else "feat"
    common = {
        "description": {"value": f"<p>{html.escape(spec['description'])}</p>", "chat": ""},
        "identifier": identifier(spec["name"]),
        "source": {"book": "Pindarian Pyramids", "page": "", "custom": "Pacts & Polyhedrals", "license": "", "revision": 1, "rules": "2024"},
        "activities": {activity_id: activity},
        "uses": {"spent": 0, "max": spec.get("uses", ""), "recovery": recovery(spec.get("recovery"))},
        "properties": ["mgc"] if item_type == "weapon" else [],
    }
    if item_type == "weapon":
        common.update(
            {
                "quantity": 1,
                "weight": {"value": 0, "units": "lb"},
                "price": {"value": 0, "denomination": "gp"},
                "rarity": "",
                "identified": True,
                "type": {"value": "simpleR" if spec.get("attack_type") == "ranged" else "simpleM", "baseItem": ""},
                "damage": {"base": {"number": None, "denomination": None, "types": [], "custom": {"enabled": False, "formula": ""}, "scaling": {"number": 1}}, "versatile": {}},
                "magicalBonus": None,
                "proficient": True,
                "ability": spec.get("ability", ""),
                "attack": {"bonus": "", "flat": False},
                "equipped": True,
            }
        )
    else:
        common.update(
            {
                "type": {"value": "monster", "subtype": ""},
                "requirements": "",
                "prerequisites": {"level": None},
                "enchant": {},
            }
        )
    item = {
        "_id": item_id,
        "name": spec["name"],
        "type": item_type,
        "img": icon,
        "sort": sort,
        "ownership": {"default": 0},
        "flags": {"pindarian-pyramids": {"actorAction": True}},
        "system": common,
        "effects": [],
    }
    key = f"!actors.items!{actor_id}.{item_id}".encode()
    return key, json.dumps(item, separators=(",", ":")).encode()


def actor_records(name: str, location: str, body: str, icon_filename: str) -> list[tuple[bytes, bytes]]:
    parent_key, parent_value = actor_record(name, location, body, icon_filename)
    actor = json.loads(parent_value)
    block = GUARDIAN_BLOCKS[name]
    ability_names = ("str", "dex", "con", "int", "wis", "cha")
    for ability, value in zip(ability_names, block["abilities"]):
        actor["system"]["abilities"][ability]["value"] = value
        actor["system"]["abilities"][ability]["proficient"] = 1 if ability in block["saves"] else 0
    actor["system"]["attributes"]["ac"] = {"flat": block["ac"], "calc": "flat", "formula": ""}
    actor["system"]["attributes"]["hp"] = {"value": block["hp"], "max": block["hp"], "temp": 0, "tempmax": 0, "formula": block["formula"]}
    actor["system"]["details"]["cr"] = block["cr"]
    actor["system"]["details"]["alignment"] = "Lawful Neutral"
    skills = {}
    for skill, ability in {
        "acr": "dex", "ani": "wis", "arc": "int", "ath": "str", "dec": "cha", "his": "int",
        "ins": "wis", "itm": "cha", "inv": "int", "med": "wis", "nat": "int", "prc": "wis",
        "prf": "cha", "per": "cha", "rel": "int", "slt": "dex", "ste": "dex", "sur": "wis",
    }.items():
        skills[skill] = {"value": block["skills"].get(skill, 0), "ability": ability, "bonuses": {"check": "", "passive": ""}}
    actor["system"]["skills"] = skills
    actor["system"]["traits"]["dr"]["custom"] = "Damage from nonmagical attacks"
    actor["system"]["traits"]["ci"] = {"value": ["poisoned"], "custom": "Does not require food, drink, sleep, or air"}
    actor["system"]["attributes"]["concentration"] = {"ability": "", "bonuses": {"save": ""}, "limit": 1, "roll": {"min": None, "max": None, "mode": 0}}
    actor["system"]["attributes"]["death"] = {"ability": "", "bonuses": {"save": ""}, "roll": {}, "success": 0, "failure": 0}
    records = [(parent_key, json.dumps(actor, separators=(",", ":")).encode())]
    for sort, spec in enumerate(block["actions"], 1):
        records.append(actor_action_record(actor["_id"], name, actor["img"], spec, sort * 100000))
    return records


ABILITY_KEYS = ("str", "dex", "con", "int", "wis", "cha")

SKILL_ABILITY = {
    "acr": "dex", "ani": "wis", "arc": "int", "ath": "str", "dec": "cha", "his": "int",
    "ins": "wis", "itm": "cha", "inv": "int", "med": "wis", "nat": "int", "prc": "wis",
    "prf": "cha", "per": "cha", "rel": "int", "slt": "dex", "ste": "dex", "sur": "wis",
}

SECTION_ACTIVATION = {
    "trait": "special", "action": "action", "bonus": "bonus", "reaction": "reaction",
    "legendary": "legendary", "mythic": "mythic", "lair": "lair",
}


def statblock_actor_records(unit: dict, category: str, icon: str) -> list[tuple[bytes, bytes]]:
    """Build an NPC and its embedded features from a unit dict.

    Feature counts come from the data, not from a template - a Vector Trooper gets
    three items and a Reality Architect gets eight.
    """
    actor_id = foundry_id(f"unit:{unit['name']}")
    biography = (
        f'<div class="pindarian-pyramids">'
        f'<p><em>{html.escape(unit.get("context") or unit["tradition"] + " tradition")} - {html.escape(unit["role"])}.</em></p>'
        f'<p>{html.escape(unit["blurb"])}</p></div>'
    )
    abilities = {
        key: {
            "value": value,
            "proficient": 1 if key in unit.get("saves", []) else 0,
            "max": None,
            "bonuses": {"check": "", "save": ""},
        }
        for key, value in zip(ABILITY_KEYS, unit["abilities"])
    }
    speed = unit.get("speed", {})
    senses = unit.get("senses", {})
    skills = {
        key: {"value": unit.get("skills", {}).get(key, 0), "ability": ability, "bonuses": {"check": "", "passive": ""}}
        for key, ability in SKILL_ABILITY.items()
    }
    actor = {
        "_id": actor_id,
        "name": unit["name"],
        "type": "npc",
        "img": icon,
        "folder": None,
        "sort": 100000,
        "prototypeToken": {
            "name": unit["name"],
            "displayName": 20,
            "actorLink": False,
            "width": 1,
            "height": 1,
            "texture": {"src": icon, "scaleX": 1, "scaleY": 1, "offsetX": 0, "offsetY": 0, "rotation": 0, "tint": "#ffffff"},
            "sight": {"enabled": True, "range": 0},
            "disposition": -1,
            "displayBars": 40,
            "bar1": {"attribute": "attributes.hp"},
            "bar2": {"attribute": None},
        },
        "system": {
            "abilities": abilities,
            "attributes": {
                "ac": {"flat": unit["ac"], "calc": "flat", "formula": ""},
                "hp": {"value": unit["hp"], "max": unit["hp"], "temp": 0, "tempmax": 0, "formula": unit["formula"]},
                "init": {"ability": "", "bonus": "", "roll": {"min": None, "max": None, "mode": 0}},
                "movement": {
                    "burrow": speed.get("burrow", 0), "climb": speed.get("climb", 0),
                    "fly": speed.get("fly", 0), "swim": speed.get("swim", 0),
                    "walk": speed.get("walk", 30), "units": "ft", "hover": False,
                },
                "senses": {
                    "darkvision": senses.get("darkvision", 0), "blindsight": senses.get("blindsight", 0),
                    "tremorsense": senses.get("tremorsense", 0), "truesight": senses.get("truesight", 0),
                    "units": "ft", "special": "",
                },
                "spellcasting": unit.get("spellcasting", ""),
                "prof": unit.get("prof"),
                "concentration": {"ability": "", "bonuses": {"save": ""}, "limit": 1, "roll": {"min": None, "max": None, "mode": 0}},
                "death": {"ability": "", "bonuses": {"save": ""}, "roll": {}, "success": 0, "failure": 0},
            },
            "details": {
                "biography": {"value": biography, "public": ""},
                "alignment": unit.get("alignment", "Any Lawful"),
                "race": None,
                "type": {
                    "value": unit.get("creature_type", "humanoid"),
                    "subtype": unit.get("subtype", "pindarian"),
                    "swarm": "",
                    "custom": "",
                },
                "environment": "Pindarian Empire",
                "cr": unit["cr"],
                "spellLevel": 0,
                "source": {"book": "Pindarian Pyramids", "page": "", "custom": "Pacts & Polyhedrals", "license": "", "revision": 1, "rules": "2024"},
            },
            "traits": {
                "size": unit.get("size", "med"),
                "di": {"value": [], "bypasses": [], "custom": unit.get("di", "")},
                "dr": {"value": [], "bypasses": [], "custom": unit.get("dr", "")},
                "dv": {"value": [], "bypasses": [], "custom": unit.get("dv", "")},
                "ci": {"value": [], "custom": unit.get("ci", "")},
                "languages": {"value": [], "custom": unit.get("languages", "Pindarian")},
            },
            "skills": skills,
            "tools": {},
            "spells": {},
            "resources": {
                "legact": {"value": unit.get("legact", 0), "max": unit.get("legact", 0)},
                "legres": {"value": unit.get("legres", 0), "max": unit.get("legres", 0)},
                "lair": {
                    "value": bool(unit.get("lair_initiative")),
                    "initiative": unit.get("lair_initiative"),
                },
            },
            "bonuses": {},
        },
        "effects": [],
        "ownership": {"default": 0},
        "flags": {"pindarian-pyramids": {"category": category, "tradition": unit.get("tradition", "")}},
        "_stats": stats(),
    }
    records = [(f"!actors!{actor_id}".encode(), json.dumps(actor, separators=(",", ":")).encode())]
    for sort, (section, name, body, spec) in enumerate(unit["features"], 1):
        feature = dict(spec or {})
        feature["name"] = name
        feature["description"] = body
        feature.setdefault("activation", SECTION_ACTIVATION.get(section, "special"))
        records.append(
            statblock_feature_record(actor_id, unit["name"], icon, section, feature, sort * 100000)
        )
    base = (len(unit["features"]) + 1) * 100000
    for offset, spell in enumerate(unit.get("spells", [])):
        records.append(actor_spell_record(actor_id, unit, icon, spell, base + offset * 1000))
    return records


def actor_spell_record(actor_id: str, unit: dict, icon: str, spell: tuple, sort: int) -> tuple[bytes, bytes]:
    """A prepared spell embedded on an NPC sheet.

    A sixth element, when present, is an activity spec: the spell rolls attacks,
    saves and damage from the sheet rather than being a reference entry.
    """
    actor_name = unit["name"]
    name, level, school, components, spell_range, body = spell[:6]
    spec = spell[6] if len(spell) > 6 else None
    item_id = foundry_id(f"actor-spell:{actor_name}:{sort}:{name}")
    range_value, range_units = spell_range
    activities: dict = {}
    if spec:
        feature = dict(spec)
        feature["name"] = name
        feature["description"] = body
        feature.setdefault("activation", "action")
        feature.setdefault("range", range_value or 0)
        if feature.get("kind") == "save":
            feature.setdefault("dc", unit.get("spell_dc", 15))
        activity = activity_from_feature(actor_name, item_id, feature, 0)
        activity["consumption"]["spellSlot"] = level > 0
        if "attack" in activity:
            activity["attack"]["type"]["classification"] = "spell"
            activity["attack"]["bonus"] = str(unit.get("spell_attack", ""))
            activity["attack"]["flat"] = True
        activities[activity["_id"]] = activity
    item = {
        "_id": item_id,
        "name": name,
        "type": "spell",
        "img": spell_art(name),
        "sort": sort,
        "ownership": {"default": 0},
        "flags": {"pindarian-pyramids": {"section": "spell"}},
        "system": {
            "description": {"value": f'<div class="pindarian-pyramids">{markdown_to_html(body)}</div>', "chat": ""},
            "identifier": identifier(name),
            "source": {"book": "Pindarian Pyramids", "page": "", "custom": "Pacts & Polyhedrals", "license": "", "revision": 1, "rules": "2024"},
            "activation": {"type": "action", "condition": "", "value": None},
            "duration": {"value": "", "units": "inst"},
            "range": {"value": range_value or None, "units": range_units, "special": ""},
            "target": {"affects": {"count": "", "type": "", "choice": False, "special": ""}, "template": {"count": "", "contiguous": False, "type": "", "size": "", "units": "ft"}},
            "uses": {"max": "", "recovery": [], "spent": 0},
            "level": level,
            "school": school,
            "properties": [part for part in components.split(",") if part],
            "materials": {"value": "", "consumed": False, "cost": 0, "supply": 0},
            "activities": activities,
            "method": "spell",
            "prepared": 1,
            "sourceClass": "",
        },
        "effects": [],
    }
    return f"!actors.items!{actor_id}.{item_id}".encode(), json.dumps(item, separators=(",", ":")).encode()


def statblock_feature_record(actor_id: str, actor_name: str, icon: str, section: str, feature: dict, sort: int) -> tuple[bytes, bytes]:
    # The section and position are part of the seed: a legendary action and an
    # action may share a name ("Glaive", "Strike", "Errata") and must not collide.
    item_id = foundry_id(f"unit-item:{actor_name}:{section}:{sort}:{feature['name']}")
    feature = dict(feature)
    feature["chat"] = ""
    activity = activity_from_feature(actor_name, item_id, feature, 0)
    item_type = "weapon" if feature.get("kind") == "attack" else "feat"
    description = f'<div class="pindarian-pyramids">{markdown_to_html(feature["description"])}</div>'
    system = {
        "description": {"value": description, "chat": ""},
        "identifier": identifier(feature["name"]),
        "source": {"book": "Pindarian Pyramids", "page": "", "custom": "Pacts & Polyhedrals", "license": "", "revision": 1, "rules": "2024"},
        "activities": {activity["_id"]: activity},
        "uses": {
            "spent": 0,
            "max": "1" if feature.get("recharge") else feature.get("uses", ""),
            "recovery": (
                [{"period": "recharge", "type": "recoverAll", "formula": str(feature["recharge"])}]
                if feature.get("recharge")
                else recovery(feature.get("recovery"))
            ),
        },
        "properties": ["mgc"] if item_type == "weapon" else [],
    }
    if item_type == "weapon":
        system.update({
            "quantity": 1,
            "weight": {"value": 0, "units": "lb"},
            "price": {"value": 0, "denomination": "gp"},
            "rarity": "",
            "identified": True,
            "type": {"value": "simpleR" if feature.get("attack_type") == "ranged" else "simpleM", "baseItem": ""},
            "damage": {"base": {"number": None, "denomination": None, "types": [], "custom": {"enabled": False, "formula": ""}, "scaling": {"number": 1}}, "versatile": {}},
            "magicalBonus": None,
            "proficient": True,
            "ability": feature.get("ability", ""),
            "attack": {"bonus": "", "flat": False},
            "equipped": True,
        })
    else:
        system.update({
            "type": {"value": "monster", "subtype": ""},
            "requirements": "",
            "prerequisites": {"level": None},
            "enchant": {},
        })
    item = {
        "_id": item_id,
        "name": feature["name"],
        "type": item_type,
        "img": icon,
        "sort": sort,
        "ownership": {"default": 0},
        "flags": {"pindarian-pyramids": {"section": section}},
        "system": system,
        "effects": [],
    }
    return f"!actors.items!{actor_id}.{item_id}".encode(), json.dumps(item, separators=(",", ":")).encode()


def spell_item_record(tradition: str, people: str, spell: tuple, sort: int) -> tuple[bytes, bytes]:
    name, level, school, components, duration, spell_range, body, spec = spell
    spell_id = foundry_id(f"spell:{name}")
    properties = [part for part in components.split(",") if part]
    feature = dict(spec or {})
    feature["name"] = name
    feature["description"] = body
    feature.setdefault("activation", "action")
    activity = activity_from_feature(name, spell_id, feature, 0)
    activity["consumption"]["spellSlot"] = True
    if feature.get("kind") in {"save", "attack"}:
        if "save" in activity:
            activity["save"]["dc"] = {"calculation": "spellcasting", "formula": ""}
        if "attack" in activity:
            activity["attack"]["type"]["classification"] = "spell"
    description = (
        f'<div class="pindarian-pyramids">'
        f'<p><em>{html.escape(tradition)} - magic of the {html.escape(people)}.</em></p>'
        f'{markdown_to_html(body)}</div>'
    )
    range_value, range_units = spell_range
    duration_value, duration_units = duration
    item = {
        "_id": spell_id,
        "name": name,
        "type": "spell",
        "img": spell_art(name),
        "folder": None,
        "sort": sort,
        "ownership": {"default": 0},
        "flags": {"pindarian-pyramids": {"tradition": tradition}},
        "system": {
            "description": {"value": description, "chat": ""},
            "identifier": identifier(name),
            "source": {"book": "Pindarian Pyramids", "page": tradition, "custom": "Pacts & Polyhedrals", "license": "", "revision": 1, "rules": "2024"},
            "activation": {"type": feature["activation"], "condition": "", "value": None},
            "duration": {"value": duration_value, "units": duration_units},
            "range": {"value": range_value or None, "units": range_units, "special": ""},
            "target": {"affects": {"count": "", "type": "", "choice": False, "special": ""}, "template": {"count": "", "contiguous": False, "type": "", "size": "", "units": "ft"}},
            "uses": {"max": "", "recovery": [], "spent": 0},
            "level": level,
            "school": school,
            "properties": properties,
            "materials": {"value": "", "consumed": False, "cost": 0, "supply": 0},
            "activities": {activity["_id"]: activity},
            "method": "spell",
            "prepared": 0,
            "sourceClass": "",
        },
        "effects": [],
        "_stats": stats(),
    }
    return f"!items!{spell_id}".encode(), json.dumps(item, separators=(",", ":")).encode()


def scene_record(
    name: str,
    image_path: str,
    width: int,
    height: int,
    *,
    grid_type: int = 0,
    grid_size: int = 100,
    navigation: bool = False,
    sort: int = 100000,
) -> tuple[bytes, bytes]:
    scene_id = foundry_id(f"scene:{name}")
    scene = {
        "_id": scene_id,
        "name": name,
        "active": False,
        "navigation": navigation,
        "navOrder": sort,
        "navName": "",
        "background": {
            "src": image_path,
            "anchorX": 0,
            "anchorY": 0,
            "offsetX": 0,
            "offsetY": 0,
            "fit": "fill",
            "scaleX": 1,
            "scaleY": 1,
            "rotation": 0,
            "tint": "#ffffff",
            "alphaThreshold": 0,
        },
        "foreground": None,
        "foregroundElevation": 4,
        "thumb": image_path,
        "width": width,
        "height": height,
        "padding": 0,
        "initial": {"x": None, "y": None, "scale": None},
        "backgroundColor": "#15110f",
        "grid": {
            "type": grid_type,
            "size": grid_size,
            "distance": 5,
            "units": "ft",
            "style": "solidLines",
            "thickness": 1,
            "color": "#000000",
            "alpha": 0.22 if grid_type else 0,
        },
        "tokenVision": True,
        "fog": {
            "exploration": True,
            "overlay": None,
            "colors": {"explored": None, "unexplored": None},
            "exploredColor": None,
            "unexploredColor": None,
        },
        "environment": {
            "globalLight": {"enabled": True, "darkness": {"max": 1, "min": 0}},
            "darknessLevel": 0,
            "base": {"hue": 0, "intensity": 0, "luminosity": 0, "saturation": 0, "shadows": 0},
            "dark": {"hue": 0, "intensity": 0, "luminosity": 0, "saturation": 0, "shadows": 0},
        },
        "drawings": [],
        "tokens": [],
        "lights": [],
        "notes": [],
        "sounds": [],
        "templates": [],
        "tiles": [],
        "walls": [],
        "regions": [],
        "playlist": None,
        "playlistSound": None,
        "journal": None,
        "weather": "",
        "folder": None,
        "sort": sort,
        "ownership": {"default": 0},
        "flags": {"pindarian-pyramids": {"illustrated": True}},
        "_stats": stats(),
    }
    return f"!scenes!{scene_id}".encode(), json.dumps(scene, separators=(",", ":")).encode()


def varint(value: int) -> bytes:
    result = bytearray()
    while value >= 0x80:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value)
    return bytes(result)


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


# Foundry stores embedded documents under their own sublevel keys, but the PARENT
# document must still carry an array of the embedded _id values, or the core
# document loader has nothing to resolve and the collection comes back empty.
# This mirrors mapHierarchy() in @foundryvtt/foundryvtt-cli.
HIERARCHY = {
    "actors": ["items", "effects"],
    "items": ["effects"],
    "journal": ["pages", "categories"],
    "cards": ["cards"],
    "combats": ["combatants", "groups"],
    "playlists": ["sounds"],
    "regions": ["behaviors"],
    "tables": ["results"],
    "scenes": [
        "drawings", "tokens", "levels", "lights", "notes",
        "regions", "sounds", "templates", "tiles", "walls",
    ],
}


def link_embedded_documents(records: list[tuple[bytes, bytes]]) -> list[tuple[bytes, bytes]]:
    """Populate each parent document's embedded collections with their child _ids."""
    children: dict[tuple[str, str], dict[str, list[str]]] = {}
    for key, _ in records:
        name = key.decode()
        sublevel, _, ids = name[1:].partition("!")
        if "." not in sublevel:
            continue
        parent_collection, _, embedded_collection = sublevel.rpartition(".")
        parent_id, _, child_id = ids.partition(".")
        bucket = children.setdefault((parent_collection, parent_id), {})
        bucket.setdefault(embedded_collection, []).append(child_id)

    linked: list[tuple[bytes, bytes]] = []
    for key, value in records:
        name = key.decode()
        sublevel, _, doc_id = name[1:].partition("!")
        if sublevel not in HIERARCHY:
            linked.append((key, value))
            continue
        document = json.loads(value)
        bucket = children.get((sublevel, doc_id), {})
        for embedded_collection in HIERARCHY[sublevel]:
            document[embedded_collection] = bucket.get(embedded_collection, [])
        linked.append((key, json.dumps(document, separators=(",", ":")).encode()))
    return linked


def write_pack(path: Path, records: list[tuple[bytes, bytes]]) -> None:
    records = link_embedded_documents(records)
    path.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMPLATE_PACK / "CURRENT", path / "CURRENT")
    shutil.copy2(TEMPLATE_PACK / "MANIFEST-000002", path / "MANIFEST-000002")
    body = bytearray(struct.pack("<QI", 1, len(records)))
    for key, value in records:
        body.append(1)
        body.extend(varint(len(key)))
        body.extend(key)
        body.extend(varint(len(value)))
        body.extend(value)
    if len(body) > 32761:
        # LevelDB log fragments are limited to 32 KiB blocks.
        fragments = []
        remaining = bytes(body)
        first = True
        while remaining:
            block_room = 32768 - sum(len(x) for x in fragments) % 32768
            if block_room < 7:
                fragments.append(bytes(block_room))
                block_room = 32768
            chunk = remaining[: block_room - 7]
            remaining = remaining[len(chunk):]
            record_type = 2 if first else (4 if not remaining else 3)
            header = struct.pack("<IHB", masked_crc32c(bytes([record_type]) + chunk), len(chunk), record_type)
            fragments.append(header + chunk)
            first = False
        log = b"".join(fragments)
    else:
        record_type = 1
        log = struct.pack("<IHB", masked_crc32c(bytes([record_type]) + body), len(body), record_type) + body
    (path / "000003.log").write_bytes(log)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def build() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    (OUTPUT / "assets/art").mkdir(parents=True)
    (OUTPUT / "assets/maps").mkdir(parents=True)
    (OUTPUT / "source").mkdir(parents=True)

    source_texts = {name: path.read_text(encoding="utf-8") for name, path in SOURCES.items()}
    for source_path in INPUT.glob("*.md"):
        shutil.copy2(source_path, OUTPUT / "source" / source_path.name)

    shutil.copytree(ASSET_ROOT, OUTPUT / "assets/art", dirs_exist_ok=True)
    shutil.copy2(MAP_ROOT / "pyramid-complex.jpg", OUTPUT / "assets/maps/pyramid-complex.jpg")
    shutil.copy2(MAP_ROOT / "pyramid-exterior.jpg", OUTPUT / "assets/maps/pyramid-exterior.jpg")

    manifest = {
        "id": MODULE_ID,
        "title": "Pindarian Pyramids",
        "description": "<p>The Nine Pyramids of Pindar, the Ninefold Prohibition, nine sentient demon relics, six living mimic weapons, and the Fivefold Scale for an epic fantasy campaign.</p>",
        "version": VERSION,
        "authors": [{"name": "Ben \"Asmo\" Vale", "url": "https://www.patreon.com/pactsandpolyhedrals"}],
        "compatibility": {"minimum": "14", "verified": "14", "maximum": "14"},
        "relationships": {"systems": [{"id": "dnd5e", "type": "system", "compatibility": {"minimum": "5.3.3", "verified": "5.3.3"}}]},
        "packs": [
            {"name": "lore", "label": "Pindarian Pyramids - Lore & Adventures", "path": "packs/lore", "type": "JournalEntry", "system": "dnd5e", "ownership": {"PLAYER": "OBSERVER", "ASSISTANT": "OWNER"}, "flags": {}},
            {"name": "relics", "label": "Pindarian Pyramids - Magic Items", "path": "packs/relics", "type": "Item", "system": "dnd5e", "ownership": {"PLAYER": "OBSERVER", "ASSISTANT": "OWNER"}, "flags": {}},
            {"name": "guardians", "label": "Pindarian Pyramids - Saharim Guardians", "path": "packs/guardians", "type": "Actor", "system": "dnd5e", "ownership": {"PLAYER": "OBSERVER", "ASSISTANT": "OWNER"}, "flags": {}},
            {"name": "scenes", "label": "Pindarian Pyramids - Maps & Illustrated Scenes", "path": "packs/scenes", "type": "Scene", "system": "dnd5e", "ownership": {"PLAYER": "OBSERVER", "ASSISTANT": "OWNER"}, "flags": {}},
            {"name": "legions", "label": "Pindarian Pyramids - Pindarian Armed Forces", "path": "packs/legions", "type": "Actor", "system": "dnd5e", "ownership": {"PLAYER": "OBSERVER", "ASSISTANT": "OWNER"}, "flags": {}},
            {"name": "bestiary", "label": "Pindarian Pyramids - Bestiary & Boss Roster", "path": "packs/bestiary", "type": "Actor", "system": "dnd5e", "ownership": {"PLAYER": "OBSERVER", "ASSISTANT": "OWNER"}, "flags": {}},
            {"name": "spells", "label": "Pindarian Pyramids - The Pindarian Arcana", "path": "packs/spells", "type": "Item", "system": "dnd5e", "ownership": {"PLAYER": "OBSERVER", "ASSISTANT": "OWNER"}, "flags": {}},
        ],
        "packFolders": [{"name": "Pindarian Pyramids", "sorting": "m", "color": "#b78b3e", "packs": ["lore", "relics", "guardians", "bestiary", "scenes", "legions", "spells"]}],
        "styles": ["styles/pindarian-pyramids.css"],
        "media": [
            {
                "type": "setup",
                "url": f"modules/{MODULE_ID}/assets/art/branding/module-cover.webp",
                "thumbnail": f"modules/{MODULE_ID}/assets/art/branding/module-cover.webp",
            }
        ],
        "url": REPOSITORY,
        "manifest": f"{REPOSITORY}/releases/latest/download/module.json",
        "download": f"{REPOSITORY}/releases/download/v{VERSION}/pindarian-pyramids.zip",
        "license": "LICENSE.md",
        "readme": f"{REPOSITORY}/blob/main/README.md",
        "flags": {},
    }
    write_text(OUTPUT / "module.json", json.dumps(manifest, indent=2) + "\n")

    readme = f"""# Pindarian Pyramids - Foundry VTT Module

The Nine Pyramids of Pindar, their deathless guardians, the Ninefold Prohibition,
nine demonic artifact weapons, and six dormant Mimic Relics.

## Installation

In Foundry VTT, open **Add-on Modules**, choose **Install Module**, and use:

```text
{REPOSITORY}/releases/latest/download/module.json
```

For manual installation, extract `pindarian-pyramids.zip` into
`Data/modules/pindarian-pyramids/` and restart Foundry.

## Included Compendiums

- **Pindarian Pyramids - Lore & Adventures:** Three journals covering the nine pyramids,
  their trials and guardians, all demon relics, all Mimic Relics, and awakening guidance.
- **Pindarian Pyramids - Magic Items:** Nine artifact weapons, six rare dormant Mimic
  weapons, and the very rare Fivefold Scale. Every item has multiple configured
  activities; applicable passive properties are supplied as Active Effects.
- **Pindarian Pyramids - Saharim Guardians:** Ten narrative NPC actors representing
  the named deathless guardians. The source does not provide combat stat blocks, so
  these actors carry biographies and neutral baseline statistics for GM adaptation.
- **Pindarian Pyramids - Maps & Illustrated Scenes:** The two supplied pyramid maps and
  nine theater-of-the-mind scenes, one for each pyramid.

The module includes 36 original grotesque chibi comic-book illustrations: one cover,
nine locations, ten guardian portraits, and sixteen magic-item images. The two supplied maps
are preserved under `assets/maps/`, and editable source text remains in `source/`.

## Compatibility

- Foundry VTT 14
- dnd5e 5.3.3
- No automation dependencies

## Credits

**Author and creator:** Ben \"Asmo\" Vale  
**Publisher:** Pacts & Polyhedrals  
**Repository:** {REPOSITORY}
"""
    write_text(OUTPUT / "README.md", readme)

    license_text = """# License

## Module code and packaging

Copyright (c) Ben \"Asmo\" Vale / Pacts & Polyhedrals.

## Game content

Original text, items, adventure content, and lore in this supplement are the copyright
of Ben \"Asmo\" Vale / Pacts & Polyhedrals. Generated module illustrations were created
for this project. The two supplied reference maps remain copyright of their respective
creators and are included as supplied by the project owner. All rights reserved except
where separately licensed by the applicable rights holder.
"""
    write_text(OUTPUT / "LICENSE.md", license_text)

    changelog = """# Changelog

## 2.3.1

- Repoints the repository, manifest, download and readme URLs at the `macv0223/pindarian-pyramids`
  repository.

## 2.3.0

- **Art is now assigned per entity.** Every journal page, spell, relic and actor resolves its own
  image by slug: 148 per-page journal illustrations, 55 spell cards, 16 relic icons and 44 actor
  portraits. Unmatched creatures fall back to their home pyramid's plate rather than the cover.
- Adds three travelling NPCs as real actors so their supplied portraits are used: Nuru, Cass Dree
  and Vharo Sellick.
- **Fixes an ID collision that silently deleted actions.** Embedded feature IDs were keyed on the
  feature name alone, so a legendary action sharing a name with an action ("Glaive", "Strike",
  "Errata") overwrote it. IDs now include the section and position.
- The build prints an art report, and the validator asserts that every referenced image exists.

## 2.2.0

- **Pindarians are Large.** All 41 Pindarian creatures - the nineteen legion units, all nine Saharim
  guardians, and every Pindarian construct, custodian and undead in the Bestiary - are resized from
  Medium to Large, with d10 hit dice and 10-foot reach on their melee attacks.
- Adds a "Pindarian Physiology" page to the core lore journal and a "Pindarian Scale" note to all nine
  site guides, covering doorways, stairs, furniture, and salvaged Pindarian gear.
- Guardian read-aloud text updated so the scale is described rather than stated.

## 2.1.0

- Adds the ten Original Creatures as real stat blocks: Starveling Pursuer, Tooth-Mimic, Concordant
  Echo, Moon Cantor, Maze Stalker, Pindarian Void Warden, Archive Bloom, Unmade Duplicate, Verity
  Eater and Grievance Colossus.
- Adds full stat blocks for the seven remaining guardians (Rhakkar Sol, Vaelis, Vaelith, Korveth
  Anor, Nymara Thess, Aul Tareth, Irio Venn, Hestra Vaun); the narrative placeholders are retired.
- Spells on NPC sheets are now castable: attack rolls, save DCs and damage roll from the sheet
  rather than being reference entries.

## 2.0.0

- **All nine pyramids now ship as full site guides.** Adds Khal'Vethar: 11 pages covering the
  Underside Gate through the Final Nail, with the Vengeance budget, the pyramid's initiative-20
  purchases, and the campaign's three endings.
- The Lore compendium now holds 12 journals and 148 pages.

## 1.11.0

- Adds the Nar'Vael site guide to the Lore compendium: 10 pages covering the Bright Shadow Dock
  through the Black-Sun Nail, with the Observation/Memory/Claim labelling law, the Certainty track,
  the nine murals with their false clauses, and Irio Venn's nine questions.

## 1.10.0

- Adds the Thaal-Uluun site guide to the Lore compendium: 10 pages covering the Softstone Portal
  through the Dissolving Nail, with the Dissolution track, Void Marks, and an explicit statement of
  what the Stripping Chamber does and does not take from a character sheet.

## 1.9.0

- Adds the Myr'Velora site guide to the Lore compendium: 10 pages covering the Quarantine Bloom
  through the Keeper's Nail, with the Blight track, the symbiosis system and the Garden of Corpses.

## 1.8.0

- Adds the Gor-Mazaal site guide to the Lore compendium: 10 pages covering the Blind Gate through
  the Wandering Nail, with the Bearings track, Declared Purpose, and the Maze Stalker clocks.

## 1.7.0

- Adds the Ilyr-Ameul site guide to the Lore compendium: 10 pages covering the Bifurcation through
  the Concordant Nail, with the Sun/Moon perspective split, the Discord track and Concord Tokens.

## 1.6.0

- Adds the Khar'Zhul site guide to the Lore compendium: 10 pages covering the Threshing Gate through
  the Gnawing Nail, with the Predation track, the Rations subsystem and the Last Meal.

## 1.5.0

- Adds the **Bestiary & Boss Roster** compendium: 18 set-piece creatures for the Astra and
  Vhal'Kathar site guides, including six mythic two-phase bosses (Seryth Vael, the Keeper,
  Vhaskar Corr, Vhessara and the Projected Avatar of Orcus, alongside Kathandar in Guardians).
- Legendary, lair and mythic sections throughout; shared legendary pools are noted on the blocks
  that appear in groups rather than given to every creature.
- Every mythic boss states its non-combat resolution on the sheet.

## 1.4.1

- Reconciles the three circulating versions of Kathandar into one canonical actor: a CR 22 Elder
  Dragonlord lich with 28 features across traits, actions, bonus, reaction, legendary, lair and
  mythic sections, plus an 18-spell prepared list. The narrative placeholder is no longer shipped.
- Adds legendary, lair and mythic activation support and prepared-spell embedding to the stat-block
  builder.

## 1.4.0

- Adds the **Pindarian Armed Forces** compendium: 19 Solaari, Lunari, Veylari and combined-tradition
  units from Linewarden to Vael'Shaar Reality Architect, each built with only the features it needs
  (3 to 8 per unit) rather than a fixed template.
- Adds **The Pindarian Arcana** compendium: 60 original spells across Solar, Lunar and Void Arcana,
  two at every level from cantrip to 9th.
- Adds recharge support to the activity builder, and a generic stat-block actor builder.

## 1.3.0

- Adds two expanded site guides to the Lore compendium: Astra (10 pages) and Vhal'Kathar
  (37 pages), covering every keyed area with read-aloud text, room contents, DM notes,
  trap and puzzle mechanics, NPCs, set pieces, lore drops, and plot hooks.
- Vhal'Kathar incorporates the Wahyrst siege, the Council of Horns, and the upper
  necropolis as a three-act site ending at the Last-Breath Nail.
- Adds an H2 page splitter so keyed-area documents become one journal page per area.

## 1.2.1

- Fixes empty journals and incomplete stat blocks: every parent document now carries the
  `_id` array for its embedded collections (`journal.pages`, `actors.items`,
  `items.effects`), which Foundry requires to resolve records stored in pack sublevels.
- All 30 journal pages, 40 actor actions/features, and 7 Active Effects now load.

## 1.2.0

- Rebuilds all Actor records with full ability scores, AC, hit points, challenge ratings,
  skills, saves, and four embedded action/feature Items each.
- Adds structured v5.3.3 activities to every magic item.
- Adds the Fivefold Scale with nine activities and six transferable Active Effects.
- Corrects JournalEntryPage image data for Foundry v14 validation.
- Targets Foundry VTT 14 and dnd5e 5.3.3 explicitly.

## 1.1.0

- Adds one cover, nine pyramid illustrations, ten guardian portraits, and fifteen relic
  illustrations in an original grotesque chibi comic-book style.
- Adds two map scenes from the supplied reference maps.
- Adds nine illustrated theater-of-the-mind scenes.
- Integrates artwork into every Actor and Item and across all journal sections.
- Makes the project builder self-contained and reproducible.

## 1.0.1

- Corrects the Foundry journal parent record keys so all 30 pages load properly.
- Adds ten Saharim guardian actors with source-derived biographies.

## 1.0.0

- Initial release.
- Adds three Pindarian lore and campaign journals.
- Adds nine Demon Relic artifact weapons and six dormant Mimic Relics.
- Includes two supplied pyramid illustrations and editable source text.
- Configures all project, manifest, download, and readme links for the
  `macv0223/pindarian-pyramids` repository.
"""
    write_text(OUTPUT / "CHANGELOG.md", changelog)

    css = """.pindarian-pyramids {
  line-height: 1.45;
}

.pindarian-pyramids blockquote {
  border-left: 3px solid #b78b3e;
  margin: 0.75rem 0;
  padding: 0.35rem 0.8rem;
}

.pindarian-pyramids h1,
.pindarian-pyramids h2,
.pindarian-pyramids h3 {
  color: #6f351f;
}

.pindarian-pyramids .pindarian-splash {
  margin: 0 0 1rem;
}

.pindarian-pyramids .pindarian-splash img {
  aspect-ratio: 3 / 2;
  display: block;
  object-fit: cover;
  width: 100%;
}

.pindarian-pyramids .pindarian-splash figcaption {
  background: #211713;
  color: #f3dfb5;
  font-size: 0.8rem;
  padding: 0.3rem 0.5rem;
  text-align: center;
}
"""
    write_text(OUTPUT / "styles/pindarian-pyramids.css", css)

    workflow = """name: Release Foundry Module

on:
  push:
    tags:
      - "v*"

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build release archive
        run: zip -r pindarian-pyramids.zip assets packs source styles module.json README.md LICENSE.md CHANGELOG.md
      - name: Publish release
        env:
          GH_TOKEN: ${{ github.token }}
        run: gh release create "${{ github.ref_name }}" pindarian-pyramids.zip module.json --generate-notes
"""
    write_text(OUTPUT / ".github/workflows/release.yml", workflow)

    journal_records_all: list[tuple[bytes, bytes]] = []
    journal_records_all.extend(journal_records("The Nine Pyramids of Pindar", source_texts["The Nine Pyramids of Pindar"]))
    journal_records_all.extend(journal_records("The Nine Pindarian Demon Relics", source_texts["The Nine Pindarian Demon Relics"]))
    journal_records_all.extend(journal_records("The Mimic Relics of the Pyramids", source_texts["The Mimic Relics of the Pyramids"]))
    for guide_name in SITE_GUIDE_ART:
        journal_records_all.extend(journal_records(guide_name, source_texts[guide_name]))
    write_pack(OUTPUT / "packs/lore", journal_records_all)

    relic_records: list[tuple[bytes, bytes]] = []
    demon_text = source_texts["The Nine Pindarian Demon Relics"]
    demon_titles = [row[0] for row in DEMON_RELICS]
    for name, base_item, rarity, icon in DEMON_RELICS:
        body = extract_relic(demon_text, name, demon_titles)
        relic_records.extend(item_records(name, base_item, rarity, icon, body, "Demon Relic"))

    mimic_text = source_texts["The Mimic Relics of the Pyramids"]
    mimic_titles = [row[0] for row in MIMIC_RELICS]
    for name, base_item, rarity, icon in MIMIC_RELICS:
        body = extract_relic(mimic_text, name, mimic_titles)
        relic_records.extend(item_records(name, base_item, rarity, icon, body, "Mimic Relic"))
    relic_records.extend(fivefold_scale_records((INPUT / "fivefold-scale.md").read_text(encoding="utf-8")))
    write_pack(OUTPUT / "packs/relics", relic_records)

    pyramid_text = source_texts["The Nine Pyramids of Pindar"]
    guardian_records = []
    for boss in BOSSES:
        guardian_records.extend(statblock_actor_records(boss, "Saharim Guardian",
                                 actor_art(boss["name"],
                                           fallback=context_fallback(boss.get("context")))))
    # Seryth's full mythic block lives in the Bestiary pack; the rest are in BOSSES.
    # Either way the narrative placeholder is retired.
    boss_names = {boss["name"] for boss in BOSSES}
    boss_names.add("High Priestess Seryth Vael - The Last Dawn")
    for name, location, heading, icon in GUARDIANS:
        if name in boss_names:
            # A full stat block exists for this guardian; do not also ship the
            # narrative placeholder under the same name.
            continue
        body = extract_subsection(pyramid_text, heading)
        guardian_records.extend(actor_records(name, location, body, icon))
    write_pack(OUTPUT / "packs/guardians", guardian_records)

    scene_records = [
        scene_record(
            "Pindarian Pyramid Exterior Map",
            f"modules/{MODULE_ID}/assets/maps/pyramid-exterior.jpg",
            1228,
            2048,
            navigation=True,
            sort=100000,
        ),
        scene_record(
            "Pindarian Pyramid Complex Map",
            f"modules/{MODULE_ID}/assets/maps/pyramid-complex.jpg",
            2048,
            1507,
            grid_type=1,
            grid_size=60,
            navigation=True,
            sort=200000,
        ),
    ]
    for index, (title, filename) in enumerate(LOCATION_ART.items(), 3):
        ART_USED.add(f"locations/{filename}")
        with Image.open(ASSET_ROOT / "locations" / filename) as artwork:
            width, height = artwork.size
        scene_records.append(
            scene_record(
                title,
                f"modules/{MODULE_ID}/assets/art/locations/{filename}",
                width,
                height,
                navigation=False,
                sort=index * 100000,
            )
        )
    write_pack(OUTPUT / "packs/scenes", scene_records)

    legion_records: list[tuple[bytes, bytes]] = []
    legion_icon = f"modules/{MODULE_ID}/assets/art/branding/module-cover.webp"
    for unit in LEGIONS:
        legion_records.extend(statblock_actor_records(unit, "Pindarian Armed Forces", actor_art(unit["name"])))
    write_pack(OUTPUT / "packs/legions", legion_records)

    bestiary_records: list[tuple[bytes, bytes]] = []
    for creature in BESTIARY:
        bestiary_records.extend(statblock_actor_records(creature, "Bestiary",
                                actor_art(creature["name"],
                                          fallback=context_fallback(creature.get("context")))))
    write_pack(OUTPUT / "packs/bestiary", bestiary_records)

    spell_records: list[tuple[bytes, bytes]] = []
    for tradition, people, spells in SPELL_TRADITIONS:
        for index, spell in enumerate(spells):
            spell_records.append(spell_item_record(tradition, people, spell, index * 1000))
    write_pack(OUTPUT / "packs/spells", spell_records)

def report_art() -> None:
    ART_USED.add(MODULE_COVER)
    """Print unmatched content and unused art files at the end of a build."""
    every = set()
    for folder in ("actors", "items", "spells", "journals", "locations", "branding"):
        every |= set(_art_index(folder).values())
    unused = sorted(every - ART_USED)
    if ART_MISSES:
        print(f"  ART: {len(ART_MISSES)} unmatched (fell back to the module cover)")
        for folder, want in ART_MISSES[:20]:
            print(f"    - {folder}/{art_slug(want)}.webp")
        if len(ART_MISSES) > 20:
            print(f"    ... and {len(ART_MISSES) - 20} more")
    else:
        print("  ART: every actor, item, spell and journal page has its own image")
    if unused:
        print(f"  ART: {len(unused)} supplied files unused")
        for name in unused[:20]:
            print(f"    - {name}")
        if len(unused) > 20:
            print(f"    ... and {len(unused) - 20} more")


if __name__ == "__main__":
    build()
    report_art()
