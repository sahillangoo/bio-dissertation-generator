import zipfile
import xml.etree.ElementTree as ET
import re

docx_path = r"d:\sandbox\work-box\dissertation-skills\dissertation.docx"
print(f"Reading {docx_path}...")

with zipfile.ZipFile(docx_path, "r") as z:
    xml_content = z.read("word/document.xml")

root = ET.fromstring(xml_content)
namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

text_parts = []
for node in root.iter():
    if node.tag.endswith('}t'):
        if node.text:
            text_parts.append(node.text)

full_docx_text = " ".join(text_parts)

print(f"Total extracted text length: {len(full_docx_text)} characters")

checks = [
    ("Yield 24.13%", "24.13%"),
    ("Lat 34.12981", "34.12981"),
    ("Long 74.83396", "74.83396"),
    ("WGS84", "WGS84"),
    ("E. coli C1 11.94", "11.94"),
    ("E. coli C2 14.99", "14.99"),
    ("E. coli GEN5 17.00", "17.00"),
    ("P. aer C1 16.03", "16.03"),
    ("P. aer C2 12.53", "12.53"),
    ("P. aer GEN5 17.17", "17.17"),
    ("K. pneu C1 12.35", "12.35"),
    ("K. pneu C2 13.25", "13.25"),
    ("K. pneu GEN5 15.17", "15.17"),
    ("Replicate 11.78", "11.78"),
    ("Replicate 12.05", "12.05"),
    ("Replicate 15.50", "15.50"),
    ("Replicate 14.48", "14.48"),
    ("Replicate 16.30", "16.30"),
    ("Replicate 15.80", "15.80"),
    ("Replicate 12.10", "12.10"),
    ("Replicate 17.50", "17.50"),
    ("Replicate 12.75", "12.75"),
    ("Disclaimer: voucher", "voucher"),
    ("Disclaimer: strain IDs/ATCC", "ATCC"),
    ("Disclaimer: well volume", "volume")
]

failed = False
for label, target in checks:
    if target.lower() in full_docx_text.lower():
        print(f"[PASS] DOCX contains: {label} ('{target}')")
    else:
        print(f"[FAIL] DOCX missing: {label} ('{target}')")
        failed = True

if failed:
    print("DOCX verification failed!")
    exit(1)
else:
    print("DOCX verification completely PASSED!")
