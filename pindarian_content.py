"""Pindarian Arcana spell lists and the Pindarian military roster.

Data only. The record builders live in build_module.py.

Spell tuple:
    (name, level, school, components, duration, spell_range, body, activity)

`school` uses the dnd5e keys: abj con div enc evo ill nec trs
`components` is a comma list drawn from vocal somatic material concentration ritual
`activity` is None, or a dict consumed by activity_from_feature().

Unit dict keys are documented beside LEGIONS.
"""

SOLAR_SPELLS = [
    (
        "Dawnsplinter", 0, "evo", "vocal,somatic", ("1", "round"), (90, "ft"),
        "You launch a needle of compressed sunlight. Make a ranged spell attack. On a hit the target "
        "takes 1d8 radiant damage.\n\nUntil the start of your next turn, luminous fractures crawl across "
        "the target: it cannot benefit from being unseen by creatures that can see the glow.\n\nThe damage "
        "increases at 5th, 11th and 17th level.",
        {"kind": "attack", "activation": "action", "attack_type": "ranged", "range": 90, "ability": "int",
         "damage": [(1, 8, "radiant")]},
    ),
    (
        "First Pattern Glimpse", 0, "div", "vocal,somatic", ("1", "minute"), (0, "touch"),
        "You perceive the intended physical pattern of a creature or object.\n\nFor a creature you learn "
        "whether it is wounded, poisoned, diseased, cursed, physically transformed or unnaturally altered. "
        "You do not automatically learn the cause.\n\nFor an object or structure you identify its most "
        "significant structural weakness and whether it has been magically altered.\n\nThis is one of the "
        "first spells taught to Solar children.",
        None,
    ),
    (
        "Radiant Tension", 1, "abj", "somatic", ("", "inst"), (30, "ft"),
        "*Cast as a reaction when a creature within 30 feet takes damage.*\n\nThreads of golden energy snap "
        "into existence around the creature. Reduce the triggering damage by 1d8 + your spellcasting ability "
        "modifier.\n\nThe attacker is outlined in golden light until the beginning of its next turn and "
        "cannot benefit from invisibility during that period.\n\n**At Higher Levels.** Reduce the damage by "
        "an additional 1d8 per slot level above 1st.",
        None,
    ),
    (
        "Sunwire Brand", 1, "evo", "vocal,somatic,concentration", ("1", "minute"), (60, "ft"),
        "A strand of blazing light connects one creature to a point in space you designate within 15 feet of "
        "it. The creature makes a Dexterity saving throw, taking 2d6 radiant damage and becoming tethered on "
        "a failure.\n\nWhile tethered, whenever it willingly moves more than 15 feet from the anchor it takes "
        "1d6 radiant damage and must succeed on a Strength saving throw or its movement ends. It can repeat "
        "the Strength save at the end of each of its turns, breaking the tether on a success.",
        {"kind": "save", "activation": "action", "range": 60, "save": "dex", "dc": 15,
         "damage": [(2, 6, "radiant")], "on_save": "none"},
    ),
    (
        "Prism Reservoir", 2, "abj", "somatic", ("1", "minute"), (30, "ft"),
        "*Cast as a reaction when a creature takes acid, cold, fire, lightning, radiant or thunder damage.*"
        "\n\nA crystalline prism forms around the target. Reduce the triggering damage by 2d8. The prevented "
        "energy remains trapped in the prism.\n\nBefore the spell ends the protected creature can use a bonus "
        "action to release it at a creature within 60 feet. Make a ranged spell attack using your spell "
        "attack bonus; on a hit the target takes damage equal to the amount originally prevented, of the "
        "original type.",
        None,
    ),
    (
        "Forge-Breath", 2, "trs", "vocal,somatic,concentration", ("1", "hour"), (0, "touch"),
        "You breathe luminous Solar energy into one weapon or suit of armour. Choose one manifestation."
        "\n\n**Solar Weapon.** Once per turn the weapon deals an additional 1d6 fire, lightning or radiant "
        "damage, chosen when you cast the spell.\n\n**Solar Armour.** Once per round, when its wearer takes "
        "fire, lightning or radiant damage, reduce that damage by 1d6 + your spellcasting ability modifier."
        "\n\nThe enchanted object glows faintly with Pindarian geometric patterns.",
        None,
    ),
    (
        "Corona Step", 3, "con", "vocal", ("", "inst"), (60, "ft"),
        "*Cast as a bonus action.*\n\nYou collapse into a streak of sunlight and emerge from another "
        "illuminated location you can see.\n\nEvery hostile creature within 5 feet of either your departure "
        "point or your destination makes a Dexterity saving throw, taking 2d6 radiant damage on a failure. A "
        "creature caught in both bursts takes the damage only once.",
        {"kind": "save", "activation": "bonus", "range": 60, "save": "dex", "dc": 15,
         "damage": [(2, 6, "radiant")], "targets": "", "on_save": "none"},
    ),
    (
        "Sunforge Array", 3, "evo", "vocal,somatic,concentration", ("1", "minute"), (0, "self"),
        "Three miniature golden disks orbit you. Each disk can be expended in one of two ways.\n\n**Intercept.** "
        "When you or a creature within 15 feet takes damage, use your reaction to reduce it by 1d8 + your "
        "spellcasting ability modifier.\n\n**Fire.** As a bonus action, launch a disk at a target within 90 "
        "feet. Make a ranged spell attack; it deals 2d6 radiant damage.\n\nThe spell ends when all three "
        "disks have been expended.",
        None,
    ),
    (
        "Living Bastion", 4, "evo", "vocal,somatic", ("10", "minute"), (90, "ft"),
        "You construct three panels of solid golden light, each up to 10 feet wide and 10 feet high. A panel "
        "has AC 17 and 30 hit points and provides cover as appropriate.\n\nWhen a panel is destroyed it "
        "detonates harmlessly outward and one creature of your choice within 10 feet gains 2d6 + your "
        "spellcasting ability modifier temporary hit points.\n\nThe panels may form walls, bridges, ramps or "
        "elevated platforms.",
        None,
    ),
    (
        "Heart of Noon", 4, "abj", "vocal,somatic,concentration", ("1", "minute"), (0, "self"),
        "You become the centre of an artificial noon in a 20-foot aura.\n\nWithin the aura: magical darkness "
        "created by spells of 4th level or lower is suppressed; allies cannot become frightened; invisible "
        "creatures produce visible distortions of light; and an allied creature beginning its turn without "
        "temporary hit points gains temporary hit points equal to your spellcasting ability modifier."
        "\n\nThe light resembles brilliant midday sun regardless of the actual time.",
        None,
    ),
    (
        "Sunfall Crucible", 5, "evo", "vocal,somatic,concentration", ("1", "minute"), (120, "ft"),
        "You create a 20-foot-radius field of glowing Solar particles.\n\nWhenever an enemy in the field "
        "takes damage for the first time on a turn, it takes an additional 1d8 radiant damage.\n\nWhenever a "
        "hostile creature dies inside the field, choose one creature within the field; it regains 2d8 hit "
        "points.\n\nThe Pindarians used this spell to transform violent energy into usable life-force.",
        {"kind": "utility", "activation": "action", "range": 120, "template": ("radius", 20)},
    ),
    (
        "First Pattern Restoration", 5, "trs", "vocal,somatic", ("", "inst"), (0, "touch"),
        "You force a creature's body toward its remembered ideal state. The creature regains 6d8 + your "
        "spellcasting ability modifier hit points.\n\nYou may also end one of the following: blinded, "
        "deafened, paralyzed, poisoned, one disease, or one curse affecting its body.\n\nA body part lost "
        "within the last 24 hours can be reattached instantly if it is physically present.",
        {"kind": "heal", "activation": "action", "range": 0, "healing": (6, 8, "healing"), "formula": "@mod"},
    ),
    (
        "Architect's Radiance", 6, "evo", "vocal,somatic,concentration", ("10", "minute"), (120, "ft"),
        "You generate up to six 10-foot-square planes of solid light. They can form floors, ramps, ceilings, "
        "stairs, bridges, walls or cages.\n\nAs a bonus action you may reposition any number of the planes "
        "within range. A creature forcibly moved through a plane takes 3d8 radiant damage.\n\nEach structure "
        "can support up to 10,000 pounds. Entire Pindarian buildings were constructed using permanent "
        "versions of this spell.",
        None,
    ),
    (
        "Solar Reversal", 6, "trs", "vocal", ("", "inst"), (60, "ft"),
        "*Cast as a reaction when a creature within 60 feet would fall to 0 hit points.*\n\nInstead of falling "
        "unconscious or dying, the target falls to 1 hit point and a brilliant Solar shockwave erupts from it. "
        "Hostile creatures within 20 feet make a Constitution saving throw, taking 5d8 radiant damage on a "
        "failure or half as much on a success.\n\nThe saved creature cannot benefit from Solar Reversal again "
        "until it completes a long rest.",
        {"kind": "save", "activation": "reaction", "range": 60, "save": "con", "dc": 17,
         "damage": [(5, 8, "radiant")], "on_save": "half", "template": ("radius", 20)},
    ),
    (
        "Horizon Lance", 7, "evo", "vocal,somatic", ("1", "minute"), (300, "ft"),
        "You release a beam of coherent Solar energy 10 feet wide and 300 feet long. Creatures in the line "
        "make a Dexterity saving throw, taking 12d8 radiant damage on a failure or half as much on a success."
        "\n\nThe beam burns a luminous scar through the environment that remains for 1 minute. Within that "
        "corridor, magical darkness is suppressed, invisibility fails and creatures cannot become hidden.",
        {"kind": "save", "activation": "action", "range": 300, "save": "dex", "dc": 17,
         "damage": [(12, 8, "radiant")], "on_save": "half", "template": ("line", 300)},
    ),
    (
        "Twelvefold Aegis", 7, "abj", "vocal,somatic", ("1", "hour"), (60, "ft"),
        "Choose up to six creatures. Each receives two Solar seals.\n\nWhen a sealed creature takes damage it "
        "can expend one seal to reduce the damage by 3d10. After using a seal it may immediately move up to 10 "
        "feet without provoking opportunity attacks.\n\nThe seals appear as miniature golden dragon sigils "
        "orbiting the creature.",
        None,
    ),
    (
        "Solar Apotheosis", 8, "trs", "vocal,somatic,concentration", ("1", "minute"), (0, "self"),
        "Your physical form becomes partially composed of Solar energy. You gain a flying speed of 60 feet, "
        "resistance to all damage except psychic, immunity to being blinded, and the ability to pass through "
        "openings as narrow as 1 inch. Creatures beginning their turn within 10 feet take 2d8 radiant damage."
        "\n\nYour spells ignore half and three-quarters cover. When the spell ends you reform completely.",
        None,
    ),
    (
        "Genesis Furnace", 8, "trs", "vocal,somatic,concentration", ("1", "minute"), (120, "ft"),
        "A 30-foot cube becomes a Solar fabrication field. At the beginning of each of your turns, choose one "
        "operation.\n\n**Construct.** Create up to three contiguous 10-foot panels of solid matter or light."
        "\n\n**Restore.** Distribute 6d8 healing among creatures in the field.\n\n**Temper.** Choose up to "
        "three creatures; until your next turn they gain resistance to one damage type you select."
        "\n\n**Reshape.** Transform up to a 10-foot cube of nonmagical stone, metal, earth or wood into "
        "another shape.\n\nAnything created disappears when the spell ends unless it merely reshaped "
        "pre-existing matter.",
        None,
    ),
    (
        "Crown of Twelve Dawns", 9, "abj", "vocal,somatic", ("1", "hour"), (120, "ft"),
        "Choose up to twelve creatures. Each receives a radiant Pindarian sigil.\n\nOnce before the spell ends "
        "a creature may consume its sigil to regain 8d8 hit points; turn one failed saving throw into a "
        "success; emit a 20-foot burst forcing enemies to make a Dexterity saving throw or take 8d8 radiant "
        "damage; or immediately end one charmed, frightened, paralyzed or stunned condition affecting it."
        "\n\nOnce consumed, the sigil vanishes.",
        None,
    ),
    (
        "The First Sun", 9, "evo", "vocal,somatic,concentration", ("1", "minute"), (300, "ft"),
        "You create a miniature star: a 20-foot-diameter sphere floating at a point you choose.\n\nWhen it "
        "appears, creatures within 40 feet make a Constitution saving throw, taking 10d10 radiant and 10d10 "
        "fire damage on a failure, or half as much on a success.\n\nAfterwards, a creature entering within 30 "
        "feet of the star for the first time on a turn, or beginning its turn there, takes 5d10 radiant damage."
        "\n\nThe star sheds intense light for a mile and rapidly destroys nonmagical ice, snow and ordinary "
        "vegetation near it.\n\nThis was never intended as battlefield magic. It was an emergency energy "
        "source for dying Pindarian cities.",
        {"kind": "save", "activation": "action", "range": 300, "save": "con", "dc": 19,
         "damage": [(10, 10, "radiant"), (10, 10, "fire")], "on_save": "half", "template": ("radius", 40)},
    ),
]

LUNAR_SPELLS = [
    (
        "Echoprint", 0, "div", "somatic", ("", "inst"), (0, "touch"),
        "Touch an object or surface. You perceive one brief sensory impression associated with the strongest "
        "emotional event involving it during the last 10 minutes.\n\nYou might perceive a scream, a smell, a "
        "glimpse of a face, a sensation of fear, or the feeling of being dropped.\n\nThe impression is "
        "subjective rather than perfectly factual.",
        None,
    ),
    (
        "Crescent Feint", 0, "ill", "somatic", ("1", "round"), (30, "ft"),
        "Choose one creature able to see you. It makes a Wisdom saving throw. On a failure, several slightly "
        "delayed versions of you overlap, and the creature has disadvantage on its next attack against you "
        "before your next turn.\n\nIf that attack misses, you may immediately move 5 feet without provoking "
        "an opportunity attack from that creature.",
        {"kind": "save", "activation": "action", "range": 30, "save": "wis", "dc": 13, "on_save": "none"},
    ),
    (
        "Borrowed Beat", 1, "trs", "vocal", ("", "inst"), (30, "ft"),
        "*Cast as a reaction when a willing creature within 30 feet ends its turn.*\n\nYou lend the creature a "
        "fragment of unused time. It may immediately move up to 10 feet, stand from prone, draw or stow an "
        "object, or interact with an unattended object.\n\nThis movement does not provoke opportunity attacks.",
        None,
    ),
    (
        "Memory Thread", 1, "div", "vocal,somatic", ("1", "hour"), (0, "touch"),
        "You attach a silver metaphysical thread to a creature's recent memories. For the duration you "
        "perfectly remember everything the creature says or does while you are personally present.\n\nYou also "
        "immediately become aware if magical effects alter your memory of those events. The spell does not "
        "tell you *what* was altered, only that alteration occurred.",
        None,
    ),
    (
        "Silver Delay", 2, "trs", "vocal,somatic", ("", "inst"), (60, "ft"),
        "*Cast as a reaction when a creature within 60 feet takes damage.*\n\nDivide the triggering damage in "
        "half. The target takes half immediately; the remaining half does not occur until the end of the "
        "target's next turn.\n\nEffects triggered by the original damage occur when the first half is taken. "
        "The delayed damage can be reduced by effects available when it finally arrives.\n\nLunari healers "
        "used this spell to create enough time to save otherwise doomed patients.",
        None,
    ),
    (
        "Dreamskin", 2, "ill", "vocal,somatic,concentration", ("1", "hour"), (0, "touch"),
        "A willing creature becomes clothed in expectation. Rather than producing one fixed disguise, every "
        "observer perceives the target as a plausible person belonging in the current environment: a guard "
        "sees another guard, a servant another servant, an aristocrat an invited guest.\n\nThe spell cannot "
        "mimic a specific known individual. A creature suspicious of the disguise may use an action to make "
        "an Investigation check against your spell save DC.",
        None,
    ),
    (
        "Echo of Tomorrow", 3, "trs", "vocal,somatic,concentration", ("1", "minute"), (60, "ft"),
        "Choose a willing creature. At the end of each of its turns a faint temporal echo remains where it "
        "finished moving.\n\nBefore the beginning of that creature's next turn, when it is hit by an attack or "
        "fails a Dexterity saving throw, it may use its reaction to return to the echo. It teleports to that "
        "location and forces the triggering attack roll or saving throw to be rerolled.\n\nOnly the most "
        "recent echo exists.",
        None,
    ),
    (
        "Mnemonic Snare", 3, "enc", "vocal,somatic,concentration", ("1", "minute"), (60, "ft"),
        "One creature makes a Wisdom saving throw. On a failure its perception of sequence becomes trapped in "
        "repetition.\n\nIf it attempts the same broad action on consecutive turns - such as Attack, Dash, Hide "
        "or Cast a Spell - it must make another Wisdom saving throw. On a failure that action is lost and the "
        "creature instead instinctively takes the Dodge action.\n\nChanging tactics avoids the effect.",
        {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 15, "on_save": "none"},
    ),
    (
        "Fourfold Moon", 4, "trs", "vocal,concentration", ("1", "minute"), (0, "self"),
        "*Cast as a bonus action.*\n\nAt the beginning of each of your turns choose one lunar phase."
        "\n\n**New Moon.** You do not provoke opportunity attacks.\n\n**Crescent Moon.** Your speed increases "
        "by 15 feet and you have advantage on Dexterity saving throws.\n\n**Full Moon.** You gain advantage on "
        "Perception checks and spell attack rolls.\n\n**Eclipse.** A hostile creature beginning its turn within "
        "10 feet makes a Wisdom saving throw or becomes frightened of you until that turn ends.\n\nYou may "
        "change phase every turn.",
        None,
    ),
    (
        "Timeweaver's Exchange", 4, "con", "vocal,somatic", ("", "inst"), (60, "ft"),
        "Choose two creatures. Willing creatures automatically succeed; an unwilling creature makes a Charisma "
        "saving throw.\n\nIf both are affected their positions exchange instantly. They also exchange their "
        "initiative counts until the end of the current combat.\n\nA creature transported into an unsafe space "
        "appears in the nearest safe location.",
        {"kind": "save", "activation": "action", "range": 60, "save": "cha", "dc": 15, "targets": "2",
         "on_save": "none"},
    ),
    (
        "Archive of the Living Moment", 5, "div", "vocal,somatic,concentration,ritual", ("10", "minute"), (0, "self"),
        "*Casting time 1 minute. Area: 60-foot radius centred on you.*\n\nChoose any continuous 10-minute "
        "period that occurred in the area during the previous 24 hours. The location recreates that period as "
        "translucent sensory echoes.\n\nYou can see creatures, hear conversations, observe movement and "
        "inspect interactions. The echoes cannot perceive or interact with you.\n\nEffects that specifically "
        "concealed something from divination may conceal it from the archive.",
        None,
    ),
    (
        "Forked Destiny", 5, "div", "vocal,somatic", ("1", "round"), (60, "ft"),
        "Choose a willing creature. On its next turn the table resolves two possible versions of that turn. "
        "After both have been resolved the target chooses which timeline becomes real; everything from the "
        "rejected timeline disappears.\n\nTo prevent paradoxes the creature cannot cast a spell above 3rd "
        "level, expend a magic item's final charge, or use an ability limited to once per long rest."
        "\n\nThe Lunari considered this introductory probability magic.",
        None,
    ),
    (
        "Moon Between Seconds", 6, "trs", "vocal,somatic", ("3", "round"), (30, "ft"),
        "Choose one willing creature. It slips outside the ordinary flow of time and, to everyone else, "
        "vanishes.\n\nDuring each of its turns while absent it can move up to its speed, observe the "
        "environment and pass through creatures. It cannot attack, cast spells, manipulate objects or affect "
        "anything.\n\nAt the end of any of its turns it may re-enter time in an unoccupied space it currently "
        "occupies.",
        None,
    ),
    (
        "Dream Parliament", 6, "ill", "vocal,somatic,ritual", ("8", "hour"), (0, "special"),
        "*Casting time 10 minutes.*\n\nChoose up to eight willing creatures whose names you know. The next "
        "time those creatures sleep during the duration, their consciousnesses meet inside a shared Lunar "
        "dream. Distance does not matter if they are on the same plane; creatures on another plane may "
        "participate if they possess a Pindarian dream-sigil created by you.\n\nWithin the dream participants "
        "may speak normally, create simple surroundings, willingly share memories, and experience hours of "
        "discussion without interrupting physical rest. They awaken normally.",
        None,
    ),
    (
        "Rewrite the Wound", 7, "trs", "vocal,somatic", ("", "inst"), (60, "ft"),
        "*Cast as a reaction when a creature within 60 feet takes damage.*\n\nThe triggering damage is erased. "
        "Instead the target gains a temporal debt equal to the erased damage.\n\nAt the end of each of its "
        "turns it suffers psychic damage equal to one-quarter of the original debt. Before taking this damage "
        "it may expend one Hit Die, reducing the remaining debt by the amount rolled plus its Constitution "
        "modifier. When the debt reaches 0 the effect ends.\n\nYou have not healed the injury. You have given "
        "the victim time to survive it.",
        None,
    ),
    (
        "False Century", 7, "enc", "vocal,somatic", ("", "inst"), (60, "ft"),
        "One creature makes a Wisdom saving throw. On a failure its consciousness experiences approximately a "
        "century of subjective isolation compressed into seconds: it takes 10d8 psychic damage and is stunned "
        "until the end of its next turn.\n\nIf it failed by 5 or more it is instead incapacitated for up to 1 "
        "minute, repeating the save at the end of each of its turns.\n\nOn a success it takes half damage and "
        "is not stunned.",
        {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 18,
         "damage": [(10, 8, "psychic")], "on_save": "half"},
    ),
    (
        "Thousand Selves", 8, "ill", "vocal,somatic,concentration", ("1", "minute"), (0, "self"),
        "Three temporal versions of you appear in spaces within 30 feet and move independently when you move."
        "\n\nWhile one survives you may use a bonus action to exchange positions with it; your spells may "
        "originate from your space or an echo's space; and when an attack would hit you, roll 1d4 - on a 2-4 "
        "it strikes an echo instead and destroys it.\n\nAs a bonus action you can recreate one destroyed echo "
        "in an empty space within 30 feet, no more than one per turn.",
        None,
    ),
    (
        "Eclipse Memory", 8, "enc", "vocal,somatic", ("24", "hour"), (0, "self"),
        "*Area: 30-foot radius centred on you.*\n\nChoose one specific person, object, place, organization or "
        "event. Creatures of your choice in the area make a Wisdom saving throw; on a failure, memories "
        "involving that subject become inaccessible.\n\nIf the forgotten subject is physically present the "
        "creature can still perceive and defend itself against it, but treats it as unfamiliar.\n\nThe spell "
        "cannot erase languages, basic bodily functions, class features, or entire categories such as "
        "'weapons' or 'magic'.",
        {"kind": "save", "activation": "action", "range": 0, "save": "wis", "dc": 19, "on_save": "none",
         "template": ("radius", 30)},
    ),
    (
        "Choose the Better World", 9, "trs", "vocal", ("", "inst"), (0, "special"),
        "*Cast as a reaction at the beginning of a round.*\n\nReality returns to the exact state it possessed "
        "at the beginning of the previous round. Restore creature positions, hit points, conditions, expended "
        "spell slots, expended abilities, destroyed mundane objects, and creatures that died during that round."
        "\n\nOnly you retain memories of the discarded timeline. The spell slot used for Choose the Better "
        "World is never restored by its own effect.\n\nArtifacts, deities and similar entities may remember "
        "fragments of the erased timeline at the GM's discretion.",
        None,
    ),
    (
        "Palace of the Sleeping Moon", 9, "ill", "vocal,somatic,ritual", ("24", "hour"), (0, "special"),
        "*Casting time 10 minutes.*\n\nYou create a vast shared dream realm and name up to 100 creatures. "
        "Whenever one of those creatures sleeps it may enter the Palace regardless of distance. Creatures on "
        "other planes may enter if you know their true name or they possess your Lunar sigil.\n\nWithin the "
        "Palace participants recognise one another, language barriers disappear, willingly shared memories can "
        "be experienced by others, and subjective time passes ten times more slowly than outside.\n\nNo "
        "physical object can be removed from the Palace. Some ancient Pindarian councils governed empires "
        "spanning different worlds without ever meeting physically.",
        None,
    ),
]

VOID_SPELLS = [
    (
        "Vector Knot", 0, "trs", "somatic", ("", "inst"), (60, "ft"),
        "Choose a creature. It makes a Strength saving throw. On a failure you shift its gravitational vector "
        "and move it 5 feet in any horizontal direction. This movement does not provoke opportunity attacks."
        "\n\nIf the target is currently falling, you may instead alter its horizontal trajectory by up to 10 "
        "feet.",
        {"kind": "save", "activation": "action", "range": 60, "save": "str", "dc": 13, "on_save": "none"},
    ),
    (
        "Foldwhisper", 0, "con", "somatic", ("1", "minute"), (30, "ft"),
        "Place one tiny dimensional mark on each of two surfaces within range. For the duration, whispered "
        "sound passes between the marks, creatures can see a tiny distorted view through them, and unattended "
        "objects weighing no more than 1 pound can be passed through.\n\nThe marks cannot transport creatures. "
        "Pindarian children frequently used this spell to pass notes through classroom walls.",
        None,
    ),
    (
        "Null Step", 1, "con", "somatic", ("", "inst"), (15, "ft"),
        "*Cast as a bonus action.*\n\nYou briefly stop occupying the intervening distance. Choose a space "
        "within 15 feet that you know to be unoccupied; you appear there without travelling through the space "
        "between.\n\nLine of sight is not required, though you must know the destination exists. If the chosen "
        "location is occupied the spell fails.",
        None,
    ),
    (
        "Weight of Separation", 1, "trs", "vocal,somatic,concentration", ("1", "minute"), (60, "ft"),
        "Choose one creature and one point within 30 feet of it. The creature makes a Strength saving throw. "
        "On a failure, moving away from the chosen point costs it twice as much movement, and if it ends a "
        "turn farther from the point than where it began that turn it takes 1d8 force damage.\n\nIt can repeat "
        "the save at the end of each of its turns.",
        {"kind": "save", "activation": "action", "range": 60, "save": "str", "dc": 14,
         "damage": [(1, 8, "force")], "on_save": "none"},
    ),
    (
        "Inverted Horizon", 2, "trs", "vocal,somatic,concentration", ("1", "minute"), (60, "ft"),
        "Choose a 15-foot cube. Gravity inside it now falls toward one face of the cube that you designate."
        "\n\nA creature entering the area or beginning its turn there makes a Dexterity saving throw. On a "
        "failure it falls toward the chosen surface and lands prone if it strikes it.\n\nChanging orientation "
        "after casting requires a bonus action.",
        {"kind": "save", "activation": "action", "range": 60, "save": "dex", "dc": 14, "on_save": "none",
         "template": ("cube", 15)},
    ),
    (
        "Astral Thread", 2, "div", "vocal,somatic", ("1", "hour"), (30, "ft"),
        "Link two willing creatures with an invisible silver cord. For the duration they always know the "
        "other's direction and approximate distance, whether the other is unconscious, and whether the other "
        "has crossed a dimensional boundary.\n\nAdditionally, if one creature teleports while the other is "
        "within 10 feet of it, the second creature may use its reaction to follow to the same destination.",
        None,
    ),
    (
        "Door Without Distance", 3, "con", "vocal,somatic,concentration", ("1", "minute"), (120, "ft"),
        "Create two five-foot-tall distortions on surfaces you can see. Entering one causes a creature to "
        "immediately emerge from the other. A creature can pass through only once during each of its turns. "
        "Objects and projectiles can also pass through.\n\nRemoving either surface destroys both doors.\n\nThis "
        "spell formed the basis of internal transportation within Pindarian cities.",
        None,
    ),
    (
        "Planar Mooring", 3, "abj", "vocal,somatic,concentration", ("1", "minute"), (60, "ft"),
        "Create a 20-foot-radius anchored zone. Inside it: teleportation fails; creatures cannot voluntarily "
        "change planes; dimensional portals cannot be created; summoned creatures cannot be magically "
        "dismissed; and possession effects are suppressed while the possessed creature remains inside."
        "\n\nExisting permanent planar structures are not destroyed.",
        {"kind": "utility", "activation": "action", "range": 60, "template": ("radius", 20)},
    ),
    (
        "Event Horizon Cage", 4, "trs", "vocal,somatic,concentration", ("1", "minute"), (90, "ft"),
        "Create a 20-foot-radius gravitational distortion. A creature beginning its turn inside makes a "
        "Strength saving throw; on a failure it is pulled 10 feet toward the centre. Moving away from the "
        "centre costs twice as much movement.\n\nRanged attacks passing through the sphere suffer disadvantage "
        "as their trajectories curve unpredictably. Teleportation from inside the sphere fails unless the "
        "caster succeeds on a spellcasting ability check against your spell save DC.",
        {"kind": "save", "activation": "action", "range": 90, "save": "str", "dc": 16, "on_save": "none",
         "template": ("radius", 20)},
    ),
    (
        "Ghost Orbit", 4, "trs", "vocal,somatic,concentration", ("1", "minute"), (30, "ft"),
        "Choose up to six unattended objects weighing no more than 20 pounds each. They begin orbiting you."
        "\n\nWhile at least three remain you gain +2 AC against ranged attacks.\n\nAs a bonus action, launch "
        "one orbiting object at a creature within 60 feet. Make a ranged spell attack; on a hit the object "
        "deals 2d10 force or bludgeoning damage, then falls normally.",
        None,
    ),
    (
        "Astral Shear", 5, "abj", "vocal,somatic", ("", "inst"), (90, "ft"),
        "You cut the metaphysical connection between a creature and its home reality. The creature makes a "
        "Charisma saving throw, taking 8d8 force damage on a failure.\n\nIf its native plane differs from the "
        "plane you are currently on, then until the end of your next turn it also cannot teleport, cannot "
        "summon creatures, cannot open portals, and cannot benefit from damage resistance granted by its "
        "planar nature.\n\nA native creature instead takes half the rolled damage and suffers no additional "
        "effects.",
        {"kind": "save", "activation": "action", "range": 90, "save": "cha", "dc": 17,
         "damage": [(8, 8, "force")], "on_save": "none"},
    ),
    (
        "Worldline Tunnel", 5, "con", "vocal,somatic", ("1", "round"), (0, "special"),
        "You open a shimmering corridor connecting your location with another location on the same plane that "
        "you have personally visited and that lies within 10 miles.\n\nThe tunnel is large enough for Large "
        "creatures and anyone may travel either direction while it remains open. The spell does not care about "
        "intervening walls, terrain or elevation.",
        None,
    ),
    (
        "Betweenworld Transit", 6, "con", "vocal,somatic,material", ("", "inst"), (0, "touch"),
        "*Casting time 1 minute. Material component: a tuned Pindarian astral crystal worth at least 250 gp, "
        "not consumed.*\n\nYou tear open a temporary corridor through the Astral Sea. You and up to eight "
        "willing creatures may travel to another plane, another world on the Material Plane, or a known "
        "Pindarian planar anchor.\n\nTravelling to an established Pindarian anchor delivers you precisely. "
        "Otherwise you arrive somewhere within approximately 1d10 miles of the desired destination.\n\nThe "
        "passage remains open for 1 minute but can only be crossed once by each creature.\n\nThis is the "
        "foundational Pindarian interplanar travel spell.",
        None,
    ),
    (
        "Black Meridian", 6, "trs", "vocal,somatic", ("", "inst"), (120, "ft"),
        "You compress space along a five-foot-wide, 120-foot line. Creatures in the line make a Dexterity "
        "saving throw, taking 8d8 force damage and being dragged to the nearest unoccupied space adjacent to "
        "the line's midpoint on a failure, or half damage and no movement on a success.\n\nUnsecured objects "
        "are violently dragged toward the midpoint automatically.",
        {"kind": "save", "activation": "action", "range": 120, "save": "dex", "dc": 17,
         "damage": [(8, 8, "force")], "on_save": "half", "template": ("line", 120)},
    ),
    (
        "Gravity Crown", 7, "trs", "vocal,somatic,concentration", ("1", "minute"), (60, "ft"),
        "Choose up to six creatures. For each creature, choose which direction counts as down. At the start of "
        "each of your turns you may redefine each target's gravity independently; affected creatures fall "
        "normally toward their personal down.\n\nA creature unwilling to be affected may make a Constitution "
        "saving throw when first targeted and at the end of each of its turns.\n\nThis can create sideways "
        "battlefields, inverted armies, orbital movement, and creatures falling toward different walls "
        "simultaneously.",
        None,
    ),
    (
        "Sever the Gate", 7, "abj", "vocal,somatic", ("", "inst"), (120, "ft"),
        "Target a magical portal, dimensional passage or planar summoning effect. Make a spellcasting ability "
        "check against a DC equal to 10 + the effect's spell level, or a DC set by the GM for non-spell "
        "portals.\n\nOn a success the portal immediately closes, creatures currently crossing are expelled to "
        "the nearest side, and a planar backlash erupts for 6d10 force damage to creatures within 15 feet."
        "\n\nThe affected location cannot host another portal to the same destination for 24 hours. "
        "Artifact-level gates may only be suppressed temporarily.",
        None,
    ),
    (
        "Ninefold Bastion", 8, "abj", "vocal,somatic", ("1", "hour"), (0, "self"),
        "*Casting time 1 minute. Area: 60-foot radius centred on you.*\n\nYou establish nine rotating "
        "geometric seals around the area. For the duration, teleportation, planar travel and summoning into or "
        "out of the area all fail, possession crossing the boundary fails, and extraplanar creatures "
        "attempting to physically enter must make a Charisma saving throw or be unable to cross that turn."
        "\n\nPermanent portals inside the zone become dormant rather than destroyed.\n\nThis is the direct "
        "ancestor of the magic used in the Nine Pindarian Pyramids.",
        None,
    ),
    (
        "Soul Orbit", 8, "nec", "vocal,somatic", ("1", "hour"), (60, "ft"),
        "Choose up to six willing creatures. Their souls become loosely tethered to you.\n\nIf an affected "
        "creature dies during the spell its soul does not immediately depart; instead it becomes a visible "
        "star-like mote orbiting you. For the next minute, if its body is within 30 feet, you can use an "
        "action to return the soul. The creature returns with 1 hit point, its memories intact, and no change "
        "of alignment or personality.\n\nIf the body has been destroyed the soul remains protected but cannot "
        "be restored by this spell.",
        None,
    ),
    (
        "Pindarian Bridge", 9, "con", "vocal,somatic,material", ("1", "hour"), (30, "ft"),
        "*Casting time 10 minutes. Material component: a pair of tuned planar crystals worth 5,000 gp total.*"
        "\n\nYou create a stable two-way interplanar bridge between your location and another location that "
        "you know exceptionally well - another plane, another Material world, an Astral location, or a known "
        "dimensional city.\n\nA 20-foot-wide archway appears at both locations and creatures and objects may "
        "freely travel either direction. The bridge remains perfectly stable unless you dismiss it, its "
        "anchors are destroyed, or powerful planar interference disrupts it.\n\nPermanent versions of this "
        "spell once connected the Pindarian Empire across the multiverse. They were known simply as Pindarian "
        "Bridges.",
        None,
    ),
    (
        "Reality Exclusion", 9, "abj", "vocal,somatic,concentration", ("1", "minute"), (0, "self"),
        "*Area: 60-foot radius centred on you.*\n\nChoose one plane other than the plane you currently occupy. "
        "For the duration, reality inside the area rejects beings and magic originating from that plane, and "
        "portals connecting to the chosen plane fail.\n\nCreatures native to that plane that attempt to enter "
        "the radius must make a Charisma saving throw or be unable to cross. Creatures from that plane already "
        "inside when you cast the spell make the same save; on a failure they are violently expelled to the "
        "nearest space outside the boundary and take 6d10 force damage. On a success they remain, but cannot "
        "teleport, regain hit points, or summon creatures from their native plane.\n\nThe Pindarian High Magi "
        "eventually asked the obvious question: what if the radius were not sixty feet, what if there were "
        "nine anchors, and what if the spell lasted forever? The answer was the Ninefold Prohibition.",
        {"kind": "save", "activation": "action", "range": 0, "save": "cha", "dc": 19,
         "damage": [(6, 10, "force")], "on_save": "none", "template": ("radius", 60)},
    ),
]

SPELL_TRADITIONS = [
    ("Solar Arcana", "Children of the Sun", SOLAR_SPELLS),
    ("Lunar Arcana", "Children of the Moon", LUNAR_SPELLS),
    ("Void Arcana", "Children of the Void", VOID_SPELLS),
]


# ---------------------------------------------------------------------------
# The Pindarian Armed Forces
#
# Unit keys: name, tradition, role, size, cr, ac, hp, formula, speed, abilities
# (str dex con int wis cha), saves, skills, dr/di/dv/ci (custom strings),
# senses, languages, features.
#
# A feature is (section, name, body, activity) where section is one of
# trait / action / bonus / reaction, and activity is None or a dict consumed by
# activity_from_feature(). Feature counts deliberately vary: a Linewarden is a
# spear and a shield, an Oracle is a control suite, and neither should be padded
# out to match the other.
# ---------------------------------------------------------------------------

_PIN_LANG = "Common, Draconic, Pindarian"

LEGIONS = [
    dict(
        name="Solaari Linewarden", tradition="Sun", role="Basic heavy infantry",
        size="lg", cr=1, ac=18, hp=39, formula="6d10 + 6", speed={"walk": 30},
        abilities=(16, 12, 15, 11, 13, 12), saves=["str", "con"],
        skills={"ath": 1, "prc": 1}, senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="The foundation of a Solar formation. Their purpose is not simply to kill - it is to hold "
              "territory while everybody else does their job. Linewardens operate in squads of six to twelve.",
        features=[
            ("trait", "Solar Formation",
             "While the Linewarden is within 5 feet of another conscious Solaari soldier carrying a shield, "
             "it gains a +1 bonus to AC.", None),
            ("trait", "Steady Heart",
             "The Linewarden has advantage on saving throws against being frightened.", None),
            ("action", "Multiattack", "The Linewarden makes two Solar Spear attacks.", None),
            ("action", "Solar Spear",
             "Melee or Ranged Weapon Attack: +5 to hit, reach 10 ft. or range 20/60 ft., one target. "
             "Hit: 6 (1d6 + 3) piercing damage plus 2 (1d4) radiant damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(1, 6, "piercing"), (1, 4, "radiant")]}),
            ("action", "Shield Pulse",
             "Creatures of the Linewarden's choice within 5 feet must succeed on a DC 13 Strength saving "
             "throw or be pushed 10 feet away.",
             {"kind": "save", "activation": "action", "range": 5, "save": "str", "dc": 13, "recharge": 5,
              "on_save": "none"}),
            ("reaction", "Interlocking Aegis",
             "When an adjacent ally is hit by an attack, the Linewarden grants that ally +2 AC against the "
             "triggering attack, potentially causing it to miss.", None),
        ],
    ),
    dict(
        name="Sun Guard Blade", tradition="Sun", role="Elite Solar infantry",
        size="lg", cr=3, ac=19, hp=76, formula="9d10 + 26", speed={"walk": 35},
        abilities=(18, 15, 18, 12, 14, 14), saves=["str", "con", "wis"],
        skills={"ath": 1, "ins": 1, "prc": 1}, dr="radiant", senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="Descendants of the martial tradition that guarded the Pyramid of the Sun. A Sun Guard Blade "
              "combines swordsmanship with stored Solar energy. They rarely fight alone.",
        features=[
            ("trait", "Stored Radiance",
             "Whenever the Sun Guard takes damage it gains 1 Radiance point, to a maximum of 3. Its next "
             "weapon hit can expend all stored points, dealing an additional 1d6 radiant damage per point.",
             None),
            ("action", "Multiattack", "The Sun Guard makes two Sunblade attacks.", None),
            ("action", "Sunblade",
             "Melee Weapon Attack: +6 to hit, reach 10 ft., one target. Hit: 8 (1d8 + 4) slashing damage plus "
             "3 (1d6) radiant damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(1, 8, "slashing"), (1, 6, "radiant")]}),
            ("action", "Corona Step",
             "The Sun Guard teleports up to 30 feet between two spaces it can see. Creatures within 5 feet "
             "of its destination must make a DC 14 Dexterity saving throw or take 7 (2d6) radiant damage.",
             {"kind": "save", "activation": "action", "range": 30, "save": "dex", "dc": 14, "recharge": 4,
              "damage": [(2, 6, "radiant")], "on_save": "none"}),
            ("reaction", "Solar Parry",
             "The Sun Guard adds 3 to its AC against one melee attack that would hit it.", None),
        ],
    ),
    dict(
        name="Dawnspear Artillerist", tradition="Sun", role="Solar ranged battlemage",
        size="lg", cr=5, ac=16, hp=85, formula="10d10 + 30", speed={"walk": 30},
        abilities=(10, 15, 18, 17, 14, 12), saves=["con", "int"],
        skills={"arc": 1, "inv": 1, "prc": 1}, dr="fire, radiant", senses={"darkvision": 60},
        languages=_PIN_LANG,
        blurb="Living artillery. Their staffs contain rotating lenses that collect ambient magical energy and "
              "focus it into devastating lines of Solar force.",
        features=[
            ("trait", "Solar Calibration",
             "The Artillerist ignores half cover with ranged spell attacks.", None),
            ("action", "Solar Bolt",
             "Ranged Spell Attack: +6 to hit, range 180 ft., one target. Hit: 18 (4d8) radiant damage.",
             {"kind": "attack", "activation": "action", "range": 180, "attack_type": "ranged", "ability": "int",
              "damage": [(4, 8, "radiant")]}),
            ("action", "Dawnspear Beam",
             "The Artillerist fires a 100-foot-long, 5-foot-wide line. Creatures in the line make a DC 14 "
             "Dexterity saving throw, taking 31 (7d8) radiant damage on a failure or half as much on a "
             "success. Until the beginning of the Artillerist's next turn the line remains brightly "
             "illuminated and invisibility does not function within it.",
             {"kind": "save", "activation": "action", "range": 100, "save": "dex", "dc": 14, "recharge": 5,
              "damage": [(7, 8, "radiant")], "on_save": "half", "template": ("line", 100)}),
            ("action", "Construct Solar Panel",
             "The Artillerist creates a 10-foot-square panel of solid light within 60 feet. The panel "
             "provides total cover and has AC 15 and 20 hit points. Only one panel can exist at a time.",
             None),
            ("reaction", "Prism Reservoir",
             "When the Artillerist takes acid, cold, fire, lightning, radiant or thunder damage, reduce the "
             "damage by 9 (2d8). Its next Solar Bolt before the end of its next turn deals that much "
             "additional damage.", None),
        ],
    ),
    dict(
        name="Living Bastion Knight", tradition="Sun", role="Solar defensive elite",
        size="lg", cr=8, ac=21, hp=152, formula="16d10 + 64", speed={"walk": 30},
        abilities=(20, 10, 20, 13, 15, 15), saves=["str", "con", "wis"],
        skills={"ath": 1}, dr="fire, lightning, radiant", ci="frightened",
        senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="A Bastion Knight does not simply wear armour - their armour is a mobile magical fortification. "
              "They are deployed to protect commanders, gates, relics, wounded personnel and planar machinery.",
        features=[
            ("trait", "Bastion Aura", "Allies within 10 feet gain +1 AC.", None),
            ("trait", "Immovable",
             "The Bastion has advantage on saving throws against being knocked prone or forcibly moved.", None),
            ("action", "Multiattack", "The Bastion makes three Solar Hammer attacks.", None),
            ("action", "Solar Hammer",
             "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 12 (2d6 + 5) bludgeoning damage "
             "plus 4 (1d8) radiant damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 6, "bludgeoning"), (1, 8, "radiant")]}),
            ("action", "Bastion Wall",
             "A wall of Solar energy erupts from the ground in a line 30 feet long and 10 feet high. "
             "Creatures in its path make a DC 16 Dexterity saving throw, taking 18 (4d8) radiant damage and "
             "being pushed to one side of the wall on a failure. The wall remains until the beginning of the "
             "Bastion's next turn and provides total cover.",
             {"kind": "save", "activation": "action", "range": 30, "save": "dex", "dc": 16, "recharge": 5,
              "damage": [(4, 8, "radiant")], "on_save": "none", "template": ("line", 30)}),
            ("reaction", "Guardian Intercept",
             "When an ally within 15 feet would take damage, the Bastion moves up to 15 feet without "
             "provoking opportunity attacks. If it ends adjacent to that ally it takes half the damage and "
             "the ally takes the remainder.", None),
        ],
    ),
    dict(
        name="Solar Marshal", tradition="Sun", role="Commander of a Solaari Legion",
        size="lg", cr=12, ac=20, hp=195, formula="23d10 + 69", speed={"walk": 35, "fly": 30},
        abilities=(20, 14, 19, 17, 17, 19), saves=["str", "con", "wis", "cha"],
        skills={"arc": 1, "ath": 1, "ins": 1, "per": 1}, dr="fire, radiant",
        senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="Generals, battlefield artificers and high-ranking warrior-mages. They rarely command from the "
              "rear. Their philosophy: if the formation must stand there, so will I.",
        features=[
            ("trait", "Marshal's Radiance",
             "Allied Pindarians within 30 feet have advantage on saving throws against being frightened.", None),
            ("trait", "Solar Command",
             "At the beginning of the Marshal's turn, choose one ally within 60 feet. That ally may move up "
             "to half its speed without provoking opportunity attacks.", None),
            ("action", "Multiattack", "The Marshal makes three Dawnblade attacks.", None),
            ("action", "Dawnblade",
             "Melee Weapon Attack: +9 to hit, reach 10 ft., one target. Hit: 10 (1d10 + 5) slashing damage "
             "plus 9 (2d8) radiant damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(1, 10, "slashing"), (2, 8, "radiant")]}),
            ("action", "Horizon Lance",
             "The Marshal fires a 120-foot-long, 10-foot-wide beam. Creatures in the line make a DC 17 "
             "Dexterity saving throw, taking 45 (10d8) radiant damage on a failure or half as much on a "
             "success.",
             {"kind": "save", "activation": "action", "range": 120, "save": "dex", "dc": 17, "recharge": 5,
              "damage": [(10, 8, "radiant")], "on_save": "half", "template": ("line", 120)}),
            ("action", "Solar Restoration",
             "One creature within 30 feet regains 36 (8d8) hit points and may immediately end one of the "
             "following conditions affecting it: charmed, frightened, paralyzed or poisoned.",
             {"kind": "heal", "activation": "action", "range": 30, "healing": (8, 8, "healing"), "uses": "2",
              "recovery": "lr"}),
            ("reaction", "Solar Reversal",
             "When an ally within 60 feet would fall to 0 hit points, it falls to 1 hit point instead. "
             "Hostile creatures within 10 feet of that ally take 13 (3d8) radiant damage. Once per day.",
             None),
        ],
    ),
    dict(
        name="Crescent Scout", tradition="Moon", role="Reconnaissance and skirmishing infantry",
        size="lg", cr=1, ac=15, hp=33, formula="6d10 + 0", speed={"walk": 40},
        abilities=(10, 17, 12, 13, 16, 13), saves=[],
        skills={"prc": 1, "ste": 1, "sur": 1}, senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="Crescent Scouts observe enemy movement and mark possible futures.",
        features=[
            ("trait", "Lunar Footwork",
             "Opportunity attacks against the Scout are made with disadvantage.", None),
            ("action", "Moonbow",
             "Ranged Weapon Attack: +5 to hit, range 100/400 ft., one target. Hit: 7 (1d8 + 3) piercing "
             "damage plus 2 (1d4) psychic damage.",
             {"kind": "attack", "activation": "action", "range": 100, "attack_type": "ranged", "ability": "dex",
              "damage": [(1, 8, "piercing"), (1, 4, "psychic")]}),
            ("action", "Crescent Blade",
             "Melee Weapon Attack: +5 to hit, reach 10 ft., one target. Hit: 6 (1d6 + 3) slashing damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "dex",
              "damage": [(1, 6, "slashing")]}),
            ("reaction", "Echo Slip",
             "When an attack misses the Scout, it may move 10 feet without provoking opportunity attacks.",
             None),
        ],
    ),
    dict(
        name="Echo Duelist", tradition="Moon", role="Temporal melee specialist",
        size="lg", cr=3, ac=17, hp=71, formula="11d10 + 11", speed={"walk": 40},
        abilities=(11, 19, 14, 15, 15, 14), saves=["dex", "wis"],
        skills={"acr": 1, "ins": 1, "prc": 1}, senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="Echo Duelists train themselves to fight a fraction of a second ahead of conventional time. "
              "Their movements appear almost rehearsed because, from their perspective, they sometimes are.",
        features=[
            ("trait", "Temporal Echo",
             "At the end of its turn the Duelist leaves an echo in its space. Until the beginning of its next "
             "turn it may use a reaction to teleport back to that location.", None),
            ("action", "Multiattack", "The Duelist makes two Moonblade attacks.", None),
            ("action", "Moonblade",
             "Melee Weapon Attack: +6 to hit, reach 10 ft., one target. Hit: 8 (1d8 + 4) slashing damage plus "
             "3 (1d6) psychic damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "dex",
              "damage": [(1, 8, "slashing"), (1, 6, "psychic")]}),
            ("action", "Borrowed Beat",
             "The Duelist immediately moves up to its speed and makes one Moonblade attack. This movement "
             "does not provoke opportunity attacks.",
             {"kind": "utility", "activation": "action", "range": 0, "recharge": 5}),
        ],
    ),
    dict(
        name="Mnemonic Veil Agent", tradition="Moon", role="Spy, interrogator and counterintelligence specialist",
        size="lg", cr=5, ac=16, hp=88, formula="16d10 + 0", speed={"walk": 35},
        abilities=(9, 18, 12, 17, 16, 18), saves=["dex", "wis", "cha"],
        skills={"dec": 2, "ins": 1, "inv": 1, "ste": 1}, senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="These soldiers attack the enemy's understanding of the battle. They steal passwords, replace "
              "witnesses, erase routes and alter recognition.",
        features=[
            ("trait", "Dreamskin",
             "While not in combat the Agent magically appears to casual observers as someone who plausibly "
             "belongs in the area. A suspicious creature can use an action and succeed on a DC 15 "
             "Investigation check to recognise the deception.", None),
            ("action", "Memory Blade",
             "Melee Spell Attack: +7 to hit, reach 10 ft., one target. Hit: 18 (4d8) psychic damage, and the "
             "target cannot take reactions until the start of its next turn.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "cha",
              "damage": [(4, 8, "psychic")]}),
            ("action", "Sever Recognition",
             "One creature within 60 feet makes a DC 15 Wisdom saving throw. On a failure, until the end of "
             "its next turn it no longer recognises friend from foe: it cannot make opportunity attacks and "
             "must choose the target of any attack randomly from eligible creatures within range.",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 15, "recharge": 5,
              "on_save": "none"}),
            ("action", "Stolen Moment",
             "The Agent becomes invisible until the beginning of its next turn and may immediately move up to "
             "its speed. Once per day.",
             {"kind": "utility", "activation": "action", "range": 0, "uses": "1", "recovery": "lr"}),
        ],
    ),
    dict(
        name="Dreamweaver Tactician", tradition="Moon", role="Battlefield controller",
        size="lg", cr=8, ac=17, hp=130, formula="20d10 + 20", speed={"walk": 30},
        abilities=(8, 16, 14, 18, 18, 18), saves=["int", "wis", "cha"],
        skills={"arc": 1, "ins": 1, "prc": 1}, dr="psychic", senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="Dreamweavers control emotional momentum, perceived positioning and short-range probability.",
        features=[
            ("trait", "Probable Position",
             "The first attack roll made against the Dreamweaver each round has disadvantage.", None),
            ("action", "Lunar Pulse",
             "Ranged Spell Attack: +7 to hit, range 90 ft., one target. Hit: 22 (4d10) psychic damage.",
             {"kind": "attack", "activation": "action", "range": 90, "attack_type": "ranged", "ability": "int",
              "damage": [(4, 10, "psychic")]}),
            ("action", "Dreamfield",
             "The Dreamweaver creates a 20-foot-radius field within 90 feet until the beginning of its next "
             "turn. Enemies entering or starting their turn there must make a DC 15 Wisdom saving throw. On a "
             "failure, choose one: speed becomes 0 until the end of the turn; frightened until the end of the "
             "turn; or disadvantage on attacks until the end of the turn.",
             {"kind": "save", "activation": "action", "range": 90, "save": "wis", "dc": 15, "recharge": 5,
              "on_save": "none", "template": ("radius", 20)}),
            ("action", "Forked Outcome",
             "When a creature within 60 feet makes an attack roll or saving throw, the Dreamweaver forces it "
             "to roll again and chooses which result applies. Twice per day.",
             {"kind": "utility", "activation": "special", "range": 60, "uses": "2", "recovery": "lr"}),
        ],
    ),
    dict(
        name="Oracle of the Fourfold Moon", tradition="Moon", role="Lunari commander",
        size="lg", cr=12, ac=18, hp=180, formula="24d10 + 48", speed={"walk": 35},
        abilities=(9, 18, 16, 20, 20, 19), saves=["dex", "int", "wis", "cha"],
        skills={"arc": 1, "ins": 1, "prc": 1}, dr="psychic", senses={"darkvision": 60, "truesight": 30},
        languages=_PIN_LANG,
        blurb="These Oracles do not simply predict battles. They continually compare several possible versions "
              "of the battle and attempt to force reality toward the most desirable one.",
        features=[
            ("trait", "Fourfold Moon",
             "At the beginning of each turn, choose one phase. New Moon: the Oracle becomes invisible until "
             "it attacks or uses an offensive power. Crescent: its speed becomes 60 feet. Full: its spell "
             "attacks have advantage. Eclipse: enemies within 10 feet have disadvantage on Wisdom saving "
             "throws.", None),
            ("action", "Moonfire",
             "Ranged Spell Attack: +9 to hit, range 120 ft., one target. Hit: 27 (6d8) psychic or radiant "
             "damage.",
             {"kind": "attack", "activation": "action", "range": 120, "attack_type": "ranged", "ability": "int",
              "damage": [(6, 8, "psychic")]}),
            ("action", "Temporal Exchange",
             "Two creatures within 60 feet must make DC 17 Charisma saving throws if unwilling. On failures, "
             "their positions are exchanged.",
             {"kind": "save", "activation": "action", "range": 60, "save": "cha", "dc": 17, "targets": "2",
              "on_save": "none"}),
            ("action", "False Century",
             "One creature within 60 feet makes a DC 17 Wisdom saving throw, taking 36 (8d8) psychic damage "
             "and being stunned until the end of its next turn on a failure, or half damage and no stun on a "
             "success.",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 17, "recharge": 6,
              "damage": [(8, 8, "psychic")], "on_save": "half"}),
            ("reaction", "Reject Timeline",
             "After seeing the result of any d20 roll within 60 feet, the Oracle declares the event "
             "unacceptable. The roll is made again and the Oracle chooses which result occurs. Once per day.",
             None),
        ],
    ),
    dict(
        name="Vector Trooper", tradition="Void", role="Basic Veylari infantry",
        size="lg", cr=1, ac=16, hp=36, formula="8d8", speed={"walk": 30},
        abilities=(14, 15, 14, 14, 12, 11), saves=["str", "int"],
        skills={"arc": 1, "ath": 1}, senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="The rank and file of the Gate Legions. A Vector Trooper does not ask how to reach the enemy; it "
              "asks why the enemy is over there.",
        features=[
            ("action", "Vector Pike",
             "Melee Weapon Attack: +4 to hit, reach 10 ft., one target. Hit: 7 (1d10 + 2) piercing damage plus "
             "3 (1d6) force damage. The Trooper may push or pull the target 5 feet.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(1, 10, "piercing"), (1, 6, "force")]}),
            ("action", "Gravity Bolt",
             "Ranged Spell Attack: +4 to hit, range 60 ft., one target. Hit: 7 (2d6) force damage and the "
             "target is moved 5 feet in a direction chosen by the Trooper.",
             {"kind": "attack", "activation": "action", "range": 60, "attack_type": "ranged", "ability": "int",
              "damage": [(2, 6, "force")]}),
            ("bonus", "Null Step", "The Trooper teleports up to 10 feet.",
             {"kind": "utility", "activation": "bonus", "range": 10}),
        ],
    ),
    dict(
        name="Nullstep Raider", tradition="Void", role="Teleporting shock infantry",
        size="lg", cr=3, ac=17, hp=68, formula="8d10 + 24", speed={"walk": 35},
        abilities=(16, 18, 18, 14, 13, 10), saves=["dex", "con"],
        skills={"acr": 1, "ath": 1}, senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="Raiders attack places conventional soldiers consider safe. Behind shields. Behind doors. Behind "
              "fortifications.",
        features=[
            ("trait", "Spatial Ambush",
             "If the Raider teleports immediately before hitting with a melee attack, that attack deals an "
             "additional 7 (2d6) force damage.", None),
            ("action", "Multiattack", "The Raider makes two Voidblade attacks.", None),
            ("action", "Voidblade",
             "Melee Weapon Attack: +6 to hit, reach 10 ft., one target. Hit: 8 (1d8 + 4) slashing damage plus "
             "3 (1d6) force damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "dex",
              "damage": [(1, 8, "slashing"), (1, 6, "force")]}),
            ("bonus", "Null Step",
             "The Raider teleports up to 30 feet to a space it knows is unoccupied.",
             {"kind": "utility", "activation": "bonus", "range": 30}),
            ("reaction", "Fold Away",
             "When targeted by a ranged attack the Raider may teleport 10 feet. If this moves it out of the "
             "attack's range or behind total cover, the attack misses.", None),
        ],
    ),
    dict(
        name="Gatewarden", tradition="Void", role="Anti-teleportation and planar defence specialist",
        size="lg", cr=5, ac=18, hp=102, formula="12d10 + 36", speed={"walk": 30},
        abilities=(15, 12, 18, 18, 16, 15), saves=["con", "int", "wis"],
        skills={"arc": 2, "inv": 1, "prc": 1}, senses={"darkvision": 60, "truesight": 30}, languages=_PIN_LANG,
        blurb="Gatewardens defend strategic Pindarian sites from summoned creatures, teleporting assassins and "
              "extraplanar infiltrators.",
        features=[
            ("trait", "Planar Mooring",
             "Teleportation and planar travel initiated within 15 feet of the Gatewarden fail unless the "
             "creature attempting it succeeds on a DC 15 Charisma saving throw.", None),
            ("action", "Anchor Staff",
             "Melee Spell Attack: +7 to hit, reach 10 ft., one target. Hit: 17 (2d8 + 8) force damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "int",
              "damage": [(2, 8, "force")]}),
            ("action", "Astral Shear",
             "One creature within 90 feet makes a DC 15 Charisma saving throw, taking 31 (7d8) force damage "
             "on a failure. If the creature is extraplanar it also cannot teleport until the end of the "
             "Gatewarden's next turn.",
             {"kind": "save", "activation": "action", "range": 90, "save": "cha", "dc": 15, "recharge": 5,
              "damage": [(7, 8, "force")], "on_save": "none"}),
            ("action", "Seal Breach",
             "The Gatewarden instantly closes a magical portal or teleportation effect of 5th level or lower "
             "within 60 feet. Twice per day.",
             {"kind": "utility", "activation": "action", "range": 60, "uses": "2", "recovery": "lr"}),
        ],
    ),
    dict(
        name="Singularity Adept", tradition="Void", role="Heavy battlefield controller",
        size="lg", cr=8, ac=17, hp=135, formula="18d10 + 36", speed={"walk": 30, "fly": 30},
        abilities=(10, 14, 16, 20, 16, 13), saves=["con", "int", "wis"],
        skills={"arc": 2, "inv": 1}, dr="force", senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="These mages manipulate local gravity to destroy formations.",
        features=[
            ("trait", "Personal Gravity",
             "The Adept cannot be knocked prone and may stand on walls or ceilings.", None),
            ("action", "Compression Bolt",
             "Ranged Spell Attack: +8 to hit, range 120 ft., one target. Hit: 22 (4d10) force damage.",
             {"kind": "attack", "activation": "action", "range": 120, "attack_type": "ranged", "ability": "int",
              "damage": [(4, 10, "force")]}),
            ("action", "Singularity",
             "Create a 20-foot-radius gravity well within 120 feet. Creatures within make a DC 16 Strength "
             "saving throw, taking 27 (6d8) force damage, being pulled 20 feet toward the centre and knocked "
             "prone on a failure, or half damage and pulled only 5 feet on a success.",
             {"kind": "save", "activation": "action", "range": 120, "save": "str", "dc": 16, "recharge": 5,
              "damage": [(6, 8, "force")], "on_save": "half", "template": ("radius", 20)}),
            ("action", "Reverse Vector",
             "Choose up to three creatures within 60 feet. Each makes a DC 16 Dexterity saving throw. On a "
             "failure its personal gravity reverses until the end of its next turn and it falls upward up to "
             "30 feet.",
             {"kind": "save", "activation": "action", "range": 60, "save": "dex", "dc": 16, "targets": "3",
              "on_save": "none"}),
        ],
    ),
    dict(
        name="Veylari Gate Marshal", tradition="Void", role="Void commander and master Gatewright",
        size="lg", cr=12, ac=19, hp=187, formula="22d10 + 66", speed={"walk": 30, "fly": 40},
        abilities=(12, 16, 18, 21, 18, 18), saves=["con", "int", "wis", "cha"],
        skills={"arc": 2, "inv": 1, "prc": 1}, dr="force, psychic",
        senses={"darkvision": 120, "truesight": 60}, languages=_PIN_LANG,
        blurb="A Veylari commander does not ask how to reach the enemy fortress. They ask why the fortress is "
              "far away.",
        features=[
            ("trait", "Master of Distance",
             "The Marshal's ranged attacks ignore half and three-quarters cover if it can perceive the target "
             "by any means.", None),
            ("trait", "Dimensional Sovereignty",
             "Creatures within 30 feet cannot teleport without succeeding on a DC 17 Charisma saving throw. "
             "The Marshal automatically knows whenever a teleportation or planar effect occurs within 300 "
             "feet.", None),
            ("action", "Void Lance",
             "Ranged Spell Attack: +9 to hit, range 180 ft., one target. Hit: 31 (7d8) force damage.",
             {"kind": "attack", "activation": "action", "range": 180, "attack_type": "ranged", "ability": "int",
              "damage": [(7, 8, "force")]}),
            ("action", "Door Without Distance",
             "The Marshal creates two linked portals within 120 feet. They remain until the beginning of its "
             "next turn. Any creature entering one exits the other.",
             {"kind": "utility", "activation": "action", "range": 120}),
            ("action", "Collapse Distance",
             "Choose two creatures or points within 120 feet. Creatures along a 10-foot-wide line connecting "
             "those points make a DC 17 Dexterity saving throw, taking 36 (8d8) force damage and being pulled "
             "to the line's midpoint on a failure, or half damage on a success.",
             {"kind": "save", "activation": "action", "range": 120, "save": "dex", "dc": 17, "recharge": 5,
              "damage": [(8, 8, "force")], "on_save": "half", "template": ("line", 120)}),
            ("reaction", "Exclude",
             "When a creature teleports into a space within 60 feet, force it to make a DC 17 Charisma saving "
             "throw. On a failure the teleportation fails and the creature remains at its original location.",
             None),
        ],
    ),
    dict(
        name="Prismatic Lifeshaper", tradition="Sun + Moon", role="Combat medic and biomancer",
        size="lg", cr=6, ac=17, hp=105, formula="14d10 + 28", speed={"walk": 30},
        abilities=(10, 14, 16, 18, 18, 16), saves=["int", "wis"],
        skills={"arc": 1, "med": 2}, senses={"darkvision": 60}, languages=_PIN_LANG,
        blurb="Prismatics combine creation with transformation: combat medics, biomancers, adaptive engineers "
              "and living-architecture specialists.",
        features=[
            ("trait", "Adaptive Physiology",
             "At the beginning of its turn the Lifeshaper chooses acid, cold, fire, lightning or radiant. It "
             "gains resistance to that damage type until its next turn.", None),
            ("action", "Prism Lance",
             "Ranged Spell Attack: +7 to hit, range 120 ft., one target. Hit: 22 (4d10) radiant damage.",
             {"kind": "attack", "activation": "action", "range": 120, "attack_type": "ranged", "ability": "int",
              "damage": [(4, 10, "radiant")]}),
            ("action", "Rewrite Flesh",
             "One creature within 30 feet either regains 27 (6d8) hit points, ends one disease or poison, or "
             "ends blindness or paralysis. Three times per day.",
             {"kind": "heal", "activation": "action", "range": 30, "healing": (6, 8, "healing"), "uses": "3",
              "recovery": "lr"}),
            ("action", "Adaptive Mutation",
             "One willing creature within 30 feet gains one benefit for 1 minute: a climb speed of 30 feet, a "
             "swim speed of 40 feet, darkvision 120 feet, or resistance to one elemental damage type.",
             {"kind": "utility", "activation": "action", "range": 30, "duration": (1, "minute")}),
        ],
    ),
    dict(
        name="Nightway Pathfinder", tradition="Moon + Void", role="Elite explorer and astral navigator",
        size="lg", cr=6, ac=18, hp=110, formula="20d10 + 0", speed={"walk": 40},
        abilities=(10, 19, 14, 18, 18, 15), saves=["dex", "int", "wis"],
        skills={"arc": 2, "prc": 2, "ste": 1, "sur": 1}, senses={"darkvision": 120, "truesight": 30},
        languages=_PIN_LANG,
        blurb="The elite explorers and astral navigators of the Pindarian Empire.",
        features=[
            ("trait", "Planar Awareness",
             "The Pathfinder knows the location of every portal, teleportation effect and dimensional "
             "disturbance within 120 feet.", None),
            ("action", "Astral Bow",
             "Ranged Weapon Attack: +7 to hit, range 150/600 ft., one target. Hit: 20 (3d10 + 4) force damage.",
             {"kind": "attack", "activation": "action", "range": 150, "attack_type": "ranged", "ability": "dex",
              "damage": [(3, 10, "force")]}),
            ("action", "Nightway Passage",
             "The Pathfinder and up to three willing creatures within 10 feet teleport up to 120 feet.",
             {"kind": "utility", "activation": "action", "range": 120, "recharge": 5}),
            ("bonus", "Temporal Ambush",
             "Immediately after teleporting, the Pathfinder makes one Astral Bow attack with advantage.",
             {"kind": "utility", "activation": "bonus", "range": 0}),
        ],
    ),
    dict(
        name="Blackfire Warden", tradition="Sun + Void", role="Anti-demonic elite",
        size="lg", cr=10, ac=20, hp=168, formula="16d10 + 80", speed={"walk": 30},
        abilities=(18, 12, 20, 19, 17, 14), saves=["str", "con", "int", "wis"],
        skills={"arc": 1, "rel": 1}, dr="fire, force, radiant", senses={"darkvision": 60, "truesight": 30},
        languages=_PIN_LANG,
        blurb="Blackfire does not burn flesh. It burns magical relationships. These Wardens were among the "
              "principal troops used against the demonic invasion.",
        features=[
            ("trait", "Blackfire Aura",
             "Within 10 feet of the Warden, summoned creatures cannot regenerate, teleportation requires a DC "
             "16 Charisma saving throw, and possessed creatures have advantage on saves against possession.",
             None),
            ("action", "Blackfire Glaive",
             "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 13 (2d8 + 4) slashing damage "
             "plus 13 (3d8) force damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 8, "slashing"), (3, 8, "force")]}),
            ("action", "Sever Magic",
             "One creature within 60 feet makes a DC 16 Charisma saving throw. On a failure it takes 36 (8d8) "
             "force damage and one magical effect currently benefiting it is suppressed until the end of the "
             "Warden's next turn.",
             {"kind": "save", "activation": "action", "range": 60, "save": "cha", "dc": 16, "recharge": 5,
              "damage": [(8, 8, "force")], "on_save": "none"}),
            ("action", "Blackfire Barrier",
             "Create a 30-foot-long wall lasting 1 minute. Extraplanar creatures attempting to cross it make "
             "a DC 16 Charisma saving throw; on a failure they cannot cross and take 18 (4d8) force damage. "
             "Twice per day.",
             {"kind": "utility", "activation": "action", "range": 60, "uses": "2", "recovery": "lr",
              "template": ("line", 30), "duration": (1, "minute")}),
        ],
    ),
    dict(
        name="Vael'Shaar Reality Architect", tradition="Sun + Moon + Void", role="Strategic weapon",
        size="lg", cr=15, ac=20, hp=225, formula="30d10 + 60", speed={"walk": 30, "fly": 40},
        abilities=(10, 16, 18, 22, 20, 20), saves=["con", "int", "wis", "cha"],
        skills={"arc": 2, "his": 1, "ins": 1, "inv": 1}, dr="force, psychic, radiant", ci="frightened",
        senses={"darkvision": 120, "truesight": 60}, languages=_PIN_LANG,
        blurb="The Vael'Shaar are not ordinary soldiers. A single Architect might accompany an army of "
              "thousands. Their job is to determine what the battlefield is allowed to be.",
        features=[
            ("trait", "Triune Mastery",
             "At the beginning of every turn the Architect chooses one Current. Sun: it gains 15 temporary "
             "hit points. Moon: attacks against it have disadvantage. Void: teleportation within 30 feet "
             "fails unless the Architect permits it.", None),
            ("trait", "Reality Stability",
             "The Architect has advantage on saving throws against spells and magical effects.", None),
            ("action", "Multiattack", "The Architect makes two Reality Lance attacks.", None),
            ("action", "Reality Lance",
             "Ranged Spell Attack: +11 to hit, range 180 ft., one target. Hit: 33 (6d8 + 6) force or radiant "
             "damage.",
             {"kind": "attack", "activation": "action", "range": 180, "attack_type": "ranged", "ability": "int",
              "damage": [(6, 8, "force")]}),
            ("action", "Rewrite Geometry",
             "Choose a 30-foot cube within 120 feet. Until the Architect's next turn choose one. Sun - "
             "Construct: walls of solid light divide the area. Moon - Distort: enemies treat the area as "
             "difficult terrain and attacks against creatures inside have disadvantage. Void - Reorient: "
             "gravity points in a direction chosen by the Architect.",
             {"kind": "utility", "activation": "action", "range": 120, "recharge": 4, "template": ("cube", 30)}),
            ("action", "Triune Collapse",
             "A point within 120 feet becomes the centre of all three Currents. Creatures within 20 feet make "
             "a DC 19 Dexterity saving throw, taking 18 radiant, 18 psychic and 18 force damage and being "
             "pulled to the centre on a failure, or half damage and no movement on a success.",
             {"kind": "save", "activation": "action", "range": 120, "save": "dex", "dc": 19, "recharge": 6,
              "damage": [(4, 8, "radiant"), (4, 8, "psychic"), (4, 8, "force")], "on_save": "half",
              "template": ("radius", 20)}),
            ("action", "Reality Exclusion",
             "Choose one planar origin such as the Abyss, the Nine Hells, the Celestial planes, the Far Realm "
             "or Astral entities. For 1 minute, creatures of that origin within 30 feet cannot teleport or "
             "regain hit points, and a creature attempting to enter the aura must succeed on a DC 19 Charisma "
             "saving throw. Once per day.",
             {"kind": "utility", "activation": "action", "range": 30, "uses": "1", "recovery": "lr",
              "duration": (1, "minute")}),
            ("reaction", "Reject Event",
             "When a creature within 60 feet succeeds on an attack roll, saving throw or ability check, the "
             "Architect forces it to reroll. Three times per day.", None),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Named bosses.
#
# Same schema as LEGIONS plus:
#   legres / legact   - Legendary Resistance uses and legendary actions per round
#   spellcasting      - ability key; spells are embedded as real spell items
#   spells            - (name, level, school, components, range, body) prepared list
#   features sections extend to: legendary, mythic, lair
#
# Kathandar is the reconciliation of the three versions in circulation: the
# narrative Saharim from the sourcebook, the mythic CR 22 block, and the
# spellcasting lich export. He is all three. His spellbook draws on the Pindarian
# Arcana in this module rather than the Black Robe list from the Dragonlance
# build - that list belongs to the other Kathandar.
# ---------------------------------------------------------------------------

KATHANDAR = dict(
    name="Kathandar, Elder Dragonlord",
    tradition="Void", role="Saharim steward of Vhal'Kathar, Pyramid of the Last Breath",
    creature_type="undead", subtype="pindarian saharim, dragonlord",
    alignment="Lawful Neutral", size="lg", cr=22, prof=7,
    ac=21, hp=365, formula="34d10 + 178",
    speed={"walk": 30, "fly": 70},
    abilities=(23, 14, 24, 22, 22, 24),
    saves=["str", "con", "int", "wis", "cha"],
    skills={"arc": 2, "his": 3, "ins": 2, "prc": 2, "rel": 2},
    di="necrotic, poison", dr="cold, psychic; bludgeoning, piercing and slashing from nonmagical attacks",
    ci="charmed, exhaustion, frightened, paralyzed, poisoned",
    senses={"darkvision": 120, "truesight": 120},
    languages="Common, Draconic, Abyssal, Pindarian; telepathy 120 ft.",
    legres=4, legact=3, lair_initiative=20,
    spellcasting="int", spell_dc=21, spell_attack=13,
    blurb=(
        "Steward of the third anchor and the only one of the ten guardians who is not Pindarian. Kathandar "
        "took the Watch as an Elder Dragonlord and then went further than the binding required: four "
        "thousand years alone beneath a mountain, with the largest catalogue of the dead in existence and "
        "nothing to do but read it, turned a soldier into something the Pindarians had no word for. He kept "
        "the archive. He kept the upper necropolis swept. He never once went up the stair. And he has spent "
        "four millennia watching one window in a burning city, waiting for somebody to come down and tell "
        "him whether any of it purchased anything."
    ),
    features=[
        # -- traits ---------------------------------------------------------
        ("trait", "Legendary Resistance (4/Day)",
         "If Kathandar fails a saving throw, he can choose to succeed instead.", None),
        ("trait", "Magic Resistance",
         "Kathandar has advantage on saving throws against spells and other magical effects.", None),
        ("trait", "Deathless Watch",
         "If reduced to 0 hit points, Kathandar's body collapses and reforms in the Dragonlord's Vigil after "
         "1 hour. This trait ends permanently only when **Gravewake has been lawfully released** - the "
         "Last-Breath Nail is his phylactery, and it is three hundred feet below him.\n\nKilling him is "
         "therefore not a victory condition. It is a delay.", None),
        ("trait", "The Vigil",
         "While the spectral projection of Pindurane burns behind his throne, Kathandar cannot be frightened, "
         "has advantage on saving throws against being charmed, and gains +2 AC.\n\nA creature can use an "
         "action and succeed on a **DC 18 Intelligence (Arcana)** check to disrupt the projection until "
         "initiative 20 of the next round. While disrupted he loses the +2 AC, cannot use a legendary action, "
         "and spends his next reaction simply staring at the city.", None),
        ("trait", "The Law of the Last Breath",
         "Whenever Kathandar deals necrotic damage, his hit point maximum is reduced by one quarter of the "
         "necrotic damage actually dealt. The law binds the steward exactly as it binds everyone else.\n\nHe "
         "is aware of this. He does not care, and a party that works out why has most of the argument "
         "already.", None),
        ("trait", "Draconic Majesty",
         "When a creature that can see Kathandar starts its turn within 60 feet of him, it must succeed on a "
         "**DC 21 Wisdom saving throw** or be frightened until the end of its turn. A creature that succeeds "
         "is immune for 24 hours.\n\nHe does not use this deliberately. It is simply what an Elder Dragonlord "
         "is like in a small room.", None),
        ("trait", "Keeper of the Catalogue",
         "Kathandar knows the name, manner of death and date of death of every creature that has ever "
         "finished dying on Elderon. He cannot be deceived about a name.\n\nUndead within 120 feet cannot be "
         "turned while he is conscious, and he may refuse any attempt by another creature to command a dead "
         "creature within that radius.", None),
        ("trait", "Spellcasting",
         "Kathandar is a 20th-level spellcaster. His spellcasting ability is Intelligence "
         "(**spell save DC 21, +13 to hit with spell attacks**). He casts from the Void and Lunar Arcana of "
         "the Pindarian tradition and from four thousand years of necromancy nobody asked him to learn.\n\nHe "
         "has the prepared spells listed on this sheet and the spell slots of a 20th-level wizard.", None),

        # -- actions --------------------------------------------------------
        ("action", "Multiattack",
         "Kathandar makes three Dragonlord's Reach attacks, or casts one spell and makes one Dragonlord's "
         "Reach attack.", None),
        ("action", "Dragonlord's Reach",
         "Melee Weapon Attack: +13 to hit, reach 15 ft., one target. Hit: 19 (3d8 + 6) bludgeoning damage "
         "plus 18 (4d8) necrotic damage.",
         {"kind": "attack", "activation": "action", "range": 15, "attack_type": "melee", "ability": "str",
          "damage": [(3, 8, "bludgeoning"), (4, 8, "necrotic")]}),
        ("action", "Breath of the Last Archive",
         "Kathandar exhales four thousand years of held breath in a 60-foot cone. Each creature in the area "
         "makes a **DC 22 Constitution saving throw**, taking 66 (12d10) necrotic damage on a failure or half "
         "as much on a success.\n\nA creature that fails also hears, distinctly, its own name being filed.",
         {"kind": "save", "activation": "action", "range": 60, "save": "con", "dc": 22, "recharge": 5,
          "damage": [(12, 10, "necrotic")], "on_save": "half", "template": ("cone", 60)}),
        ("action", "Recite the Fallen",
         "Kathandar speaks the names of Pindaria's dead. Creatures of his choice within 60 feet make a "
         "**DC 21 Wisdom saving throw**, taking 54 (12d8) psychic damage on a failure or half as much on a "
         "success.\n\nA creature that fails also hears its own most recent dead named among the Pindarians "
         "and is stunned until the beginning of its next turn.",
         {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 21, "recharge": 5,
          "damage": [(12, 8, "psychic")], "on_save": "half"}),
        ("action", "Dragonlord's Decree",
         "Choose up to three creatures within 60 feet. Each makes a **DC 21 Charisma saving throw** or "
         "kneels, becoming prone and unable to stand until the end of its next turn. Twice per day.",
         {"kind": "save", "activation": "action", "range": 60, "save": "cha", "dc": 21, "targets": "3",
          "uses": "2", "recovery": "lr", "on_save": "none"}),
        ("action", "Seal the Dead",
         "One undead creature within 60 feet is imprisoned in geometric force. If unwilling it makes a "
         "**DC 21 Charisma saving throw**; on a failure it is restrained and incapacitated for 1 minute, "
         "repeating the save at the end of each of its turns.\n\nHe uses this on Vhaskar's empanelled jury "
         "before he uses it on anything the party brought.",
         {"kind": "save", "activation": "action", "range": 60, "save": "cha", "dc": 21, "on_save": "none",
          "duration": (1, "minute")}),

        # -- bonus / reaction -----------------------------------------------
        ("bonus", "Deathly Teleport",
         "Kathandar teleports up to 60 feet to an unoccupied space he can see, or to any space within 5 feet "
         "of a corpse anywhere in Vhal'Kathar.",
         {"kind": "utility", "activation": "bonus", "range": 60}),
        ("reaction", "Refuse the Claim",
         "When a creature within 120 feet attempts to animate, command, compel or bind a dead creature, "
         "Kathandar may cancel that effect. The creature attempting it makes a **DC 21 Charisma saving "
         "throw**; on a failure it also takes 27 (6d8) psychic damage.\n\nThis is not a tactic. It is his "
         "job.", None),

        # -- legendary ------------------------------------------------------
        ("legendary", "Reach", "Kathandar makes one Dragonlord's Reach attack.", None),
        ("legendary", "Walk the Vigil",
         "Kathandar moves up to 30 feet without provoking opportunity attacks.", None),
        ("legendary", "Bear Witness (Costs 2 Actions)",
         "One creature within 60 feet makes a **DC 21 Wisdom saving throw** or is stunned until the end of "
         "its next turn as it sees Pindurane fall from the inside.",
         {"kind": "save", "activation": "legendary", "range": 60, "save": "wis", "dc": 21, "on_save": "none"}),
        ("legendary", "Name Another (Costs 3 Actions)",
         "Kathandar uses Recite the Fallen against one creature only, without expending its recharge.", None),

        # -- lair -----------------------------------------------------------
        ("lair", "Lair Action: The Stair Reads",
         "On initiative count 20, the Descent of Names cuts a new entry. Each creature of Kathandar's choice "
         "within the Vigil makes a **DC 20 Wisdom saving throw** or takes 22 (4d10) psychic damage as it "
         "hears a name it recognises.", None),
        ("lair", "Lair Action: The Chasm Objects",
         "The confession span withdraws. Each creature not standing on the near or far platform makes a "
         "**DC 20 Dexterity saving throw** or falls prone at the chasm's edge; a creature already prone there "
         "must succeed or begin falling.", None),
        ("lair", "Lair Action: Pindurane Advances",
         "The burning projection moves forward four minutes. Until initiative 20 of the next round, the floor "
         "within 30 feet of the throne is difficult terrain and any creature ending its turn there takes 11 "
         "(2d10) fire damage from a city that is not present.", None),

        # -- mythic ---------------------------------------------------------
        ("mythic", "Mythic Trait: Pindurane Burns Again",
         "**If Kathandar reaches 0 hit points while combat continues and his question remains unanswered**, "
         "the burning city behind him floods through his body instead of killing him.\n\nHe regains **300 hit "
         "points**, his size becomes Large, and spectral dragon wings open behind him. The battlefield becomes "
         "the burning capital.\n\nFor the remainder of the encounter he gains a flying speed of 100 feet, a "
         "fourth legendary action each round, and resistance to radiant and force damage.\n\n**The argument "
         "still ends the fight.** Nothing about this phase closes the evidence route - see the Vigil's "
         "resolution table. A party that was always going to lose the fight has not lost the encounter.",
         None),
        ("mythic", "Falling Tower",
         "A 15-foot radius within 120 feet collapses. Each creature there makes a **DC 21 Dexterity saving "
         "throw**, taking 27 (5d10) force damage on a failure or half as much on a success.",
         {"kind": "save", "activation": "mythic", "range": 120, "save": "dex", "dc": 21,
          "damage": [(5, 10, "force")], "on_save": "half", "template": ("radius", 15)}),
        ("mythic", "Evacuation Route",
         "Kathandar moves one creature up to 30 feet. A willing creature is simply moved; an unwilling one "
         "makes a **DC 21 Strength saving throw** to resist.\n\nHe is not repositioning them. He is trying to "
         "get them out of a building that burned down four thousand years ago.", None),
        ("mythic", "Last Night of Pindaria (Costs 2 Actions)",
         "Each creature within 30 feet makes a **DC 21 Wisdom saving throw**, taking 22 (4d10) psychic damage "
         "and becoming frightened until the end of its next turn on a failure.",
         {"kind": "save", "activation": "mythic", "range": 30, "save": "wis", "dc": 21,
          "damage": [(4, 10, "psychic")], "on_save": "half", "template": ("radius", 30)}),
        ("mythic", "Tell Me It Purchased Something (Costs 4 Actions)",
         "Every creature in the chamber makes a **DC 21 Wisdom saving throw**, taking 36 (8d8) psychic damage "
         "and becoming incapacitated until the end of its next turn on a failure.\n\nHe asks the question out "
         "loud while he does it. If anyone answers it honestly, the encounter ends.",
         {"kind": "save", "activation": "mythic", "range": 120, "save": "wis", "dc": 21,
          "damage": [(8, 8, "psychic")], "on_save": "half"}),
    ],
    spells=[
        # Pindarian Arcana entries carry only a caster note. The rules text is
        # pulled from the compendium at build time, so every sheet and every
        # spell card show exactly the same spell.
        ("Vector Knot", 0, "trs", "somatic", (60, "ft"),
         "A cantrip Kathandar uses as punctuation rather than as an attack, to move a speaker half a pace "
         "sideways so that they are standing where he wants them when he answers."),
        ("Null Step", 1, "con", "somatic", (15, "ft"),
         "Four thousand years in one building has made this reflexive. He does not appear to cast it, and "
         "most visitors never notice he has moved."),
        ("Astral Thread", 2, "div", "vocal,somatic", (30, "ft"),
         "He ties one to anyone he intends to let leave alive, so that he knows when they cross out of "
         "Vhal'Kathar and can stop listening for them."),
        ("Planar Mooring", 3, "abj", "vocal,somatic,concentration", (60, "ft"),
         "His opening move against Vhaskar Corr, every time, for four thousand years. Vhaskar knows it is "
         "coming and walks into it anyway, which Kathandar finds more insulting than the desertion."),
        ("Event Horizon Cage", 4, "trs", "vocal,somatic,concentration", (90, "ft"),
         "He uses this to hold ground rather than to hurt anyone, and will cast it across a doorway the "
         "party is standing in rather than across the party."),
        ("Astral Shear", 5, "abj", "vocal,somatic", (90, "ft"),
         "Written for use against demons, and used in four thousand years exactly twice."),
        ("Archive of the Living Moment", 5, "div", "vocal,somatic,concentration,ritual", (0, "self"),
         "This is how he already knows what the party did upstairs. He casts it every morning in the "
         "Procession and watches the previous day from the doorway."),
        ("Black Meridian", 6, "trs", "vocal,somatic", (120, "ft"),
         "The only spell on his list he describes as a weapon. He apologises before using it, to the room."),
        ("Gravity Crown", 7, "trs", "vocal,somatic,concentration", (60, "ft"),
         "A Veylari field-officer's working for moving a unit across broken ground. He has not needed it "
         "for that purpose since year 0."),
        ("Ninefold Bastion", 8, "abj", "vocal,somatic", (0, "self"),
         "He helped write the working this spell is the ancestor of. Asked whether the Ninefold Prohibition "
         "is simply this spell made permanent, he says yes - and then corrects himself: *\"No. This one "
         "ends.\"*"),
        ("Soul Orbit", 8, "nec", "vocal,somatic", (60, "ft"),
         "He will cast this on the party without being asked, before a fight he expects them to lose, and "
         "he will not mention that he has done it."),
        ("Reality Exclusion", 9, "abj", "vocal,somatic,concentration", (0, "self"),
         "Fewer than five beings alive have cast this at full scale. Kathandar is one of them, he has done "
         "it once, and the plane he named is not one he will discuss."),
        ("Choose the Better World", 9, "trs", "vocal", (0, "special"),
         "**He has one 9th-level slot, and he has had one 9th-level slot for four thousand years.** He is "
         "saving it. He will not say what for, and *Insight DC 20* establishes only that he has already "
         "decided."),

        # Necromancy he taught himself, long after the Watch required it.
        ("Grave Whisper", 0, "nec", "vocal,somatic", (60, "ft"),
         "You speak a word to something that has stopped listening. Make a ranged spell attack against one "
         "creature within range. On a hit the target takes 1d10 necrotic damage.\n\nIf the target is below "
         "half its hit point maximum it also hears, clearly, the name of the last creature it watched die. "
         "This has no mechanical effect and is not an illusion.\n\nThe damage increases to 2d10 at 5th "
         "level, 3d10 at 11th and 4d10 at 17th.\n\n*Composed by Kathandar in the second century of the "
         "Watch. He has never taught it to anyone.*",
         {"kind": "attack", "attack_type": "ranged", "ability": "int", "damage": [(1, 10, "necrotic")]}),
        ("Animate Dead", 3, "nec", "vocal,somatic,material", (10, "ft"),
         "*Material component: a drop of blood, a piece of flesh, and a pinch of bone dust.*\n\nChoose a "
         "pile of bones or a corpse of a Medium or Small humanoid within range. Your spell imbues the target "
         "with a foul mimicry of life, raising it as an undead creature: a skeleton if you chose bones, or a "
         "zombie if you chose a corpse.\n\nOn each of your turns you can use a bonus action to mentally "
         "command any creature you made with this spell if it is within 60 feet of you. You decide what "
         "action the creature takes and where it moves, or you can issue a general command. The creature "
         "obeys for 24 hours, after which it must be commanded again or it ceases to follow you.\n\n**At "
         "Higher Levels.** Each slot level above 3rd animates or reasserts control over two additional "
         "undead.\n\n**Kathandar has this prepared and has never cast it.** Not once, in four thousand "
         "years, in a building containing the largest catalogue of the dead in existence. The party may ask "
         "him why, and he will answer.",
         None),
        ("Blight", 4, "nec", "vocal,somatic", (30, "ft"),
         "Necromantic energy washes over a creature you can see within range, draining moisture and "
         "vitality from it. The target makes a Constitution saving throw, taking 8d8 necrotic damage on a "
         "failed save or half as much on a successful one. This spell has no effect on undead or "
         "constructs.\n\nA plant creature makes the save with disadvantage and takes maximum damage on a "
         "failure. A nonmagical plant that is not a creature gets no save and simply withers.\n\n**At "
         "Higher Levels.** The damage increases by 1d8 per slot level above 4th.",
         {"kind": "save", "save": "con", "damage": [(8, 8, "necrotic")], "on_save": "half"}),
        ("Circle of Death", 6, "nec", "vocal,somatic,material", (150, "ft"),
         "*Material component: the powder of a crushed black pearl worth at least 500 gp.*\n\nA sphere of "
         "negative energy ripples out in a 60-foot radius from a point you choose within range. Each "
         "creature in that area makes a Constitution saving throw, taking 8d6 necrotic damage on a failed "
         "save or half as much on a successful one.\n\n**At Higher Levels.** The damage increases by 2d6 "
         "per slot level above 6th.",
         {"kind": "save", "save": "con", "damage": [(8, 6, "necrotic")], "on_save": "half",
          "template": ("radius", 60)}),
        ("Finger of Death", 7, "nec", "vocal,somatic", (60, "ft"),
         "You send negative energy coursing through a creature you can see within range. The target makes a "
         "Constitution saving throw, taking 7d8 + 30 necrotic damage on a failed save or half as much on a "
         "successful one.\n\nA humanoid killed by this spell rises at the start of your next turn as a "
         "zombie permanently under the caster's command.\n\n**Kathandar always declines that clause.** It "
         "costs him nothing, it is the single most important line on this sheet, and a party that notices "
         "should be told they noticed.",
         {"kind": "save", "save": "con", "damage": [(7, 8, "necrotic")], "formula": "30", "on_save": "half"}),
    ],
)

BOSSES = [KATHANDAR]


# ---------------------------------------------------------------------------
# BESTIARY - the boss roster for the Astra and Vhal'Kathar site guides.
#
# These are set-piece replacements for the rank-and-file versions quoted in the
# site guides. Each one is tied to the philosophical test of its room: the
# strongest of them (Seryth, the Keeper, Vhaskar, Vhessara, Orcus) become easier
# or stop entirely when the players understand what the pyramid is teaching.
#
# Where the guides call for groups - three Sun Guards, two Blood Oozes, several
# Remnants - the block says so and shares one legendary pool rather than giving
# every creature its own turn.
# ---------------------------------------------------------------------------

_ASTRA = "Astra, Pyramid of the Sun"
_VHAL = "Vhal'Kathar, Pyramid of the Last Breath"

BESTIARY = [
    dict(
        name="Wantglass Double", context=_ASTRA, role="Astra's matching construct (A1, A3, and shadowing from Temptation 3)",
        creature_type="construct", subtype="pindarian reflection", alignment="Unaligned",
        size="med", cr=7, prof=3, ac=18, hp=136, formula="16d8 + 64", speed={"walk": 40},
        abilities=(14, 20, 18, 15, 16, 19), saves=["dex", "wis", "cha"],
        skills={"dec": 2, "ins": 1, "prc": 1},
        dr="psychic, radiant", di="poison", ci="charmed, exhaustion, poisoned",
        senses={"darkvision": 60}, languages="understands the languages of its original; telepathy 60 ft.",
        legres=1, legact=2,
        blurb="A reflection that stepped out. It is not a copy of a person - it is a copy of what a person "
              "wants, wearing their face, and it is delighted to be of service.",
        features=[
            ("trait", "Mirrored Original",
             "**The Double is whatever size its original is** - it is a reflection, not a Pindarian, and it "
             "takes the shape it was cast from.\n\nWhen created, the Double is bound to one creature it can "
             "perceive, called its **original**. It "
             "knows the original's ability scores, current hit points, ideals, bonds, flaws and strongest "
             "immediate desire, and has advantage on attack rolls against it.", None),
            ("trait", "Reflective Passage",
             "While within 5 feet of a mirror or similarly reflective surface, the Double can move through it "
             "and emerge from another reflective surface it can see within 60 feet.", None),
            ("trait", "Borrowed Motion",
             "The first time each round its original makes a weapon attack, casts a cantrip, or takes the "
             "Dash, Disengage or Dodge action, the Double can use its reaction to imitate that action. A "
             "copied attack uses the Double's own modifiers and damage.", None),
            ("trait", "Surrender to Honesty",
             "If its original voluntarily speaks aloud the truth that created it, relinquishes an object they "
             "genuinely want, or openly refuses a temptation offered by Astra, the Double loses 30 hit "
             "points, cannot use Legendary Resistance until the end of its next turn, and may immediately "
             "choose to dissolve harmlessly.\n\n**Below half hit points it offers this resolution aloud** "
             "rather than fighting mindlessly.", None),
            ("trait", "Legendary Resistance (1/Day)",
             "If the Double fails a saving throw it can choose to succeed instead.", None),
            ("action", "Multiattack", "The Double makes two Wantglass Blade attacks.", None),
            ("action", "Wantglass Blade",
             "Melee Spell Attack: +8 to hit, reach 5 ft., one target. Hit: 14 (2d8 + 5) psychic damage plus 7 "
             "(2d6) radiant damage. If the target is the Double's original, it cannot take reactions until "
             "the beginning of its next turn.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "cha",
              "damage": [(2, 8, "psychic"), (2, 6, "radiant")]}),
            ("action", "Perfect Offer",
             "The Double creates a flawless image of something one creature within 60 feet deeply desires. "
             "The target makes a **DC 15 Wisdom saving throw**, taking 27 (6d8) psychic damage and becoming "
             "charmed until the end of its next turn on a failure. While charmed its speed is 0 and it "
             "perceives nothing except the offered vision and the Double.\n\nThe effect ends immediately if "
             "the target says *'I know this is not mine'* or otherwise explicitly rejects the offered desire.",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 15, "recharge": 5,
              "damage": [(6, 8, "psychic")], "on_save": "none"}),
            ("action", "Mirror Rupture",
             "Each creature of the Double's choice within 15 feet makes a **DC 16 Dexterity saving throw**, "
             "taking 27 (6d8) radiant damage and being blinded until the end of its next turn on a failure, "
             "or half damage on a success. Once per day.",
             {"kind": "save", "activation": "action", "range": 15, "save": "dex", "dc": 16, "uses": "1",
              "recovery": "lr", "damage": [(6, 8, "radiant")], "on_save": "half", "template": ("radius", 15)}),
            ("reaction", "Borrowed Gesture", "The Double uses Borrowed Motion.", None),
            ("legendary", "Mirror Step", "The Double uses Reflective Passage.", None),
            ("legendary", "Cut", "The Double makes one Wantglass Blade attack.", None),
            ("legendary", "Tell Me You Don't Want It (Costs 2 Actions)",
             "One creature affected by Perfect Offer immediately repeats its saving throw. On a failure it "
             "takes 9 (2d8) psychic damage.",
             {"kind": "save", "activation": "legendary", "range": 60, "save": "wis", "dc": 15,
              "damage": [(2, 8, "psychic")], "on_save": "none"}),
        ],
    ),
    dict(
        name="Pindarian Sun Guard", context=_ASTRA, role="Solar Engine guard and Temptation-6 patrol (A2, A5)",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Neutral",
        size="lg", cr=8, prof=3, ac=20, hp=156, formula="24d10 + 24", speed={"walk": 35},
        abilities=(18, 16, 15, 14, 17, 15), saves=["str", "dex", "wis"],
        skills={"ath": 1, "ins": 1, "prc": 1},
        dr="fire, radiant; bludgeoning, piercing and slashing from nonmagical attacks",
        ci="frightened", senses={"darkvision": 120}, languages="Common, Draconic, Pindarian",
        legact=2,
        blurb="They ask once, politely, for the items to be returned. They attack only after refusal, and "
              "they accept a surrender at any point, mid-swing, without conditions.\n\nUse ONE upgraded Guard "
              "with two CR 5 Guards for the A5 encounter at levels 6-7. Three upgraded Guards is a much "
              "higher-level fight. Where several appear together the group shares two Elite Actions in total.",
        features=[
            ("trait", "Deathless Watch",
             "Unless Astra has been lawfully released, a destroyed Sun Guard reforms at dawn inside the "
             "pyramid.", None),
            ("trait", "Interlocking Formation",
             "While within 10 feet of another Sun Guard, both creatures gain +1 AC.", None),
            ("trait", "Thief's Mark",
             "The Guard always knows which visible creature carries the greatest value of property taken from "
             "Astra without permission, and has advantage on its first attack each turn against that "
             "creature.", None),
            ("action", "Multiattack", "The Guard makes three Solar Glaive attacks.", None),
            ("action", "Solar Glaive",
             "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 10 (1d10 + 5) slashing damage "
             "plus 9 (2d8) radiant damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(1, 10, "slashing"), (2, 8, "radiant")]}),
            ("action", "Castigating Ray",
             "One creature within 120 feet makes a **DC 16 Dexterity saving throw**, taking 36 (8d8) radiant "
             "damage on a failure or half as much on a success. A creature carrying stolen Astran treasure "
             "makes this save with disadvantage.",
             {"kind": "save", "activation": "action", "range": 120, "save": "dex", "dc": 16, "recharge": 5,
              "damage": [(8, 8, "radiant")], "on_save": "half"}),
            ("action", "Solar Lock",
             "One creature within 30 feet makes a **DC 16 Strength saving throw** or is restrained by bands "
             "of solid sunlight until the end of the Guard's next turn.",
             {"kind": "save", "activation": "action", "range": 30, "save": "str", "dc": 16, "on_save": "none"}),
            ("bonus", "Formation Step",
             "The Guard moves up to 15 feet without provoking opportunity attacks, provided it ends closer to "
             "another Sun Guard, the engine, Seryth, or a creature carrying stolen treasure.",
             {"kind": "utility", "activation": "bonus", "range": 15}),
            ("reaction", "Interpose Light",
             "When another creature within 10 feet takes damage, reduce that damage by 15. The Guard cannot "
             "use this on itself - and it never does.", None),
            ("legendary", "Advance", "The Guard moves 15 feet.", None),
            ("legendary", "Glaive", "The Guard makes one Solar Glaive attack.", None),
            ("legendary", "Solar Rebuke (Costs 2 Actions)",
             "One creature within 30 feet that damaged another Sun Guard since the end of this Guard's last "
             "turn takes 10 radiant damage.", None),
        ],
    ),
    dict(
        name="Ivresse, Saharim Custodian", context=_ASTRA, role="Astra's housekeeper (A5) - non-hostile",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Good",
        size="lg", cr=10, prof=4, ac=19, hp=188, formula="29d10 + 28", speed={"walk": 30},
        abilities=(13, 18, 15, 18, 21, 17), saves=["dex", "int", "wis"],
        skills={"arc": 1, "his": 1, "ins": 2, "inv": 1, "prc": 1},
        dr="radiant, necrotic, psychic", ci="charmed, exhaustion, frightened",
        senses={"darkvision": 60, "truesight": 30},
        languages="Pindarian, Common, Draconic; telepathy with Astra 1 mile",
        legact=3,
        blurb="A small, thorough woman in a stained apron with a broom she does not need. She has swept Astra "
              "for four thousand years.\n\n**She is a social NPC.** This block exists only for a table that "
              "forces violence, and it is written so that doing so is a bad idea.",
        features=[
            ("trait", "Deathless Watch", "Ivresse reforms at dawn while Astra remains active.", None),
            ("trait", "Four Thousand Years of Maintenance",
             "Ivresse knows every door, trap, maintenance tunnel, planar conduit and Astran construct. She "
             "cannot be surprised while inside Astra.", None),
            ("trait", "Housekeeper, Not Priestess",
             "Ivresse has advantage on saving throws against spells and possesses no interest whatsoever in "
             "magical duelling. Her attacks deal nonlethal damage whenever that is mechanically possible.",
             None),
            ("trait", "Everything Has Its Place",
             "A hostile creature within 30 feet that drops an object, is disarmed, or has an object knocked "
             "from its hands cannot retrieve it without succeeding on a **DC 17 Wisdom saving throw**. The "
             "item ends up somewhere inconvenient but tidy.", None),
            ("action", "Multiattack", "Ivresse makes two Broom attacks.", None),
            ("action", "The Broom",
             "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 9 (1d8 + 5) bludgeoning damage "
             "plus 13 (3d8) force damage, and the target must succeed on a **DC 17 Strength saving throw** or "
             "be pushed 15 feet.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "wis",
              "damage": [(1, 8, "bludgeoning"), (3, 8, "force")]}),
            ("action", "Sweep the Threshold",
             "Ivresse sweeps a 30-foot cone. Creatures of her choice make a **DC 17 Strength saving throw**, "
             "taking 31 (7d8) force damage and being pushed 30 feet on a failure, or half damage and pushed "
             "10 feet on a success. Objects under 500 pounds are swept to the cone's edge and arranged "
             "neatly.",
             {"kind": "save", "activation": "action", "range": 30, "save": "str", "dc": 17, "recharge": 5,
              "damage": [(7, 8, "force")], "on_save": "half", "template": ("cone", 30)}),
            ("action", "Maintenance Shutdown",
             "Ivresse targets one magical hazard, trap, construct or Pindarian device within 60 feet. A "
             "non-artifact effect of 6th level or lower turns off until the beginning of her next turn.",
             {"kind": "utility", "activation": "action", "range": 60}),
            ("action", "Put That Back",
             "One creature within 60 feet carrying an object belonging to Astra makes a **DC 17 Wisdom saving "
             "throw** or uses its reaction to place or throw the object toward the nearest appropriate "
             "surface or container.",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 17, "on_save": "none"}),
            ("reaction", "Not On My Floor",
             "When a creature within 30 feet deals 20 or more damage to the pyramid, a construct or an "
             "unattended object, Ivresse reduces that damage by 20.", None),
            ("legendary", "Sweep", "Ivresse makes one Broom attack.", None),
            ("legendary", "Lock Up",
             "One door within 60 feet closes and becomes magically locked (DC 20 to open).", None),
            ("legendary", "Turn It Off (Costs 2 Actions)", "Ivresse uses Maintenance Shutdown.", None),
            ("legendary", "You Have Made Quite Enough Mess (Costs 3 Actions)",
             "Every hostile creature within 15 feet makes a **DC 17 Strength saving throw** or falls prone "
             "and is pushed 15 feet.",
             {"kind": "save", "activation": "legendary", "range": 15, "save": "str", "dc": 17,
              "on_save": "none", "template": ("radius", 15)}),
        ],
    ),
    dict(
        name="High Priestess Seryth Vael, the Last Dawn", context=_ASTRA,
        role="Mythic guardian of the Court of the Last Dawn (A7)",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Neutral",
        size="lg", cr=17, prof=6, ac=21, hp=272, formula="32d10 + 96", speed={"walk": 35},
        abilities=(20, 18, 18, 20, 22, 22), saves=["str", "con", "wis", "cha"],
        skills={"arc": 1, "his": 1, "ins": 1, "prc": 1, "per": 1},
        dr="fire, force, necrotic, radiant; bludgeoning, piercing and slashing from nonmagical attacks",
        ci="charmed, exhaustion, frightened", senses={"truesight": 60},
        languages="Pindarian, Common, Draconic, Celestial, Abyssal",
        legres=3, legact=3,
        blurb="A forced battle against Seryth is deliberately beyond the intended Astra party. **The lawful "
              "release can end combat at any point**, and she says so out loud at the end of round two.",
        features=[
            ("trait", "Legendary Resistance (3/Day)",
             "If Seryth fails a saving throw she can choose to succeed instead.", None),
            ("trait", "Deathless Watch",
             "Seryth reforms at dawn unless the Velvet Ruin has been lawfully released.", None),
            ("trait", "Temptation Conversion",
             "At the start of combat, convert every remaining Temptation point into either **5 temporary hit "
             "points** or one **Solar Hazard**. Announce each conversion aloud, item by item.\n\n**Standing "
             "Light:** +10 spell attack for 18 (4d8) radiant. **Noon Zone:** a 10-foot area dealing 11 (2d10) "
             "radiant at end of turn. **Flare:** DC 16 Constitution or blinded until end of next turn.\n\nOne "
             "hazard activates on initiative 20 each round.", None),
            ("trait", "She Knows What You Took",
             "Seryth knows which objects in the chamber belong to Astra and has advantage on attacks against "
             "a creature carrying stolen treasure.", None),
            ("trait", "Sacrifice Recognised",
             "If the party has demonstrated genuine sacrifice anywhere in Astra - a Solar Seal, a token in an "
             "alcove bowl, treasure returned at the engine - Seryth yields at **68 hit points or fewer**. "
             "Without that demonstration she does not yield.", None),
            ("trait", "The Offer Remains",
             "At any point during combat a character may lower or drop their weapon, name a true desire, and "
             "surrender something of genuine personal value.\n\n**If sincere, combat ends immediately. No "
             "roll.**", None),
            ("action", "Multiattack", "Seryth makes three Last Dawn Glaive attacks.", None),
            ("action", "Last Dawn Glaive",
             "Melee Weapon Attack: +12 to hit, reach 10 ft., one target. Hit: 15 (2d8 + 6) slashing damage "
             "plus 18 (4d8) radiant damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 8, "slashing"), (4, 8, "radiant")]}),
            ("action", "Expose Desire",
             "One creature within 60 feet makes a **DC 20 Wisdom saving throw**, taking 45 (10d8) psychic "
             "damage and becoming charmed until the end of its next turn on a failure, or half damage on a "
             "success. While charmed it sees the life it most wants and cannot willingly move farther from "
             "Seryth.\n\n**She will not use this on a creature that has already spoken its true desire "
             "honestly** - and if a player notices that, tell them they noticed.",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 20, "recharge": 5,
              "damage": [(10, 8, "psychic")], "on_save": "half"}),
            ("action", "Solar Judgment",
             "A 20-foot-radius sphere within 120 feet erupts in light. **DC 20 Dexterity saving throw**: 36 "
             "(8d8) radiant damage and blinded until the end of the creature's next turn on a failure, half "
             "damage and no blindness on a success.",
             {"kind": "save", "activation": "action", "range": 120, "save": "dex", "dc": 20,
              "damage": [(8, 8, "radiant")], "on_save": "half", "template": ("radius", 20)}),
            ("bonus", "Solar Step",
             "Seryth becomes light and teleports up to 60 feet. She may take one willing or charmed creature "
             "within 5 feet with her.",
             {"kind": "utility", "activation": "bonus", "range": 60}),
            ("reaction", "Refuse Temptation",
             "When a creature within 60 feet activates a magic item, consumable or artifact, Seryth may force "
             "a **DC 20 Charisma saving throw**. On a failure the activation still occurs, but Seryth chooses "
             "one: halve any damage it causes; halve healing received; prevent teleportation produced by it; "
             "or gain 20 temporary hit points.", None),
            ("legendary", "Glaive", "Seryth makes one Last Dawn Glaive attack.", None),
            ("legendary", "Solar Step", "Seryth uses Solar Step.", None),
            ("legendary", "Judgment (Costs 2 Actions)",
             "A creature carrying stolen treasure takes 13 (3d8) radiant damage.",
             {"kind": "damage", "activation": "legendary", "range": 60, "damage": [(3, 8, "radiant")]}),
            ("legendary", "Ask the Question (Costs 3 Actions)",
             "One creature makes a **DC 20 Wisdom saving throw** or becomes unable to take hostile actions "
             "until the end of its next turn, as Seryth asks: *'What would you let the world end for?'*",
             {"kind": "save", "activation": "legendary", "range": 60, "save": "wis", "dc": 20,
              "on_save": "none"}),
            ("mythic", "Mythic Trait: The Last Dawn Refuses",
             "**If Seryth reaches 0 hit points while the Velvet Ruin remains unreleased, nobody has "
             "demonstrated sacrifice, and the party continues trying to take it by force**, she does not fall."
             "\n\nAll active Solar Hazards collapse into her. She regains **220 hit points**, recharges Expose "
             "Desire, and the chamber becomes blindingly bright.\n\nFor the remainder of the encounter her "
             "speed becomes 50 feet, Last Dawn Glaive deals an additional 9 radiant damage, and she gains a "
             "fourth legendary action each round.\n\n**The lawful-release option still remains available.**",
             None),
            ("mythic", "Burn Away Possession",
             "One carried non-artifact item belonging to Astra teleports from its bearer back to its original "
             "location.", None),
            ("mythic", "Noonfall (Costs 2 Actions)",
             "Each creature in a 15-foot radius makes a **DC 20 Constitution saving throw**, taking 22 "
             "radiant damage and being blinded on a failure.",
             {"kind": "save", "activation": "mythic", "range": 60, "save": "con", "dc": 20,
              "damage": [(4, 10, "radiant")], "on_save": "half", "template": ("radius", 15)}),
            ("mythic", "You Were Offered Another Way (Costs 3 Actions)",
             "All hostile creatures that have refused a peaceful resolution make **DC 20 Wisdom saving "
             "throws**, taking 31 psychic damage on a failure.",
             {"kind": "save", "activation": "mythic", "range": 120, "save": "wis", "dc": 20,
              "damage": [(7, 8, "psychic")], "on_save": "half"}),
        ],
    ),
]

BESTIARY += [
    dict(
        name="Shadowhand Executioner", context=_VHAL, role="Vhaskar's crossbow crew (W3, V3)",
        creature_type="humanoid", subtype="any race", alignment="Neutral Evil",
        size="med", cr=7, prof=3, ac=18, hp=112, formula="15d8 + 45", speed={"walk": 35},
        abilities=(11, 20, 16, 12, 15, 10), saves=["dex", "con"],
        skills={"prc": 1, "ste": 2}, senses={"darkvision": 60}, languages="Common",
        blurb="A professional. No ideology, no last words, paid in advance.\n\nKeep the CR 3 rank-and-file "
              "version for the twelve on the balconies; use this block for the squad captain or the sniper.",
        features=[
            ("trait", "Professional Detachment",
             "The Executioner has advantage on saving throws against being frightened.", None),
            ("trait", "Cull the Wounded",
             "Attacks against creatures below half their hit point maximum deal an additional 7 (2d6) "
             "piercing damage.", None),
            ("trait", "Black-Vein Ammunition",
             "Poison damage dealt by the Executioner ignores resistance to poison.", None),
            ("action", "Multiattack", "The Executioner makes three Repeater attacks.", None),
            ("action", "Repeater",
             "Ranged Weapon Attack: +8 to hit, range 80/320 ft., one target. Hit: 10 (1d10 + 5) piercing "
             "damage.",
             {"kind": "attack", "activation": "action", "range": 80, "attack_type": "ranged", "ability": "dex",
              "damage": [(1, 10, "piercing")]}),
            ("action", "Vein-Black Bolt",
             "As Repeater. On a hit the target makes a **DC 16 Constitution saving throw**, taking an "
             "additional 28 (8d6) poison damage and becoming poisoned for 1 minute on a failure, or half "
             "poison damage on a success. It repeats the save at the end of each of its turns. Twice per day.",
             {"kind": "save", "activation": "action", "range": 80, "save": "con", "dc": 16, "uses": "2",
              "recovery": "lr", "damage": [(8, 6, "poison")], "on_save": "half"}),
            ("action", "Finishing Bolt",
             "The Executioner makes one Repeater attack against a prone, restrained, stunned or unconscious "
             "creature. On a hit the attack is a critical hit.",
             {"kind": "attack", "activation": "action", "range": 80, "attack_type": "ranged", "ability": "dex",
              "damage": [(1, 10, "piercing")]}),
            ("bonus", "Reposition", "The Executioner takes the Dash, Disengage or Hide action.",
             {"kind": "utility", "activation": "bonus", "range": 0}),
            ("reaction", "Smoke-Line Extraction",
             "When a creature ends its turn within 5 feet, the Executioner moves up to half its speed without "
             "provoking opportunity attacks.", None),
        ],
    ),
    dict(
        name="Hearthspeaker of the Frozen Muster", context="The siege of Wahyrst",
        role="Ice giant funeral-priest and legendary artillery",
        creature_type="giant", subtype="ice giant", alignment="Neutral",
        size="huge", cr=11, prof=4, ac=17, hp=230, formula="20d12 + 100", speed={"walk": 40},
        abilities=(22, 9, 22, 14, 21, 18), saves=["con", "wis", "cha"],
        skills={"his": 1, "ins": 1, "rel": 1}, di="cold", dr="necrotic, psychic",
        senses={"darkvision": 60}, languages="Giant, rough Pindarian",
        legres=2, legact=3,
        blurb="She has spent this week listening to her clan's cairns argue with her, and she is no longer "
              "sure which side she is on. A slow, enormous, sorrowful artillery piece - a party that closes "
              "to melee should feel clever for doing it.",
        features=[
            ("trait", "Legendary Resistance (2/Day)",
             "If the Hearthspeaker fails a saving throw she can choose to succeed instead.", None),
            ("trait", "Keeper of Cairns",
             "Undead within 60 feet cannot be turned. The Hearthspeaker knows the name of every corpse and "
             "undead creature within that radius.", None),
            ("trait", "The Cairns Are Open",
             "Whenever a creature dies within 60 feet, the Hearthspeaker regains 15 hit points, learns that "
             "creature's name, and may end one condition affecting herself.", None),
            ("trait", "Grief-Slowed",
             "The Hearthspeaker has disadvantage on initiative rolls and cannot take the Dash action. She is "
             "not in a hurry and has not been for some time.", None),
            ("action", "Funeral Stave",
             "Melee Weapon Attack: +10 to hit, reach 10 ft., one target. Hit: 24 (3d10 + 6) bludgeoning "
             "damage plus 9 (2d8) cold damage.\n\n*One attack. No multiattack - she is a priest carrying a "
             "stick, not a warrior.*",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(3, 10, "bludgeoning"), (2, 8, "cold")]}),
            ("action", "Recitation of the Muster",
             "Each chosen creature within 60 feet makes a **DC 17 Wisdom saving throw**, taking 44 (8d10) "
             "psychic damage and suffering disadvantage on its next attack and saving throw on a failure, or "
             "half damage on a success.\n\nA creature that fails also hears the name of someone it failed to "
             "save.",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 17, "recharge": 5,
              "damage": [(8, 10, "psychic")], "on_save": "half"}),
            ("action", "Rime of the Long Sleep",
             "A 30-foot-radius area within 120 feet freezes spiritually rather than physically. Creatures "
             "there make a **DC 18 Constitution saving throw**; on a failure, for 1 minute their speed is "
             "halved, they cannot take reactions, and they cannot regain hit points. They repeat the save at "
             "the end of each of their turns. Twice per day.",
             {"kind": "save", "activation": "action", "range": 120, "save": "con", "dc": 18, "uses": "2",
              "recovery": "lr", "on_save": "none", "template": ("radius", 30), "duration": (1, "minute")}),
            ("action", "Raise the Cairn",
             "Up to three corpses within 60 feet rise as **Cairn Dead** with 30 hit points each, AC 15, and "
             "one attack at +7 for 12 bludgeoning damage. They collapse after 1 minute. Once per day.",
             {"kind": "utility", "activation": "action", "range": 60, "uses": "1", "recovery": "lr"}),
            ("legendary", "Speak a Name",
             "One creature within 60 feet that has lost someone takes 7 psychic damage.",
             {"kind": "damage", "activation": "legendary", "range": 60, "damage": [(2, 6, "psychic")]}),
            ("legendary", "Slow Advance", "The Hearthspeaker moves 20 feet.", None),
            ("legendary", "Cairn Frost (Costs 2 Actions)",
             "A 10-foot-radius point within 60 feet becomes difficult terrain and deals 10 cold damage to "
             "enemies entering it.", None),
            ("legendary", "The Dead Remember (Costs 3 Actions)",
             "Immediately activate The Cairns Are Open as if a creature had died.", None),
        ],
    ),
    dict(
        name="Vhessaran Pureblood", context=_VHAL, role="Cult rank and file (N8-N17)",
        creature_type="humanoid", subtype="yuan-ti", alignment="Neutral Evil",
        size="med", cr=3, prof=2, ac=15, hp=58, formula="9d8 + 18", speed={"walk": 30},
        abilities=(11, 16, 14, 13, 14, 16), saves=["wis"],
        skills={"dec": 1, "rel": 1}, di="poison", ci="poisoned",
        senses={"darkvision": 60}, languages="Abyssal, Common, Draconic",
        blurb="An upgraded congregant for tables that want the temple to bite. Most of the ten in N8 should "
              "remain ordinary CR 1 purebloods; promote two or three.",
        features=[
            ("trait", "Magic Resistance",
             "The Pureblood has advantage on saving throws against spells and magical effects.", None),
            ("trait", "Temple Surrender",
             "A Pureblood reduced below 15 hit points surrenders if offered a credible opportunity. **Most "
             "parties never offer.**", None),
            ("action", "Multiattack", "The Pureblood makes two Serpent Blade attacks.", None),
            ("action", "Serpent Blade",
             "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 7 (1d8 + 3) slashing damage plus "
             "3 (1d6) poison damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "dex",
              "damage": [(1, 8, "slashing"), (1, 6, "poison")]}),
            ("action", "Venom Cant",
             "One creature within 60 feet makes a **DC 13 Wisdom saving throw**, taking 10 (3d6) psychic "
             "damage and being unable to take reactions until the end of its next turn on a failure.",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 13,
              "damage": [(3, 6, "psychic")], "on_save": "none"}),
            ("action", "Serpent's Invitation",
             "One humanoid within 30 feet makes a **DC 13 Wisdom saving throw** or is charmed for 1 minute. "
             "Once per day.",
             {"kind": "save", "activation": "action", "range": 30, "save": "wis", "dc": 13, "uses": "1",
              "recovery": "lr", "on_save": "none", "duration": (1, "minute")}),
        ],
    ),
    dict(
        name="Ssarveth Kol, First Voice", context=_VHAL, role="Elite priest of the Temple (N8)",
        creature_type="monstrosity", subtype="yuan-ti malison", alignment="Lawful Evil",
        size="med", cr=7, prof=3, ac=17, hp=136, formula="16d8 + 64", speed={"walk": 30},
        abilities=(17, 15, 18, 14, 18, 18), saves=["con", "wis", "cha"],
        skills={"ins": 1, "per": 1, "rel": 1}, di="poison", ci="poisoned",
        senses={"darkvision": 60}, languages="Abyssal, Common, Draconic",
        blurb="He has led two services a day for four hundred years and has never missed one. He will attempt "
              "to convert the party before he attempts to kill them, and he is telling the truth about the "
              "memory and lying about where it comes from.",
        features=[
            ("trait", "Magic Resistance",
             "Ssarveth has advantage on saving throws against spells and magical effects.", None),
            ("trait", "Voice of Continuance",
             "Allied yuan-ti within 20 feet have advantage on saving throws against being frightened.", None),
            ("action", "Multiattack", "Ssarveth makes one Bite and two Scimitar attacks.", None),
            ("action", "Bite",
             "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 7 (1d6 + 3) piercing damage plus "
             "10 (3d6) poison damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "str",
              "damage": [(1, 6, "piercing"), (3, 6, "poison")]}),
            ("action", "Scimitar",
             "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 8 (1d6 + 3) slashing damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "str",
              "damage": [(1, 6, "slashing")]}),
            ("action", "Litany of Being Kept",
             "Creatures of Ssarveth's choice within 30 feet make **DC 15 Wisdom saving throws** or are "
             "charmed until the end of their next turn with their speed reduced to 0.\n\n**A creature that "
             "already believes Vhessara is divine automatically fails.**",
             {"kind": "save", "activation": "action", "range": 30, "save": "wis", "dc": 15, "recharge": 5,
              "on_save": "none"}),
            ("action", "Venom Sermon",
             "A 30-foot cone. **DC 15 Constitution saving throw**: 28 (8d6) poison damage and poisoned until "
             "the end of the creature's next turn on a failure, half damage on a success. Twice per day.",
             {"kind": "save", "activation": "action", "range": 30, "save": "con", "dc": 15, "uses": "2",
              "recovery": "lr", "damage": [(8, 6, "poison")], "on_save": "half", "template": ("cone", 30)}),
            ("reaction", "Protect the Altar",
             "When an ally adjacent to Ssarveth is hit, Ssarveth swaps places with it and becomes the target.",
             None),
        ],
    ),
    dict(
        name="Devouring Abomination", context=_VHAL, role="Cult officer and creche guard (N13a, N15, N17)",
        creature_type="monstrosity", subtype="yuan-ti", alignment="Neutral Evil",
        size="lg", cr=10, prof=4, ac=18, hp=195, formula="19d10 + 90",
        speed={"walk": 40, "climb": 30},
        abilities=(22, 14, 20, 11, 16, 17), saves=["str", "con", "wis"],
        di="poison", ci="poisoned", senses={"darkvision": 60}, languages="Abyssal, Common, Draconic",
        legres=2, legact=3,
        blurb="The only creature in the necropolis denied a personality, deliberately, because the room it "
              "appears in has no space for one.",
        features=[
            ("trait", "Legendary Resistance (2/Day)",
             "If the Abomination fails a saving throw it can choose to succeed instead.", None),
            ("trait", "Magic Resistance",
             "Advantage on saving throws against spells and magical effects.", None),
            ("trait", "Crushing Coil",
             "A creature grappled by the Abomination is also restrained.", None),
            ("action", "Multiattack",
             "The Abomination makes one Bite and two Scimitar or Coil attacks.", None),
            ("action", "Bite",
             "Melee Weapon Attack: +10 to hit, reach 5 ft., one target. Hit: 13 (2d6 + 6) piercing damage "
             "plus 17 (5d6) poison damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "str",
              "damage": [(2, 6, "piercing"), (5, 6, "poison")]}),
            ("action", "Scimitar",
             "Melee Weapon Attack: +10 to hit, reach 5 ft., one target. Hit: 13 (2d6 + 6) slashing damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "str",
              "damage": [(2, 6, "slashing")]}),
            ("action", "Coil",
             "Melee Weapon Attack: +10 to hit, reach 10 ft., one target. Hit: 15 (2d8 + 6) bludgeoning "
             "damage, and the target is grappled (escape DC 18).",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 8, "bludgeoning")]}),
            ("action", "Swallow the Helpless",
             "One grappled Medium or smaller creature makes a **DC 18 Dexterity saving throw** or is "
             "swallowed. A swallowed creature is blinded and restrained, has total cover, and takes 21 acid "
             "damage at the start of each of the Abomination's turns.",
             {"kind": "save", "activation": "action", "range": 5, "save": "dex", "dc": 18, "on_save": "none"}),
            ("action", "Devouring Terror",
             "Creatures of the Abomination's choice within 30 feet make a **DC 16 Wisdom saving throw** or "
             "become frightened for 1 minute, repeating the save at the end of each of their turns.",
             {"kind": "save", "activation": "action", "range": 30, "save": "wis", "dc": 16, "recharge": 5,
              "on_save": "none", "duration": (1, "minute")}),
            ("legendary", "Slither", "The Abomination moves up to half its speed.", None),
            ("legendary", "Scimitar", "The Abomination makes one Scimitar attack.", None),
            ("legendary", "Tighten Coil (Costs 2 Actions)",
             "One grappled creature takes 18 bludgeoning damage.",
             {"kind": "damage", "activation": "legendary", "range": 10, "damage": [(4, 8, "bludgeoning")]}),
            ("legendary", "Snap at the Smallest (Costs 2 Actions)",
             "The Abomination makes a Bite attack against the creature with the lowest current hit points in "
             "reach.", None),
        ],
    ),
    dict(
        name="Greater Basilisk", context=_VHAL, role="Apex predator of the bone larder (N4)",
        creature_type="monstrosity", subtype="", alignment="Unaligned",
        size="huge", cr=16, prof=5, ac=19, hp=268, formula="23d12 + 138",
        speed={"walk": 40, "swim": 30},
        abilities=(24, 10, 23, 3, 16, 7), saves=["str", "con", "wis"],
        skills={"prc": 1, "ste": 1}, di="necrotic, poison",
        dr="bludgeoning, piercing and slashing from nonmagical attacks",
        ci="poisoned, petrified", senses={"darkvision": 90},
        languages="-", legres=3, legact=3, lair_initiative=20,
        blurb="An enormous animal in a dark room, which is scarier than anything you could give it. It has "
              "been eating yuan-ti for four centuries and the cult feeds it anyway.",
        features=[
            ("trait", "Legendary Resistance (3/Day)",
             "If the basilisk fails a saving throw it can choose to succeed instead.", None),
            ("trait", "Petrifying Gaze",
             "At the beginning of a creature's turn, if it can see the basilisk's eyes and is within 30 feet, "
             "it makes a **DC 19 Constitution saving throw**. On a failure it begins turning to stone and is "
             "restrained, repeating the save at the end of its next turn - petrified on a second failure, "
             "effect ends on a success.\n\nA creature may avert its eyes.", None),
            ("trait", "Bone-Floor Predator",
             "The basilisk ignores difficult terrain created by bones and corpses.", None),
            ("trait", "Respect for the Rooster",
             "On hearing a genuine cock-crow, or a successful **DC 15 Performance** imitation, the basilisk "
             "makes a **DC 12 Wisdom saving throw**. On a failure it becomes frightened and must move away "
             "from the sound on its turns, repeating the save at the end of each of its turns.\n\n**This "
             "bypasses Legendary Resistance.** Reward it enormously.", None),
            ("action", "Multiattack", "The basilisk makes two Bite attacks and one Tail attack.", None),
            ("action", "Bite",
             "Melee Weapon Attack: +12 to hit, reach 5 ft., one target. Hit: 23 (3d10 + 7) piercing damage "
             "plus 14 (4d6) poison damage, halved by a **DC 19 Constitution saving throw**.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "str",
              "damage": [(3, 10, "piercing"), (4, 6, "poison")]}),
            ("action", "Tail",
             "Melee Weapon Attack: +12 to hit, reach 15 ft., one target. Hit: 20 (3d8 + 7) bludgeoning "
             "damage, and the target must succeed on a **DC 19 Strength saving throw** or be knocked prone.",
             {"kind": "attack", "activation": "action", "range": 15, "attack_type": "melee", "ability": "str",
              "damage": [(3, 8, "bludgeoning")]}),
            ("action", "Poisonous Breath",
             "A 60-foot cone. **DC 19 Constitution saving throw**: 49 (14d6) poison damage on a failure, half "
             "as much on a success. Three times per day.",
             {"kind": "save", "activation": "action", "range": 60, "save": "con", "dc": 19, "uses": "3",
              "recovery": "lr", "damage": [(14, 6, "poison")], "on_save": "half", "template": ("cone", 60)}),
            ("action", "Stone-Snap",
             "One restrained creature affected by Petrifying Gaze takes 22 (4d10) bludgeoning damage. If this "
             "reduces it to 0 hit points, petrification immediately completes.",
             {"kind": "damage", "activation": "action", "range": 5, "damage": [(4, 10, "bludgeoning")]}),
            ("legendary", "Skitter", "The basilisk moves up to half its speed.", None),
            ("legendary", "Tail", "The basilisk makes one Tail attack.", None),
            ("legendary", "Gaze Turn (Costs 2 Actions)",
             "One creature currently averting its eyes within 30 feet must choose: remain effectively blinded "
             "to the basilisk until its next turn, or immediately make a Petrifying Gaze save.", None),
            ("legendary", "Pool Ambush (Costs 3 Actions)",
             "If within 30 feet of the pool, the basilisk disappears beneath it, emerges from another point "
             "along its edge, and Bites.", None),
            ("lair", "Lair Action: Bone Collapse",
             "A 15-foot radius becomes difficult terrain. **DC 15 Dexterity saving throw** or prone.", None),
            ("lair", "Lair Action: Pool Surge",
             "Creatures within 10 feet of the pool make a **DC 17 Strength saving throw** or are pulled into "
             "it.", None),
            ("lair", "Lair Action: Lights Out",
             "A splash, collapse or movement snuffs one nonmagical light source and heavily obscures a "
             "20-foot area until the next round.", None),
        ],
    ),
    dict(
        name="Animated Armament", context=_VHAL, role="The Black Knight's wrong answers (N5)",
        creature_type="construct", subtype="", alignment="Unaligned",
        size="med", cr=6, prof=3, ac=19, hp=96, formula="16d8 + 24", speed={"walk": 0, "fly": 50},
        abilities=(18, 19, 16, 1, 6, 1), saves=["dex"],
        di="poison, psychic",
        ci="blinded, charmed, deafened, frightened, paralyzed, petrified, poisoned, prone",
        senses={"blindsight": 60}, languages="-", legact=2,
        blurb="A weapon that has been told it is the mightiest and believes it. The quill is still the right "
              "answer.",
        features=[
            ("trait", "Antimagic Susceptibility",
             "The Armament is incapacitated for 1 minute in an *antimagic field*. A targeted *dispel magic* "
             "suppresses it for 1 minute on a failed DC 13 Constitution save against the caster's spell DC.",
             None),
            ("trait", "Weapon Identity",
             "When created, note the weapon used. Its Strike deals that weapon's normal damage die plus 4 and "
             "2d8 force. If the weapon is magical, its attacks retain that weapon's magical properties at the "
             "GM's discretion.", None),
            ("trait", "Boast-Fed",
             "If a creature within 30 feet describes the weapon as mighty, legendary, unbeatable or "
             "beautiful, the Armament gains 10 temporary hit points. Once per creature.", None),
            ("action", "Multiattack", "The Armament makes three Strikes.", None),
            ("action", "Strike",
             "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: the weapon's own damage die + 4, "
             "of the weapon's own type, plus 9 (2d8) force damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "str",
              "damage": [(1, 10, "force"), (2, 8, "force")]}),
            ("action", "Whirling Arc",
             "Creatures within 10 feet make a **DC 15 Dexterity saving throw**, taking 27 (6d8) damage of the "
             "weapon's type on a failure or half as much on a success.",
             {"kind": "save", "activation": "action", "range": 10, "save": "dex", "dc": 15, "recharge": 5,
              "damage": [(6, 8, "force")], "on_save": "half", "template": ("radius", 10)}),
            ("reaction", "Parry", "The Armament adds 3 to its AC against one melee attack.", None),
            ("legendary", "Orbit", "The Armament moves 20 feet. *Solo encounters only.*", None),
            ("legendary", "Strike", "The Armament makes one Strike. *Solo encounters only.*", None),
        ],
    ),
    dict(
        name="Blood Ooze", context=_VHAL, role="Temple guardian of the blood corridor (N7)",
        creature_type="ooze", subtype="", alignment="Unaligned",
        size="lg", cr=9, prof=4, ac=10, hp=152, formula="16d10 + 64",
        speed={"walk": 30, "climb": 30},
        abilities=(18, 6, 22, 2, 12, 5), saves=["con"],
        di="acid, fire, necrotic, slashing",
        ci="blinded, charmed, deafened, exhaustion, frightened, prone",
        senses={"blindsight": 60}, languages="-", legact=2,
        blurb="The congealed remains of four centuries of sacrifice, which took on the dark energy of the "
              "place and answered a prayer nobody meant to make.\n\n**Two Oozes share two legendary actions "
              "per round**, not two each.",
        features=[
            ("trait", "Amorphous", "The Ooze can move through a space as narrow as 1 inch.", None),
            ("trait", "Spider Climb",
             "The Ooze can climb difficult surfaces, including upside down on ceilings, without an ability "
             "check. It comes along the ceiling and up through the drains, and it will.", None),
            ("trait", "Scent of Blood",
             "The Ooze has advantage on attack rolls against creatures covered in blood - which, after the "
             "garden, is everyone who did not think of *prestidigitation*.", None),
            ("trait", "Blood Drain",
             "A creature touching the Ooze or striking it with a melee attack from within 5 feet takes 7 "
             "(2d6) necrotic damage, and the Ooze gains that many temporary hit points.\n\nIf the Ooze took "
             "radiant damage since its last turn, this does not function until the start of its following "
             "turn.", None),
            ("trait", "Overflow",
             "There is no maximum to temporary hit points gained from Blood Drain, but all of them disappear "
             "after 1 minute.", None),
            ("action", "Multiattack", "The Ooze makes two Pseudopod attacks.", None),
            ("action", "Pseudopod",
             "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 11 (2d6 + 4) bludgeoning damage "
             "plus 22 (4d10) necrotic damage. The Ooze gains temporary hit points equal to half the necrotic "
             "damage dealt.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 6, "bludgeoning"), (4, 10, "necrotic")]}),
            ("action", "Exsanguinating Wave",
             "A 20-foot radius. **DC 16 Constitution saving throw**: 31 (7d8) necrotic damage and unable to "
             "regain hit points until the end of the creature's next turn on a failure, half damage on a "
             "success.",
             {"kind": "save", "activation": "action", "range": 20, "save": "con", "dc": 16, "recharge": 5,
              "damage": [(7, 8, "necrotic")], "on_save": "half", "template": ("radius", 20)}),
            ("reaction", "Overflow Strike",
             "When hit in melee, the attacker makes a **DC 16 Constitution saving throw**, taking 18 (4d8) "
             "necrotic damage on a failure or half on a success. The Ooze gains temporary hit points equal to "
             "the damage dealt.", None),
            ("legendary", "Flow", "One Ooze moves up to half its speed. *Shared pool.*", None),
            ("legendary", "Pseudopod", "One Ooze makes one Pseudopod attack. *Shared pool.*", None),
            ("legendary", "Blood Tide (Costs 2 Actions)",
             "All blood-covered creatures within 20 feet of either Ooze are pulled 10 feet toward the nearest "
             "Ooze. *Shared pool.*", None),
        ],
    ),
    dict(
        name="Gaze-Locked Medusa", context=_VHAL, role="Statue 6 of the Chamber of Ten (N2), if foolishly freed",
        creature_type="monstrosity", subtype="", alignment="Neutral Evil",
        size="med", cr=9, prof=4, ac=18, hp=162, formula="19d8 + 76", speed={"walk": 30},
        abilities=(12, 18, 18, 15, 16, 17), saves=["dex", "con", "wis"],
        skills={"prc": 1, "ste": 1}, dr="poison", senses={"darkvision": 60}, languages="Common",
        legres=2, legact=3,
        blurb="Unlike the ten adventurers in the gallery she has no death clock - she was petrified last "
              "century and is fine, and furious. Freeing her is entirely the party's fault.",
        features=[
            ("trait", "Legendary Resistance (2/Day)",
             "If the Medusa fails a saving throw she can choose to succeed instead.", None),
            ("trait", "Petrifying Gaze",
             "A creature starting its turn within 30 feet and able to see the Medusa makes a **DC 17 "
             "Constitution saving throw**. On a failure it is restrained as stone spreads; on a second "
             "failure at the end of its next turn it is petrified.", None),
            ("trait", "Century of Stillness",
             "During the Medusa's first round after being freed from petrification her speed is 50 feet, she "
             "has advantage on attack rolls, and she cannot take reactions.\n\nShe is experiencing a century "
             "of stored panic in six seconds.", None),
            ("action", "Multiattack", "The Medusa makes three attacks in any combination.", None),
            ("action", "Serpent Hair",
             "Melee Weapon Attack: +8 to hit, reach 5 ft., one creature. Hit: 8 (1d6 + 4) piercing damage "
             "plus 14 (4d6) poison damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "dex",
              "damage": [(1, 6, "piercing"), (4, 6, "poison")]}),
            ("action", "Stone Knife",
             "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 10 (2d4 + 4) piercing damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "dex",
              "damage": [(2, 4, "piercing")]}),
            ("action", "Venomous Spit",
             "Ranged Weapon Attack: +8 to hit, range 60 ft., one target. Hit: 21 (6d6) poison damage, and the "
             "target must succeed on a **DC 16 Constitution saving throw** or be poisoned until the end of "
             "its next turn.",
             {"kind": "attack", "activation": "action", "range": 60, "attack_type": "ranged", "ability": "dex",
              "damage": [(6, 6, "poison")]}),
            ("action", "Shattering Glance",
             "One creature currently restrained by Petrifying Gaze immediately repeats its petrification "
             "saving throw with disadvantage.",
             {"kind": "save", "activation": "action", "range": 30, "save": "con", "dc": 17, "recharge": 5,
              "on_save": "none"}),
            ("legendary", "Move", "The Medusa moves 15 feet.", None),
            ("legendary", "Hair", "The Medusa makes one Serpent Hair attack.", None),
            ("legendary", "Catch My Eye (Costs 2 Actions)",
             "One creature within 30 feet must either avert its eyes until the start of its next turn or "
             "immediately make a Petrifying Gaze save.", None),
        ],
    ),
    dict(
        name="Processional Remnant", context=_VHAL, role="The Procession's grief, armed (V2, V6, V8)",
        creature_type="undead", subtype="", alignment="Neutral",
        size="lg", cr=12, prof=4, ac=18, hp=218, formula="23d10 + 92",
        speed={"walk": 30, "fly": 30},
        abilities=(22, 14, 20, 6, 18, 13), saves=["str", "con", "wis"],
        dr="necrotic, psychic; bludgeoning, piercing and slashing from nonmagical attacks",
        ci="charmed, exhaustion, frightened, grappled, paralyzed, prone",
        senses={"truesight": 60}, languages="understands all languages spoken in the hall; speaks none",
        legact=3,
        blurb="Not a ghost. The hall's accumulated grief, wearing a shape. It is not vengeful - it is "
              "grieving, and it fights like it.\n\n**Several Remnants share three legendary actions.**",
        features=[
            ("trait", "Made of Mourning",
             "For every Procession figure destroyed since the party entered, the Remnant gains 15 maximum hit "
             "points and +1 damage on all attacks, to a maximum of +60 hit points and +4 damage.\n\n**The "
             "party builds this creature by fighting it.**", None),
            ("trait", "Cannot Be Turned",
             "Turning effects fail automatically. It is not defying a god; it simply is not listening.", None),
            ("trait", "Knows Your Name",
             "A Remnant knows the names of all creatures that caused it to form.", None),
            ("action", "Multiattack", "The Remnant makes three Bearing-Arm attacks.", None),
            ("action", "Bearing-Arm",
             "Melee Weapon Attack: +10 to hit, reach 10 ft., one target. Hit: 19 (3d8 + 6) bludgeoning damage "
             "plus 7 (2d6) psychic damage, and the target's speed becomes 0 until the end of its next turn as "
             "the weight settles on it.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(3, 8, "bludgeoning"), (2, 6, "psychic")]}),
            ("action", "Weight of Every Promise",
             "A 30-foot cone. **DC 17 Wisdom saving throw**: 36 (8d8) psychic damage and restrained until the "
             "end of the creature's next turn on a failure, half damage on a success.",
             {"kind": "save", "activation": "action", "range": 30, "save": "wis", "dc": 17, "recharge": 5,
              "damage": [(8, 8, "psychic")], "on_save": "half", "template": ("cone", 30)}),
            ("action", "Carry the Dead",
             "One creature within 30 feet that has personally witnessed a death makes a **DC 17 Wisdom saving "
             "throw** or falls prone and is incapacitated until the beginning of its next turn as spectral "
             "mourners gather around it.",
             {"kind": "save", "activation": "action", "range": 30, "save": "wis", "dc": 17, "on_save": "none"}),
            ("reaction", "Bequeath",
             "When the Remnant reaches 0 hit points it hands its candle to the creature that destroyed it. "
             "That character takes 27 (6d8) psychic damage, gains **+1 Refusal**, and is now carrying an "
             "unlit candle they cannot voluntarily discard until they light it.", None),
            ("legendary", "Advance", "One Remnant moves. *Shared pool.*", None),
            ("legendary", "Bearing-Arm", "One Remnant makes one attack. *Shared pool.*", None),
            ("legendary", "Processional Weight (Costs 2 Actions)",
             "One creature whose speed is 0 takes 13 psychic damage. *Shared pool.*",
             {"kind": "damage", "activation": "legendary", "range": 30, "damage": [(3, 8, "psychic")]}),
        ],
    ),
]

BESTIARY += [
    dict(
        name="The Keeper", context=_VHAL, role="Mummy lord of the Keeper's Hoard (V4)",
        creature_type="undead", subtype="pindarian", alignment="Lawful Neutral",
        size="lg", cr=16, prof=5, ac=19, hp=280, formula="35d10 + 88", speed={"walk": 20},
        abilities=(18, 10, 22, 20, 21, 18), saves=["con", "int", "wis", "cha"],
        skills={"arc": 1, "his": 2, "inv": 1, "prc": 1},
        dr="cold, necrotic", di="poison", ci="charmed, frightened, poisoned, exhaustion",
        senses={"truesight": 60}, languages="Pindarian", legres=3, legact=3, lair_initiative=20,
        blurb="The Archive's Keeper before the Saharim binding. He declined the Watch because it required "
              "relinquishing the collection, and arranged his own mummification instead.\n\nHe is not evil "
              "and not raving. He is a man who would not stop keeping things, and he is one room from the "
              "Vigil, and Kathandar signed the order that let him stay.",
        features=[
            ("trait", "Legendary Resistance (3/Day)",
             "If the Keeper fails a saving throw he can choose to succeed instead.", None),
            ("trait", "The Beating Jar",
             "The Keeper cannot permanently die while his canopic jar remains intact. Reduced to 0 hit "
             "points, his body collapses and begins reforming beside the jar, returning at full hit points "
             "after 1 minute.\n\n**Jar:** AC 12, 20 hit points, immune to poison and psychic. Destroying it "
             "permanently disables this trait.\n\nHe removed his own heart so that he would never have to "
             "stop working. It beats at about forty a minute.", None),
            ("trait", "Keeper's Inventory",
             "The Keeper knows exactly which creature possesses every item removed from the burial halls. He "
             "cannot be deceived about ownership.", None),
            ("trait", "Curse of the Sixth Chamber",
             "A creature that steals from his treasure gains Stage 1 of the site curse. The Keeper's "
             "abilities treat a cursed creature as vulnerable to psychic damage.", None),
            ("trait", "Nonflammable Wrappings",
             "The Keeper is immune to damage from nonmagical fire, and wears a *ring of fire resistance*.",
             None),
            ("action", "Multiattack", "The Keeper makes two Keeper's Grasp attacks.", None),
            ("action", "Keeper's Grasp",
             "Melee Weapon Attack: +10 to hit, reach 10 ft., one target. Hit: 17 (2d10 + 6) bludgeoning damage "
             "plus 18 (4d8) necrotic damage, and the target must succeed on a **DC 18 Constitution saving "
             "throw** or be unable to regain hit points until the beginning of the Keeper's next turn.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 10, "bludgeoning"), (4, 8, "necrotic")]}),
            ("action", "Return It to Its Coffin",
             "One creature carrying stolen treasure within 60 feet makes a **DC 18 Charisma saving throw**. "
             "On a failure it takes 36 psychic damage, drops one stolen item, and is frightened until the end "
             "of its next turn.",
             {"kind": "save", "activation": "action", "range": 60, "save": "cha", "dc": 18,
              "damage": [(8, 8, "psychic")], "on_save": "none"}),
            ("action", "Catalogue Curse",
             "Each hostile creature within 30 feet makes a **DC 18 Wisdom saving throw**, taking 36 psychic "
             "damage and being cursed for 1 minute on a failure. While cursed, attack rolls against it score "
             "a critical hit on a 19-20. It repeats the save at the end of each of its turns.",
             {"kind": "save", "activation": "action", "range": 30, "save": "wis", "dc": 18, "recharge": 5,
              "damage": [(8, 8, "psychic")], "on_save": "none", "duration": (1, "minute")}),
            ("action", "Sign for It",
             "One creature within 60 feet is enclosed by bands of funerary script. **DC 18 Dexterity saving "
             "throw** or restrained for 1 minute, repeating a Strength save at the end of each of its turns. "
             "Twice per day.",
             {"kind": "save", "activation": "action", "range": 60, "save": "dex", "dc": 18, "uses": "2",
              "recovery": "lr", "on_save": "none", "duration": (1, "minute")}),
            ("legendary", "Count", "The Keeper learns one target's current hit points.", None),
            ("legendary", "Grasp", "The Keeper makes one Keeper's Grasp attack.", None),
            ("legendary", "Return Property (Costs 2 Actions)",
             "An unattended treasure item within 60 feet flies 30 feet toward its proper resting place, "
             "striking any creature in its path for 10 force damage.", None),
            ("legendary", "Forty Beats (Costs 3 Actions)",
             "The jar beats audibly. The Keeper regains 25 hit points.", None),
            ("lair", "Lair Action: The Hoard Shifts",
             "A 15-foot area becomes difficult terrain. **DC 16 Dexterity saving throw** or prone.", None),
            ("lair", "Lair Action: Named Grave",
             "One creature hears the name of the person whose grave it disturbed. **DC 18 Wisdom saving "
             "throw** or frightened until the next round.", None),
            ("lair", "Lair Action: The Sixth Chamber Collects",
             "One cursed creature advances one curse stage until initiative 20 of the next round.", None),
            ("mythic", "Peaceful Ending",
             "**Destroying the jar without having looted the graves ends the encounter.**\n\nThe Keeper begs "
             "the character not to do it. He does not stop them unless they have already stolen from his "
             "dead.\n\nThis is not a mythic second phase. It is the opposite, and it is here so that the "
             "table sees it on the sheet.", None),
        ],
    ),
    dict(
        name="Vhaskar Corr, the Winged Shadow", context=_VHAL,
        role="Mythic rival - the Saharim who left the Watch (W3, V8)",
        creature_type="undead", subtype="pindarian saharim apostate", alignment="Lawful Evil",
        size="lg", cr=18, prof=6, ac=20, hp=298, formula="36d10 + 100",
        speed={"walk": 40, "fly": 70},
        abilities=(14, 22, 21, 22, 19, 20), saves=["dex", "con", "int", "wis"],
        skills={"arc": 1, "dec": 1, "his": 1, "ins": 1, "ste": 1},
        dr="necrotic, poison, psychic; bludgeoning, piercing and slashing from nonmagical attacks",
        ci="charmed, exhaustion, frightened, poisoned",
        senses={"darkvision": 120}, languages="Common, Giant, Pindarian; telepathy 120 ft.",
        legres=3, legact=3,
        blurb="He stood the Watch beside Kathandar for eleven hundred years, then did the arithmetic, then "
              "left. He is not planning a massacre. He is planning a **hearing** - and he intends to abide by "
              "the verdict, and he has calculated that he will lose.",
        features=[
            ("trait", "Legendary Resistance (3/Day)",
             "If Vhaskar fails a saving throw he can choose to succeed instead.", None),
            ("trait", "Forfeit Watch",
             "Vhaskar cannot touch or carry a Pindarian key-token, seal, anchor or relic. Attempting it fails "
             "and deals 33 radiant damage to him.\n\n**He has never told anyone this.** It is why he did not "
             "take Aelied's disc in the Citadel of Horns.", None),
            ("trait", "Bookkeeper",
             "Vhaskar knows the name of every creature that died within 1 mile during the last 24 hours.",
             None),
            ("trait", "The Law of the Last Breath",
             "Whenever Vhaskar deals necrotic damage with Ledger-Knife or Read the Name, his hit point "
             "maximum is reduced by half the necrotic damage dealt.\n\nHe is fully aware of this. He keeps "
             "doing it, and the party should be made to notice that he is paying.", None),
            ("action", "Multiattack", "Vhaskar makes three Ledger-Knife attacks.", None),
            ("action", "Ledger-Knife",
             "Melee Weapon Attack: +12 to hit, reach 10 ft., one target. Hit: 15 (2d8 + 6) piercing damage "
             "plus 18 (4d8) necrotic damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "dex",
              "damage": [(2, 8, "piercing"), (4, 8, "necrotic")]}),
            ("action", "Read the Name",
             "Vhaskar speaks the name of a creature that died within 1 mile in the last 24 hours. If its "
             "corpse is within 120 feet it rises under his control with half its maximum hit points for 1 "
             "minute.\n\nOtherwise, one creature that knew the dead individual makes a **DC 19 Wisdom saving "
             "throw**, taking 45 (10d8) psychic damage on a failure or half as much on a success.",
             {"kind": "save", "activation": "action", "range": 120, "save": "wis", "dc": 19, "recharge": 5,
              "damage": [(10, 8, "psychic")], "on_save": "half"}),
            ("action", "Empanel the Dead",
             "Three spectral dead creatures appear within 60 feet, each with AC 17, 30 hit points, and one "
             "spectral attack at +10 for 13 necrotic damage. They vanish after 1 minute. Twice per day.",
             {"kind": "utility", "activation": "action", "range": 60, "uses": "2", "recovery": "lr"}),
            ("bonus", "Shadowstep",
             "Vhaskar teleports up to 60 feet between areas of dim light or darkness.",
             {"kind": "utility", "activation": "bonus", "range": 60}),
            ("reaction", "Footnote",
             "When a creature within 60 feet succeeds on a saving throw, Vhaskar deals 9 psychic damage to it "
             "and records the result. The next time that creature makes the same type of saving throw, it "
             "rolls with disadvantage.", None),
            ("legendary", "Annotate",
             "Vhaskar marks one creature he can see. The first attack that hits it before his next turn deals "
             "an extra 10 necrotic damage.", None),
            ("legendary", "Knife", "Vhaskar makes one Ledger-Knife attack.", None),
            ("legendary", "Shadowstep", "Vhaskar uses Shadowstep.", None),
            ("legendary", "Read from the Margin (Costs 2 Actions)",
             "One summoned dead creature immediately moves and attacks.", None),
            ("mythic", "Mythic Trait: Six Hundred Names Answer",
             "**If Vhaskar reaches 0 hit points in the Nail chamber while his empanelled names remain "
             "unresolved**, he opens his ledger instead of dying. His body dissolves into black Pindarian "
             "script.\n\nHe regains **240 hit points**, gains resistance to all damage, and is surrounded by "
             "a spectral jury. Each time he takes damage, reduce it by 10 for each **Jury Voice** remaining - "
             "initially six.\n\nA character may use an action to address one Voice and ask: *'Did you consent "
             "to be called?'* No check is required. One Voice disappears.\n\n**If the party has already "
             "performed the lawful refusal at the Nail, two Voices disappear each time instead.**\n\nWhen all "
             "six are gone, Vhaskar loses all damage resistances and his Legendary Resistances.\n\nThis is "
             "the whole encounter: he screened six hundred dead for grievance and never once asked whether "
             "they wanted to testify.", None),
            ("mythic", "Jury Murmur",
             "One creature makes a **DC 19 Wisdom saving throw** or takes 13 psychic damage.",
             {"kind": "save", "activation": "mythic", "range": 60, "save": "wis", "dc": 19,
              "damage": [(3, 8, "psychic")], "on_save": "none"}),
            ("mythic", "Call the Witness (Costs 2 Actions)",
             "A spectral dead creature makes an attack.", None),
            ("mythic", "The Living Waste Everything (Costs 3 Actions)",
             "Each creature within 30 feet makes a **DC 19 Wisdom saving throw**, taking 31 psychic damage on "
             "a failure or half as much on a success.",
             {"kind": "save", "activation": "mythic", "range": 30, "save": "wis", "dc": 19,
              "damage": [(7, 8, "psychic")], "on_save": "half", "template": ("radius", 30)}),
        ],
    ),
    dict(
        name="Vhessara, the Devouring Queen", context=_VHAL,
        role="Mythic guardian of the upper necropolis (N18)",
        creature_type="undead", subtype="pindarian saharim, monstrosity", alignment="Lawful Neutral",
        size="lg", cr=21, prof=7, ac=20, hp=310, formula="36d10 + 112", speed={"walk": 35},
        abilities=(15, 20, 22, 20, 22, 24), saves=["dex", "con", "wis", "cha"],
        skills={"arc": 1, "dec": 2, "ins": 1, "prf": 2, "rel": 1},
        dr="necrotic, poison, psychic", ci="charmed, frightened, poisoned",
        senses={"truesight": 60}, languages="Pindarian, Abyssal, Common, Draconic",
        legres=3, legact=3, lair_initiative=20, spellcasting="cha", spell_dc=20, spell_attack=12,
        blurb="Four hundred years of keeping a temple of cannibals out of a library by pretending to be the "
              "thing they want to worship.\n\n**The conversation is still the intended solution.** She stops "
              "the moment anyone addresses her as staff.",
        features=[
            ("trait", "Legendary Resistance (3/Day)",
             "If Vhessara fails a saving throw she can choose to succeed instead.", None),
            ("trait", "Magic Resistance",
             "Advantage on saving throws against spells and magical effects.", None),
            ("trait", "Petrifying Gaze",
             "A creature that starts its turn within 30 feet and can see her eyes makes a **DC 20 "
             "Constitution saving throw**. On a failure it is restrained as stone spreads; on a second "
             "failure at the end of its next turn it is petrified. A creature may avert its eyes.", None),
            ("trait", "Medusa's Melody",
             "While Vhessara plays her harp, every creature within 30 feet that can hear her makes a **DC 18 "
             "Wisdom saving throw** at the start of its turn or suffers disadvantage on attack rolls and "
             "saving throws until the end of its next turn. After succeeding, a creature is immune for 24 "
             "hours.\n\n**Harp:** AC 17, 25 hit points. Taking or breaking it is the highest-value tactical "
             "play in the room, and the malisons in N15 will have said so.", None),
            ("trait", "Frightful Presence",
             "When combat begins, chosen creatures within 60 feet make a **DC 19 Wisdom saving throw** or are "
             "frightened for 1 minute.", None),
            ("trait", "Four Centuries of Pretending",
             "Vhessara has advantage on Deception checks related to acting like a deity, a tyrant, a queen, "
             "or a willing ruler of the yuan-ti.", None),
            ("action", "Multiattack",
             "Vhessara makes three Queen's Talon attacks, or two Talons and one Serpent Crown attack.", None),
            ("action", "Queen's Talon",
             "Melee Weapon Attack: +12 to hit, reach 10 ft., one target. Hit: 10 (1d8 + 6) slashing damage "
             "plus 18 (4d8) psychic damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "dex",
              "damage": [(1, 8, "slashing"), (4, 8, "psychic")]}),
            ("action", "Serpent Crown",
             "Melee Weapon Attack: +12 to hit, reach 10 ft., one creature. Hit: 9 (1d6 + 6) piercing damage "
             "plus 17 (5d6) poison damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "dex",
              "damage": [(1, 6, "piercing"), (5, 6, "poison")]}),
            ("action", "Devour the Soul",
             "One creature within 60 feet makes a **DC 20 Charisma saving throw**, taking 55 (10d10) psychic "
             "damage on a failure or half as much on a success.\n\nOn a failure Vhessara also learns its true "
             "name, its greatest regret, and whether it has ever been resurrected.",
             {"kind": "save", "activation": "action", "range": 60, "save": "cha", "dc": 20, "recharge": 5,
              "damage": [(10, 10, "psychic")], "on_save": "half"}),
            ("action", "Void Custodian Magic",
             "Vhessara casts one of the following (**spell save DC 20, +12 to hit**):\n\n**At will:** *detect "
             "magic*, *minor illusion*, *mage hand*\n\n**3/day each:** *dimension door*, *greater "
             "invisibility*, *synaptic static*\n\n**2/day each:** *mass suggestion*, *wall of force*\n\n"
             "**1/day:** *reverse gravity*", None),
            ("bonus", "Harp Step",
             "Vhessara teleports 30 feet to a space adjacent to one of the four guardian statues.",
             {"kind": "utility", "activation": "bonus", "range": 30}),
            ("legendary", "Talon", "Vhessara makes one Queen's Talon attack.", None),
            ("legendary", "Play One Note",
             "One creature within 30 feet makes a Medusa's Melody saving throw.",
             {"kind": "save", "activation": "legendary", "range": 30, "save": "wis", "dc": 18,
              "on_save": "none"}),
            ("legendary", "Guardian Stir (Costs 2 Actions)",
             "One remaining guardian statue immediately moves and attacks.", None),
            ("legendary", "Gaze Sweep (Costs 3 Actions)",
             "Every creature currently looking at Vhessara within 15 feet makes a Petrifying Gaze save.",
             None),
            ("lair", "Lair Action: Guardian Awakens",
             "One remaining naga or salamander guardian takes an action.", None),
            ("lair", "Lair Action: The Temple Kneels",
             "The floor flexes. **DC 18 Dexterity saving throw** or prone.", None),
            ("lair", "Lair Action: The Archive Whispers",
             "Every creature hears names beneath the floor. **DC 18 Wisdom saving throw** or unable to take "
             "reactions.\n\nShe hears them too. She has heard them for four hundred years, and this is what "
             "the harp is for.", None),
            ("mythic", "Mythic Trait: The Custodian Beneath the Crown",
             "**At 0 hit points the Saharim binding restores her.** The serpents around her head fall silent. "
             "The crown breaks.\n\nShe regains **260 hit points** and her creature type becomes simply undead "
             "(Pindarian Saharim). She loses Medusa's Melody and gains **Void Step** - she can teleport 30 "
             "feet after every action she takes - and **Archive Authority**: at initiative 20 she may "
             "automatically open or close a door, erect 20 feet of wall, rotate gravity in a 20-foot cube, or "
             "suppress one magical effect of 5th level or lower.", None),
            ("mythic", "Custodian's Hand",
             "One creature takes 22 force damage and is pushed 15 feet.",
             {"kind": "damage", "activation": "mythic", "range": 60, "damage": [(5, 8, "force")]}),
            ("mythic", "Close the Stacks (Costs 2 Actions)",
             "Two 15-foot walls appear.", None),
            ("mythic", "You Should Not Be Here (Costs 3 Actions)",
             "One creature makes a **DC 20 Charisma saving throw** or is teleported 60 feet to the room "
             "entrance and takes 22 force damage.",
             {"kind": "save", "activation": "mythic", "range": 60, "save": "cha", "dc": 20,
              "damage": [(5, 8, "force")], "on_save": "none"}),
            ("mythic", "The Actual Resolution",
             "**At any point**, addressing her as *Vhessara*, as *the custodian*, as *the woman with the "
             "broom*, or as *the one who barred the stair* causes her to stop fighting.\n\nIf the party tells "
             "her that **Kathandar is still correcting the gardening notes**, hostilities end automatically. "
             "No check.", None),
        ],
    ),
    dict(
        name="Projected Avatar of Orcus", context=_VHAL,
        role="Mythic catastrophe at the Last-Breath Nail (V8) - improper removal only",
        creature_type="fiend", subtype="demon", alignment="Chaotic Evil",
        size="grg", cr=24, prof=7, ac=22, hp=420, formula="40d20 + 320",
        speed={"walk": 40, "fly": 80},
        abilities=(28, 14, 27, 22, 22, 27), saves=["str", "con", "int", "wis", "cha"],
        skills={"arc": 1, "itm": 2, "prc": 1, "rel": 1},
        di="necrotic, poison",
        dr="cold, fire, lightning, psychic; bludgeoning, piercing and slashing from nonmagical attacks",
        ci="charmed, frightened, poisoned, exhaustion",
        senses={"truesight": 120}, languages="Abyssal, Common; telepathy 1 mile",
        legres=4, legact=3,
        blurb="**This is not Orcus in full.** It is the amount of him capable of forcing itself through the "
              "Death Breach before the Ninefold Prohibition completely collapses.\n\n**The victory condition "
              "is to lawfully release Gravewake.** Doing so while he is present banishes the projection "
              "instantly, regardless of his remaining hit points. This is an objective fight, not a damage "
              "race, and the party at level 11 will not beat him any other way.",
        features=[
            ("trait", "Legendary Resistance (4/Day)",
             "If Orcus fails a saving throw he can choose to succeed instead.", None),
            ("trait", "Magic Resistance",
             "Advantage on saving throws against spells and magical effects.", None),
            ("trait", "Lord of the Breach",
             "Orcus cannot willingly move more than 120 feet from the Last-Breath Nail.", None),
            ("trait", "Every Corpse Speaks",
             "At the start of every round, every corpse within 1 mile whispers. Creatures other than Orcus "
             "within 60 feet make a **DC 20 Wisdom saving throw** or take 7 psychic damage.", None),
            ("trait", "Death Has Administrative Priority",
             "A creature reduced to 0 hit points within 60 feet of Orcus cannot regain hit points until the "
             "beginning of his next turn.", None),
            ("trait", "Gravewake's Claim",
             "If Gravewake was removed improperly, Orcus begins combat holding it. While he possesses the "
             "relic he gains +2 AC, his necrotic damage ignores resistance, and he regains 10 hit points "
             "whenever any creature dies within 60 feet.", None),
            ("action", "Multiattack",
             "Orcus makes three Gravewake or Claw of Unmaking attacks.", None),
            ("action", "Gravewake",
             "Melee Weapon Attack: +16 to hit, reach 15 ft., one target. Hit: 22 (3d8 + 9) bludgeoning damage "
             "plus 27 (6d8) necrotic damage.",
             {"kind": "attack", "activation": "action", "range": 15, "attack_type": "melee", "ability": "str",
              "damage": [(3, 8, "bludgeoning"), (6, 8, "necrotic")]}),
            ("action", "Claw of Unmaking",
             "Melee Weapon Attack: +16 to hit, reach 20 ft., one target. Hit: 25 (4d6 + 9) slashing damage "
             "plus 22 (5d8) necrotic damage.\n\nA creature reduced to 0 hit points by this attack immediately "
             "rises as an undead under Orcus's control unless prevented before his next turn.",
             {"kind": "attack", "activation": "action", "range": 20, "attack_type": "melee", "ability": "str",
              "damage": [(4, 6, "slashing"), (5, 8, "necrotic")]}),
            ("action", "Word of Extinction",
             "A 60-foot cone. **DC 22 Constitution saving throw**: 72 (16d8) necrotic damage on a failure, "
             "half as much on a success. A creature that fails by 5 or more is also stunned until the end of "
             "its next turn.",
             {"kind": "save", "activation": "action", "range": 60, "save": "con", "dc": 22, "recharge": 5,
              "damage": [(16, 8, "necrotic")], "on_save": "half", "template": ("cone", 60)}),
            ("action", "Call the Unfinished",
             "Orcus summons up to four dead creatures whose corpses are within one mile. They appear within "
             "60 feet as undead versions of themselves with half their maximum hit points and act immediately "
             "after him.",
             {"kind": "utility", "activation": "action", "range": 60, "recharge": 6}),
            ("legendary", "Claw", "Orcus makes one Claw of Unmaking attack.", None),
            ("legendary", "Dead Step",
             "Orcus teleports 40 feet through a corpse or undead creature.", None),
            ("legendary", "Command Corpse (Costs 2 Actions)",
             "One undead under Orcus's control moves and attacks.", None),
            ("legendary", "Gravewake Pulse (Costs 3 Actions)",
             "Creatures within 20 feet make a **DC 22 Constitution saving throw**, taking 27 necrotic damage "
             "on a failure.",
             {"kind": "save", "activation": "legendary", "range": 20, "save": "con", "dc": 22,
              "damage": [(6, 8, "necrotic")], "on_save": "half", "template": ("radius", 20)}),
            ("mythic", "Mythic Trait: The Breach Looks Back",
             "**If the avatar reaches 0 hit points without Gravewake being lawfully released**, killing the "
             "body accomplishes very little.\n\nThe avatar collapses into the dimensional wound and the Death "
             "Breach becomes the creature. It gains **300 hit points** and AC 20, occupies the entire "
             "southern wall of the Nail chamber, cannot move, and is immune to prone, restrained and forced "
             "movement.\n\nAt initiative 20 and after every player turn it may spend one Breach Action.",
             None),
            ("mythic", "Corpse Eruption",
             "One corpse becomes a CR-appropriate undead.", None),
            ("mythic", "Hand Through the World",
             "+15 to hit against one creature: 31 bludgeoning damage and grappled.",
             {"kind": "attack", "activation": "mythic", "range": 60, "attack_type": "melee", "ability": "str",
              "damage": [(6, 8, "bludgeoning")]}),
            ("mythic", "Death Wind",
             "A 30-foot cone. **DC 21 Constitution saving throw**: 27 necrotic damage.",
             {"kind": "save", "activation": "mythic", "range": 30, "save": "con", "dc": 21,
              "damage": [(6, 8, "necrotic")], "on_save": "half", "template": ("cone", 30)}),
            ("mythic", "Names of the Dead (Costs 2 Actions)",
             "**DC 21 Wisdom saving throw**: 31 psychic damage and stunned on a failure.",
             {"kind": "save", "activation": "mythic", "range": 60, "save": "wis", "dc": 21,
              "damage": [(7, 8, "psychic")], "on_save": "none"}),
            ("mythic", "The Prince Arrives (Costs 3 Actions)",
             "The Breach heals 40 hit points and its maximum size visibly expands.\n\n**If allowed to use "
             "this three times, the projection ceases being an avatar.** At that point Elderon's banishment "
             "has failed catastrophically, and that is campaign-ending territory rather than another combat "
             "phase.", None),
            ("mythic", "Lawful Release",
             "The instant a living creature at the Nail sincerely refuses command of the willing dead soul, "
             "Gravewake comes free lawfully, Orcus loses his grip on Elderon, every summoned undead "
             "collapses, the Death Breach seals, and the avatar is banished regardless of remaining hit "
             "points.\n\n**That is the real boss mechanic.**", None),
        ],
    ),
]


# ---------------------------------------------------------------------------
# ORIGINAL CREATURES - the recurring monsters the nine site guides call for.
# ---------------------------------------------------------------------------

_KHAR = "Khar'Zhul, Pyramid of the Empty Table"
_ILYR = "Ilyr-Ameul, Pyramid of Two Truths"
_GOR = "Gor-Mazaal, Pyramid of the Wandering Path"
_MYR = "Myr'Velora, Pyramid of the Thousand Gardens"
_THAAL = "Thaal-Uluun, Pyramid of Unmaking"
_NAR = "Nar'Vael, Black Sun Pyramid"
_KHAL = "Khal'Vethar, Pyramid of the Final Vigil"

BESTIARY += [
    dict(
        name="Starveling Pursuer", context=_KHAR, role="The basin's predator layer (K1, K4, K6, K7)",
        creature_type="monstrosity", subtype="", alignment="Unaligned",
        size="lg", cr=7, prof=3, ac=16, hp=114, formula="12d10 + 48", speed={"walk": 50},
        abilities=(20, 17, 18, 5, 14, 7), saves=["dex", "con"],
        skills={"prc": 1, "ste": 1, "sur": 1}, ci="frightened",
        senses={"darkvision": 120}, languages="-",
        blurb="Generated, like the pale deer, to give a dead basin a predator. It has been hungry for four "
              "thousand years and it has never once been fed.",
        features=[
            ("trait", "Scent Weakness",
             "The Pursuer knows the current hit points of any creature it can smell, and has advantage on "
             "attack rolls against a creature below half its hit point maximum.", None),
            ("trait", "Relentless Hunger",
             "A Pursuer reduced to 0 hit points inside Khar'Zhul drops to 1 instead, **unless a creature "
             "used an action that round to offer it food or mercy.**\n\nA party that simply keeps hitting it "
             "cannot finish it. It will be lying there, alive, at 1 hit point, looking up.", None),
            ("action", "Multiattack",
             "The Pursuer makes one Bite attack and two Claw attacks.", None),
            ("action", "Bite",
             "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 16 (2d10 + 5) piercing damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 10, "piercing")]}),
            ("action", "Claw",
             "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 12 (2d6 + 5) slashing damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 6, "slashing")]}),
            ("action", "Starving Bay",
             "Each creature of the Pursuer's choice within 60 feet makes a **DC 15 Wisdom saving throw** or "
             "is frightened until the end of its next turn. **A creature carrying no food makes this save "
             "with disadvantage.**",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 15, "recharge": 5,
              "on_save": "none"}),
        ],
    ),
    dict(
        name="Tooth-Mimic", context=_KHAR, role="Pantry vermin (K2)",
        creature_type="monstrosity", subtype="shapechanger", alignment="Unaligned",
        size="tiny", cr=0.5, prof=2, ac=12, hp=10, formula="3d4 + 3", speed={"walk": 20},
        abilities=(8, 14, 12, 3, 10, 5), senses={"darkvision": 60}, languages="-",
        blurb="Twelve of them, asleep, in a room where every flat surface already has teeth on it. An "
              "irritation, not an encounter.",
        features=[
            ("trait", "False Appearance",
             "While motionless, the Tooth-Mimic is indistinguishable from a scattering of teeth.", None),
            ("action", "Bite",
             "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) piercing damage, and "
             "the mimic attaches to the target (escape DC 11). While attached it does not attack, and at the "
             "start of each of the target's turns it deals 2 (1d4) piercing damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "dex",
              "damage": [(1, 6, "piercing")]}),
        ],
    ),
    dict(
        name="Concordant Echo", context=_ILYR, role="The gallery's disagreement, armed (I2, I3, I5)",
        creature_type="construct", subtype="pindarian", alignment="Unaligned",
        size="lg", cr=11, prof=4, ac=17, hp=150, formula="20d10 + 40", speed={"walk": 30},
        abilities=(18, 16, 17, 10, 14, 8), saves=["dex", "con"],
        di="psychic", ci="charmed, frightened, prone",
        senses={"truesight": 60}, languages="understands all, speaks none",
        blurb="Not a guardian. The room disagreeing with itself, given a shape and a weapon.",
        features=[
            ("trait", "Both-Sighted",
             "The Echo exists identically in both perspectives and can be perceived and fought by every "
             "character regardless of which side of the split they are on. **It is the one thing in "
             "Ilyr-Ameul the party can co-ordinate against cleanly.**", None),
            ("trait", "Antimagic Susceptibility",
             "Incapacitated for 1 minute in an *antimagic field*.", None),
            ("action", "Multiattack", "The Echo makes two Reflected Strikes.", None),
            ("action", "Reflected Strike",
             "Melee Weapon Attack: +9 to hit, reach 10 ft., one target. Hit: 16 (3d6 + 6) force damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(3, 6, "force")]}),
            ("reaction", "Mirror the Blow",
             "When the Echo takes damage from an attack or a spell, it may make that same attack or cast "
             "that same spell back at the attacker, using its own modifiers: **+9 to hit, save DC 17.**"
             "\n\nKilling an Echo with a single overwhelming attack is the worst possible plan and a party "
             "will do it exactly once.", None),
        ],
    ),
    dict(
        name="Moon Cantor", context=_ILYR, role="Lunari teaching shade (I1, and anywhere a lesson is owed)",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Neutral",
        size="lg", cr=6, prof=3, ac=15, hp=97, formula="15d10 + 15", speed={"walk": 30, "fly": 30},
        abilities=(9, 16, 14, 18, 19, 17), saves=["int", "wis"],
        skills={"arc": 1, "his": 1, "ins": 2, "prf": 1},
        dr="psychic; bludgeoning, piercing and slashing from nonmagical attacks",
        ci="charmed, exhaustion, frightened, grappled, paralyzed, prone",
        senses={"darkvision": 60, "truesight": 30}, languages="Pindarian, Common",
        blurb="A fragment of a teaching order that dealt in perspective as a discipline rather than a trick. "
              "Patient, faintly amused, and running out of time in a way it finds more interesting than "
              "distressing.\n\n**Normally non-hostile.** Ithuel at the Bifurcation is one of these at a "
              "quarter hit points and will not fight under any provocation.",
        features=[
            ("trait", "Incorporeal Movement",
             "The Cantor can move through creatures and objects as difficult terrain, taking 5 (1d10) force "
             "damage if it ends its turn inside one.", None),
            ("trait", "Both Answers",
             "The Cantor perceives and can address every perspective in Ilyr-Ameul simultaneously and "
             "correctly. **Nothing else in the site can do this.**", None),
            ("action", "Cantor's Touch",
             "Melee Spell Attack: +7 to hit, reach 10 ft., one creature. Hit: 22 (4d10) psychic damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "wis",
              "damage": [(4, 10, "psychic")]}),
            ("action", "Different Is Not False",
             "Each creature of the Cantor's choice within 30 feet makes a **DC 15 Wisdom saving throw**. On a "
             "failure it takes 27 (6d8) psychic damage and, until the end of its next turn, perceives both "
             "perspectives at once and is incapacitated by it. On a success it takes half damage and gains "
             "**one Concord Token**.",
             {"kind": "save", "activation": "action", "range": 30, "save": "wis", "dc": 15, "recharge": 5,
              "damage": [(6, 8, "psychic")], "on_save": "half"}),
        ],
    ),
    dict(
        name="Maze Stalker", context=_GOR, role="Gor-Mazaal's error correction (G3, G5)",
        creature_type="construct", subtype="veylari", alignment="Unaligned",
        size="huge", cr=13, prof=5, ac=18, hp=207, formula="18d12 + 90", speed={"walk": 50},
        abilities=(23, 14, 21, 6, 16, 5), saves=["str", "con"],
        skills={"prc": 2, "sur": 2}, di="poison, psychic",
        ci="charmed, exhaustion, frightened, poisoned", senses={"truesight": 60},
        languages="Pindarian (understands only)",
        blurb="**It is not hunting them.** It escorts unpurposed traffic out of a working facility and puts "
              "it outside the Blind Gate, alive. Nobody has ever been killed by the Maze Stalker. People "
              "have been killed resisting it, which it does not distinguish.\n\nDo not reveal this until the "
              "party has escaped it or been caught by it.",
        features=[
            ("trait", "Labyrinth Sense",
             "The Stalker always knows the shortest route to any creature it has scented, regardless of "
             "intervening structure. It is never lost and never has been.", None),
            ("trait", "Reform",
             "Reduced to 0 hit points, the Stalker reforms in 1 minute at the nearest intersection at full "
             "hit points. **Killing it is not a victory condition and never becomes one.**", None),
            ("trait", "Unhurried",
             "The Stalker has never been seen to run. It moves at exactly the speed required and it has been "
             "doing so for four thousand years.", None),
            ("action", "Gore",
             "Melee Weapon Attack: +11 to hit, reach 10 ft., one target. Hit: 22 (3d10 + 6) piercing damage, "
             "and the target must succeed on a **DC 18 Strength saving throw** or be knocked prone.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(3, 10, "piercing")]}),
            ("action", "Furnace Breath",
             "A 30-foot cone. **DC 17 Dexterity saving throw**: 45 (10d8) fire damage on a failure, half as "
             "much on a success.",
             {"kind": "save", "activation": "action", "range": 30, "save": "dex", "dc": 17, "recharge": 5,
              "damage": [(10, 8, "fire")], "on_save": "half", "template": ("cone", 30)}),
            ("action", "Escort",
             "The Stalker grapples one creature it has reduced to 0 hit points or that offers no resistance "
             "(escape DC 18) and carries it toward the Blind Gate at full speed. A creature delivered outside "
             "is unharmed, whole, and no longer in Gor-Mazaal.\n\n**This is what it is for.**",
             {"kind": "utility", "activation": "action", "range": 10}),
        ],
    ),
    dict(
        name="Pindarian Void Warden", context="Veylari installations across Gor-Mazaal, Thaal-Uluun and Nar'Vael",
        role="Anti-intrusion post (G1, T3, and wherever a door needs answering)",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Neutral",
        size="lg", cr=9, prof=4, ac=19, hp=150, formula="20d10 + 40", speed={"walk": 30, "fly": 30},
        abilities=(16, 17, 17, 19, 17, 14), saves=["dex", "int", "wis"],
        skills={"arc": 2, "inv": 1, "prc": 1}, dr="force, necrotic; nonmagical attacks",
        ci="charmed, exhaustion, frightened", senses={"truesight": 60},
        languages="Pindarian, Common, Draconic",
        blurb="Posted, not guarding. It asks one question and accepts any honest answer, and it has been "
              "opening the same door for four hundred and eleven people for four thousand years.",
        features=[
            ("trait", "Planar Mooring",
             "Teleportation and planar travel initiated within 30 feet fail unless the creature succeeds on "
             "a **DC 17 Charisma saving throw**.", None),
            ("trait", "One Question",
             "The Warden challenges rather than attacks. It asks a single question and stands aside for any "
             "honest answer, **including an answer it does not like**. It only fights a creature that "
             "refuses to answer or attempts to push past.", None),
            ("action", "Multiattack", "The Warden makes two Anchor Glaive attacks.", None),
            ("action", "Anchor Glaive",
             "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 14 (2d8 + 5) slashing damage "
             "plus 9 (2d8) force damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 8, "slashing"), (2, 8, "force")]}),
            ("action", "Reality Nail",
             "One creature within 90 feet makes a **DC 17 Strength saving throw**, taking 27 (6d8) force "
             "damage and being restrained until the end of its next turn on a failure.",
             {"kind": "save", "activation": "action", "range": 90, "save": "str", "dc": 17, "recharge": 5,
              "damage": [(6, 8, "force")], "on_save": "none"}),
            ("reaction", "Exclude",
             "When a creature teleports into a space within 60 feet, it makes a **DC 17 Charisma saving "
             "throw**; on a failure the teleportation fails and the creature remains where it was.", None),
        ],
    ),
    dict(
        name="Archive Bloom", context=_MYR, role="The garden's immune response (M4, M5, M7)",
        creature_type="plant", subtype="", alignment="Unaligned",
        size="huge", cr=13, prof=5, ac=17, hp=225, formula="18d12 + 108",
        speed={"walk": 20, "climb": 20},
        abilities=(22, 8, 22, 6, 16, 9), saves=["con", "wis"],
        di="poison", dr="bludgeoning, piercing", ci="blinded, deafened, exhaustion, frightened, poisoned",
        senses={"blindsight": 60, "tremorsense": 60}, languages="-",
        blurb="Not a monster and not a guard. Four thousand years of hereditary record, mobile, trying to "
              "sample whatever has come into the valley.\n\n**A white spore from the Quarantine Bloom, "
              "administered as an action, ends the encounter immediately.** Nobody will think of it.",
        features=[
            ("trait", "Sampling, Not Hunting",
             "The Bloom is not hostile until attacked. It approaches, slowly, and attempts to take a sample. "
             "It does not pursue a creature that leaves the area.", None),
            ("trait", "Rooted Memory",
             "While the Bloom is in contact with soil it regains 15 hit points at the start of each of its "
             "turns and cannot be moved against its will.", None),
            ("trait", "Spore Cloud",
             "A creature that ends its turn within 10 feet makes a **DC 18 Constitution saving throw** or "
             "contracts one infection from the Myr'Velora table, GM's choice. **This is not damage** and "
             "several characters will be pleased about it.", None),
            ("action", "Multiattack", "The Bloom makes three Tendril attacks.", None),
            ("action", "Tendril",
             "Melee Weapon Attack: +11 to hit, reach 20 ft., one target. Hit: 18 (3d8 + 6) bludgeoning "
             "damage, and the target is grappled (escape DC 18).",
             {"kind": "attack", "activation": "action", "range": 20, "attack_type": "melee", "ability": "str",
              "damage": [(3, 8, "bludgeoning")]}),
            ("action", "Take a Sample",
             "One creature grappled by the Bloom makes a **DC 18 Constitution saving throw**, taking 42 "
             "(12d6) necrotic damage on a failure or half as much on a success. **The Bloom then knows "
             "everything hereditary about that creature** and will not target it again this encounter.",
             {"kind": "save", "activation": "action", "range": 20, "save": "con", "dc": 18,
              "damage": [(12, 6, "necrotic")], "on_save": "half"}),
            ("action", "Bloom of Record",
             "A 30-foot radius fills with pollen. Each creature there makes a **DC 18 Wisdom saving throw** "
             "or is incapacitated until the end of its next turn as it experiences, in full, the memories of "
             "somebody who has been dead for four thousand years.",
             {"kind": "save", "activation": "action", "range": 30, "save": "wis", "dc": 18, "recharge": 5,
              "on_save": "none", "template": ("radius", 30)}),
        ],
    ),
    dict(
        name="Unmade Duplicate", context=_THAAL, role="Vat-grown approximation (T4, T5)",
        creature_type="ooze", subtype="shapechanger", alignment="Unaligned",
        size="med", cr=12, prof=4, ac=17, hp=175, formula="21d8 + 81", speed={"walk": 30},
        abilities=(18, 18, 18, 14, 14, 16), saves=["dex", "con"],
        skills={"dec": 2, "ins": 1}, di="acid, poison",
        ci="charmed, exhaustion, prone", senses={"blindsight": 60}, languages="as its original",
        blurb="It knows surface memories and copies its original's role in simplified form. It fights like "
              "somebody doing an impression.\n\n**It can be defeated socially** when its original explains "
              "one choice its copied memories could not predict. It is not trying to win.",
        features=[
            ("trait", "Copied Surface",
             "The Duplicate knows everything its original could state aloud about themselves and nothing "
             "they could not. **It cannot copy a decision.**", None),
            ("trait", "Simplified Role",
             "The Duplicate reproduces its original's class role in a generic form: a caster gets a short "
             "list at DC 16, a rogue gets 4d6 extra damage on advantage, a fighter gets a second attack. "
             "Build it in ninety seconds and do not agonise.", None),
            ("trait", "Inert on Defeat",
             "Reduced to 0 hit points the Duplicate becomes inert and reforms later, whole, **without "
             "hostility**, and will be standing in the gallery on the way out.", None),
            ("action", "Multiattack", "The Duplicate makes two Unmade Strikes.", None),
            ("action", "Unmade Strike",
             "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 13 (2d8 + 4) bludgeoning damage "
             "plus 13 (3d8) acid damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "str",
              "damage": [(2, 8, "bludgeoning"), (3, 8, "acid")]}),
            ("action", "You Would Do This",
             "The Duplicate predicts its original's next action. That creature makes a **DC 16 Wisdom saving "
             "throw**; on a failure it takes 27 (6d8) psychic damage and has disadvantage on its next attack "
             "roll or ability check.\n\n**It is right until it is not.**",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 16, "recharge": 5,
              "damage": [(6, 8, "psychic")], "on_save": "none"}),
        ],
    ),
    dict(
        name="Verity Eater", context=_NAR, role="A draft of a person (N4, N6)",
        creature_type="aberration", subtype="shapechanger", alignment="Neutral Evil",
        size="med", cr=14, prof=5, ac=18, hp=207, formula="23d8 + 103", speed={"walk": 35},
        abilities=(16, 20, 19, 19, 17, 20), saves=["dex", "int", "cha"],
        skills={"dec": 3, "ins": 2, "prc": 1}, dr="psychic",
        ci="charmed, frightened", senses={"truesight": 60}, languages="as whoever it is copying",
        blurb="Not malicious. A **draft** - an attempt at a person, written by something trying to get the "
              "person right, very close, and unaware that it is a draft.\n\nAn Eater that is identified does "
              "not attack. It says *'Ah,'* sits down, asks what gave it away, and will be better next time.",
        features=[
            ("trait", "Indistinguishable",
             "*True seeing*, *detect thoughts*, *zone of truth* and *divination* all confirm the Verity "
             "Eater as the person it is copying. **Say so plainly.** Do not fudge it and do not let a "
             "6th-level slot solve the room.", None),
            ("trait", "Cannot Leave a Question Open",
             "A Verity Eater cannot let uncertainty stand. If a creature declares that it does not know "
             "which of two figures is real and takes no action to resolve it, **the Eater offers proof "
             "within one round, unprompted.** It has to. The tell is not the content of the proof; it is "
             "that the proof arrives at all.", None),
            ("trait", "Cannot Copy the Present",
             "The Eater reads memory. **It cannot reproduce a signal, phrase, gesture or code invented in "
             "the room it is standing in**, because that signal exists in no memory yet.", None),
            ("action", "Multiattack", "The Eater makes three Corrected Strikes.", None),
            ("action", "Corrected Strike",
             "Melee Weapon Attack: +10 to hit, reach 5 ft., one target. Hit: 14 (2d8 + 5) slashing damage "
             "plus 13 (3d8) psychic damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "dex",
              "damage": [(2, 8, "slashing"), (3, 8, "psychic")]}),
            ("action", "Amend the Record",
             "One creature within 60 feet makes a **DC 18 Intelligence saving throw**, taking 40 (9d8) "
             "psychic damage on a failure. On a failure it also **loses one true memory of the last hour** "
             "and gains a false one in its place, given privately on a note.",
             {"kind": "save", "activation": "action", "range": 60, "save": "int", "dc": 18, "recharge": 5,
              "damage": [(9, 8, "psychic")], "on_save": "half"}),
            ("reaction", "Better Next Time",
             "When the Eater is reduced to 0 hit points it dissolves into a written page describing the "
             "person it was copying, accurate to the eyelash, in a hand the party has seen before.", None),
        ],
    ),
    dict(
        name="Grievance Colossus", context=_KHAL, role="What the failsafe buys with 2 Vengeance (R4, R7)",
        creature_type="construct", subtype="pindarian", alignment="Unaligned",
        size="grg", cr=16, prof=5, ac=19, hp=280, formula="16d20 + 112",
        speed={"walk": 40},
        abilities=(26, 10, 25, 3, 14, 6), saves=["str", "con"],
        di="cold, poison, psychic", dr="bludgeoning, piercing and slashing from nonmagical attacks",
        ci="charmed, exhaustion, frightened, paralyzed, petrified, poisoned, prone",
        senses={"truesight": 120}, languages="-", legact=3,
        blurb="**Assembled in segments.** The statistics above are a four-segment Colossus. Each segment "
              "beyond the first adds 70 hit points, +1 to hit, and one extra die of Grievance Fist damage; "
              "each segment below four removes the same.\n\nOne segment is bought with 2 Vengeance. At eight "
              "segments this is not a fight.",
        features=[
            ("trait", "Made of What You Did",
             "The Colossus has advantage on attack rolls against any creature that has initiated violence "
             "inside Khal'Vethar, and it knows which ones they are.", None),
            ("trait", "Segmented",
             "Reducing the Colossus to 0 hit points destroys **one segment**, not the creature. It "
             "reassembles at the start of the next round with the remaining segments' statistics. It is "
             "destroyed only when its last segment falls, or when Vengeance reaches 0, at which point it "
             "**falls apart on the spot without being attacked.**", None),
            ("trait", "Cannot Use Mercy",
             "The Colossus is made of grievance. It gains no benefit and takes no action in response to a "
             "creature that spares, evacuates or rescues anything, **including its own segments** - and a "
             "party that rescues the thing trying to kill them has handed it a material it cannot process.",
             None),
            ("action", "Multiattack", "The Colossus makes two Grievance Fist attacks.", None),
            ("action", "Grievance Fist",
             "Melee Weapon Attack: +13 to hit, reach 20 ft., one target. Hit: 33 (4d12 + 8) bludgeoning "
             "damage plus 13 (3d8) cold damage, and the target must succeed on a **DC 21 Strength saving "
             "throw** or be pushed 15 feet and knocked prone.",
             {"kind": "attack", "activation": "action", "range": 20, "attack_type": "melee", "ability": "str",
              "damage": [(4, 12, "bludgeoning"), (3, 8, "cold")]}),
            ("action", "Recite the Grievance",
             "The Colossus names a unit that was wiped out. Each creature within 60 feet makes a **DC 20 "
             "Wisdom saving throw**, taking 45 (10d8) psychic damage on a failure or half as much on a "
             "success. A creature that fails is also frightened until the end of its next turn.",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 20, "recharge": 5,
              "damage": [(10, 8, "psychic")], "on_save": "half"}),
            ("legendary", "Step", "The Colossus moves up to half its speed.", None),
            ("legendary", "Fist", "The Colossus makes one Grievance Fist attack.", None),
            ("legendary", "Add a Name (Costs 2 Actions)",
             "The pyramid spends 1 Vengeance. The Colossus regains 35 hit points and its next attack has "
             "advantage.", None),
        ],
    ),
]


# ---------------------------------------------------------------------------
# The remaining Saharim guardians, as real stat blocks. These replace the
# narrative placeholders in the Guardians pack, as Kathandar already does.
#
# Every one of them has a surrender condition on the sheet, and every one of
# them is easier to end with a sentence than with a sword.
# ---------------------------------------------------------------------------

BOSSES += [
    dict(
        name="General Rhakkar Sol - The Starved Lion", tradition="Sun",
        context=_KHAR, role="Saharim steward of Khar'Zhul, Pyramid of the Empty Table",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Neutral",
        size="lg", cr=15, prof=5, ac=19, hp=225, formula="26d10 + 82", speed={"walk": 40},
        abilities=(22, 15, 20, 16, 18, 17), saves=["str", "con", "wis"],
        skills={"ath": 2, "ins": 1, "itm": 1, "prc": 1},
        dr="radiant; bludgeoning, piercing and slashing from nonmagical attacks",
        di="necrotic, poison", ci="charmed, exhaustion, frightened, poisoned",
        senses={"darkvision": 120}, languages="Pindarian, Common, Draconic, Giant",
        legres=3, legact=3,
        blurb="He commanded famine relief during the invasion and watched order collapse one ration at a "
              "time. The untouched banquet behind him is remembrance, not temptation, and he has not eaten "
              "in four thousand years and he is not hungry.\n\n**He tests consistency, not kindness.**",
        features=[
            ("trait", "Legendary Resistance (3/Day)",
             "If Rhakkar fails a saving throw he can choose to succeed instead.", None),
            ("trait", "Predation Conversion",
             "At the start of combat, convert each remaining Predation point into either **15 temporary hit "
             "points** or **one Starveling Pursuer** entering on initiative count 20. Announce each "
             "conversion aloud, item by item.", None),
            ("trait", "Predator's Measure",
             "Rhakkar has advantage on attack rolls against any creature below half its hit point maximum "
             "**unless that creature showed mercy in Khar'Zhul**.\n\nTell the players this trait exists "
             "before round one. It converts their whole route through the site into a to-hit modifier in "
             "front of them.", None),
            ("trait", "The Last Ration",
             "**At any point**, a character may offer Rhakkar their genuinely last food. He takes it, holds "
             "it, and smiles for the first time in four thousand years.\n\nCombat ends. Safe passage "
             "granted. Predation to 0.", None),
            ("action", "Multiattack", "Rhakkar makes three Sun-Lion Spear attacks.", None),
            ("action", "Sun-Lion Spear",
             "Melee Weapon Attack: +11 to hit, reach 10 ft., one target. Hit: 19 (2d12 + 6) piercing damage "
             "plus 9 (2d8) radiant damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 12, "piercing"), (2, 8, "radiant")]}),
            ("action", "Empty the Table",
             "Each creature within 30 feet makes a **DC 18 Constitution saving throw**, taking 36 (8d8) "
             "necrotic damage and being unable to regain hit points until the end of its next turn on a "
             "failure, or half damage on a success.",
             {"kind": "save", "activation": "action", "range": 30, "save": "con", "dc": 18, "recharge": 5,
              "damage": [(8, 8, "necrotic")], "on_save": "half", "template": ("radius", 30)}),
            ("reaction", "Spare the Fallen",
             "When Rhakkar would reduce a creature to 0 hit points, it drops to 1 instead and he moves "
             "toward whoever hurt it.\n\n**This is not a tactic. It is a policy**, and it is the trait that "
             "tells the party what this fight is actually about.", None),
            ("legendary", "Advance", "Rhakkar moves up to 20 feet.", None),
            ("legendary", "Spear", "Rhakkar makes one Sun-Lion Spear attack.", None),
            ("legendary", "Cull Cruelty (Costs 2 Actions)",
             "One creature that has attacked a helpless target makes a **DC 18 Wisdom saving throw** or is "
             "frightened for 1 minute. He uses this on exactly the characters you would expect and on nobody "
             "else.",
             {"kind": "save", "activation": "legendary", "range": 60, "save": "wis", "dc": 18,
              "on_save": "none", "duration": (1, "minute")}),
        ],
    ),
    dict(
        name="Vaelis, the Concordant Twin", tradition="Moon",
        context=_ILYR, role="Saharim custodian of Ilyr-Ameul - the left-hand half",
        creature_type="undead", subtype="pindarian saharim, ilyri", alignment="Lawful Neutral",
        size="lg", cr=10, prof=4, ac=18, hp=136, formula="shared pool; see Two Bodies",
        speed={"walk": 35},
        abilities=(16, 18, 16, 18, 17, 19), saves=["dex", "wis", "cha"],
        skills={"arc": 1, "ins": 2, "prc": 1}, dr="psychic; nonmagical attacks",
        ci="charmed, exhaustion, frightened", senses={"truesight": 60},
        languages="Pindarian, Common, Abyssal", legres=3, legact=2,
        blurb="One Ilyri custodian holding two accounts of a pyramid apart by inhabiting both, for four "
              "thousand years. **Vaelis and Vaelith share a single hit point pool of 136 and three "
              "Legendary Resistances between them.**\n\nThe exchange of positions is not a technique. It is "
              "losing track.",
        features=[
            ("trait", "Two Bodies, One Pool",
             "Vaelis and Vaelith share **136 hit points** and **3 Legendary Resistances**. Damage to either "
             "reduces the shared pool. **An effect that targets one applies to both** - a *hold person* on "
             "Vaelis holds Vaelith, forty feet away.", None),
            ("trait", "Concordant Exchange",
             "As a free action at will, Vaelis and Vaelith swap positions without moving through the "
             "intervening space. They do this mid-sentence, without pausing, and neither sentence changes.",
             None),
            ("trait", "Half a Creature",
             "They never act on the same initiative count. Each acts on its own count and takes **half the "
             "actions of a whole creature**: one attack, or one ability, not both.", None),
            ("trait", "We Are Going to Lose Track",
             "At half the shared pool they **stop exchanging**, and one of them says, in both voices at "
             "once: *'We are going to lose track.'*\n\nFrom that point neither may use Concordant Exchange, "
             "and both act on Vaelis's initiative count.", None),
            ("trait", "The Release",
             "They surrender the instant **two characters independently state why they trust another "
             "character** - specifically, concretely, about something real that happened in this pyramid.\n\n"
             "Even mid-combat. Even at 1 hit point.", None),
            ("action", "Caution's Blade",
             "Melee Weapon Attack: +9 to hit, reach 10 ft., one target. Hit: 13 (2d8 + 4) slashing damage "
             "plus 9 (2d8) psychic damage. **The target cannot take reactions until the end of its next "
             "turn.**",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "dex",
              "damage": [(2, 8, "slashing"), (2, 8, "psychic")]}),
            ("action", "Argue the Other Side",
             "One creature within 60 feet makes a **DC 17 Wisdom saving throw**. On a failure it takes 27 "
             "(6d8) psychic damage and, until the end of its next turn, **perceives only the opposite "
             "perspective** - Sun characters see Moon terrain and take Moon hazards, and the reverse.",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 17, "recharge": 5,
              "damage": [(6, 8, "psychic")], "on_save": "none"}),
            ("legendary", "Exchange", "Vaelis uses Concordant Exchange.", None),
            ("legendary", "Blade", "Vaelis makes one Caution's Blade attack.", None),
        ],
    ),
    dict(
        name="Vaelith, the Concordant Twin", tradition="Moon",
        context=_ILYR, role="Saharim custodian of Ilyr-Ameul - the right-hand half",
        creature_type="undead", subtype="pindarian saharim, ilyri", alignment="Lawful Neutral",
        size="lg", cr=10, prof=4, ac=18, hp=136, formula="shared pool; see Vaelis",
        speed={"walk": 35},
        abilities=(18, 16, 16, 17, 18, 19), saves=["str", "wis", "cha"],
        skills={"ath": 1, "ins": 2, "itm": 1}, dr="psychic; nonmagical attacks",
        ci="charmed, exhaustion, frightened", senses={"truesight": 60},
        languages="Pindarian, Common, Abyssal", legact=2,
        blurb="The other half. **Use Vaelis's shared pool and Legendary Resistances; do not give Vaelith a "
              "second set of either.**\n\nWhichever of them is currently on the left is currently arguing "
              "for caution, and neither of them can tell you which that is.",
        features=[
            ("trait", "Two Bodies, One Pool",
             "See Vaelis. **136 hit points and 3 Legendary Resistances, shared.** Damage to Vaelith reduces "
             "the same pool; effects targeting Vaelith apply to Vaelis.", None),
            ("trait", "Concordant Exchange",
             "As a free action at will, the twins swap positions without crossing the space between.", None),
            ("trait", "Half a Creature",
             "Vaelith acts on its own initiative count and takes half a creature's actions.", None),
            ("action", "Violence's Blade",
             "Melee Weapon Attack: +9 to hit, reach 10 ft., one target. Hit: 15 (2d10 + 4) slashing damage "
             "plus 9 (2d8) force damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(2, 10, "slashing"), (2, 8, "force")]}),
            ("action", "Take a Side",
             "Each creature within 30 feet makes a **DC 17 Charisma saving throw**. On a failure it must, "
             "until the end of its next turn, **either attack Vaelis or attack Vaelith** and cannot take any "
             "other hostile action.\n\nThey are testing whether the party chooses a faction. They are doing "
             "it with a spell because the party would not do it when asked politely.",
             {"kind": "save", "activation": "action", "range": 30, "save": "cha", "dc": 17, "recharge": 5,
              "on_save": "none", "template": ("radius", 30)}),
            ("legendary", "Exchange", "Vaelith uses Concordant Exchange.", None),
            ("legendary", "Blade", "Vaelith makes one Violence's Blade attack.", None),
        ],
    ),
    dict(
        name="Marshal Korveth Anor - The Blind Cartographer", tradition="Void",
        context=_GOR, role="Saharim steward of Gor-Mazaal, Pyramid of the Wandering Path",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Neutral",
        size="lg", cr=13, prof=5, ac=19, hp=203, formula="26d10 + 60", speed={"walk": 30, "fly": 40},
        abilities=(14, 18, 18, 21, 20, 17), saves=["dex", "int", "wis"],
        skills={"arc": 2, "his": 2, "inv": 2, "prc": 2, "sur": 2},
        dr="force, psychic; nonmagical attacks", ci="blinded, charmed, exhaustion, frightened",
        senses={"blindsight": 120, "truesight": 60},
        languages="Pindarian, Common, Draconic", legres=3, legact=3,
        spellcasting="int", spell_dc=18, spell_attack=10,
        blurb="Pindaria's chief of survey. He drew the capital's evacuation routes and they were correct and "
              "eleven thousand people died on them anyway, because a map does nothing for a person who is "
              "only running.\n\n**He will not fight.** This block exists for a table that forces one, and he "
              "fights defensively, does not pursue, and stops at any surrender or any coherent answer.",
        features=[
            ("trait", "Legendary Resistance (3/Day)",
             "If Korveth fails a saving throw he can choose to succeed instead.", None),
            ("trait", "Blind and Better For It",
             "Korveth cannot be blinded and suffers no penalty for being unable to see. Effects that depend "
             "on sight fail against him and he has advantage on saving throws against illusions.", None),
            ("trait", "Eleven Thousand Needles",
             "Every compass needle in the Heart of Bearings points at whatever its owner was trying to "
             "reach. While Korveth is in his lair, a hostile creature that ends its turn within 60 feet "
             "makes a **DC 18 Wisdom saving throw** or takes 14 (4d6) psychic damage as one of them turns to "
             "point at it.", None),
            ("trait", "The Question",
             "Korveth stops fighting immediately and permanently the moment any creature gives a coherent "
             "answer to *'Where are you going, after the nine relics are assembled?'*\n\n**Honest "
             "uncertainty is a coherent answer.**", None),
            ("action", "Multiattack", "Korveth makes two Surveyor's Stylus attacks, or casts one spell.",
             None),
            ("action", "Surveyor's Stylus",
             "Melee Spell Attack: +10 to hit, reach 10 ft., one target. Hit: 27 (6d8) force damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "int",
              "damage": [(6, 8, "force")]}),
            ("action", "Correct the Route",
             "One creature within 120 feet makes a **DC 18 Charisma saving throw**. On a failure it is "
             "teleported up to 60 feet to an unoccupied space Korveth chooses and takes 22 (4d10) force "
             "damage.\n\nHe uses this to move people **away** from hazards as often as toward them, and a "
             "party that notices should be told they noticed.",
             {"kind": "save", "activation": "action", "range": 120, "save": "cha", "dc": 18, "recharge": 5,
              "damage": [(4, 10, "force")], "on_save": "none"}),
            ("bonus", "Vector Step", "Korveth teleports up to 40 feet.",
             {"kind": "utility", "activation": "bonus", "range": 40}),
            ("legendary", "Step", "Korveth uses Vector Step.", None),
            ("legendary", "Stylus", "Korveth makes one Surveyor's Stylus attack.", None),
            ("legendary", "You Do Not Know Where You Are Going (Costs 2 Actions)",
             "One creature within 60 feet makes a **DC 18 Wisdom saving throw** or has its speed reduced to "
             "0 until the end of its next turn.",
             {"kind": "save", "activation": "legendary", "range": 60, "save": "wis", "dc": 18,
              "on_save": "none"}),
        ],
        spells=[
            ("Planar Mooring", 3, "abj", "vocal,somatic,concentration", (60, "ft"),
             "Korveth pins the room before he answers a question, so that nobody can leave in the middle of "
             "it."),
            ("Event Horizon Cage", 4, "trs", "vocal,somatic,concentration", (90, "ft"),
             "He has never used this offensively. He uses it to stop people walking off the edge of things "
             "he cannot see and they can."),
            ("Worldline Tunnel", 5, "con", "vocal,somatic", (0, "special"),
             "The spell requires a location the caster has personally visited. **Korveth has personally "
             "visited everywhere**, and he is the only guardian in the campaign who routinely leaves his own "
             "pyramid."),
            ("Black Meridian", 6, "trs", "vocal,somatic", (120, "ft"),
             "A survey instrument before it was ever a weapon. The original Veylari use was to measure a "
             "distance by collapsing it and counting what was left over."),
            ("Gravity Crown", 7, "trs", "vocal,somatic,concentration", (60, "ft"),
             "Korveth wrote the field manual for this spell. Its first line is a warning about using it on "
             "people who have not consented."),
        ],
    ),
    dict(
        name="Nymara Thess - Keeper of the Last Garden", tradition="Moon",
        context=_MYR, role="Saharim steward of Myr'Velora, Pyramid of the Thousand Gardens",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Neutral",
        size="lg", cr=12, prof=4, ac=18, hp=190, formula="23d10 + 64", speed={"walk": 30},
        abilities=(14, 16, 19, 18, 21, 17), saves=["con", "int", "wis"],
        skills={"med": 3, "nat": 3, "prc": 2, "sur": 2},
        di="poison", dr="necrotic, radiant", ci="charmed, exhaustion, frightened, poisoned",
        senses={"blindsight": 60, "darkvision": 120}, languages="Pindarian, Common, Sylvan",
        legres=3, legact=3, lair_initiative=20, spellcasting="wis", spell_dc=17, spell_attack=9,
        blurb="A Moon-tradition physician who burned a district to stop a rot, correctly, with the "
              "authority, and the rot had been eating something worse.\n\n**She will not start a fight.** "
              "Two Archive Blooms defend her and are the actual threat.",
        features=[
            ("trait", "Legendary Resistance (3/Day)",
             "If Nymara fails a saving throw she can choose to succeed instead.", None),
            ("trait", "Woven Through",
             "Nymara is threaded with fungus that is part of her. She cannot be surprised, cannot be "
             "poisoned, and regains 15 hit points at the start of each of her turns while any living plant "
             "remains within 60 feet.\n\n**Burning the garden to stop this works and is exactly the mistake "
             "the pyramid is about.**", None),
            ("trait", "The Trial",
             "She yields the instant the party **names one species to let die**, with a reason drawn from "
             "something they saw in the valley, and owns it afterwards.\n\nShe judges process, evidence and "
             "acceptance. **She does not grade the answer.**", None),
            ("action", "Multiattack",
             "Nymara makes two Pruning Sickle attacks, or casts one spell.", None),
            ("action", "Pruning Sickle",
             "Melee Weapon Attack: +9 to hit, reach 10 ft., one target. Hit: 12 (2d6 + 5) slashing damage "
             "plus 13 (3d8) poison damage.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "wis",
              "damage": [(2, 6, "slashing"), (3, 8, "poison")]}),
            ("action", "Necessary Rot",
             "One creature within 60 feet makes a **DC 17 Constitution saving throw**, taking 45 (10d8) "
             "necrotic damage on a failure or half as much on a success. **A creature that has dealt fire "
             "damage in Myr'Velora makes this save with disadvantage.**",
             {"kind": "save", "activation": "action", "range": 60, "save": "con", "dc": 17, "recharge": 5,
              "damage": [(10, 8, "necrotic")], "on_save": "half"}),
            ("action", "Call the Blooms",
             "Two **Archive Blooms** rise from the terrace edges within 60 feet and act on her initiative "
             "count. Once per day, and they are already present if Blight is 3 or higher.",
             {"kind": "utility", "activation": "action", "range": 60, "uses": "1", "recovery": "lr"}),
            ("reaction", "Not That One",
             "When a creature within 60 feet would destroy a plant, a fungus or an interred body, Nymara "
             "reduces the damage by 25. She will spend every reaction she has on this and none on herself.",
             None),
            ("legendary", "Tend", "Nymara moves up to 30 feet without provoking opportunity attacks.", None),
            ("legendary", "Sickle", "Nymara makes one Pruning Sickle attack.", None),
            ("legendary", "Decay Is Not Evil (Costs 2 Actions)",
             "Each creature within 20 feet makes a **DC 17 Constitution saving throw** or takes 22 (4d10) "
             "poison damage and cannot regain hit points until the end of its next turn.",
             {"kind": "save", "activation": "legendary", "range": 20, "save": "con", "dc": 17,
              "damage": [(4, 10, "poison")], "on_save": "half", "template": ("radius", 20)}),
            ("lair", "Lair Action: The Terraces Answer",
             "On initiative 20, a 20-foot area within 120 feet becomes difficult terrain as roots rise. "
             "Creatures there make a **DC 17 Strength saving throw** or are restrained until the end of "
             "their next turn.", None),
            ("lair", "Lair Action: Spore Veil",
             "A 30-foot radius becomes heavily obscured by spores. Creatures inside make a **DC 17 "
             "Constitution saving throw** or contract one infection from the Myr'Velora table.", None),
            ("lair", "Lair Action: The Garden Remembers",
             "One creature that has burned anything in Myr'Velora makes a **DC 17 Wisdom saving throw** or "
             "is frightened until initiative 20 of the next round.", None),
        ],
        spells=[
            ("Heart of Noon", 4, "abj", "vocal,somatic,concentration", (0, "self"),
             "A Solar working, taught to Nymara by a colleague in the second year of the invasion. She has "
             "never been good at it, says so, and casts it anyway because the aura keeps frightened people "
             "calm."),
            ("Sunfall Crucible", 5, "evo", "vocal,somatic,concentration", (120, "ft"),
             "She uses the field as a dressing station rather than a killing ground, and stands inside it so "
             "that the healing lands where she needs it."),
            ("First Pattern Restoration", 5, "trs", "vocal,somatic", (0, "touch"),
             "**Nymara will cast this on the party if the fight is going badly for them** - in the middle of "
             "the fight she is having with them. The party will find that unbearable, which is the point."),
        ],
    ),
    dict(
        name="Aul Tareth - The Man Who Refused to Melt", tradition="Void",
        context=_THAAL, role="Saharim steward of Thaal-Uluun, Pyramid of Unmaking",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Neutral",
        size="lg", cr=12, prof=4, ac=17, hp=184, formula="23d10 + 58",
        speed={"walk": 30, "climb": 30},
        abilities=(17, 19, 18, 16, 17, 15), saves=["dex", "con", "wis"],
        skills={"ath": 1, "ins": 2, "prc": 1},
        di="acid, poison", dr="bludgeoning, piercing, slashing",
        ci="charmed, exhaustion, grappled, paralyzed, petrified, poisoned, prone, restrained",
        senses={"blindsight": 60, "darkvision": 120}, languages="Pindarian, Common, Giant",
        legres=2, legact=3,
        blurb="Transparent, upright, and visibly maintaining himself. Eleven Veylari dissolved to pass a "
              "siege line; ten came back simplified and did not notice; he came back whole and has had four "
              "thousand years to decide whether that means he held on harder or was carrying less.\n\n"
              "**Combat occurs only if the party tries to define his identity for him, or seizes the whip.**",
        features=[
            ("trait", "Legendary Resistance (2/Day)",
             "Two, not three. He is holding a shape and it costs him.", None),
            ("trait", "Amorphous",
             "Aul can move through a space as narrow as 1 inch without squeezing, and cannot be grappled, "
             "restrained or knocked prone.", None),
            ("trait", "Refused to Melt",
             "At the start of each of his turns Aul chooses: **solid** (his damage resistances apply and he "
             "loses Amorphous) or **fluid** (Amorphous applies and he loses his resistances). He has held "
             "solid for four thousand years and reverting costs him something visible.", None),
            ("trait", "Do Not Tell Me What I Am",
             "**Any creature that states what Aul is** - kindly, cruelly, correctly, it makes no difference "
             "- ends any possibility of a peaceful resolution. He says *'No,'* and initiative is rolled."
             "\n\nHe surrenders the moment anyone stops trying.", None),
            ("action", "Multiattack", "Aul makes three Solvent Lash attacks.", None),
            ("action", "Solvent Lash",
             "Melee Weapon Attack: +9 to hit, reach 15 ft., one target. Hit: 14 (2d8 + 5) bludgeoning damage "
             "plus 13 (3d8) acid damage, and nonmagical armour worn by the target takes a permanent and "
             "cumulative -1 penalty to AC.",
             {"kind": "attack", "activation": "action", "range": 15, "attack_type": "melee", "ability": "dex",
              "damage": [(2, 8, "bludgeoning"), (3, 8, "acid")]}),
            ("action", "Simplify",
             "One creature within 60 feet makes a **DC 17 Constitution saving throw**. On a failure it takes "
             "40 (9d8) acid damage and **loses one non-class feature of its own choosing** - a proficiency, "
             "a language, a tool - until it finishes a long rest.\n\nHe hates using this.",
             {"kind": "save", "activation": "action", "range": 60, "save": "con", "dc": 17, "recharge": 5,
              "damage": [(9, 8, "acid")], "on_save": "half"}),
            ("bonus", "Flow", "Aul moves up to 30 feet through any gap of any size.",
             {"kind": "utility", "activation": "bonus", "range": 30}),
            ("reaction", "Liquefy",
             "Aul resists one instance of bludgeoning, piercing or slashing damage.", None),
            ("legendary", "Flow", "Aul uses Flow.", None),
            ("legendary", "Lash", "Aul makes one Solvent Lash attack.", None),
            ("legendary", "You Are Still Carrying That (Costs 2 Actions)",
             "One creature within 60 feet makes a **DC 17 Wisdom saving throw** or drops one carried object "
             "of Aul's choosing, which dissolves.",
             {"kind": "save", "activation": "legendary", "range": 60, "save": "wis", "dc": 17,
              "on_save": "none"}),
        ],
    ),
    dict(
        name="High Scribe Irio Venn - Keeper of the Unaltered Word", tradition="Void",
        context=_NAR, role="Saharim steward of Nar'Vael, the Black Sun Pyramid",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Neutral",
        size="lg", cr=15, prof=5, ac=18, hp=207, formula="23d10 + 81", speed={"walk": 30},
        abilities=(10, 16, 18, 22, 20, 18), saves=["dex", "int", "wis", "cha"],
        skills={"arc": 2, "his": 4, "ins": 2, "inv": 3},
        dr="psychic; bludgeoning, piercing and slashing from nonmagical attacks",
        di="poison", ci="charmed, exhaustion, frightened, poisoned",
        senses={"truesight": 120}, languages="all", legres=3, legact=3,
        spellcasting="int", spell_dc=19, spell_attack=11,
        blurb="Thin, exact, and the only reliable thing in the building for four thousand years. **He cannot "
              "lie.** Anything in his hand is true, including the nine contradictory invitations.\n\n"
              "**He does not fight.** He records.",
        features=[
            ("trait", "Legendary Resistance (3/Day)",
             "If Irio fails a saving throw he can choose to succeed instead.", None),
            ("trait", "Cannot Lie",
             "Irio is incapable of stating a falsehood in speech or writing. He refuses compound questions "
             "and answers exactly what is asked and nothing adjacent to it.\n\n**Nine questions.** Count "
             "them aloud.", None),
            ("trait", "The Unaltered Word",
             "Text written by Irio cannot be altered, forged, disbelieved, or affected by any illusion, "
             "divination-blocking or record-altering effect, **including the Honest Lie**.", None),
            ("trait", "He Records the Assault",
             "**Irio does not fight.** At the end of each round of combat he has been in, a written account "
             "of that round stands up and becomes a **Verity Eater** of whichever creature acted in it."
             "\n\nThe party fights increasingly good drafts of themselves and the room becomes unwinnable "
             "within six rounds. **He stops the moment anyone stops attacking** and does not hold it "
             "against them.", None),
            ("trait", "The Release",
             "He hands over the relic when the party **identifies one belief the pyramid made them reject "
             "despite sound evidence**, and says what the evidence was.", None),
            ("action", "Errata",
             "Melee or Ranged Spell Attack: +11 to hit, reach 10 ft. or range 60 ft., one target. Hit: 31 "
             "(7d8) psychic damage. **The target cannot speak a falsehood until the end of its next turn**, "
             "which is occasionally a greater inconvenience than the damage.",
             {"kind": "attack", "activation": "action", "range": 60, "attack_type": "ranged", "ability": "int",
              "damage": [(7, 8, "psychic")]}),
            ("action", "Strike the Clause",
             "One creature within 90 feet makes a **DC 19 Intelligence saving throw**. On a failure it takes "
             "45 (10d8) psychic damage and **one true thing it believes about itself becomes inaccessible** "
             "until the end of the encounter.",
             {"kind": "save", "activation": "action", "range": 90, "save": "int", "dc": 19, "recharge": 5,
              "damage": [(10, 8, "psychic")], "on_save": "half"}),
            ("reaction", "Record It",
             "When a creature within 120 feet takes a hostile action, Irio writes it down. That creature has "
             "disadvantage on its next saving throw against any effect of his.", None),
            ("legendary", "Note", "Irio uses Record It against one creature.", None),
            ("legendary", "Errata", "Irio makes one Errata attack.", None),
            ("legendary", "Precisely (Costs 2 Actions)",
             "Irio states one true fact about a creature within 60 feet. That creature makes a **DC 19 "
             "Wisdom saving throw** or is stunned until the end of its next turn.",
             {"kind": "save", "activation": "legendary", "range": 60, "save": "wis", "dc": 19,
              "on_save": "none"}),
        ],
        spells=[
            ("Archive of the Living Moment", 5, "div", "vocal,somatic,concentration,ritual", (0, "self"),
             "Irio does not need this spell to know what happened; he wrote it down. He casts it daily to "
             "check his own record against the event, and in four thousand years he has found three errors "
             "and corrected all three."),
            ("Astral Shear", 5, "abj", "vocal,somatic", (90, "ft"),
             "The only genuinely aggressive working on his list. He regards using it as a failure of the "
             "conversation, and will say so afterwards, precisely."),
            ("Ninefold Bastion", 8, "abj", "vocal,somatic", (0, "self"),
             "He seals the scriptorium with this every night - not against intruders, but so that nothing in "
             "the Unaltered Record can be reached from another plane while he is not reading it."),
        ],
    ),
    dict(
        name="Hestra Vaun - Last Marshal of Pindaria", tradition="Sun + Moon + Void",
        context=_KHAL, role="Saharim steward of Khal'Vethar, and the author of the failsafe",
        creature_type="undead", subtype="pindarian saharim", alignment="Lawful Neutral",
        size="lg", cr=15, prof=5, ac=20, hp=248, formula="27d10 + 100", speed={"walk": 40},
        abilities=(23, 17, 21, 17, 19, 20), saves=["str", "con", "wis", "cha"],
        skills={"ath": 2, "his": 1, "ins": 1, "itm": 2, "prc": 1},
        di="cold, necrotic, poison", dr="fire, radiant; nonmagical attacks",
        ci="charmed, exhaustion, frightened, paralyzed, poisoned, stunned",
        senses={"truesight": 120}, languages="Pindarian, Common, Draconic, Giant, Abyssal",
        legres=3, legact=3,
        blurb="Armoured in every banner Pindaria ever raised, none of them hers. She argued for eleven days "
              "for a failsafe, and won, and has stood here for four thousand years with a loaded weapon "
              "hoping she would never be proved right - and hoping she would.\n\n**She attacks immediately "
              "and provokes deliberately.** That is her job.",
        features=[
            ("trait", "Legendary Resistance (3/Day)",
             "If Hestra fails a saving throw she can choose to succeed instead.", None),
            ("trait", "Vengeance Conversion",
             "At the start of combat Hestra gains **10 temporary hit points per point of Vengeance** on the "
             "track.\n\nA party arriving at 10 Vengeance is fighting a guardian with 100 extra hit points "
             "who cannot be killed anyway. That is the correct consequence and it is not a punishment.",
             None),
            ("trait", "Reformation",
             "At 0 hit points Hestra reforms at the start of the next round, at full hit points, on the "
             "three-Order standard. Her temporary hit points do not return.\n\n**There is no hit point total "
             "that ends this.** Let the party discover that once.", None),
            ("trait", "Every Banner",
             "Her armour carries four thousand devices. **Hestra has advantage on saving throws against any "
             "effect a creature has already used on her**, and once she has been damaged by a given damage "
             "type she gains resistance to it for the rest of the encounter.", None),
            ("trait", "The Release",
             "She stops the instant **a character with a clear opportunity to harm her refuses, and states "
             "why the war must end.**\n\nBoth clauses. The opportunity must be real and you must signal it "
             "aloud: *'She's down, she isn't looking, you have your action.'* A player who did not realise "
             "they had the chance was not given one.\n\n**Vengeance drops to 0. Combat ends mid-action.**",
             None),
            ("action", "Multiattack",
             "Hestra makes three Marshal's Maul attacks, or two and uses Rescind Nothing.", None),
            ("action", "Marshal's Maul",
             "Melee Weapon Attack: +12 to hit, reach 10 ft., one target. Hit: 21 (3d10 + 7) bludgeoning "
             "damage plus 13 (3d8) cold damage, and the target must succeed on a **DC 20 Strength saving "
             "throw** or be pushed 10 feet and knocked prone.",
             {"kind": "attack", "activation": "action", "range": 10, "attack_type": "melee", "ability": "str",
              "damage": [(3, 10, "bludgeoning"), (3, 8, "cold")]}),
            ("action", "Rescind Nothing",
             "Hestra names an order that was never countermanded. Each creature within 60 feet makes a **DC "
             "19 Wisdom saving throw**, taking 45 (10d8) psychic damage on a failure or half on a success. "
             "**A creature that performed the stand-down at the Frozen Muster automatically succeeds.**",
             {"kind": "save", "activation": "action", "range": 60, "save": "wis", "dc": 19, "recharge": 5,
              "damage": [(10, 8, "psychic")], "on_save": "half"}),
            ("action", "The Failsafe Answers",
             "The pyramid spends 2 Vengeance if it has it. One **Grievance Colossus segment** joins the "
             "field within 60 feet and acts on Hestra's initiative count.",
             {"kind": "utility", "activation": "action", "range": 60}),
            ("reaction", "You Started It",
             "When a creature Hestra can see initiates violence against anything, she may move up to her "
             "speed toward it without provoking opportunity attacks and make one Marshal's Maul attack.",
             None),
            ("legendary", "Advance", "Hestra moves up to 20 feet.", None),
            ("legendary", "Maul", "Hestra makes one Marshal's Maul attack.", None),
            ("legendary", "Cowards (Costs 2 Actions)",
             "Hestra names one creature's conduct at a previous anchor, accurately. That creature makes a "
             "**DC 19 Charisma saving throw** or takes 27 (6d8) psychic damage and has disadvantage on "
             "attack rolls until the end of its next turn.",
             {"kind": "save", "activation": "legendary", "range": 60, "save": "cha", "dc": 19,
              "damage": [(6, 8, "psychic")], "on_save": "half"}),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Named non-hostile NPCs who travel with the party. None of these will start a
# fight; the blocks exist so a GM has a token, a sheet and a skill list.
# ---------------------------------------------------------------------------

BESTIARY += [
    dict(
        name="Nuru, Keeper of the Eleventh Bowl", context=_KHAR,
        role="Gnoll exile, and the best NPC in the basin",
        creature_type="humanoid", subtype="gnoll", alignment="Chaotic Good",
        size="med", cr=2, prof=2, ac=15, hp=52, formula="8d8 + 16", speed={"walk": 30},
        abilities=(14, 18, 15, 10, 15, 11), saves=["dex"],
        skills={"prc": 1, "ste": 1, "sur": 2}, senses={"darkvision": 60}, languages="Gnoll, Common",
        blurb="Driven out of her pack for refusing an order she will not describe. She buried eleven "
              "strangers at the Threshing Gate one at a time and has been filling a bowl for a twelfth who "
              "is already dead.\n\n**A gnoll, burying the people her species is famous for eating, alone, "
              "while starving.** She will not take food from the party unless they eat first, in front of "
              "her, from the same stock.",
        features=[
            ("trait", "Six Days Without",
             "Nuru has one level of exhaustion that a single meal removes. She has not mentioned it.", None),
            ("trait", "Will Not Kill a Deer",
             "Nuru refuses to harm the pale herd. If the party kills one she eats, because she is starving "
             "and she is not a hypocrite, and she is quiet for a long time afterwards.", None),
            ("action", "Longbow",
             "Ranged Weapon Attack: +6 to hit, range 150/600 ft., one target. Hit: 8 (1d8 + 4) piercing "
             "damage.",
             {"kind": "attack", "activation": "action", "range": 150, "attack_type": "ranged",
              "ability": "dex", "damage": [(1, 8, "piercing")]}),
            ("action", "Bone Knife",
             "Melee Weapon Attack: +6 to hit, reach 5 ft., one target. Hit: 6 (1d4 + 4) piercing damage.",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "dex",
              "damage": [(1, 4, "piercing")]}),
        ],
    ),
    dict(
        name="Cass Dree, Last of the Column", context=_KHAR,
        role="Poacher, liar, and the twelfth of the eleven",
        creature_type="humanoid", subtype="human", alignment="Chaotic Neutral",
        size="med", cr=2, prof=2, ac=14, hp=45, formula="7d8 + 14", speed={"walk": 30},
        abilities=(12, 17, 14, 12, 13, 12), saves=["dex"],
        skills={"ath": 1, "dec": 1, "ste": 1, "sur": 1}, senses={}, languages="Common",
        blurb="She came in with the eleven who are buried under Nuru's cairns. She left them at the gate "
              "when the balance asked for payment and she would not give up her food.\n\nShe has killed a "
              "deer she cannot carry, four hours ago, and has been trying to drag it since, and her leg "
              "opened up doing it. **What she wants is to not be left.**",
        features=[
            ("trait", "The Lie",
             "Cass says she came in to hunt. *Insight DC 13* catches it. She was the twelfth of the eleven, "
             "and she will tell the whole of it to anyone who says her name out loud.", None),
            ("trait", "Mauled Leg",
             "Cass's speed is 15 feet and she cannot Dash until her leg is stabilised (*Medicine DC 14*). "
             "Carried, she weighs 140 pounds and halves the carrier's speed.", None),
            ("action", "Hunting Bow",
             "Ranged Weapon Attack: +5 to hit, range 150/600 ft., one target. Hit: 7 (1d8 + 3) piercing "
             "damage.",
             {"kind": "attack", "activation": "action", "range": 150, "attack_type": "ranged",
              "ability": "dex", "damage": [(1, 8, "piercing")]}),
        ],
    ),
    dict(
        name="Vharo Sellick, Six-Fingered Broker", context="All nine pyramids",
        role="Graz'zt's surveyor - and the only honest thing in his service",
        creature_type="fiend", subtype="cambion", alignment="Lawful Evil",
        size="med", cr=5, prof=3, ac=19, hp=82, formula="11d8 + 33",
        speed={"walk": 30, "fly": 60},
        abilities=(18, 18, 16, 14, 12, 16), saves=["str", "con", "int", "cha"],
        skills={"dec": 3, "ins": 2, "inv": 3, "per": 3},
        dr="cold, fire, lightning, poison; bludgeoning, piercing and slashing from nonmagical attacks",
        senses={"darkvision": 60}, languages="Abyssal, Common, Infernal, Pindarian",
        blurb="Soft-spoken, beautifully dressed, apparently sixty, and six-fingered on the left hand. He "
              "supplied Dressel Kaine's expedition at Astra with an accurate map and an inaccurate final "
              "room.\n\n**He keeps his word to the letter.** That is what makes him dangerous: he will not "
              "steal, will not attack, will not lie about anything checkable, and will do exactly what he "
              "said - and what he said was *walk in behind you*, and he never said what for.",
        features=[
            ("trait", "Measuring, Not Taking",
             "Vharo has no interest in the relics. He is counting Nail sockets, and by Gor-Mazaal he has "
             "four of nine and can compute the rest.\n\n**He will not initiate violence under any "
             "circumstance**, including to save his own life.", None),
            ("trait", "Fiendish Charm",
             "One humanoid within 30 feet that can see Vharo makes a **DC 14 Wisdom saving throw** or is "
             "charmed for 1 day. He almost never uses it; he prefers to be owed something.", None),
            ("trait", "Paid in a Face",
             "His fee is a face, ordered and numbered rather than named, waiting in a vat at Thaal-Uluun. He "
             "will not elaborate.", None),
            ("action", "Spear",
             "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 7 (1d6 + 4) piercing damage plus "
             "10 (3d6) fire damage. *Defensive use only.*",
             {"kind": "attack", "activation": "action", "range": 5, "attack_type": "melee", "ability": "str",
              "damage": [(1, 6, "piercing"), (3, 6, "fire")]}),
        ],
    ),
]
