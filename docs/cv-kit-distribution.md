# CV kit installation and validation

The original `geekbye-cv-kit` is separate from the curated upstream catalog. The existing catalog installer and its telemetry opt-out behavior are unchanged.

## Install the preview

```sh
npx skills@1.5.26 add 'aiescu/agent-skills#codex/geekbye-cv-kit' --skill geekbye-cv-kit
```

After publication on main, use:

```sh
npx skills@1.5.26 add aiescu/agent-skills --list
npx skills@1.5.26 add aiescu/agent-skills --skill geekbye-cv-kit
```

The pinned CLI requires Node.js >=22.20.0. Basic rendering uses Python 3.9+ and the standard library. Tectonic is required for PDF compilation; Poppler and pypdf support independent extraction checks. Rendering needs no account credentials or sibling repository.

## Reproduce verification

```sh
npm test
npm run build
npm run build:check
npm run test:cv-kit-install -- 'aiescu/agent-skills#codex/geekbye-cv-kit'
```

The explicit network test uses a temporary HOME, cache and project, disables test telemetry, compares installed assets with the local package and runs the installed example. Its raw machine-specific logs stay outside the repository. Run against a checkout matching the selected public revision. The basic install example deliberately skips compilation; it does not establish PDF, model-drafting or ATS performance.

The package includes public synthetic examples, reproducible runtime checks and a [paired drafting evaluation](cv-kit-evaluation/README.md). These tests do not establish universal ATS compatibility. All candidate examples in this repository are fictional.

## Directory visibility

Successful CLI discovery and installation do not verify a Skills.sh listing. On 2026-09-16 the checked repository page was unavailable, the proposed skill page displayed an unavailable message despite HTTP 200, and exact-source/name search did not establish a listing. No directory badge is presented as verified.

[Skills.sh documentation](https://www.skills.sh/docs/faq) describes discovery through genuine CLI installation telemetry. Preserve `DISABLE_TELEMETRY=1` and `DO_NOT_TRACK=1` preferences. Test installs are not indexing activity. Verify rendered directory content and actual source/name before adding a listing link or badge; no indexing deadline is guaranteed.
