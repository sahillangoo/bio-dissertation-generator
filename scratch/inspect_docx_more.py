#!/usr/bin/env python3
from __future__ import annotations
import re
import zipfile
from pathlib import Path

path = Path("dissertation.docx")
with zipfile.ZipFile(path) as z:
    styles = z.read("word/styles.xml").decode("utf-8")
    doc = z.read("word/document.xml").decode("utf-8")
    theme = z.read("word/theme/theme1.xml").decode("utf-8") if "word/theme/theme1.xml" in z.namelist() else ""

for style_id in ("Normal", "BodyText", "Compact", "Heading1", "Heading2", "Title"):
    match = re.search(rf'<w:style[^>]*w:styleId="{style_id}".*?</w:style>', styles, re.DOTALL)
    assert match
    xml = match.group(0)
    print("=" * 60, style_id)
    print("color", re.findall(r"<w:color[^/]*/>", xml))
    print("szCs", re.findall(r'<w:szCs w:val="([^"]+)"', xml))
    print("basedOn", re.findall(r'<w:basedOn w:val="([^"]+)"', xml))
    print("link", re.findall(r'<w:link w:val="([^"]+)"', xml))
    print("pPr", "YES" if "<w:pPr>" in xml else "NO")
    print("rPr", "YES" if "<w:rPr>" in xml else "NO")

# How many Compact paras have jc center?
compact_blocks = re.findall(r'<w:p>.*?</w:p>', doc, re.DOTALL)
center = 0
compact = 0
body = 0
for para in compact_blocks:
    if 'w:val="Compact"' in para:
        compact += 1
        if "center" in para:
            center += 1
    if 'w:val="BodyText"' in para:
        body += 1
print("compact_paras", compact, "compact_with_center_hint", center, "body", body)

# table borders sample
print("tblBorders_count", len(re.findall(r"<w:tblBorders>", doc)))
print("insideH", doc.count("<w:insideH"))
print("top_border", len(re.findall(r"<w:top ", doc)))

# major/minor latin fonts
print("majorLatin", re.findall(r'<a:latin typeface="([^"]+)"', theme)[:4])
print("minor", re.search(r'<a:minorFont>.*?</a:minorFont>', theme, re.DOTALL))
minor = re.search(r"<a:minorFont>.*?</a:minorFont>", theme, re.DOTALL)
if minor:
    print("minorLatin", re.findall(r'<a:latin typeface="([^"]+)"', minor.group(0))[:2])
major = re.search(r"<a:majorFont>.*?</a:majorFont>", theme, re.DOTALL)
if major:
    print("majorLatin", re.findall(r'<a:latin typeface="([^"]+)"', major.group(0))[:2])
