"""Original LaTeX layouts and PDF-only, section-aware candidate extraction.

The parser accepts text only. Ground truth is loaded separately by validate.py.
"""

import re

VARIANTS = {
    "research": {"font": "11pt", "margin": "18mm", "family": "serif"},
    "compact": {"font": "10pt", "margin": "14mm", "family": "sans"},
    "extended": {"font": "11pt", "margin": "20mm", "family": "serif"},
}
DATE_RANGE = re.compile(r"^(\d{4}(?:-(?:0[1-9]|1[0-2]))?)?\s*-\s*(\d{4}(?:-(?:0[1-9]|1[0-2]))?|Present)?$")
SECTIONS = ("Summary", "Experience", "Education", "Skills", "Projects", "Publications")


def escape_tex(value):
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def date_line(start, end):
    # Poppler drops a standalone hyphen, so absence needs visible words.
    return start + " - " + end if start or end else "Dates: not provided"


def render_text(c):
    lines = [
        c["name"],
        c["title"],
        f"Email: {c['email']}",
        f"Phone: {c['phone']}",
        f"Location: {c['location']}",
    ]
    lines += ["Link: " + link for link in c["links"]]
    lines += ["Summary", c["objective"], "Experience"]
    for e in c["experience"]:
        lines += [
            e["title"] + " | " + e["company"],
            date_line(e["startDate"], e["endDate"]),
        ]
        lines += ["- " + line for line in e["description"].splitlines()]
    lines += ["Education"]
    for e in c["education"]:
        lines += [
            e["degree"] + " | " + e["field"] + " | " + e["school"],
            "Education date: " + e["graduationDate"],
        ]
    lines += ["Skills", "; ".join(c["skills"]), "Projects"]
    for p in c["projects"]:
        lines += [
            p["name"],
            date_line(p["startDate"], p["endDate"]),
            "Technologies: " + p["technologies"],
            "URL: " + p["url"],
        ]
        lines += ["- " + line for line in p["description"].splitlines()]
    if c["publications"]:
        lines += ["Publications"]
        for p in c["publications"]:
            lines += [
                "Title: " + p["title"],
                "Authors: " + p["authors"],
                "Venue: " + p["venue"],
                "Date: " + p["date"],
                "URL: " + p["url"],
            ]
    return "\n".join(line.rstrip() for line in lines) + "\n"


def render_tex(candidate, variant, sample=True):
    style = VARIANTS[variant]
    c = candidate
    if sample and not c["name"]:
        c = {
            **c,
            "name": "Your name",
            "title": "Your target role",
            "email": "you@example.com",
            "phone": "Your phone",
            "location": "City, Country",
            "objective": "Replace these prompts with your own facts. Describe your relevant experience and contribution.",
        }
    preamble = r"""\documentclass[FONT,a4paper]{article}
\usepackage[margin=MARGIN]{geometry}
\usepackage{fontspec}
\setmainfont{lmroman10-regular.otf}[BoldFont=lmroman10-bold.otf,ItalicFont=lmroman10-italic.otf,Ligatures=NoCommon,RawFeature={-kern}]
\setsansfont{lmsans10-regular.otf}[BoldFont=lmsans10-bold.otf,ItalicFont=lmsans10-oblique.otf,Ligatures=NoCommon,RawFeature={-kern}]
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{needspace}
\usepackage[unicode,hidelinks]{hyperref}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\setlist[itemize]{leftmargin=13pt,nosep,label=\textbullet}
\titleformat{\section}{\large\bfseries}{}{0pt}{}[\titlerule]
\titlespacing*{\section}{0pt}{9pt}{4pt}
\hyphenpenalty=10000
\exhyphenpenalty=10000
\emergencystretch=2em
\begin{document}
""".replace("FONT", style["font"]).replace("MARGIN", style["margin"])
    if style["family"] == "sans":
        preamble += "\\sffamily\n"
    out = [
        preamble,
        r"{\LARGE\bfseries " + escape_tex(c["name"]) + "}\\par",
        escape_tex(c["title"]) + r"\par",
    ]
    for label in ["email", "phone", "location"]:
        out.append(escape_tex(label.title() + ": " + c[label]) + r"\par")
    for link in c["links"]:
        out.append(escape_tex("Link: " + link) + r"\par")
    if sample:
        out.append(r"{\small\itshape Fictional sample data. Not a real candidate.}\par")
    out += [r"\section*{Summary}", escape_tex(c["objective"])]

    def bullets(description):
        lines = [line for line in description.splitlines() if line.strip()]
        if not lines:
            return []
        return (
            [r"\begin{itemize}"]
            + [r"\item " + escape_tex(line) for line in lines]
            + [r"\end{itemize}"]
        )

    out.append(r"\section*{Experience}")
    for e in c["experience"]:
        out += [
            r"\needspace{5\baselineskip}",
            r"\textbf{" + escape_tex(e["title"] + " | " + e["company"]) + r"}\par",
            escape_tex(date_line(e["startDate"], e["endDate"])) + r"\par",
        ] + bullets(e["description"])
    out.append(r"\section*{Education}")
    for e in c["education"]:
        out += [
            escape_tex(e["degree"] + " | " + e["field"] + " | " + e["school"])
            + r"\par",
            escape_tex("Education date: " + e["graduationDate"]) + r"\par",
        ]
    out += [r"\section*{Skills}", escape_tex("; ".join(c["skills"]))]
    if variant == "extended" and len(c["experience"]) > 1 and c["projects"]:
        out.append(r"\newpage")
    if c["projects"] or sample:
        out += [r"\needspace{9\baselineskip}", r"\section*{Projects}"]
    for p in c["projects"]:
        out += [
            r"\needspace{6\baselineskip}",
            r"\textbf{" + escape_tex(p["name"]) + r"}\par",
            escape_tex(date_line(p["startDate"], p["endDate"])) + r"\par",
            escape_tex("Technologies: " + p["technologies"]) + r"\par",
            escape_tex("URL: " + p["url"]) + r"\par",
        ] + bullets(p["description"])
    if c["publications"]:
        out.append(r"\section*{Publications}")
        for p in c["publications"]:
            out += [escape_tex("Title: " + p["title"]) + r"\par"] + [
                escape_tex(("URL" if k == "url" else k.title()) + ": " + p[k]) + r"\par"
                for k in ["authors", "venue", "date", "url"]
            ]
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


def parse_text(text):
    """Read this pack's documented text grammar, never infer missing facts.

    Reject ambiguous records. This is a pack-specific parser, not a claim about
    arbitrary CVs, vendor ATS imports or the existing AI parser's reliability.
    """
    lines = [
        line.strip() for line in text.replace("\x0c", "\n").splitlines() if line.strip()
    ]
    lines = [
        line for line in lines if line != "Fictional sample data. Not a real candidate."
    ]
    result = {
        k: "" for k in ["name", "title", "email", "phone", "location", "objective"]
    }
    result.update(
        {
            k: []
            for k in [
                "links",
                "skills",
                "experience",
                "education",
                "projects",
                "publications",
            ]
        }
    )
    if not lines:
        return result
    result["name"] = lines[0]
    header_start = 1
    if (
        len(lines) > 1
        and lines[1] not in SECTIONS
        and not lines[1].startswith(("Email:", "Phone:", "Location:", "Link:"))
    ):
        result["title"] = lines[1]
        header_start = 2
    section = None
    record = None
    bullet = False
    pending = []
    for index, line in enumerate(lines[header_start:], start=header_start):
        if line in SECTIONS:
            if pending:
                raise ValueError("Ambiguous unassociated text: " + repr(pending))
            section, record, bullet = line, None, False
            continue
        if section is None:
            for key in ["email", "phone", "location"]:
                if line.startswith(key.title() + ":"):
                    result[key] = line.partition(":")[2].strip()
            if line.startswith("Link: "):
                result["links"].append(line[6:])
        elif section == "Summary":
            result["objective"] += (" " if result["objective"] else "") + line
        elif section == "Skills":
            result["skills"].extend(x.strip() for x in line.split(";") if x.strip())
        elif section in ("Experience", "Projects"):
            date_match = DATE_RANGE.fullmatch(line)
            if date_match or line == "Dates: not provided":
                if not pending:
                    raise ValueError("Date has no associated role/project")
                heading = " ".join(pending)
                start, end = (
                    (value or "" for value in date_match.groups())
                    if date_match
                    else ("", "")
                )
                if section == "Experience":
                    parts = [part.strip() for part in heading.split("|")]
                    if len(parts) != 2:
                        raise ValueError("Ambiguous role/employer: " + heading)
                    record = {
                        "title": parts[0],
                        "company": parts[1],
                        "startDate": start,
                        "endDate": end,
                        "description": "",
                    }
                else:
                    record = {
                        "name": heading,
                        "startDate": start,
                        "endDate": end,
                        "technologies": "",
                        "url": "",
                        "description": "",
                    }
                result[section.lower()].append(record)
                pending, bullet = [], False
            elif line.startswith(("• ", "- ")):
                if record is None:
                    raise ValueError("Achievement has no associated entry")
                record["description"] += ("\n" if record["description"] else "") + line[
                    2:
                ]
                bullet = True
            elif section == "Projects" and line.startswith(("Technologies:", "URL:")):
                if record is None:
                    raise ValueError("Project field has no associated entry")
                key, _, value = line.partition(":")
                value = value.strip()
                record["technologies" if key == "Technologies" else "url"] = value
            elif ("|" in line and section == "Experience") or (
                index + 1 < len(lines)
                and (
                    DATE_RANGE.fullmatch(lines[index + 1])
                    or lines[index + 1] == "Dates: not provided"
                )
            ):
                pending.append(line)
                bullet = False
            elif bullet and record is not None:
                record["description"] += " " + line
            else:
                pending.append(line)
        elif section == "Education":
            if line.startswith(("Education date:", "Graduated:")):
                parts = [part.strip() for part in " ".join(pending).split("|")]
                if len(parts) != 3:
                    raise ValueError("Ambiguous education entry")
                result["education"].append(
                    {
                        "degree": parts[0],
                        "field": parts[1],
                        "school": parts[2],
                        "graduationDate": line.partition(":")[2].strip(),
                    }
                )
                pending = []
            else:
                pending.append(line)
        elif section == "Publications":
            match = re.match(r"^(Title|Authors|Venue|Date|URL):\s*(.*)$", line)
            if match:
                key, value = match.group(1).lower(), match.group(2)
                if key == "title":
                    record = {
                        "title": value,
                        "authors": "",
                        "venue": "",
                        "date": "",
                        "url": "",
                    }
                    result["publications"].append(record)
                elif record is None:
                    raise ValueError("Publication field has no associated title")
                else:
                    if record[key]:
                        raise ValueError("Duplicate publication field")
                    record[key] = value
                publication_field = key
            elif record is None:
                raise ValueError("Publication title must be labeled")
            else:
                record[publication_field] += (
                    "" if publication_field == "url" else " "
                ) + line
    if pending:
        raise ValueError("Unassociated text: " + repr(pending))
    return result


def compare_fields(expected, actual, path=""):
    """Exact leaf comparison, including array cardinality and role association."""
    differences = []
    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in expected.keys() | actual.keys():
            if key not in expected or key not in actual:
                differences.append(path + "/" + key)
            else:
                differences += compare_fields(
                    expected[key], actual[key], path + "/" + key
                )
    elif isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            differences.append(path + "/length")
        for i, (e, a) in enumerate(zip(expected, actual)):
            differences += compare_fields(e, a, path + "/" + str(i))
    elif expected != actual:
        differences.append(path)
    return differences


def builder_data(c):
    """Add canonical links/publications/dates while retaining legacy builder fields."""
    return {
        k: c[k]
        for k in [
            "name",
            "title",
            "email",
            "phone",
            "location",
            "objective",
            "experience",
            "education",
        ]
    } | {
        "website": c["links"][0] if c["links"] else "",
        "links": c["links"],
        "publications": c["publications"],
        "skills": [{"id": str(i), "name": s} for i, s in enumerate(c["skills"])],
        "projects": [
            {k: p[k] for k in ["name", "technologies", "startDate", "endDate", "url"]}
            | {
                "description": p["startDate"]
                + " - "
                + p["endDate"]
                + "\n"
                + p["url"]
                + "\n"
                + p["description"]
            }
            for p in c["projects"]
        ],
    }
