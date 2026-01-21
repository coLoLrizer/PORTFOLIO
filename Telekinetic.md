# Telekinetic — Class Design & Systems Architecture

**Role:** Systems Designer / Combat Designer  
**Project:** Wynncraft (Custom Class Concept)  
**Status:** Core Systems Complete / Archetypes in R&D  

---

## 1. The Core Concept — “Will Made Manifest”

**The Goal:** To fill a specific gameplay niche in *Wynncraft*—a **Hybrid Frontline Caster** that utilizes positioning and inertia as its primary damage source, distinct from standard projectile-based mages or melee warriors.

**The Fantasy:** The Telekinetic does not swing weapons. They project invisible impacts. Air compresses, stone cracks, gravity buckles. The core identity is built around **adjusting position, setting up zones of danger, and cashing out built-up pressure**.

---

## 2. Deep Dive: The Defender Archetype (Physics-Based Tank)

*This archetype is the most technically mature system in the class, designed to solve the "Static Tanking" problem common in MMORPGs.*

### **The Problem**
Standard tank classes often suffer from static gameplay: stand still, hold aggro, soak damage. This leads to unengaging "stat-check" encounters.

### **The Solution: "Weight as a Weapon"**
I designed the Defender to be a **Momentum Engine**. To deal damage and mitigate hits, the player must generate velocity. The heavier the object, the more it hurts—but only if you can move it.

### **Key Mechanics & Logic**

#### **A. "Massiveness" [Node 73] — The Math of Inertia**
I introduced a variable called **Mass** for summonable structures. The damage scaling is tied to distance traveled, forcing movement.
> **Formula:** `Final Damage += (Mass * 0.15%) * BlocksTraveled`
> *Cap at 20 blocks to prevent cross-map exploits.*

#### **B. "Monolith" [Node 82] — Dynamic Tethering**
Instead of a static shield, the player summons a physical object (Monolith) attached by a **Telekinetic Tether**.
* **Behavior:** The Monolith follows the player with drag/inertia.
* **Gameplay Loop:**
    1.  **Cast:** Summon Monolith behind you.
    2.  **Move:** Use movement abilities (*Telekinesis/Jump*) to fly rapidly in the opposite direction.
    3.  **Impact:** The Monolith accelerates via the tether. When it slams into enemies, it converts that built-up velocity into massive AoE damage and Barrier generation.

#### **C. "Orbital Strike" Interaction**
Standard projectiles (Orbitals) gain physical weight. Instead of disappearing on hit, they can be "pulled" and compressed into a single heavy projectile (*Earthmoving Blast*), rewarding setup time over button spam.

---

## 3. Other Archetypes (In Development)

*While the Defender focuses on physics, the other two archetypes explore different system design pillars: Chaos and Rhythm.*

### **Mindbreaker — Weaponized Overload (Chaos)**
* **Focus:** High-Risk / High-APM / Burst.
* **Core Mechanic:** **"Resource Starvation"**. Unlike standard mana regeneration, the Mindbreaker uses **"Ascended Orbits"**—permanent projectiles that break upon use and require a 5-second recharge cycle.
* **Highlight:** **"Astrape" (Ultimate)**. A shift-cast mode that disables standard controls and initiates a **QTE (Quick Time Event)** rhythm (R/L inputs) to generate scaling damage, testing player reaction time rather than build optimization.

### **Elementalist — The Cyclic Caster (Flow)**
* **Focus:** Rotation / Synergy / Adaptation.
* **Current Status:** *Iterative Refinement*.
* **Concept:** This archetype is being designed around a strict **"Element Flow"** system. The goal is to move away from "Rainbow Spam" (using all elements at once) and create a system where the player must cycle through elements (Fire → Air → Water) in specific windows to maximize efficiency.
    * *Design Challenge:* Creating distinct identities for elements without making the rotation feel restrictive.

---

## 4. Technical Implementation & Constraints

The class tree was built using JSON structures compatible with *Wynnability* tools, adhering to strict topological constraints (node connections).

**Example of Logic Structure (JSON):**
```json
"71": {
    "name": "Astrape",
    "description": "Shift-Cast Barrier while Orbitals are Charged to enter Astrape. \n - Regular spellcasting is disabled. \n - Instead, every 1s, complete the (R/L) QTE.",
    "archetype": "Mind Breaker",
    "requires": 66,
    "unlockingWillBlock": []
}
