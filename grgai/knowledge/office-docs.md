# Generating documents — PowerPoint, Excel, Word, PDF

## Python (best for scripts / a backend endpoint)
- **PowerPoint (.pptx)** — `python-pptx`:
```python
from pptx import Presentation
from pptx.util import Inches, Pt
p = Presentation()
s = p.slides.add_slide(p.slide_layouts[0])       # title slide
s.shapes.title.text = "Quarterly Review"
s.placeholders[1].text = "2026 Q1"
b = p.slides.add_slide(p.slide_layouts[1])        # title + content
b.shapes.title.text = "Highlights"
tf = b.placeholders[1].text_frame; tf.text = "Revenue up 24%"
tf.add_paragraph().text = "Churn down 3%"
p.save("deck.pptx")
```
- **Excel (.xlsx)** — `openpyxl` (styling/formulas) or `pandas.to_excel` (dataframes):
```python
import openpyxl
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Sales"
ws.append(["Month", "Revenue"]); ws.append(["Jan", 12000]); ws.append(["Feb", 15000])
ws["C1"] = "Total"; ws["C2"] = "=SUM(B2:B3)"
wb.save("report.xlsx")
```
- **Word (.docx)** — `python-docx`:
```python
from docx import Document
d = Document(); d.add_heading("Proposal", 0)
d.add_paragraph("Executive summary…")
d.add_heading("Scope", level=1); d.add_paragraph("Item one", style="List Bullet")
t = d.add_table(rows=1, cols=2); t.rows[0].cells[0].text = "Task"; t.rows[0].cells[1].text = "Owner"
d.save("proposal.docx")
```
- **PDF** — `reportlab` (from scratch) or render HTML→PDF with `weasyprint`.
- Install: `pip install python-pptx openpyxl python-docx pandas reportlab`.

## In the browser (client-side, no server)
- **Excel/CSV**: SheetJS (`xlsx`) — `XLSX.utils.json_to_sheet(rows)` → `XLSX.writeFile(wb, "out.xlsx")`.
- **Word**: `docx` (npm) — build `Document`/`Paragraph`, `Packer.toBlob()` → download.
- **PowerPoint**: `pptxgenjs` — `let p=new pptxgen(); p.addSlide().addText("Hi",{x:1,y:1}); p.writeFile({fileName:"deck.pptx"})`.
- **PDF**: `jspdf` (+ `jspdf-autotable` for tables), or `html2pdf.js` to snapshot a DOM node.
- Trigger a download: create a Blob → `URL.createObjectURL` → `<a download>` click.

## Guidance
- Ask what content + structure they want first (sections, columns, chart types). Keep styling consistent (one font, a header row, brand color).
- For data → spreadsheet, put headers in row 1, one record per row, real formulas where useful.
- For slides, 1 idea per slide, short bullets, a clear title; offer a title + agenda + section slides.
- Return the file for download (server endpoint or client Blob), and summarize what you generated.
