# HomeStage — home & interiors demo theme

## Goal
A demo store for home and furniture brands that shows our fixed-price product page upgrade: swatches with "order a sample", a dimensions block, lead-time messaging, a 3D/AR product viewer and crafted motion. Three product pages share the same sections: **sofa** (first), **linen bedding**, **ceramics**. Built to Theme Store standards so it can later become a sellable home & interiors theme. Design direction lives in `docs/DESIGN.md` once it exists; follow it.

## Store and tooling
- Dev store: `homestage-uqutijpv.myshopify.com` (default in `shopify.theme.toml`). Products are our own demo products, not Shopify test data.
- Base: Shopify Skeleton theme at commit `a4f32d39` (Feb 2026, sections + JSON templates). Skeleton v2 (Oct 2026) dropped sections; we stay on the section architecture because merchants edit sections in the theme editor and client themes (Dawn, Horizon) are section-based.
- Preview: `shopify theme dev` (needs the storefront password; the user runs it in their own terminal).
- Lint: `shopify theme check`.
- Shopify Dev MCP is configured in the parent folder: call `learn_shopify_api` (api: liquid) first, search docs before using unfamiliar objects/filters, and run `validate_theme` on every file created or changed.
- Git: commits go out as darx6. Commit messages are a single line, no body, no Co-Authored-By trailer.

## Portable sections
The paid job is adding these sections to a client's existing theme. Each upgrade section (swatches, dimensions, lead time, 3D/AR viewer) must be self-contained: its own `{% stylesheet %}` / `{% javascript %}`, settings in its own schema, metafield-driven content, no dependency on this theme's global CSS beyond CSS custom properties with fallbacks.

## Theme Store rules (same as Formula, verified 2026-10-07)
- Built from Shopify's Skeleton theme or fully original code. Never copy code from Dawn, Horizon or other themes.
- Lighthouse average across home, product and collection pages, desktop and mobile: performance ≥ 60, accessibility ≥ 90.
- No app-like features needing API access and nothing that depends on an app.
- No fake urgency, stock levels, countdowns or viewer counts. Lead times are real per-product data.
- Main product section: most elements are individual blocks; support `@app` blocks in main product and featured product sections; offer Custom Liquid blocks where apps might insert.
- Accessibility: keyboard access everywhere, visible focus, alt text on all images, labelled inputs, contrast 4.5:1 (3:1 for large text and UI), 24×24px touch targets, `lang` on `<html>`.
- Use `routes` for URLs, payment icons via `enabled_payment_types`, no Sass, no minified own CSS/JS, scripts hosted on Shopify, Open Graph/Twitter tags, rich product snippets.
- Uniqueness is judged on structure (header, product cards, media, page structure), not on colours, fonts or animation tweaks. Do not reuse Formula's structures wholesale; this theme needs its own.

## Code conventions
- Prefer sections, blocks and snippets; merchants assemble templates in the theme editor.
- Every merchant-facing value is a setting; every storefront string goes through `{{ 'key' | t }}` with keys in `locales/en.default.json`; schema labels use `t:` keys in `locales/en.default.schema.json`.
- Per-component CSS/JS in `{% stylesheet %}` / `{% javascript %}` (no Liquid inside them; pass values via CSS custom properties). Global tokens in `snippets/css-variables.liquid`.
- Snippets and statically rendered blocks start with a `{% doc %}` LiquidDoc header.
- Use `image_url` + `image_tag` with sizes/widths; lazy-load below the fold.
- 3D/AR: Shopify's native product media (`model_viewer_tag`), no third-party 3D libraries on product pages.
- No third-party JS or CSS libraries. Vanilla JS, custom elements where state is needed.
- Motion: transform/opacity/clip-path only, nothing hidden without a fallback, full `prefers-reduced-motion` support, never animate prices.
