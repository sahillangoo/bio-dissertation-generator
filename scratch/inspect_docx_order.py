#!/usr/bin/env python3
import re
import zipfile
from pathlib import Path

doc = zipfile.ZipFile(Path("dissertation.docx")).read("word/document.xml").decode("utf-8")
paras = re.findall(r"<w:p\b.*?</w:p>", doc, re.DOTALL)
print("para_tokens", len(paras))
print("tbl_tokens", len(re.findall(r"<w:tbl\b.*?</w:tbl>", doc, re.DOTALL)))
styles = []
for para in paras[:40]:
    m = re.search(r'<w:pStyle w:val="([^"]+)"', para)
    jc = re.search(r'<w:jc w:val="([^"]+)"', para)
    styles.append((m.group(1) if m else "-", jc.group(1) if jc else "-"))
print("first40", styles)
print("TOCHeading_index")
for i, para in enumerate(paras):
    if 'w:val="TOCHeading"' in para or 'w:val="Heading1"' in para:
        m = re.search(r'<w:pStyle w:val="([^"]+)"', para)
        print(i, m.group(1) if m else "?")
        if i > 5 and 'Heading1' in (m.group(1) if m else ""):
            break
