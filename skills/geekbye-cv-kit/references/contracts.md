# Candidate and application contracts

## Master

`assets/candidate.schema.json` is the canonical v1 shape. Every field is present; missing scalar values are `""`, missing collections `[]`. No extra candidate fields are silently discarded. Strings include Unicode and supplied wording. Date tokens may be `YYYY`, `YYYY-MM`, or `Present` for an ongoing end date. Unclear wording is retained but strict parsing requires clarification. Dates are never normalized to invented months. The legacy canonical field `education[].graduationDate` records a supplied date without establishing enrolled, completed, expected or current status. Output uses the neutral label `Education date:`; the strict parser also accepts legacy `Graduated:` input for compatibility, without adding a status field.

Stable references are JSON pointers into this particular unchanged master, for example `/experience/0`, `/experience/0/description`, `/projects/1`, `/skills/2`. Output `change-log.json` records the master canonical JSON hash and, when called through the CLI, its original byte hash. Index pointers are not portable between reordered or edited masters: create a new map when the master changes.

When importing the legacy builder shape, explicitly convert `website` to a `links` entry and each skill `{id,name}` to its `name`, keeping additional links when supplied. Legacy project descriptions may bundle dates and URLs; separate only facts that can be established, and leave dates/URLs empty if uncertain. Preserve an original legacy input beside the canonical master. Runtime `cv.builder.json` provides the reverse adapter: it retains legacy `website`, skill objects and project description formatting, and adds canonical links, publications and project dates/URLs. This is an adapter, not proof that an older remote builder understands the added fields.

## Application

The complete runnable records in `examples/*.application.json` illustrate this shape:

```json
{
  "job": {
    "title": "Target role", "company": "Employer",
    "description": "Verbatim advert: Node.js APIs required.",
    "requirements": [{"id": "api", "text": "Node.js APIs", "sourceQuote": "Node.js APIs required."}]
  },
  "preferences": {
    "language": "English", "region": "Romania / EU", "cvLength": "1–2 pages",
    "letterWords": [250, 300], "paper": "a4", "layout": "compact"
  },
  "selections": {
    "experience": ["/experience/0"], "education": ["/education/0"],
    "skills": ["/skills/0"], "projects": ["/projects/0"], "publications": []
  },
  "summary": {"text": "Source-grounded summary.", "evidence": ["/objective"], "reviewed": true},
  "letter": {
    "salutation": "Dear Hiring Team,",
    "paragraphs": [{"text": "Reviewed narrative grounded in these records.", "evidence": ["/experience/0"], "reviewed": true}],
    "closing": "Kind regards,"
  },
  "requirementMap": [{"requirementId": "api", "evidence": ["/experience/0"], "status": "supported", "note": "Scope explained here."}],
  "questions": ["What remains unconfirmed?"]
}
```

`layout`: `compact`, `research`, `extended`. `paper`: `a4`, `letter`. Language/region/CV length record the request; the host drafts the language and inspects actual pages. English section labels are part of the strict parser's grammar. The extended layout inserts a project-page break for multiple experience records; it does not guarantee exactly two pages. Letter word count covers paragraph bodies, excluding header, salutation and sign-off.

Selections accept whole entries only, with no duplicates. Employers, titles, dates, URLs and other metadata within a selected record are immutable. Optional `rewrites` maps `/experience/N/description` or `/projects/N/description` to a `{text,evidence,reviewed}` claim. Only selected records can be rewritten, and the evidence must come from that same master record (or its fields), preserving role/project association. The host may truthfully paraphrase, reorder or shorten bullets after checking support; no separate approval is required for ordinary grounded edits. Runtime numeric checks reject new numerical tokens, but semantic actor/scope/causality still require host review. Empty selection arrays intentionally omit a collection; the master copy preserves it. Drafting changes the summary (`objective`) and explicitly mapped description rewrites in the derived candidate. The output master remains unchanged, and the change log retains original/revised wording and evidence. Letter paragraphs remain outside the candidate facts. `reviewed` is an accountable declaration by the drafting host/user after factual review, not a bypass to set automatically. Evidence should be as narrow as the claim permits; whole collections are allowed for a paragraph genuinely drawing on multiple entries, but broad references make human review harder.

Requirements need unique IDs and exact source quotes present in the advert. Map each exactly once. Supported/partial statuses need evidence; unsupported status must have none. A partial match needs a note separating what is documented from what is absent. The runtime cannot decide semantic fit, company truth, fabricated nonnumeric claims or swapped/misattributed existing numbers. The host must review those before declaring the application factual.

## Runtime and outputs

Python 3.9+ standard library is sufficient for validation/rendering. Tectonic on PATH is optional for PDFs; font/package downloads may be needed on its first run. Poppler and pypdf are optional independent PDF extraction tools. No runtime provider API, secret, remote product checkout or model service is required.

`render` refuses an existing destination, including an empty directory or symlink. It validates input before creating outputs. Compile failure leaves inspectable source/log/validation artifacts there; choose another fresh directory for a corrected run. No shell is used for compiler invocation, filenames are fixed, and LaTeX input is escaped. Treat trusted installed renderer code separately from untrusted candidate/job data.

Outputs: `cv.{tex,pdf?,md,txt,json}`, `cv.builder.json`, `letter.{tex,pdf?,md,txt}`, copies of `master.json` and `application.json`, `requirement-map.json`, `change-log.json`, `questions.json`, `validation.json`, and compile logs when requested. Markdown uses the same plain, editable reading-order text as `.txt`. The master input file is never rewritten; the output copy is normalized JSON rather than a byte-identical source archive. These files can contain contact/career information.

`parse --text extracted.txt --output fresh.json` reads only the documented kit grammar and refuses an existing output file. It is not an arbitrary CV importer or ATS scorer. Empty role/title/contact/project/publication fields remain empty. Ambiguous unassociated lines fail rather than being guessed.
