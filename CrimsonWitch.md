# Crimson Witch — Boss Design

## 1. High-Level Concept

**Boss:** Crimson Witch  
**Zone:** “Crimson Wastes”  
**Role:** Optional boss encounter with strong identity built around potions, territory control and escalating chaos.  
**Goal:** Reward players who can read telegraphs, manage space, and adapt to random-but-bounded potion effects.

The Crimson Witch is an older, alchemy-obsessed mage who fights almost entirely through potions. She controls the arena by spreading corruption, creating hazards, and using mobility tools to punish players who try to stay still or play too close for too long.

---

## 2. Role in the Game

- **Type:** Main boss of the Crimson Wastes zone (optional, but highly rewarding).
- **Progression role:**
  - First encounter: one-time story / side content.
  - Repeatable afterwards as an optional challenge for unique rewards and crafting materials.
- **Design pillars:**
  - **Space control:** the arena becomes more and more “polluted”.
  - **Potion identity:** each potion is readable and has a clear behavior.
  - **Player-like thinking:** the boss makes decisions similar to a cautious player (buff, heal, reposition, deny space).

---

## 3. Visual Identity & Arena

### 3.1 Visual Identity

- Silhouette: older witch, thin but sharp posture, long crimson cloak, always near her cauldron.
- Animation focus:
  - Slow, deliberate walking around the edge of the arena.
  - Exaggerated hand motions when brewing or throwing potions.
  - Distinct staff swings with small knockback.
- Cauldron:
  - Visually central to her identity — bubbling, emitting colored vapors that match current potions.
  - During brewing, three (later four) bottles rise behind her and are filled with “soul-like” wisps from the cauldron.

### 3.2 Arena

- Shape: Wide circular stone platform.
- Layout:
  - Center: large alchemical circle with 4 concentric rings.
  - Outer ring: her “walking zone” — she prefers to stay on the outer perimeter.
  - Four narrow stone spikes around the edge, angled toward the center.
- Corruption:
  - Crimson stains and growths along the floor.
  - As the fight progresses, more of the floor becomes visually “contaminated” by various potion effects.

---

## 4. Core Fight Structure

### 4.1 Core Loop

1. **Brewing phase**  
   - Witch stands by the cauldron.  
   - Brews a set of potions (3 in Phase 1, 4 in Phase 2+).  
   - Each potion is clearly telegraphed by a colored glow and bottle icon.

2. **Combat phase**  
   - She moves along the outer ring, trying to keep distance.  
   - Uses a mix of:
     - **Thrown potions** → negative effects for player / arena.
     - **Self-drunk potions** → buffs or defensive tools.
   - Predictively throws potions into the player’s path, punishing lazy strafing and camping.

3. **Transition / escalation**  
   - In early phases: once all brewed potions are used, she plants the cauldron, unleashes a paralyzing shockwave, and starts a new brewing cycle.
   - In Phase 3: brewing becomes automatic; she stops using the shockwave and becomes more mobile and evasive.

4. **Repeat**  
   - Space control, chaos and overlapping effects gradually increase.

### 4.2 Phase Overview

- **Phase 1 — Introduction**
  - 3 potions per cycle.
  - Simple patterns, slower usage.
  - Paralyzing shockwave at the end of each brew cycle.
- **Phase 2 — Escalation**
  - 4 potions per cycle.
  - Faster usage, more overlapping hazards.
  - Arena starts feeling “dirty” and segmented.
- **Phase 3 — Frenzy**
  - Potions brew automatically (no pause at cauldron).
  - No more shockwave placement; she relies on movement & potions.
  - Strong emphasis on mobility, burst decision-making, and survival in a heavily corrupted arena.

---

## 5. Potions

Each potion has two modes:

- **Self:** She drinks it → positive buff.
- **Thrown:** She throws it at or near the player → negative effect or hazard.

### 5.1 Healing Potion

- **Self:**
  - Heals a chunk of her HP.
  - Used more often at low HP (AI bias towards survival).
- **Thrown:**
  - Converts part of the player’s HP into temporary HP that decays over time.
  - Design intent: punishes greedy face-tanking and makes “fake safety” moments.

### 5.2 Poison Potion

- **Self:**
  - Coats her skin in poison — hitting her applies a Poison DoT.
  - Encourages players to back off instead of brainless melee spam.
- **Thrown:**
  - Spawns 1 large poison puddle and 3 smaller ones around it.
  - Puddles linger, forcing the player to reposition and segmenting the arena.

### 5.3 Shadow Potion

- **Self:**
  - Grants partial invisibility and movement speed for a short time.
  - The next attack coming out of invisibility:
    - Stuns the player.
    - Deals bonus burst damage.
- **Thrown:**
  - Summons 3 shadow entities:
    - Low damage, high speed, medium HP.
    - Their role is to delay/chase the player, not to kill.

### 5.4 Blood Potion

- **Self:**
  - She sacrifices some HP, causing blood spikes to travel along the floor in straight or curved lines.
  - If spikes hit the player, she heals.
  - Risk–reward behavior that makes her “play like a glass cannon player” at times.
- **Thrown:**
  - Direct damage projectile that also heals her on hit.
  - Good for punishing players who carelessly eat projectiles instead of dodging.

### 5.5 Holy Potion

- **Self:**
  - Grants a temporary magic barrier (e.g. 10% of max HP).
  - Cleanses debuffs from herself.
  - Used more frequently when she is pressured or low.
- **Thrown:**
  - Marks an area with a light beam that tracks the player for a short time, then locks and detonates into a damaging zone.
  - Forces the player to leave “comfort spots”.

### 5.6 Aether Potion

- **Self:**
  - Amplifies other potion effects (radius, damage, shadow HP, etc.).
  - She can drink it at almost any point → global escalation of the arena state.
- **Thrown:**
  - Spreads Aetherfire across the ground in irregular patches.
  - Not just simple circles — patterns of fire expand in asymmetric shapes, making safe zones less predictable.

---

## 6. Behavior & AI

### 6.1 Positioning

- Prefers to move along the **outer ring** of the arena.
- Constantly tries to:
  - Maintain a medium distance from the player.
  - Avoid being cornered.
- Movement style: slow but deliberate, “walking away” while casting and throwing.

### 6.2 Anti-Melee Behavior

- If a melee player closes the gap:
  - Uses a short **staff combo** (1–3 hits) with light knockback and brief stagger.
  - If the player stays close or if she drops a hazard (e.g., Poison) at her feet:
    - She opens a **short-range portal** and teleports to the opposite side of the arena.
- **Design Intent & Uptime:**
  - The teleport is not just an escape tool; it is a **reset mechanic**.
  - If she drops poison at her feet, staying there would force the melee player to wait 10+ seconds (killing the pacing).
  - By teleporting, she pulls the fight to a clean area, ensuring the player maintains **combat uptime**.

### 6.3 Potion Targeting

- She rarely throws directly at the player’s feet.
- Instead, uses **Predictive AI**:
  - Calculates the player's velocity and trajectory.
  - Aims **slightly ahead** of the player’s movement direction (intercept course).
  - Tries to cut off escape paths or "favorite" movement patterns.
- This keeps the player in motion and punishes predictable circle-strafing.

### 6.4 Territory Control

- Her goal over the fight:
  - Fill the arena with:
    - Poison puddles.
    - Aetherfire patches.
    - Light zones.
    - Shadow minions and blood spikes.
- The longer the fight lasts, the more the arena feels like a dangerous puzzle of temporary safe spots.
- This strongly punishes static builds and rewards players who can adapt and read patterns.

### 6.5 Low HP Behavior

- At low HP, her decision-making skews towards:
  - More frequent use of:
    - Healing Potion (self).
    - Holy Potion (self).
    - Shadow Potion (self → invis + reposition).
  - More aggressive space denial:
    - Increased chance to use Aether Potion to ramp up hazards.
- The fight becomes less about “just finish her” and more about managing risk while her kit tries to stall and outplay the player.

---

## 7. Phase Details

### Phase 1 — Introduction

- 3 potions per brewing cycle.
- Slower throwing cadence.
- Shockwave mechanic:
  - After using all brewed potions, she plants the cauldron in the center.
  - Charges a paralyzing AOE wave that:
    - Pushes the player away.
    - Paralyzes if not dodged.
  - If the player avoids the wave, they get a short damage window.
  - If hit, they lose the window and she safely starts a new brew.

### Phase 2 — Escalation

- 4 potions per brewing cycle.
- Higher usage speed, more overlap.
- More frequent “bad combinations”, e.g.:
  - Shadow minions + poison puddles.
  - Light zones + blood spikes.
- Arena starts to feel divided into functional “sectors” of danger.

### Phase 3 — Frenzy

- Brewing becomes **automatic**:
  - No long pauses at the cauldron.
  - She uses potions on the fly, while moving and teleporting.
- She stops planting the cauldron and using the paralyzing wave.
- Stronger focus on:
  - Fast throws.
  - Self-buffs.
  - Invisibility into surprise attacks.
- Design intent: final act is about survival and quick decision-making inside a fully contaminated arena.

---

## 8. Death & Rewards

### 8.1 Death Animation

- **The Failed Swing:**
  - At 0 HP, she attempts to swing the cauldron from her back for one last attack.
  - Due to exhaustion, she lacks the centrifugal force to complete the arc. The cauldron tips mid-swing, pouring the raw alchemical base directly **over her shoulders and head**.
- **Dissolution:**
  - She dissolves almost instantly into crimson smoke under the torrent of the base liquid. The cauldron clatters to the floor.
- **The Vials (Loot Mechanics):**
  - The floating potion vials (representing active phases) remain suspended for a brief moment after she vanishes.
  - **Gravity kicks in:** The vials fall onto the remaining **Cloak**, shattering on impact.
  - **Visual Feedback:** The colored fluids from the shattered vials soak into the fabric, visually confirming which elemental buffs the dropped item has acquired.

### 8.2 Rewards (Concept)

- **Alchemist’s Satchel**
  - Increases maximum potion capacity for the player by +1.
- **Crimson Witch’s Staff**
  - Enhances player potions or alchemy-based abilities.
  - Possible mod: increases effect power but also adds small risks.
- **Crimson Witch’s Cloak**
  - Grants passive bonuses based on which potion types were active when she died.
  - Examples:
    - Healing: +Max HP or reduced damage taken.
    - Poison: +Poison damage or resistance.
    - Shadow: +Shadow damage or reduced shadow damage taken.
    - Blood: +Physical damage or small lifesteal.
    - Holy: Regenerating barrier or holy damage bonus.
    - Aether: +All magic damage or reduced magic damage taken.
- Design goal: reward players not just for victory, but for **how** they fought her.

---

## 9. Respawning & Progression Hooks

Optional system for long-term replayability:

- After first defeat, crimson vines grow from the spikes toward the center, forming a flower-like cocoon.
- To re-summon the boss, players need an **Alchemist’s Pearl**:
  - Crafted using materials found in the Witch’s laboratory.
  - Placed into the central alchemical circle.
- Up to 6 additional materials can be added to:
  - Increase difficulty (more hazards, more HP, faster potions).
  - Improve rewards.
- During the ritual, matching circle patterns on the arena glow to visually show which modifiers are active.

---

## 10. Author

**Design & Document:**  
Timur Lepiostkin (coLoLrizer)  

This document is part of a personal game design portfolio and is intended to demonstrate boss, combat, and system design skills.

