import csv
import zipfile
import os

csv_path = r"C:\Users\kaush\.gemini\antigravity\scratch\nse-stock-fetcher\past_30_days_closing_prices.csv"
xlsx_path = r"C:\Users\kaush\.gemini\antigravity\scratch\nse-stock-fetcher\past_30_days_closing_prices.xlsx"

with open(csv_path, "r", encoding="utf-8") as f:
    rows = list(csv.reader(f))

sheet_xml = [
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
    '<sheetData>'
]

for r_idx, row in enumerate(rows, start=1):
    sheet_xml.append(f'<row r="{r_idx}">')
    for c_idx, val in enumerate(row, start=1):
        col_letter = chr(64 + c_idx)
        cell_ref = f"{col_letter}{r_idx}"
        if r_idx == 1 or c_idx == 1:
            sheet_xml.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{val}</t></is></c>')
        else:
            try:
                num = float(val)
                sheet_xml.append(f'<c r="{cell_ref}"><v>{num:.2f}</v></c>')
            except ValueError:
                sheet_xml.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{val}</t></is></c>')
    sheet_xml.append('</row>')

sheet_xml.append('</sheetData></worksheet>')

content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>'''

rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/package/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''

wb_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>'''

workbook = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Closing_Prices" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>'''

with zipfile.ZipFile(xlsx_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
    z.writestr("xl/workbook.xml", workbook)
    z.writestr("xl/worksheets/sheet1.xml", "".join(sheet_xml))

print("XLSX successfully generated.")
