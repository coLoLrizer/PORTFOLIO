# Monolith Orbit Recast — Technical Game Design Case

## 1. High-Level Problem Statement

**Ability:** Monolith (tethered orbital weapon)  
**Genre:** Action / Top-down combat  
**Core fantasy:** A massive stone bound to the player by a chain, behaving like a controlled yoyo — never breaking flow, never invading camera space, always choosing the most powerful-looking trajectory.

![Def](https://github.com/user-attachments/assets/e5fcec1a-77a2-425a-a4df-8c76903bbb63)

### The Core Problem

Designing a throwable, tethered object that:

- Always orbits **around** the player (never through them)
- Always chooses the **largest, most expressive arc**
- Allows **recasting at any cursor position**, including directly under the player
- Remains readable and stable under **camera rotation**
- Never breaks player spatial intuition

This sounds trivial until you actually try to implement it.

---

## 2. Initial Naive Approach — 2-Sector World Split

### First Attempt

The earliest version split the world into **two halves** relative to the player:

- Cursor is either on the **left** or **right** side
- The monolith flies out from two precisely defined points perpendicular to the screen division, exactly in the center of the circle. (180 degrees)
- Monolith always chooses different side to fly out and the same side to get onto orbit.

### Why It Failed

This approach worked **only** when player gase the same side with **Monolith** (180 degrees)

The moment the camera rotated behind **Monolith** the pattern brokes (the monolith began to make a V-shaped movement)

**Key failure:**  
Binary space division is not rotationally invariant.

---

## 3. Second Attempt — Quadrant-Based Reasoning (Breakthrough)

### The Key Insight

The world must be divided **relative to the player**, not the screen.

Instead of 2 sectors → split the space into **4 quadrants**, centered on the player:

- Q1 / Q2 / Q3 / Q4  
- Defined by the player’s forward-facing reference

This immediately stabilized behavior under camera rotation.

---

## 4. Design Goal Redefined

At this point the goal became very explicit:

> **The Monolith must always travel along the largest possible arc around the player, regardless of cursor position.**

Even if The player spins the camera mid-action

---

## 5. The Core System — Tangents, Not Angles

### Why Angles Alone Are Not Enough

The previously calculated angles result in very rough behavior; the monolith begins to slow down when entering orbit, 
shakes and accelerates directly in orbit, which creates a very negative impression of the ability.

To preserve motion quality, the system must reason in **tangents**, not straight lines.

---

## 6. Dual-Tangent Model

At any moment, the system computes **two independent tangent pairs**:

### A) Monolith → Orbit Tangents  
Tangents from the **current monolith position** to the stable orbit.

### B) Cursor → Orbit Tangents  
Tangents from the **cursor position** to the same orbit.

These tangents define:
- Valid **entry points** into orbit
- Valid **exit points** from orbit

---

## 7. Phantom Orbit (Critical Innovation)

### The Problem

If the cursor is inside the orbit radius:
- Direct tangents collapse
- The monolith risks snapping or flying straight

### The Solution — Phantom Orbit

- A **secondary, dynamic orbit**
- Radius = ~95% of cursor distance
- Only exists when cursor is *inside* the main orbit
- Projects its tangent solution onto the **stable outer orbit**

**Result:**  
Even if the cursor is directly under the player, the monolith still performs a full yoyo-style arc around them.

(For context, this is necessary so that Monolith's ability gains damage from the archetype's passive ability while flying.)

---

## 8. Quadrant-Based Decision Rules

### Case 1 — Monolith in Front of Player (180°)

- Choose the **monolith tangent** on the *same side*
- Choose the **exit tangent** on the *opposite side*

Example:
- Monolith in Q1
- Use Q1→Q4 arc
- Cursor uses Q2→Q3 exit

This guarantees:
- Maximum arc length
- Clean visual wrap-around
- And not in front of the player

---

### Case 2 — Monolith Directly Behind Player (≈180°)

- Always select the **opposite-side tangent** for the monolith
- If unavailable:
  - Fall back to the rear-facing tangent
- Cursor exit is **always opposite**

This avoids:
- Short, awkward half-arcs (less damage from passive)


---

## 9. Recast Lock & Stability

To prevent oscillation and indecision:

- Once a side is chosen:
  - It becomes **frozen** for the duration of the orbit
- Recasts:
  - Temporarily boost angular velocity (This adds a branch node)
  - Apply an arc-based lockout (not time-based)

This ensures:
- Responsiveness
- No direction flipping mid-swing

You can keep a monolith in orbit for a long time like a yo-yo.

---

## 10. States Overview

- `FALLING_INIT` — Initial throw to ground
- `GROUNDED` — Idle, tethered
- `ENTER_ORBIT` — Snap to orbit entry
- `ARCING` — Stable orbital motion
- `FLYING_TANGENT` — Exit flight
- `CAPTURED` — Temporary immobilized state

Each state exists to:
- Preserve motion continuity
- Avoid teleportation
- Keep player intuition intact

---

## 11. Debug Visualization (Design Tooling)

To validate the system, a full debug overlay was built:

- Orbit rings (stable + phantom)
- Tangent lines (monolith & cursor)
- Active entry / exit points
- Quadrant highlights
- Side-lock indicators

This was essential for:
- Tuning
- Teaching the system to designers
- Proving correctness

---

## 12. Final Result

- The monolith **always** travels around the player
- Always chooses the **most powerful-looking arc**
- Never violates camera space
- Feels intentional, heavy, and readable
- Supports aggressive recasting without chaos

What began as a control problem became a **geometry-driven design system**.

---

## 14. Key Takeaway

> When an ability must *feel* correct,  
> solving geometry is not optional —  
> it **is** the design.

---

## 15. Author

**Design & Implementation:**  
Timur Lepiostkin (coLoLrizer)

This document is part of a personal technical game design portfolio and demonstrates spatial reasoning, iterative problem-solving, and player-centric motion design.
