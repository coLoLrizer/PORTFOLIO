# Telekinetic Class for Wynncraft

I'm a game designer. Short version: I'm inspired by Wynncraft, and I decided to design a class for the Wynncraft system. In my own judgment, it fits the game's ecosystem, it is balanced, and it follows the logic the game itself uses. That is how it feels to me after 2000+ hours on the server. This document is a showcase of my work.

The Telekinetic class has three archetypes: **Mind Breaker**, **Elementalist** and **Defender**. This document walks through the ability tree page by page. The reasoning, numbers, balance process and known problems are in the [summary](#summary) at the bottom.

> 🚧 **WIP** marks sections that are still being written.

---

# Part 1 — Base

## Page 1

### Orbital Strike (showcase)
**Click combo:** LEFT-RIGHT-RIGHT · **Mana:** 35 · **Slot:** heavy attack spell

<img width="429" height="295" alt="image" src="https://github.com/user-attachments/assets/9a70ee28-51f8-4a19-bf90-4c36e70db329" />

Summons 3 stones from beneath the ground. After a 1.5s preparation delay, each stone launches toward the nearest enemy, firing one by one every 1s. Each stone deals 100% of your DPS (70% Damage, 20% Earth, 10% Fire) at a range of 16 blocks.

This is your attack spell. You would start the game with it.

<!-- TODO: GIF -->

[Why it exists and how it plays: read more in the summary →](#design-rationale)

<!-- TODO: confirm which of these nodes sit on page 1 -->

### Cheaper Orbital Strike I
Ability points: 1

<img width="362" height="132" alt="image" src="https://github.com/user-attachments/assets/2ececcd7-2113-4fcb-885a-054f2377e376" />

Reduces the mana cost of Orbital Strike by 10 (35 → 25).

### Mind Proficiency I
Ability points: 1

<img width="271" height="113" alt="image" src="https://github.com/user-attachments/assets/9932f859-c8e9-462d-a374-087a17d9cca8" />

Increases your Sprint and Main Attack's damage by 5%.


## Page 2 (branches)

#### Forcing 🚧 WIP

<!-- ![Forcing](./media/forcing.png) -->
<!-- TODO: screenshot and description -->

#### Telekinesis
**Click combo:** LEFT-LEFT-LEFT · **Mana:** 20 · **Slot:** movement spell

<img width="430" height="171" alt="image" src="https://github.com/user-attachments/assets/767c0359-d679-48d8-a8fb-e1ba52fe9969" />

A movement spell: you keep floating in the direction of movement, then jump in the direction of your gaze.

<!-- TODO: GIF -->

#### Discharge Thinking
**Mind Breaker Archetype** · Ability points: 1

<img width="461" height="238" alt="image" src="https://github.com/user-attachments/assets/0a15f854-5aa9-4ccc-a6fc-05edd1187711" />

Increases your move speed by 1% per 1% Sprint gained from your equipment (max +10%), plus a flat +5% move speed. Unlocking it blocks the **Forcing** node.

#### Barrier
**Click combo:** LEFT-LEFT-RIGHT · **Mana:** 25 · **Slot:** support spell

<img width="400" height="280" alt="image" src="https://github.com/user-attachments/assets/b0ecb0a5-008b-4719-9020-39782144a1b7" />

After a 1s delay, a barrier crashes down onto your position and decays 1% every second. Deals 80% of your DPS (60% Damage, 10% Water, 10% Fire) in a 5-block circle and gives a barrier worth 15% of max HP.

<!-- TODO: GIF -->

#### Cheaper Telekinesis I
**Required ability:** Telekinesis · Ability points: 1

<img width="344" height="149" alt="image" src="https://github.com/user-attachments/assets/92d23631-8449-4c1a-9c0b-70a5dd7a7144" />

Reduces the mana cost of Telekinesis by 5 (20 → 15).

#### Magnetism
**Click combo:** LEFT-RIGHT-LEFT · **Mana:** 30 · **Slot:** light attack spell

<img width="559" height="243" alt="image" src="https://github.com/user-attachments/assets/fcddbe8e-f114-447d-bc9d-51995f5a14b4" />

Releases a slow telekinetic shockwave that expands outward and damages every enemy it touches. Deals 110% of your DPS (70% Damage, 30% Thunder, 10% Air) in an 18-block sphere.

<!-- TODO: GIF -->

---

### Awareness
Ability points: 1

<img width="369" height="116" alt="image" src="https://github.com/user-attachments/assets/5bdf0070-ef4b-48a5-9598-4c8a96274a34" />

Spell cost escalation begins after the 3rd repeated cast instead of the 2nd.

# Part 2 — Archetypes 🚧 WIP

## Page 3 🚧 WIP

<!-- TODO -->

## Page 4 🚧 WIP

<!-- TODO -->

## Page 5 🚧 WIP

<!-- TODO -->

## Page 6 🚧 WIP

<!-- TODO -->

## Page 7 🚧 WIP

<!-- TODO -->

## Page 8 🚧 WIP

<!-- TODO -->

## Mind Breaker nodes awaiting a page 🚧 WIP

> **The core idea of Mind Breaker:** the movement of the player is the engine of the damage loop, not a bonus on top of it.

### Ascended Orbits

Stones orbit the player, rotating **clockwise**. Launched stones reach a target faster when the player moves **against** the rotation (counter-clockwise), and stones deplete as they are used.

<!-- ![Ascended Orbits](./media/ascended-orbits.png) -->
<!-- TODO: exact in-game wording, numbers -->

### Centrefuge

The recharge mechanic that closed the whole loop. It **instantly refreshes depleted stones** and **reverses their rotation** (via casting Telekinesis), so the player turns around and runs the other way to stay "against the current."

<!-- ![Centrefuge](./media/centrefuge.png) -->
<!-- TODO: exact in-game wording, cooldown, refresh amount -->

### Dynamo

Reduces Centrefuge's cooldown by **blocks traveled**. This is what turns movement from an optimization into the engine of the loop.

<!-- ![Dynamo](./media/dynamo.png) -->
<!-- TODO: exact in-game wording, cooldown reduction per block -->

### Charged → Corrosion

A chain: Charged targets take bonus damage, and the chain leads into Corrosion. See [Known problems](#known-problems) for the balance risk.

<!-- ![Charged and Corrosion](./media/charged-corrosion.png) -->
<!-- TODO: exact in-game wording, numbers -->

---

# Summary

> 🚧 **WIP**

### At a glance

| | |
|---|---|
| **Role** | Solo — design, balancing, prototype |
| **Class** | Telekinetic (Mind Breaker / Elementalist / Defender) |
| **Most developed archetype** | Mind Breaker |
| **Prototype** | Python / pygame, top-down action |
| **Verification** | DPS checked across 25+ builds |

### Spell kit

| Spell | Combo | Slot | Mana | Damage (of your DPS) | Area / Range | Element split |
|---|---|---|---|---|---|---|
| Orbital Strike | L-R-R | Heavy attack | 35 | 100% per stone, 3 stones | 16 blocks | 70% Damage, 20% Earth, 10% Fire |
| Magnetism | L-R-L | Light attack | 30 | 110% | 18-block sphere | 70% Damage, 30% Thunder, 10% Air |
| Barrier | L-L-R | Support | 25 | 80% + barrier 15% max HP | 5-block circle | 60% Damage, 10% Water, 10% Fire |
| Telekinesis | L-L-L | Movement | 20 | — (movement) | — | — |

### Combo logic

In Wynncraft, the click combo tells the player what a spell is for:

- **LLL**: movement and dashes
- **LLR**: support spell
- **LRL**: light attack spell
- **LRR**: heavy attack spell

This is the archer layout; every other class uses the mirrored one. The four Telekinetic spells follow it: Telekinesis (LLL), Barrier (LLR), Magnetism (LRL), Orbital Strike (LRR).

### Design rationale

> 🚧 **WIP.** Why each spell and node exists and how it plays.

**Orbital Strike.** It is the heavy attack slot (LRR) and the spell the player starts the game with. Three stones summoned from the ground, fired one by one at the nearest enemy.

<!-- TODO: why it exists, how it plays, why 3 stones, why the 1.5s delay -->

**Magnetism.** <!-- TODO -->

**Barrier.** <!-- TODO -->

**Telekinesis.** <!-- TODO -->

**Base nodes (Cheaper Orbital Strike I, Cheaper Telekinesis I, Mind Proficiency I, Awareness).** <!-- TODO -->

**Discharge Thinking and Forcing.** <!-- TODO: why they exclude each other -->

### Mind Breaker: the core problem

The obvious version of Ascended Orbits is passive: stones spin, stones deal damage, the player does nothing. That is not a mechanic, that is a stat stick. The design question was: *how do I make orbiting stones something the player actively plays with?*

### Mind Breaker: make physics the mechanic

The stones rotate clockwise. They reach a target faster if the player moves against their rotation, the same logic as a boat crossing against a current. So running counter-clockwise maximizes damage. This is not a hidden trick bolted onto the node; it follows directly from the fact that the skill is "stones orbit you."

- **Centrefuge** refreshes depleted stones and reverses their rotation (via Telekinesis), so the player runs the other way to stay "against the current."
- **Dynamo** reduces Centrefuge's cooldown by blocks traveled.
- **Result:** constant movement is the mechanism the whole damage loop runs on. A conceptual world rule (rotation, motion, distance) works as a logical fantasy-class mechanic.

<!-- TODO: diagram of orbit / run-direction relationship -->

### Balance process

1. Built a **battle log** that tracks damage ticks with timing.
2. Used a **real community build** plus a **self-designed test legendary weapon**, deliberately third from the top tier (not best-in-slot) so the test is stricter.
3. Calculated damage ticks, including randomness, using the **official community damage-calculation guide** to get DPS.
4. Compared the result against the other archetypes.

**What the test caught:** a node designed to contribute **~30%** of the archetype's DPS was actually contributing **~5%**. I adjusted the coefficients until it contributed ~30%.

**Result:** final build DPS verified against other archetypes at roughly **levels 105-120** and found within the normal range. The Telekinetic class was DPS-checked across **25+ builds**.

### Known problems

- **Charged is a balance and performance risk.** As designed, the bonus can splash onto all nearby enemies, which risks chain-AoE behavior and server load. **Fix:** apply the bonus only to the specific Charged target.
- **Single-target vs AoE asymmetry.** The archetype performs differently in the two cases and this is not fully resolved.
- **Overall assessment:** playable if implemented as-is, but likely not balanced out of the box.

### Prototype architecture (Python / pygame)

I designed the architecture myself and used AI only to verify and critique it, because AI-generated code kept producing ad-hoc solutions instead of a coherent system.

- **Entity** is a pure data class.
- **Unified Target system** (Point vs. Direction). Targets can nest: one Target can be a parameter of another (e.g. `random_point_in_radius` using a fixed cursor point as its center).
- **`refresh_interval`** generalizes target refreshing: never (fixed), every frame (default), or periodic.
- **Single `Move` primitive.**
- **AbilityManager** is the controller layer.
- **Stances** come in two types: numeric modifiers and boolean locks.

```
Movable            position, velocity, Move
├── Entity         + HP, Stances, AbilityManager
└── Projectile     lightweight, no Entity weight

Damageable (mixin) HP + apply_damage, added to Projectile
                   only when a "dying projectile" is needed
```

**Stress test:** I ran the architecture against a full vertical slice of a complex multi-phase boss (Wynncraft's Orphion). Every mechanic reduced to existing primitives:

- **Phases** are multiple `health_below` conditions; the existing priority/channel system resolves overlaps.
- **Growing-then-collapsing black hole with pull** is a Stance whose duration-bound tick calls `Move(toward center)` instead of `apply_damage`, the same pattern as a DoT.
- **Temporary-immortality final phase** is a Stance lock (`can_die: false`) next to the existing `can_cast` / `can_act` locks, with HP clamped to 1 while active.

---

## Contact

- LinkedIn: [linkedin.com/in/timur-l-476966373](https://linkedin.com/in/timur-l-476966373)
- Portfolio: [github.com/coLoLrizer/PORTFOLIO](https://github.com/coLoLrizer/PORTFOLIO)
