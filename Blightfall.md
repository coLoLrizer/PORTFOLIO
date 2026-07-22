# Portfolio Case Study: Blightfall: Crimson Veil

## Project Overview

**Role:** Game Designer & Systems Designer
**Team:** 7-person remote team (2 engineers, 2 level designers, 1 3D artist, 1 composer/writer)
**Timeline:** 2 months (March – April 2026)
**Platform:** Hytale Modding (CurseForge New Worlds Contest)
**Status:** Shipped (submitted to contest)

---

## The Problem

Extraction games (Tarkov, Arc Raiders) are built around PvP tension, making them difficult to translate into a compelling single-player or co-op experience. The core question was:

> *How do you preserve the tension of "risk vs. reward" and the pressure of a ticking clock in a PvE setting, where there are no other players to create that friction?*

The contest constraints added another layer: we had 2 months to deliver a complete, polished experience that could be played immediately.

---

## My Role & Contribution

As the Game Designer, I owned the entire system design from concept to documentation. My specific contributions included:

- **Game Pillars** — Defined 4 non-negotiable design principles that filtered every feature decision
- **Full GDD** — Authored a 50+ page Game Design Document with spawn tables, loot distribution, crafting progression, and boss mechanics
- **Core Systems Design** — Crimson Infection escalation curve, extraction risk/reward economy, tiered progression (T1–T3)
- **Boss & Enemy Design** — Crimson Witch (multi-phase encounter) and Rooterman (elite mob with crystal-targeting mechanic)
- **Documentation & Submission** — Wrote the final CurseForge description and gameplay instructions

---

## Design Process & Iteration

### 1. Establishing the Pillars

Before writing a single line of the GDD, I formulated four pillars that would serve as a "design filter":

| Pillar | Definition | Test |
|--------|------------|------|
| **Architecture Over RNG** | Map knowledge is the player's primary skill. Static map, fixed routes. | If a mechanic breaks the value of exploring the map → cut it. |
| **Biological Time Pressure** | Time is the main resource. Crimson Infection forces movement. | If the player can farm safely indefinitely → the mechanic fails. |
| **The Economy of Greed** | Extraction must be earned. Risk more for more reward. | If death has no serious cost → the system breaks. |
| **Long-Term Progression** | Every run contributes to rebuilding the hub and progressing toward the final goal. | If an activity doesn't contribute to progression → it's secondary. |

*These pillars were approved by the team and used throughout development to evaluate every new feature proposal.*

### 2. Systems Design (GDD Excerpts)

**Map & Zone Design:** I designed 4 distinct zones with tiered difficulty (T1–T3), each with specific mob types, spawn counts, and loot tables.

**Mob Spawn Table (Example — Ravine Region, T2):**

| Mob | Count | Crimson Stage | Drop |
|-----|-------|---------------|------|
| Trork Warrior | 4-6 | 0+ | Linen Scraps |
| Corrupt Wolf | 2-4 | 0-1 | Medium Hide |
| Cave Spider | 2-3 | 0+ | Venom Sac |

**Loot & Progression (Example — Material Tiers):**

| Material | Source | Location | Tier |
|----------|--------|----------|------|
| Iron Ore | Chest Drops | 1st Area, Ravine | T1 |
| Heavy Hide | Corrupt Bear Drops | Sand Biome | T3 |
| Shadowweave Scraps | Outlander Drops | Middle Dungeon | T2 |

**Crafting (Example — Weapon Progression):**

| Weapon | Materials | Tier |
|--------|-----------|------|
| Iron Sword | 6 Iron Ore, 3 Light Leather, 3 Linen Scraps | T1 |
| Adamantite Sword | 11 Adamantite Ore, 4 Heavy Leather, 3 Cindercloth Scraps | T3 |

*The full GDD included complete tables for all weapons (swords, axes, daggers, bows, crossbows), materials, and consumables.*

### 3. Boss Design: Crimson Witch

I designed the final boss encounter with the following structure:

- **Phase 1:** Witch brews potions at a cauldron (healing, poison, shadow, blood, holy)
- **Phase 2:** Uses brewed potions against the player — projectiles, area denial, self-buffs
- **Phase 3:** Escalation — faster brewing, more aggressive spellcasting
- **Death Animation (scripted):** The witch attempts one final swing with the cauldron, loses control, and pours the raw alchemical base over herself

*Full behavior flowcharts and mechanic descriptions were handed off to the engineering team for implementation.*

### 4. Playtesting & Iteration

**Week 5–6:** First internal playtest revealed critical issues:
- **Empty loot chests** — loot system wasn't populating correctly
- **Immortality bug** — players became invincible after death in certain conditions
- **Mob over-spawning** — server froze due to excessive enemy spawns
- **Broken quest triggers** — NPC quests didn't advance properly

**Week 7–8:** Bug fixes and polish. The team submitted the mod to CurseForge on April 28, 2026.

---

## What Went Wrong & What I Learned

This project taught me critical lessons about the gap between design and execution:

| Challenge | What Happened | Lesson Learned |
|-----------|---------------|----------------|
| **Design-Implementation Gap** | Despite a detailed GDD, implementation drifted significantly: mob spawns became random (not zone-based), loot was globally randomized, crafting progression never worked | A GDD is only as good as its enforcement. Regular sync meetings and design audits are essential |
| **Lack of Authority** | Key design decisions (Master Run concept, extraction-via-item system) were overruled without compromise | In a remote team, the designer must have final authority over gameplay decisions |
| **Late QA** | Most bugs were discovered in the final week — too late to fix properly | Playtesting must begin by week 3–4 and happen regularly, not as a final-week activity |
| **Submission Materials** | The mod was only submitted to one category because NPC documentation wasn't ready | Documentation (description, screenshots, trailer) must be prepared in parallel with development |

---

## Outcome

- **Shipped:** Mod successfully submitted to CurseForge and the Hytale New Worlds Contest
- **Reach:** 50+ downloads in the first week
- **Result:** Did not advance to the finalist round

Despite this, the project demonstrates my ability to:
- Design complete systems from concept to documentation
- Balance economy, progression, and difficulty curves
- Collaborate in a cross-functional remote team
- Identify and communicate critical issues under tight deadlines

---

## Links & Artifacts

- **CurseForge Page:** [Blightfall: Crimson Veil](https://www.curseforge.com/hytale/mods/blightfall-crimson-veil)
- **GDD (Excerpt):** [Link to Screenshot / PDF]
- **Concept Art:** [Link to Folder]

---

*"One deep project > Ten shallow ones."* — Nathan Kellman[reference:8]
