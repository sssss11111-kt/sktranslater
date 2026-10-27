# bilingual-academic-pdf

A Codex Skill for translating academic and technical PDFs into Chinese while preserving the source layout, then producing an interleaved English-Chinese PDF.

## Outputs

- Chinese-only layout-preserving PDF
- Alternating bilingual PDF: English page 1, Chinese page 1, English page 2, Chinese page 2, ...
- Auditable glossary, segment review data, and QC JSON

## Design principles

- Keep source pages unchanged.
- Protect equations, variables, citations, URLs, names, and bibliography entries.
- Separate translation, layout reconstruction, bilingual assembly, and QC.
- Compare rendered page orientation separately from PDF rotation metadata.
- Keep external translation disabled unless the user explicitly authorizes it.

## Helper script

The included `scripts/make_bilingual_pdf.py` assembles and verifies an alternating PDF:

```powershell
python scripts/make_bilingual_pdf.py source.pdf translated_zh.pdf `
  --output translated_bilingual.pdf `
  --qc translated_bilingual_qc.json
```

The helper requires PyMuPDF. The layout translation engine is selected by the host workflow; BabelDOC/PDFMathTranslate is the recommended engine for scientific PDFs.

## Installation as a Codex Skill

Copy this directory into the local Codex skills directory, or clone this repository and point Codex at the skill folder. The entrypoint is `SKILL.md`.
