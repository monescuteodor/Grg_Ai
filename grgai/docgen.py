"""docgen.py — turn a JSON spec into a real .pptx / .xlsx / .docx file (bytes)."""
import io
import re

from pptx import Presentation
import openpyxl
from openpyxl.styles import Font, PatternFill
from docx import Document

MIME = {
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
MAX_SLIDES, MAX_ROWS, MAX_SHEETS = 120, 8000, 25


def _safe_name(name, ext):
    n = re.sub(r"[^A-Za-z0-9 ._-]", "", str(name or "document")).strip() or "document"
    if not n.lower().endswith("." + ext):
        n = re.sub(r"\.(pptx|xlsx|docx)$", "", n, flags=re.I) + "." + ext
    return n[:80]


def _pptx(spec):
    p = Presentation()
    if spec.get("title"):
        s = p.slides.add_slide(p.slide_layouts[0])
        s.shapes.title.text = str(spec["title"])[:200]
        if spec.get("subtitle") and len(s.placeholders) > 1:
            s.placeholders[1].text = str(spec["subtitle"])[:300]
    for sl in (spec.get("slides") or [])[:MAX_SLIDES]:
        s = p.slides.add_slide(p.slide_layouts[1])
        s.shapes.title.text = str(sl.get("title") or "")[:200]
        if len(s.placeholders) > 1:
            body = s.placeholders[1].text_frame
            bullets = sl.get("bullets") or ([sl.get("content")] if sl.get("content") else [])
            first = True
            for b in bullets[:40]:
                if first:
                    body.text = str(b)[:500]; first = False
                else:
                    body.add_paragraph().text = str(b)[:500]
        if sl.get("notes"):
            s.notes_slide.notes_text_frame.text = str(sl["notes"])[:2000]
    buf = io.BytesIO(); p.save(buf); return buf.getvalue()


def _xlsx(spec):
    wb = openpyxl.Workbook()
    sheets = spec.get("sheets") or [{"name": spec.get("title") or "Sheet1",
                                     "headers": spec.get("headers") or [], "rows": spec.get("rows") or []}]
    first = True
    for sh in sheets[:MAX_SHEETS]:
        ws = wb.active if first else wb.create_sheet(); first = False
        ws.title = (str(sh.get("name") or "Sheet")[:31]) or "Sheet"
        headers = sh.get("headers") or []
        if headers:
            ws.append([str(h) for h in headers])
            for c in ws[1]:
                c.font = Font(bold=True, color="4C1D95")
                c.fill = PatternFill("solid", fgColor="EDE9FE")
        for row in (sh.get("rows") or [])[:MAX_ROWS]:
            ws.append(list(row) if isinstance(row, (list, tuple)) else [row])
        for col in ws.columns:
            try:
                w = max((len(str(c.value)) for c in col if c.value is not None), default=10)
                ws.column_dimensions[col[0].column_letter].width = min(60, max(10, w + 2))
            except Exception:
                pass
    buf = io.BytesIO(); wb.save(buf); return buf.getvalue()


def _docx(spec):
    d = Document()
    if spec.get("title"):
        d.add_heading(str(spec["title"])[:200], 0)
    secs = spec.get("sections") or []
    for sec in secs:
        if sec.get("heading"):
            lvl = int(sec.get("level", 1) or 1)
            d.add_heading(str(sec["heading"])[:200], max(1, min(4, lvl)))
        for para in (sec.get("paragraphs") or []):
            d.add_paragraph(str(para))
        for b in (sec.get("bullets") or []):
            d.add_paragraph(str(b), style="List Bullet")
    if not secs and spec.get("body"):
        for para in str(spec["body"]).split("\n\n"):
            if para.strip():
                d.add_paragraph(para.strip())
    buf = io.BytesIO(); d.save(buf); return buf.getvalue()


def generate(spec):
    """spec: {type: 'pptx'|'xlsx'|'docx', filename, title, ...}. Returns (bytes, mime, filename)."""
    if not isinstance(spec, dict):
        raise ValueError("spec must be an object")
    t = (spec.get("type") or "").lower()
    if t not in MIME:
        raise ValueError("type must be pptx, xlsx or docx")
    data = {"pptx": _pptx, "xlsx": _xlsx, "docx": _docx}[t](spec)
    return data, MIME[t], _safe_name(spec.get("filename") or spec.get("title") or "document", t)
