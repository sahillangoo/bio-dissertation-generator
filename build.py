#!/usr/bin/env python3
"""
Master Compilation Engine for Biology & Zoology Doctoral Dissertation.
Cross-platform CLI supporting standalone Tectonic auto-bootstrapping,
Docker fallback, multi-pass cross-referencing, diagnostic validation,
clean PDF generation, and Pandoc DOCX export.
"""

from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import List, Optional, Tuple

from docx_export import export_docx

# Attempt rich and click imports; provide graceful standard fallbacks if needed
try:
    import click
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

TECTONIC_VERSION = "0.17.0"
TECTONIC_RELEASE_BASE = (
    f"https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%40{TECTONIC_VERSION}"
)

INTERMEDIATE_EXTENSIONS = [
    ".aux", ".bbl", ".blg", ".bcf", ".log", ".out", ".toc",
    ".lof", ".lot", ".xdv", ".run.xml", ".synctex.gz", "-converted-to.pdf"
]

def log_info(msg: str) -> None:
    if HAS_RICH and console:
        console.print(f"[bold blue][INFO][/bold blue] {msg}")
    else:
        print(f"[INFO] {msg}")

def log_success(msg: str) -> None:
    if HAS_RICH and console:
        console.print(f"[bold green][SUCCESS][/bold green] {msg}")
    else:
        print(f"[SUCCESS] {msg}")

def log_warning(msg: str) -> None:
    if HAS_RICH and console:
        console.print(f"[bold yellow][WARNING][/bold yellow] {msg}")
    else:
        print(f"[WARNING] {msg}")

def log_error(msg: str) -> None:
    if HAS_RICH and console:
        console.print(f"[bold red][ERROR][/bold red] {msg}")
    else:
        print(f"[ERROR] {msg}")


def get_cache_bin_dir() -> Path:
    """Determine the platform-appropriate binary cache directory."""
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


def find_tectonic_binary() -> Optional[Path]:
    """Search for existing Tectonic binary across PATH and known cache locations."""
    # 1. System PATH
    which_path = shutil.which("tectonic")
    if which_path:
        return Path(which_path)

    binary_name = "tectonic.exe" if sys.platform == "win32" else "tectonic"

    # 2. User ~/.local/bin
    local_bin = Path.home() / ".local" / "bin" / binary_name
    if local_bin.is_file() and os.access(local_bin, os.X_OK):
        return local_bin

    # 3. Platform cache directory
    cache_bin = get_cache_bin_dir() / binary_name
    if cache_bin.is_file() and os.access(cache_bin, os.X_OK):
        return cache_bin

    # 4. Project local .tectonic directory
    project_bin = Path(__file__).resolve().parent / ".tectonic" / "bin" / binary_name
    if project_bin.is_file() and os.access(project_bin, os.X_OK):
        return project_bin

    # 5. Alternate Windows locations
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            alt_path = Path(local_app_data) / "Tectonic" / binary_name
            if alt_path.is_file() and os.access(alt_path, os.X_OK):
                return alt_path

    return None


def download_and_bootstrap_tectonic(target_dir: Path) -> Path:
    """Download official standalone Tectonic binary from GitHub releases and extract it."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "windows":
        archive_name = f"tectonic-{TECTONIC_VERSION}-x86_64-pc-windows-msvc.zip"
        binary_name = "tectonic.exe"
    elif system == "linux":
        if "aarch64" in machine or "arm64" in machine:
            archive_name = f"tectonic-{TECTONIC_VERSION}-aarch64-unknown-linux-musl.tar.gz"
        else:
            archive_name = f"tectonic-{TECTONIC_VERSION}-x86_64-unknown-linux-musl.tar.gz"
        binary_name = "tectonic"
    elif system == "darwin":
        if "arm64" in machine:
            archive_name = f"tectonic-{TECTONIC_VERSION}-aarch64-apple-darwin.tar.gz"
        else:
            archive_name = f"tectonic-{TECTONIC_VERSION}-x86_64-apple-darwin.tar.gz"
        binary_name = "tectonic"
    else:
        raise RuntimeError(f"Unsupported operating system for automated binary download: {system}")

    download_url = f"{TECTONIC_RELEASE_BASE}/{archive_name}"
    archive_path = target_dir / archive_name
    extracted_binary = target_dir / binary_name

    log_info(f"Auto-bootstrapping standalone Tectonic {TECTONIC_VERSION}...")
    log_info(f"Downloading {download_url} -> {archive_path}")

    try:
        # Download archive with custom user agent
        req = urllib.request.Request(
            download_url,
            headers={"User-Agent": "Mozilla/5.0 (DissertationBuilder/1.0)"}
        )
        with urllib.request.urlopen(req) as response, open(archive_path, "wb") as out_file:
            shutil.copyfileobj(response, out_file)

        # Extract archive
        log_info(f"Extracting {archive_name}...")
        if archive_name.endswith(".zip"):
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(target_dir)
        elif archive_name.endswith(".tar.gz"):
            with tarfile.open(archive_path, "r:gz") as tar_ref:
                tar_ref.extractall(target_dir)

        if not extracted_binary.is_file():
            raise FileNotFoundError(f"Extracted binary {extracted_binary} was not found.")

        # Ensure executable permissions on Unix
        if sys.platform != "win32":
            extracted_binary.chmod(0o755)

        # Remove archive after extraction
        if archive_path.exists():
            archive_path.unlink()

        log_success(f"Tectonic binary installed successfully to {extracted_binary}")
        return extracted_binary

    except Exception as e:
        log_error(f"Failed to bootstrap standalone Tectonic: {e}")
        if archive_path.exists():
            archive_path.unlink()
        raise


def ensure_tectonic() -> Path:
    """Ensure a working Tectonic binary is available, downloading if necessary."""
    binary_path = find_tectonic_binary()
    if binary_path:
        log_info(f"Found Tectonic executable at: {binary_path}")
        return binary_path

    # Attempt bootstrapping into cache directory
    cache_dir = get_cache_bin_dir()
    try:
        return download_and_bootstrap_tectonic(cache_dir)
    except Exception:
        # Fallback to project-local .tectonic/bin
        project_bin_dir = Path(__file__).resolve().parent / ".tectonic" / "bin"
        project_bin_dir.mkdir(parents=True, exist_ok=True)
        return download_and_bootstrap_tectonic(project_bin_dir)


def check_docker_available() -> bool:
    """Check if Docker CLI and daemon are operational."""
    docker_path = shutil.which("docker")
    if not docker_path:
        return False
    try:
        res = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=8,
            check=False
        )
        return res.returncode == 0
    except Exception:
        return False


def clean_intermediates(workspace: Path, root_stem: str) -> None:
    """Clean intermediate LaTeX auxiliary files."""
    cleaned_count = 0
    # Clean files matching root stem
    for ext in INTERMEDIATE_EXTENSIONS:
        target = workspace / f"{root_stem}{ext}"
        if target.is_file():
            try:
                target.unlink()
                cleaned_count += 1
            except OSError:
                pass

    # Clean biblatex auxiliary files
    blx_bib = workspace / f"{root_stem}-blx.bib"
    if blx_bib.is_file():
        try:
            blx_bib.unlink()
            cleaned_count += 1
        except OSError:
            pass

    # Also clean general loose auxiliary files in workspace
    for item in workspace.iterdir():
        if item.is_file() and item.suffix in INTERMEDIATE_EXTENSIONS:
            try:
                item.unlink()
                cleaned_count += 1
            except OSError:
                pass

    log_info(f"Cleaned {cleaned_count} intermediate auxiliary files.")


def parse_diagnostics(transcript: str, log_file_content: str) -> Tuple[List[str], List[str], List[str]]:
    """
    Parse compilation transcript and log for warnings:
    - Undefined citations
    - Undefined references
    - Fatal errors
    """
    combined_text = transcript + "\n" + log_file_content

    # Match undefined citations
    citation_regex = re.compile(
        r"(?:LaTeX Warning:\s*Citation\s*[`']([^']+)'\s*on page \d+\s*undefined|citation [`']([^']+)'.*?undefined)",
        re.IGNORECASE
    )
    # Match undefined references
    ref_regex = re.compile(
        r"(?:LaTeX Warning:\s*Reference\s*[`']([^']+)'\s*on page \d+\s*undefined|reference [`']([^']+)'.*?undefined)",
        re.IGNORECASE
    )
    # Match fatal errors
    error_regex = re.compile(
        r"(!\s*(?:LaTeX|Package \w+) Error:.*|fatal error:.*)",
        re.IGNORECASE,
    )

    citations: List[str] = []
    for match in citation_regex.finditer(combined_text):
        cite_key = match.group(1) or match.group(2)
        if cite_key and cite_key not in citations:
            citations.append(cite_key)

    references: List[str] = []
    for match in ref_regex.finditer(combined_text):
        ref_key = match.group(1) or match.group(2)
        if ref_key and ref_key not in references:
            references.append(ref_key)

    errors: List[str] = []
    for match in error_regex.finditer(combined_text):
        err = match.group(1).strip()
        if err and err not in errors:
            errors.append(err)

    # Generic undefined markers
    if "[?]" in combined_text and not citations:
        citations.append("One or more [?] undefined citation markers detected in text.")
    if "??" in combined_text and not references:
        references.append("One or more ?? broken cross-reference markers detected in text.")

    return citations, references, errors


def compile_with_tectonic(
    tectonic_bin: Path,
    root_path: Path,
    outdir: Path,
    verbose: bool = False
) -> Tuple[int, str]:
    """Execute Tectonic compiler on root TeX document."""
    cmd = [
        str(tectonic_bin),
        str(root_path.name),
        "--outdir", str(outdir),
        "-p",  # Print engine progress
        "--keep-intermediates",
        "--keep-logs",
        # BibLaTeX (backend=bibtex) needs TeX → bibtex → TeX → TeX.
        "--reruns", "2",
    ]
    log_info(f"Executing: {' '.join(cmd)}")

    start_time = time.time()
    proc = subprocess.Popen(
        cmd,
        cwd=root_path.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    output_lines: List[str] = []
    if proc.stdout:
        for line in proc.stdout:
            output_lines.append(line)
            if verbose:
                sys.stdout.write(line)
                sys.stdout.flush()

    proc.wait()
    duration = time.time() - start_time
    transcript = "".join(output_lines)
    log_info(f"Tectonic finished in {duration:.2f} seconds (Exit code: {proc.returncode}).")
    return proc.returncode, transcript


def compile_with_docker(
    root_path: Path,
    outdir: Path,
    docker_image: str,
    verbose: bool = False
) -> Tuple[int, str]:
    """Execute Tectonic inside Docker container as fallback backend."""
    workspace_dir = root_path.parent.resolve()
    # Normalize Docker volume path
    vol_path = str(workspace_dir).replace("\\", "/")
    if vol_path[1:3] == ":/":
        # Windows drive letter C:/... -> /c/... or direct volume mount
        drive = vol_path[0].lower()
        vol_path = f"/{drive}" + vol_path[2:]

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{workspace_dir}:/workspace",
        "-w", "/workspace",
        docker_image,
        "tectonic", str(root_path.name),
        "--outdir", "/workspace",
        "-p",
        "--keep-intermediates",
        "--keep-logs",
        "--reruns", "2",
    ]
    log_info(f"Executing Docker container: {' '.join(cmd)}")

    start_time = time.time()
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    output_lines: List[str] = []
    if proc.stdout:
        for line in proc.stdout:
            output_lines.append(line)
            if verbose:
                sys.stdout.write(line)
                sys.stdout.flush()

    proc.wait()
    duration = time.time() - start_time
    transcript = "".join(output_lines)
    log_info(f"Docker compilation finished in {duration:.2f} seconds (Exit code: {proc.returncode}).")
    return proc.returncode, transcript


def build_dissertation(
    root: Path,
    output: Path,
    engine: str = "auto",
    clean: bool = False,
    keep_intermediates: bool = False,
    strict: bool = False,
    docker_image: str = "dxjoke/tectonic-docker:latest",
    verbose: bool = False
) -> int:
    """Main build coordination logic."""
    root = root.resolve()
    output = output.resolve()
    workspace = root.parent

    if not root.is_file():
        log_error(f"Root LaTeX file not found: {root}")
        return 1

    log_info(f"Starting dissertation build: {root.name} -> {output.name}")

    if clean:
        clean_intermediates(workspace, root.stem)

    # Determine backend
    selected_engine = engine.lower()
    tectonic_bin: Optional[Path] = None

    if selected_engine in ("auto", "tectonic", "system"):
        try:
            tectonic_bin = ensure_tectonic()
            selected_engine = "tectonic"
        except Exception as e:
            log_warning(f"Native Tectonic unavailable ({e}). Checking Docker...")
            if check_docker_available():
                selected_engine = "docker"
            else:
                log_error("Neither native Tectonic nor Docker is available to compile the dissertation.")
                return 1

    max_passes = 3
    pass_num = 1
    citations: List[str] = []
    references: List[str] = []
    errors: List[str] = []
    transcript = ""
    returncode = 0

    while pass_num <= max_passes:
        log_info(f"--- Compilation Pass {pass_num}/{max_passes} ---")
        if selected_engine == "docker":
            returncode, transcript = compile_with_docker(
                root, workspace, docker_image, verbose=verbose
            )
        else:
            assert tectonic_bin is not None
            returncode, transcript = compile_with_tectonic(
                tectonic_bin, root, workspace, verbose=verbose
            )

        # Check log file for diagnostic parsing
        log_file = workspace / f"{root.stem}.log"
        log_content = ""
        if log_file.is_file():
            try:
                log_content = log_file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass

        # Prefer the final engine log. -p chatter includes first-pass undefined
        # citations that later reruns (and bibtex) resolve.
        diag_source = log_content if log_content.strip() else transcript
        citations, references, errors = parse_diagnostics(diag_source, "")

        if errors:
            log_error(f"Fatal error encountered on pass {pass_num}.")
            if transcript:
                tail = "\n".join(transcript.strip().splitlines()[-12:])
                log_error(tail)
            break

        # Tectonic exits 1 while citations/labels are still resolving across passes.
        if returncode != 0 and not citations and not references:
            log_error(f"Compiler returned {returncode} on pass {pass_num} without parseable diagnostics.")
            break

        if not citations and not references:
            log_success(f"Convergence achieved on pass {pass_num}: 0 undefined citations, 0 broken references.")
            break

        log_info(f"Pass {pass_num} completed with {len(citations)} unresolved citations and {len(references)} unresolved references. Rerunning...")
        pass_num += 1

    # Check generated PDF
    default_generated_pdf = workspace / f"{root.stem}.pdf"
    if default_generated_pdf.is_file() and default_generated_pdf != output:
        try:
            if output.exists():
                output.unlink()
            shutil.move(str(default_generated_pdf), str(output))
        except Exception as e:
            log_warning(f"Could not rename {default_generated_pdf} to {output}: {e}")
            output = default_generated_pdf

    # Display Diagnostic Summary
    if HAS_RICH and console:
        diag_table = Table(title="Compilation Diagnostic Report", show_header=True)
        diag_table.add_column("Category", style="bold")
        diag_table.add_column("Count", justify="center")
        diag_table.add_column("Details")

        diag_table.add_row(
            "Fatal Errors",
            str(len(errors)),
            "[red]" + "; ".join(errors[:3]) + "[/red]" if errors else "[green]None[/green]"
        )
        diag_table.add_row(
            "Undefined Citations",
            str(len(citations)),
            "[yellow]" + ", ".join(citations[:5]) + "[/yellow]" if citations else "[green]Zero [?][/green]"
        )
        diag_table.add_row(
            "Broken References",
            str(len(references)),
            "[yellow]" + ", ".join(references[:5]) + "[/yellow]" if references else "[green]Zero ??[/green]"
        )
        console.print(diag_table)
    else:
        print("\n--- Compilation Diagnostic Report ---")
        print(f"Fatal Errors:        {len(errors)}")
        print(f"Undefined Citations: {len(citations)} -> {', '.join(citations[:5]) if citations else 'None'}")
        print(f"Broken References:   {len(references)} -> {', '.join(references[:5]) if references else 'None'}")
        print("-------------------------------------\n")

    # Output Validation
    if not output.is_file():
        log_error(f"Expected output PDF {output} was not created.")
        return 1

    pdf_size = output.stat().st_size
    if pdf_size == 0:
        log_error(f"Generated PDF {output} is empty (0 bytes).")
        return 1

    log_success(f"PDF generated successfully: {output} ({pdf_size / 1024:.2f} KB)")

    docx_output = output.with_suffix(".docx")
    docx_rc = export_docx(root, docx_output, verbose=verbose)
    if docx_rc != 0:
        log_error(f"DOCX export failed for {docx_output}")
        return 1

    if not keep_intermediates:
        clean_intermediates(workspace, root.stem)

    if strict and (citations or references or errors):
        log_error(
            f"Strict mode failure: {len(citations)} undefined citations, "
            f"{len(references)} broken references, {len(errors)} errors detected."
        )
        return 1

    return 0 if returncode == 0 else returncode


# --- Watch Mode ---
def watch_and_rebuild(root: Path, output: Path, **kwargs) -> None:
    """Watch thesis source files and automatically trigger rebuild on modification."""
    log_info(f"Watching directory {root.parent} for changes. Press Ctrl+C to terminate.")
    source_extensions = {".tex", ".bib", ".sty", ".cls", ".png", ".jpg", ".pdf"}
    ignored_names = {output.name, output.with_suffix(".docx").name}

    def get_mtimes() -> dict[Path, float]:
        mtimes = {}
        for path in root.parent.rglob("*"):
            if path.is_file() and path.suffix in source_extensions:
                # Ignore output and intermediates
                if path.name in ignored_names or path.name.startswith("."):
                    continue
                try:
                    mtimes[path] = path.stat().st_mtime
                except OSError:
                    pass
        return mtimes

    last_mtimes = get_mtimes()
    # Initial build
    build_dissertation(root, output, **kwargs)

    try:
        while True:
            time.sleep(1.0)
            current_mtimes = get_mtimes()
            changed = [p for p, mtime in current_mtimes.items() if mtime != last_mtimes.get(p)]
            if changed:
                log_info(f"Detected modification in: {', '.join(p.name for p in changed[:3])}. Rebuilding...")
                last_mtimes = current_mtimes
                build_dissertation(root, output, **kwargs)
    except KeyboardInterrupt:
        log_info("Watch mode terminated by user.")


# --- CLI Definition ---
if HAS_RICH and "click" in sys.modules:
    @click.command()
    @click.option("--root", "-r", type=click.Path(path_type=Path), default=Path("dissertation.tex"),
                  help="Path to root LaTeX document.")
    @click.option("--output", "-o", type=click.Path(path_type=Path), default=Path("dissertation.pdf"),
                  help="Destination path for compiled PDF.")
    @click.option("--engine", "-e", type=click.Choice(["auto", "tectonic", "docker", "system"]), default="auto",
                  help="Compilation backend engine.")
    @click.option("--clean", "-c", is_flag=True, default=False,
                  help="Clean auxiliary build files before and after compilation.")
    @click.option("--keep-intermediates", is_flag=True, default=False,
                  help="Retain auxiliary intermediate files.")
    @click.option("--strict", is_flag=True, default=False,
                  help="Fail with exit code 1 if undefined citations or broken cross-references exist.")
    @click.option("--watch", "-w", is_flag=True, default=False,
                  help="Watch source directory and recompile on file change.")
    @click.option("--docker-image", type=str, default="dxjoke/tectonic-docker:latest",
                  help="Docker image for containerized compilation.")
    @click.option("--verbose", "-v", is_flag=True, default=False,
                  help="Display verbose engine output.")
    def cli(root: Path, output: Path, engine: str, clean: bool, keep_intermediates: bool,
            strict: bool, watch: bool, docker_image: str, verbose: bool):
        """Automated LaTeX Dissertation Builder for Biology & Zoology."""
        if watch:
            watch_and_rebuild(
                root=root, output=output, engine=engine, clean=clean,
                keep_intermediates=keep_intermediates, strict=strict,
                docker_image=docker_image, verbose=verbose
            )
        else:
            exit_code = build_dissertation(
                root=root, output=output, engine=engine, clean=clean,
                keep_intermediates=keep_intermediates, strict=strict,
                docker_image=docker_image, verbose=verbose
            )
            sys.exit(exit_code)
else:
    def cli():
        import argparse
        parser = argparse.ArgumentParser(description="Automated LaTeX Dissertation Builder")
        parser.add_argument("--root", "-r", type=Path, default=Path("dissertation.tex"))
        parser.add_argument("--output", "-o", type=Path, default=Path("dissertation.pdf"))
        parser.add_argument("--engine", "-e", choices=["auto", "tectonic", "docker", "system"], default="auto")
        parser.add_argument("--clean", "-c", action="store_true")
        parser.add_argument("--keep-intermediates", action="store_true")
        parser.add_argument("--strict", action="store_true")
        parser.add_argument("--watch", "-w", action="store_true")
        parser.add_argument("--docker-image", default="dxjoke/tectonic-docker:latest")
        parser.add_argument("--verbose", "-v", action="store_true")
        args = parser.parse_args()

        if args.watch:
            watch_and_rebuild(
                root=args.root, output=args.output, engine=args.engine, clean=args.clean,
                keep_intermediates=args.keep_intermediates, strict=args.strict,
                docker_image=args.docker_image, verbose=args.verbose
            )
        else:
            exit_code = build_dissertation(
                root=args.root, output=args.output, engine=args.engine, clean=args.clean,
                keep_intermediates=args.keep_intermediates, strict=args.strict,
                docker_image=args.docker_image, verbose=args.verbose
            )
            sys.exit(exit_code)

if __name__ == "__main__":
    cli()
