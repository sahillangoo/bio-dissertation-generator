#!/usr/bin/env python3
"""Print named style XML snippets from dissertation.docx."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

WANTED = (
    "Normal",
    "BodyText",
    "FirstParagraph",
    "Compact",
    "Heading1",
    "Heading2",
    "Heading3",
    "Title",
    "Caption",
    "ImageCaption",
    "TableCaption",
    "Bibliography",
)

path = Path("dissertation.docx")
with zipfile.ZipFile(path) as z:
    styles = z.read("word/styles.xml").decode("utf-8")
    doc = z.read("word/document.xml").decode("utf-8")
    numbering = z.read("word/numbering.xml").decode("utf-8") if "word/numbering.xml" in z.namelist() else ""

for style_id in WANTED:
    match = re.search(
        rf'<w:style[^>]*w:styleId="{style_id}".*?</w:style>',
        styles,
        re.DOTALL,
    )
    print("=" * 72)
    print(style_id, "FOUND" if match else "MISSING")
    if match:
        xml = match.group(0)
        print(" name", re.search(r'<w:name w:val="([^"]+)"', xml).group(1) if re.search(r'<w:name w:val="([^"]+)"', xml) else "")
        print(" rFonts", re.findall(r"<w:rFonts[^/]*/>", xml)[:3])
        print(" sz", re.findall(r'<w:sz w:val="([^"]+)"', xml))
        print(" spacing", re.findall(r"<w:spacing[^/]*/>", xml))
        print(" ind", re.findall(r"<w:ind[^/]*/>", xml))
        print(" jc", re.findall(r"<w:jc[^/]*/>", xml))
        print(" caps", "<w:caps" in xml)
        print(" bold", "<w:b" in xml)

print("=" * 72)
print("document sectPr", re.findall(r"<w:sectPr.*?</w:sectPr>", doc, re.DOTALL)[:1])
print("numbering abstracts", numbering.count("<w:abstractNum "))
print("theme fonts")
if "word/theme/theme1.xml" in zipfile.ZipFile(path).namelist():
    theme = zipfile.ZipFile(path).read("word/theme/theme1.xml").decode("utf-8")
    print(re.findall(r'typeface="([^"]+)"', theme)[:20])
