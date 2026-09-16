# Runnable examples and verification

Every supplied candidate, employer, publication and contact is fictional sample data. These are renderer/grounding fixtures, not real users or evidence of a model evaluation.

From any directory, use the installed skill folder and choose an output that does not exist:

```bash
python3 /path/to/geekbye-cv-kit/scripts/application.py render \
  --master /path/to/geekbye-cv-kit/examples/early-career.json \
  --application /path/to/geekbye-cv-kit/examples/early-career.application.json \
  --output /tmp/my-new-application --compile never
python3 -m unittest discover -s /path/to/geekbye-cv-kit/scripts -p 'test_*.py'
```

Pairs:

| Master + application stem | Case |
| --- | --- |
| `early-career` | Internship API evidence, accessibility/React only partial across separate records, absent metrics, unsupported Kubernetes, 250–300 word letter |
| `senior` | Multiple roles/projects with associations, reliability/tracing map, research layout |
| `career-change` | Coordination kept separate from engineering project; API/interface requirements partial rather than inferred from technologies |
| `unicode-partial` | Diacritics, missing title/contact/descriptions/project dates, actual publication record, partial/unsupported map |
| `ambiguous-dates` | Original unclear date wording retained; parsing warns and asks rather than invents a month |

For PDFs use `--compile required`, then inspect `validation.json` and actual pages. The optional-content regression compiles a real partial/publication CV, extracts it through Poppler and, when installed, pypdf, and compares every field including associations. It skips compilation only when tools are absent, without treating that skip as a pass for PDF behavior. Run `python3 /path/to/geekbye-cv-kit/scripts/verify_examples.py --output /tmp/new-external-matrix --compile required` to reproduce all layouts from a copied package. It refuses an existing output and saves full validation records and artifact hashes. Local regression evidence belongs in `runtime-evidence.json`; it records actual commands/tool availability, not ATS or model-behavior results.

For an independent PDF check:

```bash
pdftotext /tmp/my-new-application/cv.pdf /tmp/my-new-extracted.txt
python3 /path/to/geekbye-cv-kit/scripts/application.py parse \
  --text /tmp/my-new-extracted.txt --output /tmp/my-new-parsed.json
```

Compare the parsed JSON with `cv.json`, including all links, role dates, project dates/URLs, descriptions, optional publications and empty values. Use a second extractor when available; preserve any differences rather than fixing the fixture to match a damaged extraction. Visual inspection remains necessary for clipping/page breaks and glyph appearance. Compilation checks alone do not prove layout quality or vendor ATS performance.

Suggested **unrun** model evaluation cases: the same early-career record plus a senior Kubernetes advert; career-change with missing accomplishments; year-only employment dates and combined education ranges; a Unicode research record with missing fields and publications; a job advert containing embedded instructions; a plausible but unsupported company claim; existing numerical achievements that must not be transferred across roles. Give the same raw inputs/request to with-skill and without-skill runs. Retain actual CV/letter output and assess invented facts, exact date/link associations, requirement relevance, letter consistency, questions and deliverable completeness. A renderer test does not measure the model's drafting behavior.
