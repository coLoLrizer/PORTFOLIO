# Orbital Strike — Case Study of an Evolving Spell

This document is a small breakdown of how one ability idea — **Orbital Strike** — went through three different incarnations:

- from a loose visual fantasy,
- to a prototype in my own MMO-roguelike concept **Arhea**,
- to a more stable, MMO-friendly spell for a custom **Telekinetic** class in **Wynncraft**.

---

## 1. Initial Fantasy — “Orbital Strike” as a Mental Image

The very first thing that hooked me was not mechanics, but the **name and fantasy**.

I like abilities that feel like **a magical orbital beam**: something drops from above and deletes everything.

A few things were floating in my head at the same time:

- “Orbital Strike” style skills from **Magic Survival** (Android)  
- Various **Minecraft videos** where people script orbital lasers hitting the ground  
- The general real-world idea of **kinetic orbital bombardment** — dropping heavy projectiles from orbit at insane speed

All of this boiled down to a single fantasy:

> “Something above you charges, then brutally slams down in a focused area.”

At this point it was just a **vibe**, not a concrete design.

---

## 2. Arhea Prototype — Turning the Fantasy Into a Spell

When I started designing abilities for **Arhea** (MMO-RPG with roguelike elements and one life per run), I finally tried to give this “Orbital Strike” some mechanical shape.

Here is how my brain actually chained the idea together:

1. I have the **name**: “Orbital Strike”.
2. The word “orbital” immediately gives **“orbit”**.
3. Orbit → **Saturn with its rings**, something constantly spinning around.
4. That → reminds me of **Terraria Calamity**: armor sets (like Astrageldon / Catalyst) that create **orbiting stones** around the player which shoot at enemies.
5. From there, I get:  
   > “Stones orbiting the player and launching outward with force.”

### 2.1. Arhea Orbital Strike — First Real Implementation

For Arhea, the spell became this:

- It **pulls stones from the surface** under the player.
- The **type of block** changes the behavior:
  - **Gravel** → shotgun-style spread
  - **Stone** → single, heavy projectile
  - **Dirt** → AoE splash
- Stones rise up with a distinct animation, then launch in the direction of the player’s attack / aim.
- Stones can also inherit **elemental effects**.
- It’s visually readable and quite satisfying.

This design is **perfectly fine for Arhea**, because:

- It’s a hardcore **MMO + roguelike hybrid** with one life.
- Inconsistency is acceptable — runs are not meant to be 100% controlled.
- “Weird but cool” abilities are allowed to exist as long as they are fun and thematic.
- Orbital Strike there is **just one of many tools**, not a stable endgame pillar.

So as a “first real home”, Arhea’s version worked.

---

## 3. Why the Arhea Version Completely Breaks in Wynncraft

When I started building a **Telekinetic class for Wynncraft**, I naturally tried to drag this Arhea Orbital Strike with me.

On paper it sounded cool. In practice it dies immediately for several reasons.

### 3.1. Terrain Dependency = Unstable Gameplay

In Wynncraft, you **don’t control what blocks are under your feet**:

- In **Gruutslang** arena you mostly have **dirt**.
- In **Corkus** areas — a lot of **stone**.
- In **TCC** (The Canyon Colossus raid) you have platforms, void, abstract geometry.
- **Gravel** is almost never present in relevant arenas.
- Some floors are decorative blocks that technically don’t match any “logical” category.

This leads to the worst possible outcome:

- One boss fight → you only ever get **“dirt AoE version”**
- Another boss fight → only **“stone single-target version”**
- Some setups → the spell might just **not work as intended at all**

That’s not depth. That’s just **randomness the player can’t reasonably control**, especially in raids.

For Arhea that was acceptable.  
For Wynncraft, which is a persistent MMO with buildcraft, it’s not.

### 3.2. Text and UX Bloat

On top of that, the Arhea-style description is:

- long, conditional, and overloaded
- trying to explain three or more behaviors in one spell
- not very friendly to Wynncraft’s **ability tree UI**

And this is still only **one** spell in a class with a full tree.

So mechanically and UX-wise, this version is simply **not Wynncraft-compatible**.

(Some may think that this option is even less suitable for Arhea than for Wynncraft, but without revealing all my cards, I can say that this is not the case.)

---

## 4. Wynncraft Version — A Stable Core for Telekinetic

At this point I decided to keep the **fantasy** (stones, delayed launch, “orbit-ish” feeling)  
but completely rebuild the **mechanics** to fit Wynncraft.

The result was a much cleaner base spell:

### `Orbital Strike (Wynncraft – Base Spell)`

```text
ORBITAL STRIKE
Click Combo: LEFT-LEFT-RIGHT

Summon 3 telekinetically-charged stones from beneath the ground.
After a 1.5s preparation delay, each stone launches toward
the nearest enemy, one-by-one at 1s intervals.

Mana Cost: 35

Total Damage: 100% of your DPS per stone
   70% Damage
   20% Earth
   10% Fire

Range: 16 Blocks
