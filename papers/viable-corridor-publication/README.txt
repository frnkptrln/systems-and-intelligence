The Viable Corridor - publication review package
Prepared 10 September 2026. This is a review package, not a submission.

Deliverables
- manuscript.pdf/.tex/.md: the complete erratum-bearing scientific manuscript,
  including original abstract, Appendices A-D and references (73 pages).
- article.pdf/.tex/.md: a shortened Article copy (52 pages). The cover contains
  the title, author details, abstract and six keywords; Introduction starts on
  page 2. Appendices and their figures are supplied separately.
- supplementary-material.pdf/.tex/.md: original Appendices A-D and references
  (18 pages), with title, author affiliation and correspondence details.
- figures/: all six figures as vector PDF and 600-dpi PNG. The tracked repository
  Figure 1 PNG is also regenerated from the corrected canonical script.
- manifest.json: source/artifact hashes, original seeds, runtime versions, word
  counts and immutable repository links. The manifest identifies the precise
  build source; it does not identify the independently deployed website PDF.
- arxiv-metadata.txt: unsent title, author, qualified abstract and category draft.
- review-package.zip: the complete deliverable bundle, with integrity manifest.
- cover-letter-draft.txt and review-disposition.txt: unsent cover draft and the
  remaining external scientific/author decisions.

Scientific scope
The 7 September erratum is authoritative: the original sufficiency conjunction
is refuted in its Lorentzian continuum reading. A population-specific,
coherence-floor-dependent replacement remains open. The v1.0 measurements,
original seeds and numerical definitions are unchanged. None of the three
required independent scientific reviews is supplied by this editorial audit.

The Article is derived through article-edits.json: exact text replacements
shorten the abstract and repeated framing/discussion without changing the
canonical scientific body. The complete sufficiency/erratum section, limitations,
appendix content and displayed equations are protected by regression checks.
Mechanical bibliography corrections in the source include the Strogatz-Mirollo
1991 author order, APA handling of long author lists, DOI links and individually
identified Pew 2014/2016/2022 reports. All outputs use the source manuscript title.

Reproduce from the repository root:
  python lab/tools/build_viable_publication.py --output /absolute/output/path
Required: Python dependencies from requirements.txt and requirements-docs.txt,
pandoc, and xelatex. Alternatively, install Tectonic and add --engine tectonic;
its first build downloads a TeX bundle and requires network access. DejaVu Serif
must be installed. The builder checks its programs before starting simulations.
Default generation repeats the canonical TEO and 200-seed ABM figure calculations.
--reuse-figures requires every expected figure hash and figure-source hash to
match an existing manifest. No upload or submission operation is included.

Venue check, 2026-09-10
Artificial Life's official indexed guidelines specify an Article band typically
of 6,000-12,000 words; PDF initial submissions; LaTeX/Word accepted submissions;
single-column, double-spaced text; APA 7; six or five keywords; and separate
supplementary material. Vector figure exports and 600-dpi PNGs are supplied.
The Article body, including references and editorial notice but excluding cover
details and Supplement, is below 12,000 pandoc-plain whitespace words. Exact
counts and their scope are in the manifest. The full review manuscript is longer.
The direct guideline fetch returned HTTP 403; the official indexed text was
available. Recheck the submission portal when actually submitting.
https://direct.mit.edu/artl/pages/submission-guidelines

Validation and release scope
All final PDF pages are rendered for visual inspection; missing-glyph and overfull
line warnings fail the build. Numerical regression checks preserve the historical
results. This package changes neither the journal submission state nor the live
website PDF. External scientific review and the author's final declarations and
approval remain open; accepted-stage BibTeX and publication forms follow the
journal's requirements if the manuscript is accepted.
