#!/usr/bin/env python3
import collections
import re
import zipfile
from pathlib import Path

doc = zipfile.ZipFile(Path("dissertation.docx")).read("word/document.xml").decode("utf-8")
print("jc", collections.Counter(re.findall(r'<w:jc w:val="([^"]+)"', doc)))
print("ind", collections.Counter(re.findall(r"<w:ind [^/]*/>", doc)))
print("sz_direct", collections.Counter(re.findall(r'<w:sz w:val="([^"]+)"', doc)).most_common(10))
print("large_like", "28" in re.findall(r'<w:sz w:val="([^"]+)"', doc))
print("bookmark_heading", len(re.findall(r'w:name="[^"]*introduction', doc, re.I)))
