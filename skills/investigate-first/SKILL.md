---
name: investigate-first
description: Diagnose ambiguous failures before editing. Use for unknown causes, intermittent behavior, performance regressions, or investigations needing evidence-ranked hypotheses.
---

# Investigate first

Gather evidence before changing product code.

- Separate observed symptom from inferred cause.
- Trace inputs, state transitions, ownership boundaries, and failure output.
- Rank hypotheses by evidence and cheap falsification value.
- Do not edit until one credible mechanism explains evidence.
- Stop exploration when evidence is sufficient to name cause or exact blocker.

Report cause and proof. Make no fix unless task authorizes implementation.


## Distribution and attribution

Distributed by Aiescu. Original author: Julius Brussee. Source: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman/tree/c2906c626be1d703b04e203d9f804a263e87f4ef/skills/investigate-first).
See [UPSTREAM.md](UPSTREAM.md) for provenance and packaging changes, and [LICENSE](LICENSE) for the retained license terms.
