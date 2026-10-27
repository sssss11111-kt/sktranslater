# Bilingual PDF quality checklist

## Why the workflow is split

Layout translation and bilingual assembly have different failure modes. A layout engine can produce a same-count Chinese-only PDF while page rotation metadata, rendered orientation, or segment coverage still needs review. Assemble the alternating PDF only after the Chinese-only file exists and has been rendered.

## Lessons from the reference run

- The source was a 56-page technical slide deck with a landscape visible orientation and a `/Rotate` value of 90. A normalized working copy had a different media-box representation but the same visible orientation. Comparing only `page.rect` rejected a valid visual match; compare rendered width and height and record metadata differences.
- BabelDOC required an isolated environment, compatible `bitstring`/`PyMuPDF` versions, CJK fonts, and a cached tokenizer asset. Keep these dependencies isolated and cache assets before processing a large document.
- Capture returned hundreds of ordered segments, many containing formula placeholders. Reviews must preserve tokens byte-for-byte. Formula-heavy segments should not go through broad word replacement.
- Strict validation correctly identified fragmented text runs that still contained English. Keep those findings in the QC report; do not suppress them merely to create a PDF.
- Figure labels and publisher/course identifiers may remain in English by design. Record them as preserved labels or manual-review items rather than treating every English token as a translation error.
- Always inspect rendered pages. A metadata rotation change can make a visually correct page appear sideways even when the media box looks plausible.

## Minimum QC fields

Record source and output paths, source/chinese/bilingual page counts, engine/backend, whether external text translation was used, glossary path, source-page identity checks, rendered geometry checks, Chinese-character counts, unresolved placeholders, untranslated-prose findings, visual-review scope, and known limitations.
