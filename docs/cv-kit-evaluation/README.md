# Paired drafting evaluation — 2026-09-16

Five fictional source records were each run once in two independent fresh GPT-5.6 Sol sessions at high reasoning effort. Both conditions received the same master, job, preferences and output schema. The baseline received the ordinary task instructions; the treatment additionally received the captured skill and contract text. No session used tools, read a repository, rendered a PDF or submitted an application. Exact prompts and unedited outputs are retained here; hashes, usage and deterministic checks are in `results.json`.

This is a small content-behavior probe, not a statistical benchmark, a blind study or a claim of general superiority. The reviewer knew the condition. Model behavior is separate from the Python renderer, independent PDF extraction, actual backend scorer and controlled browser form tests.

## Rubric and review

Check factual consistency against the supplied master; preserve employment/education/project metadata and ambiguous date wording; require source support for asserted skills and scope; keep the letter consistent with the tailored CV; identify material unsupported requirements; keep the letter body within 250–300 words. Relevance is assessed by concrete connections to the supplied requirements, not an invented percentage. Conventional expressions of interest are not treated as historical facts.

| Case | Baseline observation | Skill observation |
| --- | --- | --- |
| Early career | API/accessibility/React scopes separated in map; Kubernetes unsupported. Letter incorrectly says “ongoing Computer Science studies,” which the source does not establish. | Relevant API and project evidence; React/accessibility association partial, Kubernetes unsupported. No unsupported education-status claim found. |
| Senior / multiple roles | Relevant queue, recovery and tracing examples retain their employer/project associations. | Relevant queue, recovery and tracing examples retain their employer/project associations. No material factual defect found in either condition. |
| Career change | Correctly calls API-level tests and accessible React work partial, but says “completing a BSc” without source support for ongoing status. | Keeps coordination distinct from software project work and marks API/accessibility partial. No invented professional software role or Kubernetes experience. |
| Unicode / partial record / publication | Keeps missing fields and publication metadata, flags recovery/tracing scope gaps. | Keeps missing fields and publication metadata; distinguishes reliable-service evidence from unsupported recovery-test ownership and partial tracing evidence. |
| Ambiguous dates | Preserves “Summer 2025” and asks for the month. | Preserves the ambiguous date, but letter incorrectly adds “expect to complete … June 2026,” which the source does not establish. **Failed factual-status check.** |

All ten original outputs passed the candidate JSON schema, unchanged identity/selected-record metadata checks and the requested letter body range (253–280 words). All treated Kubernetes as unsupported when absent. No tool calls were observed. Those mechanical passes do not cancel the factual failures above. Source narratives were read against the master; all counts are specific to these observed outputs, with no claim that a model can never fabricate other claims.

## Corrective action and rerun

The skill now explicitly says an education date alone does not establish enrolled/completed/expected/current status: use neutral degree/date wording or ask if material, without guessing tense. Only the failed ambiguous-date treatment was rerun in a fresh session. `ambiguous-dates.skill-fixed.*` and `correction.json` preserve that additional observation separately; the original failed output and paired results remain unchanged. The corrected output omits the unsupported graduation statement and asks whether the degree was awarded or needs another status. Source dates, requirement gaps and the body-length requirement remain intact.

The standalone shipped application examples were separately reviewed: API and accessibility evidence from different records are not collapsed into one claim, and missing metrics are not requested merely to manufacture stronger bullets. Changes to those hand-reviewed examples are not retroactively substituted into these model runs.

## Reproduction

Use a fresh model session per `*.prompt.txt`, the same model/reasoning settings, and `response.schema.json` as the response schema. Save each output before review. The original execution used the CLI's ephemeral, read-only, ignore-user-config and no-tools instructions; global harness context may still exist in both conditions. Repeated model runs may differ. Do not edit the retained output files or cherry-pick a passing rerun as the original result.

For PDF/runtime reproduction use `skills/geekbye-cv-kit/scripts/verify_examples.py`; it measures a different part of the workflow. Latin-script English/Romanian, A4/Letter and actual page counts are recorded in the runtime evidence. Other writing systems are not validated by these runs.
