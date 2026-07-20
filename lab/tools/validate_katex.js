#!/usr/bin/env node
/* Validate every Arithmatex expression in a built MkDocs site with KaTeX. */

const fs = require("fs")
const path = require("path")
const katex = require("katex")

const siteRoot = path.resolve(process.argv[2] || "site")
const expressions = []

function decodeHtml(value) {
  const named = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", "#39": "'" }
  return value.replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos|#39);/gi, (_, entity) => {
    if (entity[0] !== "#") return named[entity.toLowerCase()]
    if (entity[1].toLowerCase() === "x") {
      return String.fromCodePoint(parseInt(entity.slice(2), 16))
    }
    return String.fromCodePoint(parseInt(entity.slice(1), 10))
  })
}

function inspect(filename) {
  const html = fs.readFileSync(filename, "utf8")
  const patterns = [
    { regex: /<span class="arithmatex">\\\(([\s\S]*?)\\\)<\/span>/g, display: false },
    { regex: /<div class="arithmatex">\\\[([\s\S]*?)\\\]<\/div>/g, display: true },
  ]

  for (const { regex, display } of patterns) {
    for (const match of html.matchAll(regex)) {
      expressions.push({
        display,
        expression: decodeHtml(match[1]),
        filename: path.relative(siteRoot, filename),
      })
    }
  }
}

function walk(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name)
    if (entry.isDirectory()) walk(target)
    else if (entry.isFile() && target.endsWith(".html")) inspect(target)
  }
}

if (!fs.existsSync(siteRoot)) {
  console.error(`Built site directory does not exist: ${siteRoot}`)
  process.exit(1)
}

walk(siteRoot)

const failures = []
for (const item of expressions) {
  try {
    katex.renderToString(item.expression, {
      displayMode: item.display,
      strict: "error",
      throwOnError: true,
    })
  } catch (error) {
    failures.push({ ...item, error: error.message })
  }
}

console.log(`KaTeX ${katex.version}: checked ${expressions.length} rendered expressions.`)
if (failures.length) {
  console.error(`\nFound ${failures.length} KaTeX rendering problem(s):`)
  for (const failure of failures) {
    console.error(`\n${failure.filename}\n${failure.expression}\n${failure.error}`)
  }
  process.exit(1)
}

console.log("All rendered expressions parse successfully.")
