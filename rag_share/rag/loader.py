"""DOCX document loader with section-aware parsing that handles tables."""

import glob
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from langchain_core.documents import Document as LCDocument


def _table_to_text(tbl: Table) -> str:
    """Convert a table to readable key: value lines."""
    lines = []
    rows = list(tbl.rows)
    if not rows:
        return ""

    headers = [c.text.strip() for c in rows[0].cells]

    # 2-column key-value tables (e.g. Interest Rate | value)
    if len(headers) == 2 and rows[0].cells[0].text.strip() not in ("Services", "Fixed Deposit Account"):
        for row in rows:
            cells = [c.text.strip() for c in row.cells]
            if cells[0]:
                lines.append(f"{cells[0]}: {cells[1]}")
        return "\n".join(lines)

    # Multi-column tables: header row + data rows
    lines.append(" | ".join(headers))
    for row in rows[1:]:
        cells = [c.text.strip() for c in row.cells]
        lines.append(" | ".join(cells))
    return "\n".join(lines)


def _get_para_text(para_el) -> str:
    """Extract plain text from a paragraph XML element."""
    runs = para_el.findall(".//" + qn("w:t"))
    return "".join(r.text or "" for r in runs).strip()


def _get_para_style(para_el) -> str:
    pPr = para_el.find(qn("w:pPr"))
    if pPr is None:
        return ""
    pStyle = pPr.find(qn("w:pStyle"))
    if pStyle is None:
        return ""
    return pStyle.get(qn("w:val"), "")


def load_docx_by_section(file_path: str) -> list[LCDocument]:
    """
    Parse a DOCX file by walking body elements in document order.

    Groups content under Heading1 boundaries — one LCDocument per section.
    Tables are converted to readable text and included inline.
    """
    doc = Document(file_path)
    body = doc.element.body

    sections: list[dict] = []  # [{title, lines}]
    current: dict | None = None

    for child in body:
        tag = child.tag.split("}")[-1]

        if tag == "p":
            style = _get_para_style(child)
            text = _get_para_text(child)

            # Heading1 always starts a new section.
            # Heading2 starts a new section only when it looks like a product ID
            # (begins with a digit), not a subsection label like "Charges".
            is_section_start = (style == "Heading1" and text) or (
                style == "Heading2" and text and text[0].isdigit()
            )

            if is_section_start:
                current = {"title": text, "lines": [text]}
                sections.append(current)
            elif text:
                if current is None:
                    # Pre-section content (title page etc.) — skip
                    continue
                current["lines"].append(text)

        elif tag == "tbl":
            if current is None:
                continue
            tbl = Table(child, doc)
            table_text = _table_to_text(tbl)
            if table_text:
                current["lines"].append(table_text)

    # Build LCDocuments
    documents = []
    for i, section in enumerate(sections):
        content = "\n".join(section["lines"])
        documents.append(
            LCDocument(
                page_content=content,
                metadata={
                    "source": file_path,
                    "section": section["title"],
                    "section_index": i,
                },
            )
        )

    return documents


def load_multiple_docx(file_paths: list) -> list[LCDocument]:
    """Load multiple .docx files, returning one document per section."""
    all_docs = []
    for path in file_paths:
        docs = load_docx_by_section(path)
        all_docs.extend(docs)
        print(f"  {path}: {len(docs)} sections loaded")
    print(f"Total: {len(all_docs)} documents")
    return all_docs


def find_docx_files(directory: str = "data") -> list:
    """Return all .docx files found in the given directory."""
    return glob.glob(f"{directory}/*.docx")
