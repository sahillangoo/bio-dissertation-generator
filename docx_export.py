#!/usr/bin/env python3
"""
LaTeX-to-DOCX export for the Biology & Zoology dissertation builder.

Finds or auto-bootstraps a Pandoc binary, rewrites the modular TeX tree into a
Pandoc-safe workspace, and writes an OOXML .docx sibling of the PDF artifact.
"""

from __future__ import annotations

import html
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

PANDOC_VERSION = "3.10.2"
PANDOC_RELEASE_BASE = f"https://github.com/jgm/pandoc/releases/download/{PANDOC_VERSION}"
MIN_DOCX_BYTES = 10240
DOCX_IDENTITY_STRINGS = ("Dipsacus", "Bazilla")
DOCX_SOURCE_DIRS = ("frontmatter", "chapters", "appendices")
PAGE_BREAK_MARKER = "ZZZDOCXPAGEBREAKZZZ"
OOXML_TOKEN_RE = re.compile(r"(<w:tbl\b.*?</w:tbl>|<w:p\b.*?</w:p>)", re.DOTALL)
PAGE_BREAK_PARAGRAPH = (
    "<w:p>"
    '<w:pPr><w:spacing w:before="0" w:after="0"/><w:ind w:firstLine="0"/></w:pPr>'
    '<w:r><w:br w:type="page"/></w:r>'
    "</w:p>"
)
REFERENCES_HEADING = (
    "<w:p>"
    '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
    "<w:r><w:t>REFERENCES</w:t></w:r>"
    "</w:p>"
)
PREAMBLE_INPUT_RE = re.compile(r"\\input\{preamble(?:\.tex)?\}")
SI_RE = re.compile(r"\\SI\{([^{}]+)\}\{([^{}]+)\}")
SI_UNIT_RE = re.compile(r"\\si\{([^{}]+)\}")
TIKZ_RE = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.DOTALL)
FOREST_RE = re.compile(r"\\begin\{forest\}.*?\\end\{forest\}", re.DOTALL)
TABULAR_ARRAY_RE = re.compile(r">\{[^}]*\\arraybackslash\}p\{[^}]+\}")
TABULAR_S_RE = re.compile(r"S\[[^\]]*\]")
PRINTBIBLIOGRAPHY_RE = re.compile(r"\\printbibliography(?:\[[^\]]*\])?")
BF_PAR_RE = re.compile(
    r"\{\s*(?:\\(?P<size>Large|large|normalsize|footnotesize)\s+)?\\bfseries\s+(?P<body>[^}]*?)\\par\s*\}",
    re.DOTALL,
)
IT_PAR_RE = re.compile(
    r"\{\s*(?:\\(?P<size>Large|large|normalsize|footnotesize)\s+)?\\textit\s*\{(?P<body>[^}]*)\}\s*\\par\s*\}",
    re.DOTALL,
)
SIZE_PAR_RE = re.compile(
    r"\{\s*\\(?P<size>Large|large|normalsize|footnotesize)\s+(?P<body>[^}]*?)\\par\s*\}",
    re.DOTALL,
)
SIZE_TEXTBF_PAR_RE = re.compile(
    r"\{\s*\\(?P<size>Large|large|normalsize|footnotesize)\s+\\textbf\{(?P<body>[^}]*)\}\s*\\par\s*\}",
    re.DOTALL,
)
TIMES_NEW_ROMAN = "Times New Roman"
A4_WIDTH_TWIPS = "11906"
A4_HEIGHT_TWIPS = "16838"
LINE_SPACING_ONE_HALF = "360"  # 240 = single; 360 = 1.5
FIRST_LINE_INDENT = "504"  # 0.35 in, matching preamble.tex parindent
HEADING_ACCENT = "0F4761"
UNIT_REPLACEMENTS: Tuple[Tuple[str, str], ...] = (
    (r"\milli\gram\per\milli\litre", "mg/mL"),
    (r"\micro\gram\per\milli\litre", "µg/mL"),
    (r"\micro\gram", "µg"),
    (r"\milli\litre", "mL"),
    (r"\milli\metre", "mm"),
    (r"\milli\gram", "mg"),
    (r"\celsius", "°C"),
    (r"\second", "s"),
    (r"\gram", "g"),
    (r"\hour", "h"),
    (r"\per", "/"),
)


def _log(level: str, msg: str) -> None:
    print(f"[{level}] {msg}")


def get_cache_bin_dir() -> Path:
    """Platform cache directory shared with the Tectonic bootstrap layout."""
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            cache_dir = Path(local_app_data) / "dissertation-skills" / "bin"
        else:
            cache_dir = Path.home() / ".local" / "bin"
    else:
        cache_dir = Path.home() / ".cache" / "dissertation-skills" / "bin"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def flatten_root_tex(source: str) -> str:
    """Replace the full scientific preamble with the Pandoc-safe macro file."""
    return PREAMBLE_INPUT_RE.sub(r"\\input{preamble_docx}", source, count=1)


def _pretty_unit(unit: str) -> str:
    pretty = unit
    for token, replacement in UNIT_REPLACEMENTS:
        pretty = pretty.replace(token, replacement)
    pretty = pretty.replace("\\", "")
    return pretty.strip()


def rewrite_siunitx(text: str) -> str:
    def si_repl(match: re.Match[str]) -> str:
        return f"{match.group(1).strip()} {_pretty_unit(match.group(2))}"

    def si_unit_repl(match: re.Match[str]) -> str:
        return _pretty_unit(match.group(1))

    text = SI_RE.sub(si_repl, text)
    return SI_UNIT_RE.sub(si_unit_repl, text)


def _simplify_colspec(spec: str) -> str:
    spec = TABULAR_ARRAY_RE.sub("l", spec)
    spec = TABULAR_S_RE.sub("l", spec)
    return spec


def rewrite_tabular_colspecs(text: str) -> str:
    return _simplify_colspec(text)


def rewrite_tex_font_groups(text: str) -> str:
    """Turn TeX font-size groups into commands Pandoc keeps (bold/italic/center)."""

    def _squash(body: str) -> str:
        return " ".join(body.replace("\\\\", " ").split())

    def bf_repl(match: re.Match[str]) -> str:
        body = _squash(match.group("body"))
        size = match.group("size")
        sized = f"\\{size} {body}" if size else body
        return "\\begin{center}\\textbf{" + sized + "}\\end{center}"

    def it_repl(match: re.Match[str]) -> str:
        body = _squash(match.group("body"))
        size = match.group("size")
        sized = f"\\{size} {body}" if size else body
        return "\\begin{center}\\textit{" + sized + "}\\end{center}"

    def size_repl(match: re.Match[str]) -> str:
        body = _squash(match.group("body"))
        return "\\begin{center}{\\" + match.group("size") + " " + body + "}\\end{center}"

    def size_bf_repl(match: re.Match[str]) -> str:
        body = _squash(match.group("body"))
        return (
            "\\begin{center}\\textbf{\\"
            + match.group("size")
            + " "
            + body
            + "}\\end{center}"
        )

    text = SIZE_TEXTBF_PAR_RE.sub(size_bf_repl, text)
    text = BF_PAR_RE.sub(bf_repl, text)
    text = IT_PAR_RE.sub(it_repl, text)
    text = SIZE_PAR_RE.sub(size_repl, text)
    text = re.sub(r"\\begin\{minipage\}\{[^}]+\}", "", text)
    text = text.replace(r"\end{minipage}", "")
    text = text.replace(r"\hfill", "\n\n")
    text = re.sub(r"\\hrule(?:\s+height\s+\S+)?", r"\\bigskip", text)
    return text


def rewrite_tex_page_breaks(text: str) -> str:
    """Turn LaTeX page-start commands into a marker Pandoc will keep as a paragraph."""
    text = re.sub(r"\\cleardoublepage\b", r"\\clearpage", text)
    text = re.sub(r"\\newpage\b", r"\\clearpage", text)
    return re.sub(r"\\clearpage\b", f"\n\n{PAGE_BREAK_MARKER}\n\n", text)


def rewrite_tex_for_pandoc(source: str, *, is_root: bool = False) -> str:
    """Make a TeX fragment tolerable for Pandoc without changing chapter inputs."""
    text = flatten_root_tex(source) if is_root else source
    text = TIKZ_RE.sub("[Chart rendered in the PDF edition.]", text)
    text = FOREST_RE.sub("[Phylogeny rendered in the PDF edition.]", text)
    text = rewrite_siunitx(text)
    text = rewrite_tabular_colspecs(text)
    text = rewrite_tex_font_groups(text)
    text = rewrite_tex_page_breaks(text)
    text = text.replace(r"\FloatBarrier", "")
    text = text.replace(r"\phantomsection", "")
    text = PRINTBIBLIOGRAPHY_RE.sub("", text)
    return text


def write_pandoc_workspace(root: Path, dest: Path) -> Path:
    """Copy a rewritten modular TeX tree into dest and return the flattened root."""
    dest.mkdir(parents=True, exist_ok=True)
    workspace = root.parent
    dest_root = dest / root.name
    dest_root.write_text(
        rewrite_tex_for_pandoc(root.read_text(encoding="utf-8"), is_root=True),
        encoding="utf-8",
    )

    preamble_src = workspace / "preamble_docx.tex"
    if not preamble_src.is_file():
        raise FileNotFoundError(f"Pandoc-safe preamble missing: {preamble_src}")
    shutil.copy2(preamble_src, dest / "preamble_docx.tex")

    bib = workspace / "references.bib"
    if bib.is_file():
        shutil.copy2(bib, dest / "references.bib")

    for dirname in DOCX_SOURCE_DIRS:
        src_dir = workspace / dirname
        if not src_dir.is_dir():
            continue
        out_dir = dest / dirname
        out_dir.mkdir(exist_ok=True)
        for tex in src_dir.glob("*.tex"):
            (out_dir / tex.name).write_text(
                rewrite_tex_for_pandoc(tex.read_text(encoding="utf-8"), is_root=False),
                encoding="utf-8",
            )
    return dest_root


def is_valid_docx(path: Path, *, min_bytes: int = MIN_DOCX_BYTES) -> bool:
    """True when path is a non-tiny OOXML package with a Word document part."""
    if not path.is_file():
        return False
    if path.stat().st_size < min_bytes:
        return False
    try:
        header = path.read_bytes()[:2]
    except OSError:
        return False
    if header != b"PK":
        return False
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
    except zipfile.BadZipFile:
        return False
    return "[Content_Types].xml" in names and "word/document.xml" in names


def docx_plain_text(path: Path) -> str:
    """Extract concatenated paragraph text from word/document.xml."""
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8", errors="replace")
    xml = re.sub(r"<w:tab[^/]*/>", " ", xml)
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<[^>]+>", "", xml)
    return html.unescape(xml)


def docx_missing_identity_strings(
    path: Path,
    required: Sequence[str] = DOCX_IDENTITY_STRINGS,
) -> List[str]:
    plain = docx_plain_text(path)
    lowered = plain.lower()
    return [token for token in required if token.lower() not in lowered]


def _pandoc_binary_name() -> str:
    return "pandoc.exe" if sys.platform == "win32" else "pandoc"


def find_pandoc_binary() -> Optional[Path]:
    """Search PATH, user bin, cache, and project-local .pandoc/bin."""
    which_path = shutil.which("pandoc")
    if which_path:
        return Path(which_path)

    binary_name = _pandoc_binary_name()
    candidates = [
        Path.home() / ".local" / "bin" / binary_name,
        get_cache_bin_dir() / binary_name,
        Path(__file__).resolve().parent / ".pandoc" / "bin" / binary_name,
    ]
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def _archive_name_for_platform() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system == "windows":
        return f"pandoc-{PANDOC_VERSION}-windows-x86_64.zip"
    if system == "linux":
        if "aarch64" in machine or "arm64" in machine:
            return f"pandoc-{PANDOC_VERSION}-linux-arm64.tar.gz"
        return f"pandoc-{PANDOC_VERSION}-linux-amd64.tar.gz"
    if system == "darwin":
        if "arm64" in machine:
            return f"pandoc-{PANDOC_VERSION}-arm64-macOS.zip"
        return f"pandoc-{PANDOC_VERSION}-x86_64-macOS.zip"
    raise RuntimeError(f"Unsupported operating system for Pandoc download: {system}")


def _find_extracted_pandoc(root: Path) -> Optional[Path]:
    wanted = {_pandoc_binary_name(), "pandoc", "pandoc.exe"}
    for path in root.rglob("*"):
        if not path.is_file() or path.name not in wanted:
            continue
        if "share" in path.parts:
            continue
        return path
    return None


def download_and_bootstrap_pandoc(target_dir: Path) -> Path:
    """Download the pinned Pandoc GitHub release and copy the binary into target_dir."""
    target_dir.mkdir(parents=True, exist_ok=True)
    archive_name = _archive_name_for_platform()
    download_url = f"{PANDOC_RELEASE_BASE}/{archive_name}"
    binary_name = _pandoc_binary_name()
    dest_binary = target_dir / binary_name

    _log("INFO", f"Auto-bootstrapping standalone Pandoc {PANDOC_VERSION}...")
    _log("INFO", f"Downloading {download_url}")

    with tempfile.TemporaryDirectory(prefix="pandoc-bootstrap-") as tmp:
        tmp_path = Path(tmp)
        archive_path = tmp_path / archive_name
        req = urllib.request.Request(
            download_url,
            headers={"User-Agent": "Mozilla/5.0 (DissertationBuilder/1.0)"},
        )
        with urllib.request.urlopen(req) as response, open(archive_path, "wb") as out_file:
            shutil.copyfileobj(response, out_file)

        extract_dir = tmp_path / "extracted"
        extract_dir.mkdir()
        if archive_name.endswith(".zip"):
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
        else:
            with tarfile.open(archive_path, "r:gz") as tar_ref:
                tar_ref.extractall(extract_dir)

        extracted = _find_extracted_pandoc(extract_dir)
        if extracted is None:
            raise FileNotFoundError(f"Pandoc binary was not found inside {archive_name}")

        shutil.copy2(extracted, dest_binary)
        if sys.platform != "win32":
            dest_binary.chmod(0o755)

    if not dest_binary.is_file():
        raise FileNotFoundError(f"Failed to install Pandoc to {dest_binary}")

    _log("SUCCESS", f"Pandoc binary installed successfully to {dest_binary}")
    return dest_binary


def ensure_pandoc() -> Path:
    """Return a usable Pandoc binary, downloading a pinned release if needed."""
    existing = find_pandoc_binary()
    if existing:
        _log("INFO", f"Found Pandoc executable at: {existing}")
        return existing

    cache_dir = get_cache_bin_dir()
    try:
        return download_and_bootstrap_pandoc(cache_dir)
    except Exception as exc:
        _log("WARNING", f"Cache install of Pandoc failed ({exc}). Trying project-local .pandoc/bin...")
        project_bin_dir = Path(__file__).resolve().parent / ".pandoc" / "bin"
        return download_and_bootstrap_pandoc(project_bin_dir)


HEADER_REL_TYPE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header"
)
FOOTER_REL_TYPE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"
)
HEADER_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"
)
FOOTER_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"
)
SECTPR_RE = re.compile(r"<w:sectPr\b.*?</w:sectPr>", re.DOTALL)


def _replace_style_block(styles: str, style_id: str, new_block: str) -> str:
    pattern = re.compile(
        rf'<w:style[^>]*w:styleId="{re.escape(style_id)}".*?</w:style>',
        re.DOTALL,
    )
    if not pattern.search(styles):
        return styles
    return pattern.sub(new_block, styles, count=1)


def _upsert_style_block(styles: str, style_id: str, new_block: str) -> str:
    pattern = re.compile(
        rf'<w:style[^>]*w:styleId="{re.escape(style_id)}".*?</w:style>',
        re.DOTALL,
    )
    if pattern.search(styles):
        return pattern.sub(new_block, styles, count=1)
    if "</w:styles>" in styles:
        return styles.replace("</w:styles>", new_block + "</w:styles>")
    return styles + new_block


def patch_styles_xml(styles: str) -> str:
    """Apply Kashmir thesis typography to a Pandoc reference styles.xml."""
    styles = styles.replace(
        '<w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" '
        'w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi" />',
        f'<w:rFonts w:ascii="{TIMES_NEW_ROMAN}" w:hAnsi="{TIMES_NEW_ROMAN}" '
        f'w:cs="{TIMES_NEW_ROMAN}" />',
    )
    styles = styles.replace(
        '<w:spacing w:after="200" />',
        f'<w:spacing w:after="0" w:line="{LINE_SPACING_ONE_HALF}" w:lineRule="auto" />',
    )
    styles = _replace_style_block(
        styles,
        "Normal",
        f"""<w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal" />
    <w:qFormat />
    <w:pPr>
      <w:spacing w:before="0" w:after="0" w:line="{LINE_SPACING_ONE_HALF}" w:lineRule="auto" />
      <w:ind w:firstLine="{FIRST_LINE_INDENT}" />
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="{TIMES_NEW_ROMAN}" w:hAnsi="{TIMES_NEW_ROMAN}" w:cs="{TIMES_NEW_ROMAN}" />
      <w:sz w:val="24" />
      <w:szCs w:val="24" />
      <w:color w:val="000000" />
    </w:rPr>
  </w:style>""",
    )
    styles = _replace_style_block(
        styles,
        "BodyText",
        f"""<w:style w:type="paragraph" w:styleId="BodyText">
    <w:name w:val="Body Text" />
    <w:basedOn w:val="Normal" />
    <w:link w:val="BodyTextChar" />
    <w:qFormat />
    <w:pPr>
      <w:spacing w:before="0" w:after="0" w:line="{LINE_SPACING_ONE_HALF}" w:lineRule="auto" />
      <w:ind w:firstLine="{FIRST_LINE_INDENT}" />
    </w:pPr>
  </w:style>""",
    )
    styles = _replace_style_block(
        styles,
        "FirstParagraph",
        f"""<w:style w:type="paragraph" w:customStyle="1" w:styleId="FirstParagraph">
    <w:name w:val="First Paragraph" />
    <w:basedOn w:val="BodyText" />
    <w:next w:val="BodyText" />
    <w:qFormat />
    <w:pPr>
      <w:spacing w:before="0" w:after="0" w:line="{LINE_SPACING_ONE_HALF}" w:lineRule="auto" />
      <w:ind w:firstLine="{FIRST_LINE_INDENT}" />
    </w:pPr>
  </w:style>""",
    )
    styles = _replace_style_block(
        styles,
        "Compact",
        f"""<w:style w:type="paragraph" w:customStyle="1" w:styleId="Compact">
    <w:name w:val="Compact" />
    <w:basedOn w:val="Normal" />
    <w:qFormat />
    <w:pPr>
      <w:spacing w:before="40" w:after="40" w:line="{LINE_SPACING_ONE_HALF}" w:lineRule="auto" />
      <w:ind w:firstLine="0" />
    </w:pPr>
  </w:style>""",
    )
    styles = _replace_style_block(
        styles,
        "Title",
        f"""<w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title" />
    <w:basedOn w:val="Normal" />
    <w:next w:val="BodyText" />
    <w:link w:val="TitleChar" />
    <w:uiPriority w:val="10" />
    <w:qFormat />
    <w:pPr>
      <w:spacing w:before="0" w:after="200" w:line="{LINE_SPACING_ONE_HALF}" w:lineRule="auto" />
      <w:ind w:firstLine="0" />
      <w:jc w:val="center" />
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="{TIMES_NEW_ROMAN}" w:hAnsi="{TIMES_NEW_ROMAN}" w:cs="{TIMES_NEW_ROMAN}" />
      <w:b />
      <w:color w:val="000000" />
      <w:sz w:val="32" />
      <w:szCs w:val="32" />
    </w:rPr>
  </w:style>""",
    )
    heading_specs = {
        "Heading1": ("32", "80", "320", "0", True),
        "Heading2": ("28", "240", "160", "1", False),
        "Heading3": ("24", "200", "120", "2", False),
    }
    for style_id, (size, before, after, level, caps) in heading_specs.items():
        caps_xml = "      <w:caps />\n" if caps else ""
        page_break_xml = "      <w:pageBreakBefore />\n" if style_id == "Heading1" else ""
        styles = _replace_style_block(
            styles,
            style_id,
            f"""<w:style w:type="paragraph" w:styleId="{style_id}">
    <w:name w:val="heading {style_id[-1]}" />
    <w:basedOn w:val="Normal" />
    <w:next w:val="BodyText" />
    <w:link w:val="{style_id}Char" />
    <w:uiPriority w:val="9" />
    <w:qFormat />
    <w:pPr>
{page_break_xml}      <w:keepNext />
      <w:keepLines />
      <w:spacing w:before="{before}" w:after="{after}" w:line="{LINE_SPACING_ONE_HALF}" w:lineRule="auto" />
      <w:ind w:firstLine="0" />
      <w:outlineLvl w:val="{level}" />
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="{TIMES_NEW_ROMAN}" w:hAnsi="{TIMES_NEW_ROMAN}" w:cs="{TIMES_NEW_ROMAN}" />
      <w:b />
      <w:color w:val="000000" />
      <w:sz w:val="{size}" />
      <w:szCs w:val="{size}" />
{caps_xml}    </w:rPr>
  </w:style>""",
        )
    styles = styles.replace(HEADING_ACCENT, "000000")
    styles = re.sub(r'\s*w:themeColor="accent1"', "", styles)
    styles = re.sub(r'\s*w:themeShade="BF"', "", styles)
    styles = _replace_style_block(
        styles,
        "Caption",
        f"""<w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption" />
    <w:basedOn w:val="Normal" />
    <w:pPr>
      <w:spacing w:before="80" w:after="160" w:line="{LINE_SPACING_ONE_HALF}" w:lineRule="auto" />
      <w:ind w:firstLine="0" />
      <w:jc w:val="center" />
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="{TIMES_NEW_ROMAN}" w:hAnsi="{TIMES_NEW_ROMAN}" w:cs="{TIMES_NEW_ROMAN}" />
      <w:i />
      <w:sz w:val="20" />
      <w:szCs w:val="20" />
    </w:rPr>
  </w:style>""",
    )
    styles = _upsert_style_block(
        styles,
        "Header",
        f"""<w:style w:type="paragraph" w:styleId="Header">
    <w:name w:val="header" />
    <w:basedOn w:val="Normal" />
    <w:pPr>
      <w:tabs>
        <w:tab w:val="right" w:pos="8666" />
      </w:tabs>
      <w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto" />
      <w:ind w:firstLine="0" />
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="{TIMES_NEW_ROMAN}" w:hAnsi="{TIMES_NEW_ROMAN}" w:cs="{TIMES_NEW_ROMAN}" />
      <w:b w:val="0" />
      <w:color w:val="000000" />
      <w:sz w:val="16" />
      <w:szCs w:val="16" />
    </w:rPr>
  </w:style>""",
    )
    styles = _upsert_style_block(
        styles,
        "Footer",
        f"""<w:style w:type="paragraph" w:styleId="Footer">
    <w:name w:val="footer" />
    <w:basedOn w:val="Normal" />
    <w:pPr>
      <w:tabs>
        <w:tab w:val="right" w:pos="8666" />
      </w:tabs>
      <w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto" />
      <w:ind w:firstLine="0" />
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="{TIMES_NEW_ROMAN}" w:hAnsi="{TIMES_NEW_ROMAN}" w:cs="{TIMES_NEW_ROMAN}" />
      <w:b w:val="0" />
      <w:color w:val="000000" />
      <w:sz w:val="16" />
      <w:szCs w:val="16" />
    </w:rPr>
  </w:style>""",
    )
    styles = _replace_style_block(
        styles,
        "Bibliography",
        f"""<w:style w:type="paragraph" w:styleId="Bibliography">
    <w:name w:val="Bibliography" />
    <w:basedOn w:val="Normal" />
    <w:next w:val="Bibliography" />
    <w:qFormat />
    <w:pPr>
      <w:spacing w:before="0" w:after="80" w:line="{LINE_SPACING_ONE_HALF}" w:lineRule="auto" />
      <w:ind w:left="720" w:hanging="720" w:firstLine="0" />
    </w:pPr>
  </w:style>""",
    )
    return styles


def patch_theme_xml(theme: str) -> str:
    theme = theme.replace('typeface="Aptos Display"', f'typeface="{TIMES_NEW_ROMAN}"')
    theme = theme.replace('typeface="Aptos"', f'typeface="{TIMES_NEW_ROMAN}"')
    return theme


def _hf_run_pr(*, italic: bool = False) -> str:
    italic_xml = "        <w:i/>\n" if italic else ""
    return (
        "      <w:rPr>\n"
        f'        <w:rFonts w:ascii="{TIMES_NEW_ROMAN}" w:hAnsi="{TIMES_NEW_ROMAN}" '
        f'w:cs="{TIMES_NEW_ROMAN}"/>\n'
        '        <w:color w:val="000000"/>\n'
        '        <w:sz w:val="16"/>\n'
        '        <w:szCs w:val="16"/>\n'
        f"{italic_xml}"
        "      </w:rPr>"
    )


def _header_xml() -> str:
    run_pr = _hf_run_pr(italic=True)
    run_pr_plain = _hf_run_pr()
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Header"/>
      <w:pBdr>
        <w:bottom w:val="single" w:sz="8" w:space="4" w:color="000000"/>
      </w:pBdr>
      <w:tabs>
        <w:tab w:val="right" w:pos="8666"/>
      </w:tabs>
      <w:ind w:firstLine="0"/>
    </w:pPr>
    <w:r>
{run_pr}
      <w:t xml:space="preserve">Antibacterial Potential of Dipsacus inermis: An in vitro Study</w:t>
    </w:r>
    <w:r><w:tab/></w:r>
    <w:r>
{run_pr_plain}
      <w:t>Enrollment No. 24061119001</w:t>
    </w:r>
  </w:p>
</w:hdr>
"""


def _footer_xml() -> str:
    run_pr = _hf_run_pr()
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Footer"/>
      <w:pBdr>
        <w:top w:val="single" w:sz="8" w:space="4" w:color="000000"/>
      </w:pBdr>
      <w:tabs>
        <w:tab w:val="right" w:pos="8666"/>
      </w:tabs>
      <w:ind w:firstLine="0"/>
    </w:pPr>
    <w:r>
{run_pr}
      <w:t xml:space="preserve">Department of Zoology, University of Kashmir, Srinagar, 190006, J&amp;K</w:t>
    </w:r>
    <w:r><w:tab/></w:r>
    <w:r>
{run_pr}
      <w:fldChar w:fldCharType="begin"/>
    </w:r>
    <w:r>
{run_pr}
      <w:instrText xml:space="preserve"> PAGE </w:instrText>
    </w:r>
    <w:r>
      <w:fldChar w:fldCharType="separate"/>
    </w:r>
    <w:r>
{run_pr}
      <w:t>1</w:t>
    </w:r>
    <w:r>
      <w:fldChar w:fldCharType="end"/>
    </w:r>
  </w:p>
</w:ftr>
"""


def _empty_header_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Header"/>
      <w:ind w:firstLine="0"/>
    </w:pPr>
  </w:p>
</w:hdr>
"""


def _empty_footer_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Footer"/>
      <w:ind w:firstLine="0"/>
    </w:pPr>
  </w:p>
</w:ftr>
"""


def _sectpr_xml(*, first_section: bool = False, existing: str = "") -> str:
    type_el = ""
    type_match = re.search(r"<w:type\b[^/]*/>", existing)
    if type_match:
        type_el = type_match.group(0)
    first_refs = ""
    title_pg = ""
    if first_section:
        first_refs = (
            '<w:headerReference w:type="first" r:id="rIdHeaderFirst"/>'
            '<w:footerReference w:type="first" r:id="rIdFooterFirst"/>'
        )
        title_pg = "<w:titlePg/>"
    return (
        "<w:sectPr>"
        '<w:headerReference w:type="default" r:id="rIdHeader1"/>'
        '<w:footerReference w:type="default" r:id="rIdFooter1"/>'
        f"{first_refs}"
        f"{title_pg}"
        f"{type_el}"
        "<w:footnotePr>"
        '<w:numRestart w:val="eachSect" />'
        "</w:footnotePr>"
        f'<w:pgSz w:w="{A4_WIDTH_TWIPS}" w:h="{A4_HEIGHT_TWIPS}"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1800" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        '<w:cols w:space="720"/>'
        '<w:docGrid w:linePitch="360"/>'
        "</w:sectPr>"
    )


def apply_section_headers(document: str) -> str:
    """Enable Different First Page on the opening section only; keep later chapter headers."""
    matches = list(SECTPR_RE.finditer(document))
    if not matches:
        return document
    pieces: List[str] = []
    last = 0
    for index, match in enumerate(matches):
        pieces.append(document[last:match.start()])
        pieces.append(_sectpr_xml(first_section=(index == 0), existing=match.group(0)))
        last = match.end()
    pieces.append(document[last:])
    return "".join(pieces)


def _ensure_relationship(rels: str, rel_id: str, rel_type: str, target: str) -> str:
    if f'Id="{rel_id}"' in rels:
        return rels
    tag = f'<Relationship Type="{rel_type}" Id="{rel_id}" Target="{target}"/>'
    return rels.replace("</Relationships>", tag + "</Relationships>")


def _ensure_override(types: str, part_name: str, content_type: str) -> str:
    if f'PartName="{part_name}"' in types:
        return types
    tag = f'<Override PartName="{part_name}" ContentType="{content_type}"/>'
    return types.replace("</Types>", tag + "</Types>")


def ensure_header_footer_package(parts: dict) -> None:
    """Write black running headers/footers and a blank first-page pair."""
    parts["word/header1.xml"] = _header_xml().encode("utf-8")
    parts["word/footer1.xml"] = _footer_xml().encode("utf-8")
    parts["word/headerfirst.xml"] = _empty_header_xml().encode("utf-8")
    parts["word/footerfirst.xml"] = _empty_footer_xml().encode("utf-8")

    rels = parts["word/_rels/document.xml.rels"].decode("utf-8")
    rels = _ensure_relationship(rels, "rIdHeader1", HEADER_REL_TYPE, "header1.xml")
    rels = _ensure_relationship(rels, "rIdFooter1", FOOTER_REL_TYPE, "footer1.xml")
    rels = _ensure_relationship(rels, "rIdHeaderFirst", HEADER_REL_TYPE, "headerfirst.xml")
    rels = _ensure_relationship(rels, "rIdFooterFirst", FOOTER_REL_TYPE, "footerfirst.xml")
    parts["word/_rels/document.xml.rels"] = rels.encode("utf-8")

    types = parts["[Content_Types].xml"].decode("utf-8")
    types = _ensure_override(types, "/word/header1.xml", HEADER_CONTENT_TYPE)
    types = _ensure_override(types, "/word/footer1.xml", FOOTER_CONTENT_TYPE)
    types = _ensure_override(types, "/word/headerfirst.xml", HEADER_CONTENT_TYPE)
    types = _ensure_override(types, "/word/footerfirst.xml", FOOTER_CONTENT_TYPE)
    parts["[Content_Types].xml"] = types.encode("utf-8")

    document = parts["word/document.xml"].decode("utf-8")
    parts["word/document.xml"] = apply_section_headers(document).encode("utf-8")


def write_reference_docx(pandoc_bin: Path, dest: Path) -> Path:
    """Build a thesis-styled Pandoc reference.docx from the default template."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [str(pandoc_bin), "-o", str(dest), "--print-default-data-file", "reference.docx"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    if proc.returncode != 0 or not dest.is_file():
        raise RuntimeError(proc.stderr or "Failed to export Pandoc default reference.docx")

    with zipfile.ZipFile(dest, "r") as src:
        parts = {name: src.read(name) for name in src.namelist()}

    styles = patch_styles_xml(parts["word/styles.xml"].decode("utf-8"))
    theme = patch_theme_xml(parts["word/theme/theme1.xml"].decode("utf-8"))
    parts["word/styles.xml"] = styles.encode("utf-8")
    parts["word/theme/theme1.xml"] = theme.encode("utf-8")
    ensure_header_footer_package(parts)

    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as out:
        for name, data in parts.items():
            out.writestr(name, data)
    return dest


def _ooxml_visible_text(block: str) -> str:
    return html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", block)))


def _is_heading1_para(block: str) -> bool:
    return bool(re.search(r'<w:pStyle\s+w:val="Heading1"', block))


def _is_bibliography_para(block: str) -> bool:
    return bool(re.search(r'<w:pStyle\s+w:val="Bibliography"', block))


def insert_docx_page_breaks(document: str) -> str:
    """Replace LaTeX clearpage markers with Word page breaks; skip doubles before Heading 1."""
    tokens = OOXML_TOKEN_RE.findall(document)
    rewritten: List[str] = []
    seen_content = False
    seen_bibliography = False
    for index, token in enumerate(tokens):
        if token.startswith("<w:tbl"):
            rewritten.append(token)
            seen_content = True
            continue
        text = _ooxml_visible_text(token).strip()
        if PAGE_BREAK_MARKER in text:
            lookahead = index + 1
            while lookahead < len(tokens):
                nxt = tokens[lookahead]
                if nxt.startswith("<w:tbl"):
                    break
                nxt_text = _ooxml_visible_text(nxt).strip()
                if nxt_text and PAGE_BREAK_MARKER not in nxt_text:
                    break
                lookahead += 1
            next_is_heading1 = lookahead < len(tokens) and _is_heading1_para(tokens[lookahead])
            next_is_bibliography = lookahead < len(tokens) and _is_bibliography_para(
                tokens[lookahead]
            )
            last_real = next((item for item in reversed(rewritten) if item), "")
            if (
                not seen_content
                or next_is_heading1
                or next_is_bibliography
                or last_real == PAGE_BREAK_PARAGRAPH
            ):
                rewritten.append("")
            else:
                rewritten.append(PAGE_BREAK_PARAGRAPH)
            continue
        if not seen_bibliography and _is_bibliography_para(token):
            seen_bibliography = True
            rewritten.append(REFERENCES_HEADING + token)
            seen_content = True
            continue
        rewritten.append(token)
        if text:
            seen_content = True
    token_iter = iter(rewritten)
    return OOXML_TOKEN_RE.sub(lambda _match: next(token_iter), document)


def center_frontmatter_compact(document: str) -> str:
    """Center short display lines until the first chapter heading; leave body text."""
    stop = False

    def repl(match: re.Match[str]) -> str:
        nonlocal stop
        block = match.group(0)
        if stop:
            return block
        if 'w:val="Heading1"' in block:
            stop = True
            return block
        if block.startswith("<w:tbl"):
            return block
        text = _ooxml_visible_text(block).strip()
        if not text or PAGE_BREAK_MARKER in text or len(text) > 110:
            return block
        if 'w:val="right"' in block:
            return block
        if "<w:jc " in block:
            block = re.sub(r'<w:jc w:val="[^"]+"\s*/>', '<w:jc w:val="center"/>', block)
        elif "<w:pPr>" in block:
            block = block.replace("<w:pPr>", '<w:pPr><w:jc w:val="center"/>', 1)
        else:
            block = block.replace("<w:p>", '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>', 1)
        if "<w:ind " in block:
            block = re.sub(r"<w:ind [^/]*/>", '<w:ind w:firstLine="0"/>', block)
        return block

    return OOXML_TOKEN_RE.sub(repl, document)


def polish_exported_docx(path: Path) -> None:
    """Keep thesis front-matter alignment, page starts, and first-page headers after Pandoc writes the package."""
    with zipfile.ZipFile(path, "r") as src:
        parts = {name: src.read(name) for name in src.namelist()}
    document = parts["word/document.xml"].decode("utf-8")
    document = center_frontmatter_compact(document)
    document = insert_docx_page_breaks(document)
    parts["word/document.xml"] = document.encode("utf-8")
    ensure_header_footer_package(parts)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as out:
        for name, data in parts.items():
            out.writestr(name, data)


def docx_layout_issues(path: Path) -> List[str]:
    """Return formatting contract failures for a generated dissertation DOCX."""
    issues: List[str] = []
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        styles = archive.read("word/styles.xml").decode("utf-8", errors="replace")
        document = archive.read("word/document.xml").decode("utf-8", errors="replace")
        theme = (
            archive.read("word/theme/theme1.xml").decode("utf-8", errors="replace")
            if "word/theme/theme1.xml" in names
            else ""
        )
        header = (
            archive.read("word/header1.xml").decode("utf-8", errors="replace")
            if "word/header1.xml" in names
            else ""
        )
        footer = (
            archive.read("word/footer1.xml").decode("utf-8", errors="replace")
            if "word/footer1.xml" in names
            else ""
        )
    if TIMES_NEW_ROMAN not in styles and TIMES_NEW_ROMAN not in theme:
        issues.append("Times New Roman is not the document font")
    if f'w:w="{A4_WIDTH_TWIPS}"' not in document:
        issues.append("A4 page size is missing")
    if 'w:left="1800"' not in document:
        issues.append("Thesis left margin (1.25 in) is missing")
    if f'w:line="{LINE_SPACING_ONE_HALF}"' not in styles:
        issues.append("1.5 line spacing is missing")
    heading1 = re.search(
        r'<w:style[^>]*w:styleId="Heading1".*?</w:style>',
        styles,
        re.DOTALL,
    )
    if heading1 and HEADING_ACCENT in heading1.group(0):
        issues.append("Heading 1 still uses the default teal accent colour")
    if heading1 and "<w:pageBreakBefore" not in heading1.group(0):
        issues.append("Heading 1 does not start a new page")
    if PAGE_BREAK_MARKER in document:
        issues.append("Unresolved page-break marker remains in the DOCX")
    if 'w:type="page"' not in document:
        issues.append("Front-matter page breaks are missing")
    if "word/header1.xml" not in names and "word/header.xml" not in names:
        if "headerReference" not in document:
            issues.append("Running header is missing")
    if "<w:titlePg" not in document:
        issues.append("Different first page is not enabled")
    if 'w:type="first"' not in document or "word/headerfirst.xml" not in names:
        issues.append("First-page header/footer pair is missing")
    if header and 'w:val="000000"' not in header:
        issues.append("Header text is not black")
    if footer and 'w:val="000000"' not in footer:
        issues.append("Footer text is not black")
    if "themeColor" in header or "themeColor" in footer:
        issues.append("Header/footer still use a theme accent colour")
    return issues


def _resource_path(workspace: Path) -> str:
    paths = [str(workspace), str(workspace / "figures")]
    return os.pathsep.join(paths)


def compile_with_pandoc(
    pandoc_bin: Path,
    flattened_root: Path,
    output: Path,
    workspace: Path,
    reference_doc: Optional[Path] = None,
    verbose: bool = False,
) -> Tuple[int, str]:
    bibliography = flattened_root.parent / "references.bib"
    cmd: List[str] = [
        str(pandoc_bin),
        str(flattened_root.name),
        "-o",
        str(output),
        "--from=latex",
        "--number-sections",
        "--top-level-division=chapter",
        "--resource-path",
        _resource_path(workspace),
        "--citeproc",
    ]
    if reference_doc is not None:
        cmd.extend(["--reference-doc", str(reference_doc)])
    if bibliography.is_file():
        cmd.extend(["--bibliography", str(bibliography)])

    _log("INFO", f"Executing: {' '.join(cmd)}")
    start_time = time.time()
    proc = subprocess.run(
        cmd,
        cwd=str(flattened_root.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )
    duration = time.time() - start_time
    transcript = (proc.stdout or "") + ("\n" if proc.stderr else "") + (proc.stderr or "")
    if verbose and transcript.strip():
        sys.stdout.write(transcript)
        sys.stdout.flush()
    _log("INFO", f"Pandoc finished in {duration:.2f} seconds (Exit code: {proc.returncode}).")
    return proc.returncode, transcript


def export_docx(root: Path, output: Path, verbose: bool = False) -> int:
    """Convert root LaTeX to output .docx. Returns 0 on success."""
    root = root.resolve()
    output = output.resolve()
    if not root.is_file():
        _log("ERROR", f"Root LaTeX file not found: {root}")
        return 1

    try:
        pandoc_bin = ensure_pandoc()
    except Exception as exc:
        _log("ERROR", f"Pandoc is not available: {exc}")
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        with tempfile.TemporaryDirectory(prefix="dissertation-docx-") as tmp:
            dest = Path(tmp)
            flattened = write_pandoc_workspace(root, dest)
            reference_doc = write_reference_docx(pandoc_bin, dest / "reference.docx")
            returncode, transcript = compile_with_pandoc(
                pandoc_bin,
                flattened,
                output,
                root.parent,
                reference_doc=reference_doc,
                verbose=verbose,
            )
            if returncode != 0:
                tail = "\n".join(transcript.strip().splitlines()[-20:])
                _log("ERROR", "Pandoc failed to write DOCX.")
                if tail:
                    _log("ERROR", tail)
                return 1
            polish_exported_docx(output)
    except subprocess.TimeoutExpired:
        _log("ERROR", "Pandoc timed out after 180 seconds.")
        return 1
    except Exception as exc:
        _log("ERROR", f"DOCX export failed: {exc}")
        return 1

    if not is_valid_docx(output):
        _log("ERROR", f"Expected output DOCX {output} is missing, empty, or not valid OOXML.")
        return 1

    missing = docx_missing_identity_strings(output)
    if missing:
        _log("ERROR", f"DOCX is missing identity text: {', '.join(missing)}")
        return 1

    layout_issues = docx_layout_issues(output)
    if layout_issues:
        _log("ERROR", "DOCX is missing thesis formatting: " + "; ".join(layout_issues))
        return 1

    size_kb = output.stat().st_size / 1024.0
    _log("SUCCESS", f"DOCX generated successfully: {output} ({size_kb:.2f} KB)")
    return 0


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = Path("dissertation.tex")
    output = Path("dissertation.docx")
    if args:
        root = Path(args[0])
    if len(args) > 1:
        output = Path(args[1])
    return export_docx(root, output)


if __name__ == "__main__":
    sys.exit(main())
