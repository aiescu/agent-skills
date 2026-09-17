# Original source and modifications

This is an original Aiescu skill, not a re-hosted upstream instruction pack.

The bundled renderer, candidate schema and synthetic data are original Aiescu work distributed under the MIT license in `LICENSE`. This public repository is the source for the portable package. No private candidate documents or third-party template implementations are included.

The runtime, application workflow, contracts and expanded synthetic examples were authored for this skill. Adaptations to the original renderer/parser include year-only dates, neutral education-date labels with legacy parsing compatibility, correctly labeled publication URLs, preserving empty real candidate names without sample placeholders, and an additive legacy builder adapter. LaTeX packages and fonts are compiler dependencies supplied by the user's TeX installation/Tectonic bundle; no third-party fonts, layouts or instruction packs are vendored here.

The canonical source of this portable package is `aiescu/agent-skills`, `skills/geekbye-cv-kit/`. Product-site template copies must be generated snapshots of this directory with recorded revision/hashes. Do not independently edit that snapshot and let the two renderers diverge.
