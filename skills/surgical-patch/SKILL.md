---
name: surgical-patch
description: Fix bugs and small behavior changes at the narrowest responsible layer. Use when regression proof, preserved surrounding behavior, and task-relevant tests matter.
---

# Surgical patch

Reproduce failure first when economical; otherwise capture strongest available evidence.

- Trace symptom to responsible mechanism.
- Change narrowest layer that owns incorrect behavior.
- Preserve unrelated behavior and user changes.
- Avoid cleanup, renaming, and abstraction outside fix.
- Add only regression proof relevant to task.

Run focused proof plus nearest affected gate. Stop when failure is fixed and regression proof passes.


## Distribution and attribution

Distributed by Aiescu. Original author: Julius Brussee. Source: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman/tree/c2906c626be1d703b04e203d9f804a263e87f4ef/skills/surgical-patch).
See [UPSTREAM.md](UPSTREAM.md) for provenance and packaging changes, and [LICENSE](LICENSE) for the retained license terms.
