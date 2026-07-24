# Blightfall: Crimson Veil — Design Postmortem

**Role:** Game Designer / Systems Designer  
**Team:** 7-8 person volunteer team  
**Duration:** 2 months  
**Context:** Hytale × CurseForge New Worlds Modding Contest

---

# 1. Overview

Blightfall: Crimson Veil was a volunteer Hytale project created for the CurseForge New Worlds Modding Contest.

I joined the team through the CurseForge Discord as a Game Designer. The project started with an ambitious PvE extraction concept.

My role was designing the core gameplay loop, systems, progression, encounters, and maintaining design consistency through documentation and design pillars.

This postmortem is not about presenting the project as a success story. The final build differed significantly from the original (my) design. The goal is to analyze why that happened, what I did well, where I made mistakes, and what I learned from the process.

---

# 2. Project Start

The project began with a lot of enthusiasm and ambitious ideas which came from all the developers; later, we set out the ideas on paper.

The initial direction was PvE extraction:

- A safe base as the player's starting point.
- Exploration of a dangerous world.
- Limited time outside the base.
- Resource gathering and progression.
- Gradual discovery and mastery of the map.

I developed this into a more complete gameplay loop:

**Prepare at base → Explore contaminated regions → Gather resources and progress → Return → Upgrade → Push deeper**

The Crimson infection became the main system connecting gameplay and narrative.

The infection was designed as an organic threat:
- A corrupted flower-like organism spreading through the world.
- A danger that grows over time.
- A force weakened by sunlight and connected to the player's exploration window.

---

# 3. What Went Wrong

## No clear production authority

The biggest structural issue was that the team had no producer or final decision-maker.

We had many motivated people, but nobody had the responsibility to make final scope decisions.

I tried to push for clearer ownership and structure, but it never became an established process.

As a result, many ideas survived simply because they sounded exciting.

---

## Idea Soup

The project entered an "Idea Soup" phase very early.

The problem was not that the ideas were bad. Many of them were genuinely interesting.

The problem was that we lacked a consistent filter:

> Does this support the core experience, and can we realistically build it in two months?

New concepts continued appearing:
- Larger boss concepts.
- Additional narrative layers.
- Extra gameplay systems (like abbilities for weapons).
- And more ambitious content...

Without a strong scope filter, the project kept expanding faster than it could be implemented.

---

## Design pillars were introduced too late

I suggested design pillars after realizing the project was losing direction, depends on what we actually want to make.

- Long Term Progression
- The Economy of Greed.
- Biological Time Pressure.
- Architecture Over RNG.
  
The team agreed with them, and they helped define the intended experience:
However, the pillars became a document rather than a shared production tool.
I continued using them to evaluate ideas, but the team did not consistently use them when making decisions.

---

## Different interpretations of the game

A major challenge was that different people had different ideas of what the final game should be.

My direction focused on:

- Extraction gameplay.
- Learning the world through repeated exploration.
- Environmental danger (PvE).
- Gradual progression.

Other parts of the team moved toward:

- More traditional RPG structure (open map to explore).
- NPC rescue mechanics.
- Larger fantasy lore.
- Divine-scale threats.

We discussed these differences many times, but never fully aligned on one unified vision.

---

## Scope mistakes

I was also responsible for some scope expansion.

During development, I proposed and considered ideas that were too ambitious for the timeframe.

Some examples:

- More complex world systems.
- Additional gameplay interactions.
- Larger systemic mechanics.

Many of these ideas were later reduced or removed.

The lesson was simple:

A good idea is not automatically a good idea for the current project.

---

## Documentation was not enough

I created a detailed GDD covering:

- Core gameplay loop.
- Progression.
- Economy.
- Crimson Escalation system.
- NPC framework.

However, documentation alone does not create alignment.

Ideas and decisions continued appearing in different places:
- Chats.
- Voice calls.
- Private discussions.

The GDD existed, but it was not always the single source of truth.

---

# 4. What I Contributed

## Core gameplay loop

I designed the main gameplay structure that connected exploration, progression, and the Crimson infection.

The goal was creating a loop where players gradually understand and master a dangerous world.

---

## Design pillars

I created the design pillars to stabilize the project's direction and provide a framework for evaluating new ideas.

---

## Systems design

I designed and documented:

- Crimson Escalation system.
- Progression structure.
- Crafting economy.
- Loot tables.

---

## Narrative-mechanics connection

A major design goal was making the lore affect gameplay.

The Crimson infection was not just a visual theme — it influenced:
- Exploration pressure.
- Time limits.
- Environmental danger.
- Player progression.

---

# 5. What Shipped vs Designed

| System | Designed | Shipped |
|---|---|---|
| Map | Multiple regions with progression-based exploration | Reduced map scope |
| Spawning | Region-based enemy distribution | Randomized spawning |
| Loot | Zone-based progression economy | Randomized loot |
| Crimson Escalation | Six-stage escalation system | Simplified implementation |
| Progression | Tier-based unlock structure | Did not function as intended |
| Bosses | Designed encounters with mechanics and counterplay | Basic combat behavior |

---

# 6. Lessons Learned

## Define roles before ideas

A team needs clear ownership before production starts.

Without someone responsible for scope decisions, ambition naturally grows faster than resources.

---

## "No" is a design tool

Small teams need someone who can reject ideas.

Not because ideas are bad, but because every addition has a cost.

---

## Pillars are a process, not a document

A design pillar only works when it actively influences decisions.

Writing it down is the beginning, not the solution.

---

## Validate scope early

Before accepting a feature, ask:

> Can this realistically be implemented within our current constraints?

If the answer is unclear, it belongs in a future backlog.

---

## Communication matters more than documentation

A perfect GDD cannot replace regular synchronization.

The team needs shared understanding, not just shared files.

---

# 7. Final Thoughts

Blightfall did not become the game we originally designed.

However, the project gave me experience that is difficult to gain outside real development:

- Seeing how projects lose direction.
- Understanding the importance of scope control.
- Learning the difference between having a vision and maintaining alignment.
- Experiencing the role of a designer inside a team, not just designing mechanics in isolation.

---

**Game Design & Documentation:** Timur Lepiostkin (coLoLrizer)
