# Changelog

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
