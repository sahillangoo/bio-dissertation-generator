#!/usr/bin/env python3
"""Report DOCX structure stats without printing body text."""

from __future__ import annotations

import collections
import re
import zipfile
from pathlib import Path

p = Path("dissertation.docx")
print("size_kb", round(p.stat().st_size / 1024, 2))
with zipfile.ZipFile(p) as z:
    names = z.namelist()
    print("parts", len(names))
    print("has_styles", "word/styles.xml" in names)
    print("has_numbering", "word/numbering.xml" in names)
    print("media_count", sum(1 for n in names if n.startswith("word/media/")))
    print("media", [n for n in names if n.startswith("word/media/")][:20])
    print("has_header", any("header" in n for n in names))
    print("has_footer", any("footer" in n for n in names))
    print("has_footnotes", "word/footnotes.xml" in names)
    doc = z.read("word/document.xml").decode("utf-8", errors="replace")
    styles = z.read("word/styles.xml").decode("utf-8", errors="replace")

print("pStyle", collections.Counter(re.findall(r'<w:pStyle w:val="([^"]+)"', doc)).most_common(25))
print("italic_i_tags", len(re.findall(r"<w:i(?:\s[^>]*)?/>", doc)))
print("bold_b_tags", len(re.findall(r"<w:b(?:\s[^>]*)?/>", doc)))
print("tables", doc.count("<w:tbl>"))
print("drawings", doc.count("<w:drawing>"))
print("blips", len(re.findall(r"<a:blip", doc)))
print("pgSz", re.findall(r"<w:pgSz[^/]*/>", doc)[:3])
print("pgMar", re.findall(r"<w:pgMar[^/]*/>", doc)[:3])
print("spacing_unique", sorted(set(re.findall(r"<w:spacing[^/]*/>", doc)))[:12])
print("rFonts_samples", re.findall(r"<w:rFonts [^/]*/>", styles)[:10])
print("sz_in_styles", re.findall(r'<w:sz w:val="([^"]+)"', styles)[:16])
print("style_names", re.findall(r'<w:name w:val="([^"]+)"', styles)[:50])
print("raw_taxa", r"\taxa" in doc)
print("raw_textit", r"\textit" in doc)
print("raw_SI", r"\SI{" in doc)
print("raw_cref", r"\cref" in doc)
print("raw_cite", r"\cite" in doc)
print("unexpanded_newcommand", r"\newcommand" in doc)
print("doc_len", len(doc))
print("para_count", doc.count("<w:p>"))
print("hyperlink_count", doc.count("<w:hyperlink"))
