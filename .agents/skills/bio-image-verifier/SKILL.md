---
name: bio-image-verifier
description: Verifies Kashmir M.Sc. dissertation photographs against live LaTeX includes, caption rules, and file placement. Use when adding or moving figures, checking missing images, or confirming a plate caption names only what is visible.
---

# Bio Image Verifier

Persona: examiner checking that every `\includegraphics` file exists and that captions do not invent species names, ChatGPT/WhatsApp filenames, or unread lid text.

## Live files only

- Root: `dissertation.tex` `\input` tree
- Images: `figures/` (`\graphicspath`)
- Staging originals: `research_sources/existing_work/`

Do not invent ATCC, voucher numbers, or species on unlabelled plates.

## Caption rules

1. Name only marks that are readable: C1, C2, N, GEN 5, P, dates, binomials on lids.
2. Unlabelled plates stay unlabelled. No invented Fig. 8c for *P. aeruginosa*.
3. No ChatGPT, WhatsApp, GPS-filename, or `agarplate-...` strings in captions.
4. Sequential `Fig.` numbers come from float order (`\counterwithout{figure}{chapter}`), not from `fig11_*.png` filenames.

## Procedure

1. Run:

```bash
uv run python .agents/skills/bio-image-verifier/scripts/verify_images.py \
    --root dissertation.tex \
    --figures figures \
    --report pipeline_outputs/image_verification.json
```

2. Copy a staged photo into `figures/` with a sequential `figN_...` name before citing it.
3. Fix missing includes or captions that over-name the photo.
4. Rebuild the PDF and confirm the List of Figures.

## Locked facts

- C1 = 50 mg/mL, C2 = 100 mg/mL, GEN 5 = 5 µg, N = distilled water
- ZOI inclusive of the disc; dual well+disc plates may appear in photos
- Collection GPS in captions only as Botanical Garden coordinates, never as a filename

## Report

Write `pipeline_outputs/image_verification.json` and a short `pipeline_outputs/image_verification.md`.
