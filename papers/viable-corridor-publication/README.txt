The Viable Corridor — erratum-bearing publication review package
Prepared 8 September 2026, from main 1bbf4b4 plus the publication-preparation diff.

Scientific status
The 7 September erratum is authoritative. The original sufficiency conjunction
is refuted in the Lorentzian continuum reading. A corrected statement dependent
on the coherence floor and population regime remains open. Historical v1.0
figures and numerical measurements are retained as evidence with their existing
scope. The three required independent scientific reviews remain outstanding.

Delivered
manuscript.pdf and manuscript.tex: single-column 11pt, double-spaced review copy,
including the full Abstract–References source and appendices. Website entrance,
revision history and TODO are excluded. The frozen source is preserved; only the derived export refreshes the production
caption sentence for its regenerated figure. The title page explicitly identifies the
erratum and pending reviews. Equations are reflowed without changing their values;
check/cross glyphs are written yes/no. All six figures are supplied as vector PDF
and 600-dpi PNG. The review-package Figure 1 contains the coherence-floor correction. The tracked
public PNG is unchanged pending explicit approval of its public upload.
manifest.json records exact source/artifact SHA-256 values, environment, seeds,
and the distinction between this review copy and the current live website PDF.
cover-letter-draft.txt is an unsent draft, with no unsupported declarations.
review-disposition.txt records the remaining scientific and editorial gates.

Reproduce from the repository root (pandoc and xelatex must be installed):
  python lab/tools/build_viable_publication.py --output /absolute/output/path
Python dependencies: the repository requirements.txt and requirements-docs.txt.
Default generation repeats the complete canonical TEO and 200-seed ABM figure
calculations. --reuse-figures checks an existing manifest and figure-source hashes
before reusing those files. There are no upload or submission operations.

Venue check
The Artificial Life submission-guideline search excerpt was checked on
2026-09-08: LaTeX/Word submissions and 600-dpi raster requirements are supported.
https://direct.mit.edu/artl/pages/submission-guidelines
The full page was unavailable (HTTP 403), so current end-to-end compliance is
not certified. The manuscript's author-date bibliography is preserved; the
specific remaining APA checks are in review-disposition.txt.

Validation
All 75 rendered pages were visually inspected in contact sheets, with figures,
tables and the erratum present. XeLaTeX reported no missing glyphs or overfull
horizontal lines after equation/path reflow. The regenerated numerical figures
use the original defaults and seeds, without adding a new scientific result.
Repository regression and integrity checks are recorded in the accompanying PR.
No publication, deployment, expert outreach or submission was performed.

Public artifact gate
Automatic approval review rejected uploading the regenerated PNG to the public
repository without explicit approval for scientific-artifact publication. This
PR therefore contains export code and production notes only; the complete
review package and proposed binary patch are delivered privately for review.
