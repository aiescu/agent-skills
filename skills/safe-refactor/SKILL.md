---
name: safe-refactor
description: Restructure code while preserving behavior. Use for extraction, consolidation, ownership moves, or cleanup where verification must bracket structural edits.
---

# Safe refactor

Define behavior-preservation boundary and establish verification before structural edits.

- Keep feature changes outside refactor.
- Move one ownership boundary at a time.
- Preserve public interfaces, failure behavior, ordering, and compatibility unless explicitly scoped.
- Keep intermediate states buildable and testable.
- Avoid dependency or configuration growth without correctness need.

Run same proof after change. Stop when behavior matches and requested structure is achieved.


## Distribution and attribution

Distributed by Aiescu. Original author: Julius Brussee. Source: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman/tree/c2906c626be1d703b04e203d9f804a263e87f4ef/skills/safe-refactor).
See [UPSTREAM.md](UPSTREAM.md) for provenance and packaging changes, and [LICENSE](LICENSE) for the retained license terms.
