/* Tailwind configuration for the tensor-logic apps in docs/interactive/.
 *
 * Those two pages used to load the Tailwind Play CDN, which generates this CSS
 * in the visitor's browser. The default configuration is what the Play CDN
 * applies when a page sets none, so the static build matches it; lab/tools/
 * vendor_assets.mjs writes the result to docs/assets/vendor/tailwind/. */
module.exports = {
  content: ["./docs/interactive/tensor-logic-*.html"],
  theme: { extend: {} },
  plugins: [],
}
