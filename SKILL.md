---
name: bilingual-academic-pdf
description: Translate academic PDFs into Chinese pages that preserve the source layout, then create a page-by-page English-Chinese alternating PDF with strict artifact and visual checks. Use for research papers, lecture decks, or technical PDFs when the user wants an interleaved bilingual deliverable.
---

# Bilingual Academic PDF

Create two outputs from a source PDF:

- a Chinese-only PDF with one translated page for every source page;
- an interleaved bilingual PDF in the order English page 1, Chinese page 1, English page 2, Chinese page 2, and so on.

Keep the source PDF unchanged. Do not put all English pages first or add a cover page unless requested.

## Workflow

1. Inspect the source with PyMuPDF or `pdfinfo`: page count, rendered orientation, media boxes, rotation metadata, text extractability, and whether pages are scanned.
2. Preserve the source path and create a separate working directory. Never overwrite the source.
3. Build a paper glossary from the title, headings, captions, acronym definitions, and domain terminology. Preserve equations, variables, citations, URLs, author names, model names, units, and bibliography records.
4. Prefer a layout engine such as BabelDOC/PDFMathTranslate. For quality-sensitive work, use a two-pass auditable flow:
   - `capture`: freeze the ordered translated segments and formula placeholders;
   - review: translate every segment using the glossary, preserving every placeholder exactly;
   - layout: run the reviewed translations to produce the Chinese-only PDF.
5. Keep translation local unless the user explicitly authorizes sending extracted text to an external service. If a network backend is authorized, treat its output as draft text and review it before layout.
6. Treat the source page's visible orientation separately from its `/Rotate` metadata. A layout engine may normalize rotation while preserving the same rendered landscape or portrait view. Compare rendered pixel dimensions and visual orientation before forcing page boxes or rotation metadata.
7. Generate the bilingual PDF with `scripts/make_bilingual_pdf.py`. It inserts the original page verbatim, then the corresponding Chinese page, and writes a QC report.
8. Render a contact sheet and inspect at least the title page, one dense formula page, one figure-heavy page, one boundary or table page, and the final page. Inspect every patched page.

## Required invariants

- Source page count is N; Chinese-only output has N pages; bilingual output has exactly 2N pages.
- Every odd bilingual page is byte/render/text identical to the corresponding source page.
- Every even bilingual page corresponds to the same source index and contains Chinese text.
- The rendered width and height of each Chinese page match the rendered source page. Metadata rotation may differ when the visible orientation is unchanged; record that difference in QC rather than silently rotating content.
- No formula placeholder is missing, duplicated, or left visible. Equations, figures, tables, annotations, and citation identifiers remain legible.
- Do not release an output with untranslated ordinary prose, placeholder residue, formula corruption, clipped text, or collisions. If the layout engine produces a diagnostic PDF after strict QC fails, label it as a draft and repair or report the failure.

## Translation classification

Translate titles, abstracts, body prose, headings, captions, natural-language table cells, algorithm descriptions, notes, and editable labels. Preserve names, acronyms, citations, URLs, emails, equations, symbols, units, code, and bibliography entries. Translate figure labels only when the engine can replace them without covering artwork; otherwise record them for review.

## Failure handling

- If text is not extractable on most pages, prepare a searchable OCR copy and spot-check the OCR before translation.
- If page geometry differs, compare rendered dimensions first. Do not stretch pages to hide a mismatch.
- If strict QC fails, inspect its JSON report. Repair glossary coverage, segment review, fonts, or page-scoped patches, then rerun layout. Do not report a failed proof as final.
- Keep captured segments, reviewed translations, glossary, layout logs, and QC JSON with the deliverables so the result can be audited.

## Included helper

Use [scripts/make_bilingual_pdf.py](scripts/make_bilingual_pdf.py) after the Chinese-only PDF exists. It performs page-count, rendered-geometry, source-page identity, Chinese-text, and alternating-order checks and writes a concise QC JSON report.

For the detailed quality checklist and lessons from prior runs, read [references/quality-checklist.md](references/quality-checklist.md).
