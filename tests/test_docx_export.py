"""
Unit tests for LaTeX-to-DOCX export helpers (no full Pandoc compile required).
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

from docx_export import (
    PAGE_BREAK_MARKER,
    apply_section_headers,
    center_frontmatter_compact,
    flatten_root_tex,
    insert_docx_page_breaks,
    is_valid_docx,
    patch_styles_xml,
    rewrite_tex_for_pandoc,
    rewrite_siunitx,
    rewrite_tex_font_groups,
    write_pandoc_workspace,
    _footer_xml,
    _header_xml,
)


def _write_minimal_docx(path: Path, body: str = "Hello") -> None:
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body><w:p><w:r><w:t>{body}</w:t></w:r></w:p></w:body></w:document>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("word/document.xml", document_xml)


def test_is_valid_docx_rejects_empty_and_non_zip(tmp_path):
    missing = tmp_path / "missing.docx"
    assert is_valid_docx(missing, min_bytes=1) is False

    empty = tmp_path / "empty.docx"
    empty.write_bytes(b"")
    assert is_valid_docx(empty, min_bytes=1) is False

    text_file = tmp_path / "plain.docx"
    text_file.write_text("not a zip", encoding="utf-8")
    assert is_valid_docx(text_file, min_bytes=1) is False


def test_is_valid_docx_accepts_minimal_ooxml(tmp_path):
    docx_path = tmp_path / "sample.docx"
    _write_minimal_docx(docx_path, "BAZILLA SALEEM Dipsacus inermis")
    assert is_valid_docx(docx_path, min_bytes=1) is True
    assert is_valid_docx(docx_path, min_bytes=10240) is False


def test_flatten_root_tex_replaces_preamble_keeps_chapters():
    source = (
        r"\documentclass{book}" "\n"
        r"\input{preamble}" "\n"
        r"\begin{document}" "\n"
        r"\input{chapters/01_introduction}" "\n"
        r"\end{document}" "\n"
    )
    flattened = flatten_root_tex(source)
    assert r"\input{preamble_docx}" in flattened
    assert r"\input{preamble}" not in flattened.replace(r"\input{preamble_docx}", "")
    assert r"\input{chapters/01_introduction}" in flattened


def test_rewrite_tex_font_groups_keeps_bold_center():
    source = r"{\Large \bfseries CERTIFICATE\par}" + "\n" + r"{\bfseries DEPARTMENT OF ZOOLOGY\par}"
    rewritten = rewrite_tex_font_groups(source)
    assert r"\textbf{\Large CERTIFICATE}" in rewritten
    assert r"\textbf{DEPARTMENT OF ZOOLOGY}" in rewritten
    assert r"\begin{center}" in rewritten
    assert r"\bfseries" not in rewritten


def test_patch_styles_xml_applies_thesis_typography():
    styles = """
    <w:styles>
      <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
        <w:name w:val="Normal" />
      </w:style>
      <w:style w:type="paragraph" w:styleId="Heading1">
        <w:name w:val="heading 1" />
        <w:rPr>
          <w:color w:val="0F4761" w:themeColor="accent1" w:themeShade="BF" />
          <w:sz w:val="40" />
        </w:rPr>
      </w:style>
    </w:styles>
    """
    patched = patch_styles_xml(styles)
    assert "Times New Roman" in patched
    assert 'w:line="360"' in patched
    assert 'w:styleId="Heading1"' in patched
    assert "<w:pageBreakBefore" in patched
    assert "0F4761" not in patched
    assert "<w:caps" in patched
    assert 'w:styleId="Header"' in patched
    assert 'w:styleId="Footer"' in patched


def test_header_and_footer_xml_use_black_text():
    header = _header_xml()
    footer = _footer_xml()
    assert 'w:color w:val="000000"' in header
    assert 'w:color w:val="000000"' in footer
    assert "themeColor" not in header
    assert "themeColor" not in footer


def test_apply_section_headers_enables_different_first_page():
    document = (
        "<w:body>"
        "<w:p><w:r><w:t>Title</w:t></w:r></w:p>"
        "<w:p><w:pPr><w:sectPr><w:pgSz/></w:sectPr></w:pPr></w:p>"
        "<w:p><w:r><w:t>Chapter</w:t></w:r></w:p>"
        "<w:sectPr><w:pgSz/></w:sectPr>"
        "</w:body>"
    )
    updated = apply_section_headers(document)
    sections = re.findall(r"<w:sectPr.*?</w:sectPr>", updated, re.DOTALL)
    assert len(sections) == 2
    assert updated.count("<w:titlePg") == 1
    assert "<w:titlePg" in sections[0]
    assert 'w:type="first"' in sections[0]
    assert "<w:titlePg" not in sections[1]
    assert 'w:type="first"' not in sections[1]
    assert 'w:type="default"' in sections[1]


def test_rewrite_siunitx_pretty_prints_common_units():
    source = r"C1 (\SI{50}{\milli\gram\per\milli\litre}) at \SI{37}{\celsius}."
    rewritten = rewrite_siunitx(source)
    assert "50 mg/mL" in rewritten
    assert "37 °C" in rewritten
    assert r"\SI" not in rewritten


def test_rewrite_tex_for_pandoc_simplifies_tables_and_tikz():
    source = (
        r"\begin{tabular}{@{}l*{4}{S[table-format=2.2(2)]}@{}}" "\n"
        r"\end{tabular}" "\n"
        r"\begin{tikzpicture}" "\n"
        r"\end{tikzpicture}" "\n"
        r"\FloatBarrier" "\n"
        r"\input{chapters/04_results}" "\n"
    )
    rewritten = rewrite_tex_for_pandoc(source, is_root=False)
    assert "S[table-format" not in rewritten
    assert r"\begin{tabular}{@{}l*{4}{l}@{}}" in rewritten
    assert "Chart rendered in the PDF edition." in rewritten
    assert r"\FloatBarrier" not in rewritten
    assert r"\input{chapters/04_results}" in rewritten


def test_rewrite_tex_for_pandoc_converts_clearpage():
    source = r"\clearpage" "\n" r"\chapter{Introduction}"
    rewritten = rewrite_tex_for_pandoc(source, is_root=False)
    assert r"\clearpage" not in rewritten
    assert PAGE_BREAK_MARKER in rewritten
    assert r"\chapter{Introduction}" in rewritten


def test_insert_docx_page_breaks_replaces_markers_without_doubling_chapters():
    document = f"""
    <w:document><w:body>
    <w:p><w:r><w:t>Title page</w:t></w:r></w:p>
    <w:p><w:r><w:t>{PAGE_BREAK_MARKER}</w:t></w:r></w:p>
    <w:p><w:r><w:t>CERTIFICATE</w:t></w:r></w:p>
    <w:p><w:r><w:t>{PAGE_BREAK_MARKER}</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>1 Introduction</w:t></w:r></w:p>
    </w:body></w:document>
    """
    polished = insert_docx_page_breaks(document)
    assert PAGE_BREAK_MARKER not in polished
    assert polished.count('w:type="page"') == 1
    assert "CERTIFICATE" in polished
    assert "1 Introduction" in polished


def test_insert_docx_page_breaks_starts_references():
    document = """
    <w:document><w:body>
    <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Appendix</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Bibliography"/></w:pPr><w:r><w:t>Cowan, M. M. 1999.</w:t></w:r></w:p>
    </w:body></w:document>
    """
    polished = insert_docx_page_breaks(document)
    assert polished.count(">REFERENCES<") == 1
    assert polished.index("REFERENCES") < polished.index("Cowan")
    assert polished.count('w:val="Bibliography"') == 1


def test_insert_docx_page_breaks_skips_leading_marker():
    document = f"""
    <w:document><w:body>
    <w:p><w:r><w:t>{PAGE_BREAK_MARKER}</w:t></w:r></w:p>
    <w:p><w:r><w:t>Title page</w:t></w:r></w:p>
    </w:body></w:document>
    """
    polished = insert_docx_page_breaks(document)
    assert PAGE_BREAK_MARKER not in polished
    assert 'w:type="page"' not in polished
    assert "Title page" in polished


def test_center_frontmatter_compact_stops_at_heading():
    document = """
    <w:document><w:body>
    <w:p><w:pPr><w:pStyle w:val="BodyText"/></w:pPr><w:r><w:t>CERTIFICATE</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="BodyText"/></w:pPr><w:r><w:t>This is a long certificate body paragraph that must stay left aligned because it exceeds the display-title length cutoff used for front matter.</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>1 Introduction</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Compact"/><w:jc w:val="left"/></w:pPr><w:r><w:t>Short after</w:t></w:r></w:p>
    </w:body></w:document>
    """
    polished = center_frontmatter_compact(document)
    assert polished.count('w:val="center"') == 1
    assert "stay left aligned" in polished
    assert 'w:val="left"' in polished


def test_write_pandoc_workspace_flattens_root(tmp_path, project_root):
    dest = tmp_path / "docx_ws"
    dest_root = write_pandoc_workspace(project_root / "dissertation.tex", dest)
    text = dest_root.read_text(encoding="utf-8")
    assert r"\input{preamble_docx}" in text
    assert r"\input{preamble}" not in text.replace(r"\input{preamble_docx}", "")
    assert r"\input{chapters/01_introduction}" in text
    assert (dest / "preamble_docx.tex").is_file()
    assert (dest / "chapters" / "01_introduction.tex").is_file()
    assert (dest / "references.bib").is_file()
    certificate = (dest / "frontmatter" / "certificate.tex").read_text(encoding="utf-8")
    assert PAGE_BREAK_MARKER in certificate
    assert r"\clearpage" not in certificate
