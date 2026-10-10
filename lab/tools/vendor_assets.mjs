#!/usr/bin/env node
/* Copy the browser assets the site serves itself into docs/assets/vendor/.
 *
 * The published notebook loads no code, styles or fonts from third-party
 * hosts. Everything a page needs comes from the npm packages pinned in
 * package.json (versions and integrity hashes in package-lock.json) and is
 * copied here before `mkdocs build`:
 *
 *   npm ci && npm run vendor && mkdocs build --strict
 *
 * The output directory is generated and ignored by git. A marker file with the
 * package versions is written last, so lab/tools/mkdocs_vendor_check.py can
 * refuse to build a site whose assets are missing or stale.
 */

import { execFileSync } from "node:child_process"
import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs"
import { dirname, join, resolve } from "node:path"
import { fileURLToPath } from "node:url"

const repo = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..")
const modules = join(repo, "node_modules")
const out = join(repo, "docs", "assets", "vendor")

// Weights in use: the notebook theme (Space Grotesk, JetBrains Mono) and the
// interactive apps under docs/interactive/ (Inter, JetBrains Mono).
const FONTS = {
  "space-grotesk": ["300", "400", "500", "600", "700"],
  "jetbrains-mono": ["300", "400", "500", "700", "400-italic", "700-italic"],
  inter: ["300", "400", "500", "600", "700", "800"],
}

function pkg(name) {
  const dir = join(modules, name)
  if (!existsSync(dir)) {
    throw new Error(`node_modules/${name} is missing; run \`npm ci\` first`)
  }
  return dir
}

function version(name) {
  return JSON.parse(readFileSync(join(pkg(name), "package.json"), "utf8")).version
}

function copy(from, to) {
  mkdirSync(dirname(to), { recursive: true })
  cpSync(from, to, { recursive: true })
}

rmSync(out, { recursive: true, force: true })

// KaTeX: stylesheet, renderer, auto-render, and the fonts the stylesheet names.
const katex = join(pkg("katex"), "dist")
for (const file of ["katex.min.css", "katex.min.js", "contrib/auto-render.min.js", "fonts"]) {
  copy(join(katex, file), join(out, "katex", file))
}

// Fonts: one stylesheet per family, concatenated from the fontsource weight
// files, with exactly the font files it names beside it.
for (const [family, weights] of Object.entries(FONTS)) {
  const source = pkg(`@fontsource/${family}`)
  const css = weights
    .map((weight) => readFileSync(join(source, `${weight}.css`), "utf8"))
    .join("\n")
    .replaceAll("url(./files/", `url(./${family}/`)
  mkdirSync(join(out, "fonts"), { recursive: true })
  writeFileSync(join(out, "fonts", `${family}.css`), css)
  const files = new Set([...css.matchAll(/url\(\.\/[^/]+\/([^)]+)\)/g)].map((m) => m[1]))
  for (const file of files) copy(join(source, "files", file), join(out, "fonts", family, file))
}

// Interactive apps: chart.js, plotly, and the Tailwind stylesheet the Play CDN
// used to generate in the browser (preflight plus the utilities in use).
copy(join(pkg("chart.js"), "dist", "chart.umd.min.js"), join(out, "chart.js", "chart.umd.min.js"))
copy(join(pkg("plotly.js-dist-min"), "plotly.min.js"), join(out, "plotly", "plotly.min.js"))
execFileSync(
  join(modules, ".bin", "tailwindcss"),
  [
    "--config", join(repo, "lab", "tools", "tailwind.interactive.config.cjs"),
    "--input", join(repo, "lab", "tools", "tailwind.interactive.css"),
    "--output", join(out, "tailwind", "interactive.css"),
    "--minify",
  ],
  { cwd: repo, stdio: ["ignore", "ignore", "inherit"] },
)

const versions = Object.fromEntries(
  ["katex", "chart.js", "plotly.js-dist-min", "tailwindcss", ...Object.keys(FONTS).map((f) => `@fontsource/${f}`)]
    .map((name) => [name, version(name)]),
)
writeFileSync(join(out, "VERSIONS.json"), JSON.stringify(versions, null, 2) + "\n")
console.log(`vendored into ${out.replace(repo + "/", "")}:`, versions)
