# NO HIT! — Solo Boss Fight, Built in 4 Days in an Unfamiliar Engine

**Role:** Solo Designer & Developer
**Event:** CrazyGames x Construct Game Jam 2026 (Theme: *OVERPOWERED*)
**Timeframe:** 4 days, first-ever time using Construct 3
**Tools:** Construct 3 (free tier), JavaScript (via AI-assisted coding), AI-generated art (Dreamina, Leonardo, Playground AI)
**Status:** Shipped, submitted, judged

---

## Concept

The brief was simple: a boss fight where the enemy is genuinely, mechanically overpowered — not the player. A small green square walks into a dungeon expecting a starter weapon and a tutorial enemy, and instead a seraph-like entity with six wings, rotating rings, and a central eye erupts out of a portal and unloads laser barrages, bullet-hell projectile waves, and dash-based melee rushes.

The theme brief from the organizers explicitly named this angle as valid ("*Maybe it's the enemy that's too powerful and all you can do is hide, think Alien: Isolation*"), so the design leaned all the way into it — including a deliberate "fail state" baked into the code itself (see **Design Decision: The Crash**, below).

---

## Constraints

- **First day in Construct 3, ever.** All previous prototyping experience (Crimson Witch, Mindbreaker) was in Python. No familiarity with Construct's event system, behaviors, or JS interop going in.
- **Free tier event limit** (40 events, 50 after email verification). Meant almost the entire game logic had to live inside two JavaScript blocks rather than Construct's native event sheets.
- **4-day dev window**, further cut into by recurring power outages (Sumy, Ukraine) — including one outage that hit mid-playtest, forcing a mid-session switch to a laptop.
- **No prior JS experience for this specific stack** — logic was translated from known Python patterns (used in the Crimson Witch design doc) into JS with AI-assisted coding help.

---

## Design & Technical Breakdown

### Movement (WASD move +  SHIFT dash)
Construct’s built-in keyboard input mechanism did not work with the WASD keys for control. The issue was resolved by directly intercepting the browser’s raw `keydown`/ `keyup` events and controlling movement using the `vectorX/vectorY` properties of the ‘Move’ behaviour in JavaScript — in this way, the number of events, which would otherwise have been four or more, was reduced to a single block of JavaScript code, which also resolved the event limit issue in the free version. (Looking back, I wish I’d just used those four events lol)

Dash was implemented as a temporary `maxSpeed` spike (1500) held for 0.12s on a 0.5s cooldown, using the stored input vector at the moment of activation.

### Boss Attack Pattern: Predictive Targeting
Ported the predictive-aim logic originally designed for the Crimson Witch boss (Python) into JS: the boss calculates a player-intercept point based on current velocity and estimated time-to-impact, rather than aiming at the player's current position — punishing predictable strafing, consistent with the "read the player like a player" design pillar used across both projects.

```javascript
const flightTime = distToPlayer / 500;
boss.memorizedX = player.x + pvx * flightTime * 0.6;
boss.memorizedY = player.y + pvy * flightTime * 0.6;
```

Player velocity had to be reconstructed manually via frame-to-frame position deltas, since reading it directly from the behavior object was unreliable when the behavior wasn't guaranteed to be present.

### Attack Choreography
A three-dash rush pattern was one of the core early-phase attacks: the boss performs three consecutive eased dashes (`easeOutCubic`, 0.7s each) covering 80% of the distance to the player, memorizes the player's post-dash position, then spawns a 10-projectile ring burst from that point. Getting the *order of operations* right here was a real bug — the position was originally memorized *before* the dash instead of after, which broke the read-and-punish logic that made the attack fair. Fixed once caught.

### Death & Respawn (the hardest technical problem)
The most disproportionately painful part of the build. `Restart Layout` in Construct does **not** reset JS-side global state — so naively destroying the player object and restarting the layout left orphaned projectiles, a boss stuck mid-attack, and null-reference crashes from code still trying to act on a destroyed object.

The fix that actually worked: **never destroy the player.** Instead:
- Hide and disable the player (`visible = false`, `enabled = false`)
- Run a respawn timer, then reposition and re-enable
- Explicitly reset all boss state (`rushState`, `rushPhase`, `projectiles`, timers) and manually destroy every live projectile instance via `getAllInstances()`
- Guard all movement code with `if (!player || !player.visible) return;`

This pattern — treat objects as puppets to hide/reset rather than destroy/recreate — ended up being the single most reusable lesson from the whole project for any Construct-based state reset.

### Boss Visual Design
The seraph sprite and its idle animation (6 frames: closed wings → inhale/open → peak with rotating rings → exhale/fold → micro-flinch with ring-kick and eye-blink → inertial return) were AI-generated and composited by hand (background removal, frame sequencing into a sprite sheet) to hit a specific "ornate, wrong, too beautiful to be safe" visual tone that matched the "you walked in for a starter sword and got a seraph" narrative beat.

---

## Design Decision: The Crash

After 25 failed attempts, the game intentionally overloads the browser tab's memory and crashes it — a scripted "GET OUT" state rather than a random failure. This was a deliberate, if risky, choice to push the OVERPOWERED theme past the fiction and into the actual player experience: the boss isn't just narratively unbeatable, the *engine itself* eventually refuses to keep running the fight.

**What worked:** every playtester (including a mentor who logged 75 attempts) confirmed the boss reads as genuinely, mechanically overpowered — not artificially unfair, but a real, learnable, brutal wall.

**What didn't fully land:** several testers (including friends and a written community review) noted the crash mechanic actively discourages replay and could plausibly be misread as malware-like behavior by anyone encountering it without context — a fair critique, and one I'd solve differently in a post-jam patch (e.g. a scripted "fake crash" screen instead of an actual memory overload).

**Retrospective note:** the submission form for the jam had no dedicated field to flag this as intentional (only a general "this game works as intended" checkbox meant for standard publishing, not competition entries), so the only explicit disclosure lived in a community Discord thread — a distribution channel judges weren't guaranteed to see. In hindsight, embedding the disclaimer directly in-game (a loading screen note, for example) would have been the safer call regardless of form limitations.

---

## Boss Design Breakdown

The fight is built as two phases of five attacks each, all fully deterministic and telegraphed — every attack shows its danger zone before it deals damage. One hit kills the player; the fight lives or dies on readability, not raw reaction speed.

### Intro
A 7-second scripted text sequence sets up the fiction before the fight starts: *"You are a small green square... You came to the dungeon for your first weapon... And your first enemy will be... THIS!"* — establishing the mismatch in stakes before the player ever sees the boss move.

### Phase 1

| # | Attack | Core Mechanic | Read / Counterplay |
|---|---|---|---|
| 1 | **Rush** | 3 dashes toward the player; each lands and spawns 8 claws radiating outward in a rotating ring (22.5° offset per rush so gaps don't overlap) | Stand in the gaps between claws |
| 2 | **Laser Fan** | 5 fixed beams + 1 predictive beam that locks onto the player 0.2s before firing, across 4 volleys | Avoid the predictive beam's line, weave through the fixed fan's gaps |
| 3 | **Giant Laser** | One wide beam does a full 360° rotation over 1 second; rotation direction is chosen based on the player's current movement vector (cross product) | Outrun the beam's rotation speed |
| 4 | **Rapid Telegraphs** | 8 warning lines spawn simultaneously from screen edges, aimed at a predicted player position, across 3 waves | Find the one safe pocket where lines don't intersect |
| 5 | **Charge** | Boss exits off-screen left, tracks the player's Y, then charges across with eased acceleration, dropping projectiles in a checkerboard pattern along the way — repeats 3 times | Stay off the charge's vertical line |

### Phase Transition
After 2 full attack cycles, the boss flashes, pulses, and shakes for 1.5 seconds before escalating into phase 2 — a clear, unmissable beat that tells the player "it gets worse now."

### Phase 2
Every phase 1 attack returns, restructured and layered with additional mechanics:

| # | Attack | What Changed |
|---|---|---|
| 1 | **Rush** | 5 dashes instead of 3; each spawns *two* claw rings (inner + outer, different speeds) instead of one; ends in a delayed expanding explosion the player has to outrun after weaving the rings |
| 2 | **Laser Fan + Shrapnel** | 6 volleys instead of 4; a 20-projectile radial burst fires simultaneously with the laser fan, forcing the player to track two attack types at once |
| 3 | **Twin Giant Lasers** | Two opposing beams instead of one, rotating slowly over 3 full rotations, each firing an 8-projectile volley every 22.5° of rotation |
| 4 | **Rapid Telegraphs (Top-Only)** | 24 lasers instead of 8, all from the top edge, fired individually at 0.15s intervals — trades spatial complexity for pure tempo pressure |
| 5 | **Charge + Reverse Fan + Wall** | The charge now triggers a full laser fan back toward its origin point on arrival, with only a ±12° safe corridor, while projectiles simultaneously approach from the opposite edge like an advancing wall |

### Victory & Death
Clearing all of phase 2 fades the screen to a "VICTORY!" state before resetting. Dying resets the player and clears all boss state — except after **25 deaths**, where a scripted "GET OUT!" sequence triggers instead (see *Design Decision: The Crash* below).

### Design Notes
- Every attack uses **predictive aiming** rather than aiming at the player's current position — consistent with the "boss plays like a cautious player" pillar carried over from the Crimson Witch design.
- Phase 2 isn't a new attack set; it's the *same five attacks* under load — more projectiles, more simultaneous layers, tighter safe corridors. This kept the fight's vocabulary small enough to learn while still making the power escalation legible without new telegraphs to memorize from scratch.
- All attacks run as independent state machines on the boss object, which made it possible to reuse timing/easing logic (like the predictive-intercept math from Crimson Witch) across nearly every attack instead of writing bespoke logic per pattern.

---

## Reception

- 138 total submissions to the jam; NO HIT! is very likely the only pure boss-rush entry among them.
- Feedback consistently confirmed the theme lands cleanly and without stretching ("*the enemy feels truly overpowered*" — community review), but just as consistently flagged the difficulty ceiling as a barrier to long-term engagement — a real, expected trade-off of the design, not a miss.
- A mentor play-tested to 75 attempts without clearing phase one, and described the difficulty spike as legitimate rather than unfair once he understood the pattern-based nature of the fight.

---

## What I'd Take Into the Next Project

- **Fairness vs. learnability are not the same axis.** A fight can be 100% deterministic and dodgeable and still not read as "fair" to a first-time player if the telegraphs aren't legible enough on first contact. Some of NO HIT!'s early attacks (dash-in cues, off-screen repositioning) needed to lean on the *player's* pattern memory more than their in-the-moment reaction — a valid design space, but one that needs to be flagged to the player up front, not discovered the hard way.
- **Bold mechanical risks need equally bold communication.** The crash-as-feature idea was mechanically sound and thematically justified, but its impact was undercut by having no reliable channel to explain it to the exact audience (judges) who needed that context most.
- **Constraints breed reusable patterns.** The "hide and reset, don't destroy" respawn pattern, and the raw-keydown movement workaround, are both things I'd reach for by default in any future Construct project — even outside a jam context.
