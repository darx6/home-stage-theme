---
name: HomeStage
description: An op-art gallery: white walls, black line fields, and the product as the only colour in the room.
colors:
  gallery: "#FFFFFF"
  ink: "#000000"
typography:
  display:
    fontFamily: "Big Shoulders, sans-serif"
    fontSize: "clamp(3.5rem, 2rem + 6vw, 6rem)"
    fontWeight: 800
    lineHeight: 0.88
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Big Shoulders, sans-serif"
    fontSize: "2rem"
    fontWeight: 800
    lineHeight: 1
  title:
    fontFamily: "Big Shoulders, sans-serif"
    fontSize: "2.5rem"
    fontWeight: 800
    lineHeight: 1
    fontFeature: "\"tnum\", \"lnum\""
  body:
    fontFamily: "Schibsted Grotesk, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
  body-small:
    fontFamily: "Schibsted Grotesk, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Schibsted Grotesk, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.14em"
rounded:
  none: "0"
spacing:
  space-1: "0.25rem"
  space-2: "0.5rem"
  space-3: "0.75rem"
  space-4: "1rem"
  space-5: "1.5rem"
  space-6: "2rem"
  space-7: "3rem"
  space-8: "4.5rem"
  space-9: "7rem"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.gallery}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 2.75rem 0 1rem"
    height: "3.5rem"
  button-outline:
    backgroundColor: "{colors.gallery}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 2.75rem 0 1rem"
    height: "3.5rem"
  toggle:
    backgroundColor: "{colors.gallery}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 1rem"
    height: "2.75rem"
  toggle-selected:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.gallery}"
  field:
    backgroundColor: "{colors.gallery}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0 1rem"
    height: "3rem"
  fabric-canvas:
    rounded: "{rounded.none}"
    padding: "7px"
---

# Design System: HomeStage

## Overview

**Creative North Star: "The Op-Art Gallery"**

A white gallery where the interface is drawn in black line fields and the product hangs as the only colour in the room. Every surface of the theme is one of two materials, gallery white and matte ink, and every tone between them is made by how closely ink lines are spaced, never by a grey. The product image is framed like a canvas on a wall of parallel waves; fabric swatches are a row of small numbered canvases; lead time is a set of line strips whose frequency compresses as the piece nears completion.

Density is calm and gallery-like: generous vertical spacing, square frames, 2px ink rules separating every block, and one monumental type moment per page (the product name in tall condensed caps). Ornament is never added on top of the system; hover, selection and progress are all expressed by changing line frequency within the same two colours.

The world refuses the cream-serif furniture page and the photo-left, form-right template. Colour belongs to the merchant's goods, so the interface never competes with it.

**Key Characteristics:**
- Two colours only: gallery white and ink black, both merchant settings.
- Tone, emphasis and state made by line frequency (hatching, wave fields, line strips).
- 2px ink rules and square frames; no radius, no shadow.
- Colour appears only in product photography and fabric swatches.
- Tall condensed display caps over a neutral grotesk body and small tracked caps for labels.
- Motion is a single gesture: the wave field tightens and relaxes while the photo dissolves.

## Colors

A strict two-material palette; the merchant's product supplies all colour.

### Primary
- **Matte Ink** (`ink`): all text, every rule and frame, the filled primary button, selected toggles, hatching, wave fields, selection highlight, focus outlines, caret, scrollbar thumb and native `accent-color`. Exposed as `--ink`, aliasing the merchant colour setting `--color-foreground`.

### Neutral
- **Gallery White** (`gallery`): page ground, the inner canvas that holds the product image, the outlined button, unselected toggles, and the small white plates that sit label text on top of hatching. Exposed as `--gallery`, aliasing `--color-background`.

### Named Rules
**The Two Materials Rule.** The interface uses `--ink` and `--gallery` and nothing else. No greys, no tints, no alpha overlays for tone. If a surface needs to read darker or lighter, change the spacing of ink lines over it.

**The Product Is The Accent Rule.** Colour enters the page only through product photography, the 3D model, and fabric swatch images or swatch colours (`--swatch` from the fabric entry). Never colour a button, badge, link or state.

**The Line Frequency Rule.** Tone is a frequency: wide spacing reads light, tight spacing reads dark. The shipped vocabulary: wave stage behind the product at 13px spacing (merchant setting, 6 to 24px); footer band at 6px; button and field end-cap hatch at 2px ink every 5px; button hover at 3px ink every 4px (outline variant 1px ink every 5px); swatch hover 1px every 6px, selected 2px every 4px; lead-time strips 2px ink with a gap that shrinks by 2px per stage down to 3px.

## Typography

**Display Font:** Big Shoulders 800 (theme setting `type_display_font`, with the font's fallback stack)
**Body Font:** Schibsted Grotesk 400, bold 700 for emphasis (theme setting `type_body_font`)

**Character:** A tall, condensed poster grotesk set in caps for names and figures, against a plain, sturdy grotesk that does the reading. The contrast is height and width, not style.

### Hierarchy
- **Display** (800, `clamp(3.5rem, 2rem + 6vw, 6rem)`, 0.88, uppercase, balanced, max 9ch): the product name, once per page. The `.display` class also sets the header wordmark at 2rem.
- **Headline** (800, 2rem, 1, uppercase): section-level statements in display face, such as the lead-time weeks. Dimension summaries use the same treatment at 1.75rem.
- **Title** (800, 2.5rem, 1, tabular lining numerals): the price.
- **Body** (400, 1rem, 1.55): running text; long copy capped at 65ch (52ch in the footer note). Secondary detail text drops to 0.9375rem.
- **Label** (400, 0.8125rem, 0.14em tracking, uppercase, 1.4): the `.caption` voice for nav links, legends, figure captions, dt terms, toggle and button text (buttons at 700). Plain small notes (tax note, sample note, status) use 0.8125rem without caps.

### Named Rules
**The One Monument Rule.** One display-size type moment per page: the product name. Every other display-face use is 2.5rem or smaller.

**The Numbers Line Up Rule.** Prices, counts, fabric numbers and dates use tabular lining numerals (`.numerals`).

## Layout

Content sits in Skeleton's three-column section grid: a central column of `min(page width - 2 x margin, 100% - 2 x margin)` with page width 110rem (90rem narrow option) and a minimum margin of 32px (merchant range 12 to 80px).

The product page is a 4fr / 7fr two-column grid from 990px, with a merchant-set column gap (default 72px). The left column carries name, price, buy pair, lead time, dimensions and description; the right column is sticky (top `--space-5`) and carries the canvas stage and fabric range. Below 990px both columns dissolve (`display: contents`) and blocks reorder to name, canvas, fabrics, price, buy, then the rest. Header and footer collapse at 750px; the buy pair goes side by side at 750px and above.

Spacing follows a nine-step scale from 0.25rem to 7rem (`--space-1` to `--space-9`). Inside blocks, steps 2 to 5 do the work; 6 and above separate page regions (page padding `--space-6` top, `--space-9` bottom; footer offset `--space-8`).

## Elevation & Depth

Completely flat. There are no shadows anywhere. Depth is optical: the product canvas is a white plate framed by a 2px rule and set into a field of parallel ink waves, so the image appears hung on a vibrating wall. Layering is expressed by frame-inside-frame (stage border, canvas border) and by white plates cut out of hatching for legible labels.

### Named Rules
**The Frame Not Shadow Rule.** Separate and lift with a 2px ink frame and a change of line field, never with a shadow or a tint.

## Shapes

Square everything: radius 0 on buttons, inputs, selects, frames and swatches. Rules are 2px (`--rule`) for every structural line: header underline, block dividers, frames, button and field borders, focus outlines, selected underlines. 1px lines are reserved for drawing detail (dimension measure lines, the material/care divider). Silhouettes come from technical drawing: the sofa outline is a non-scaling 2px stroke, dimension arrows are 1px ink with white-plated figures, and the floor plan uses a heavy 6px room wall around a solid ink footprint.

## Components

### Buttons
Heavy, square and engineered, with a hatched end cap that marks them as part of the line world.
- **Shape:** square (0), 2px ink border, min height 3.5rem, text left-aligned toward a 1.75rem end cap on the inline end. The cap is divided from the label by a 2px rule and filled with the hatch (2px line every 5px).
- **Primary (Add to cart):** ink fill, gallery text, gallery-coloured hatch in the cap. Label voice, bold.
- **Outline (Order a sample):** gallery fill, ink text, ink hatch in the cap.
- **Hover:** the fill turns into a horizontal line field (primary 3px ink / 1px white; outline 1px ink every 5px). Transition 180ms linear on colour.
- **Disabled / busy:** `not-allowed` or `progress` cursor; disabled currently dims to 0.45 opacity, which renders grey; treat it as a known exception to the Two Materials Rule, not a pattern to reuse.

### Toggles and Tabs
- **Style:** square, 2px ink border (or shared border in a segmented group), gallery fill, label voice, min height 2.75rem (dimension tabs and unit switch 2.5rem).
- **Selected:** solid ink fill with gallery text (`aria-pressed` / `aria-selected`).
- **Hover (view toggles):** 1px ink lines every 5px over gallery.

### Inputs / Fields
- **Style:** square 2px ink frame, transparent input, min height 3rem, with a unit end cap: 2px rule, hatch fill, unit text on a white plate in label caps.
- **Focus:** the whole field gets the 2px ink outline at 3px offset (`:focus-within`); the bare input outline is suppressed.

### Navigation
- **Header:** wordmark in display face 2rem left, label-voice links, SVG account and cart icons right (44px cart target, ink count badge with tabular numerals). A 2px ink rule underlines the whole header. Current and hovered links take a 2px underline at 0.45em offset. Below 750px the links wrap to a second row.
- **Footer:** opens on a 3rem wave-field band (6px spacing) between two 2px rules, then a 2:1 grid of concept note and label-voice links.

### Product Canvas (signature)
The product hung as a canvas on a wave field. A 2:1 stage (4:3 below 990px) framed by a 2px rule holds a full-bleed wave field and, inset 5% / 9%, a white canvas with its own 2px frame. A label-voice caption names the fabric in the canvas corner. Images crossfade over 700ms `--ease-out` with the outgoing image blurring 6px; on every variant change the wave field pulses (spacing squeezes to 45% and relaxes over 900ms). The 3D view shows a drawn turn arrow; AR is offered as its own toggle. The pulse is skipped and transitions are flattened under `prefers-reduced-motion`.

### Fabric Range (signature)
Numbered canvases. Each swatch is a square image or colour inside a 2px ink frame, mounted on a 7px margin that takes a line field on hover (1px / 6px) and when selected (2px / 4px). Beneath: "No. 01" in small tracked numerals and the fabric name; the selected name goes bold with a 2px underline. A legend row with a 2px rule names the option and counts the fabrics. Material and care are listed below. Selection never relies on colour.

### Lead Time Strips (signature)
A 2px rule, the weeks in headline display caps, the arrival window in tabular numerals, then one 1.25rem strip per making stage whose vertical-line gap shrinks toward the final stage, so the list reads as compression toward completion.

### Dimensions (signature)
Three distances behind a segmented tab group: technical outline drawings with 1px measure lines, a floor plan with the piece as a solid ink footprint in a 6px-walled room, and a fit check built from the hatched-cap fields. An in/cm unit switch sits in the header.

### Disclosure
Description rows are separated by 2px rules; the summary uses the label voice and ends in a small hatched block that compresses (scaleY 0.4) when open instead of a chevron.

## Do's and Don'ts

### Do:
- **Do** build every new surface from `--ink` and `--gallery` only, and make tone with line spacing.
- **Do** use the 2px `--rule` for frames, dividers, borders and focus; keep 1px for drawing detail.
- **Do** end buttons and fields with the hatched end cap (2px ink every 5px behind a 2px divider).
- **Do** show state by changing line frequency or by inverting to solid ink, never by colour.
- **Do** give every swatch a visible number and name, and keep the selected name bold and underlined.
- **Do** use the 2px ink outline at 3px offset for every focus state, and keep targets at least 2.5rem (44px for icon links).
- **Do** route motion through `--ease-out` with `--duration-quick` (180ms) or `--duration-slow` (700ms), and stop all fields and transitions under `prefers-reduced-motion`.
- **Do** keep upgrade blocks self-contained: their own `{% stylesheet %}` and `{% javascript %}`, content from product metafields (`homestage.fabrics`, width/depth/height, lead-time weeks, making stages, sample product, outline drawings).

### Don't:
- **Don't** introduce greys, tints, gradients or alpha overlays to make tone.
- **Don't** colour any interface element; colour belongs to product photos and swatches.
- **Don't** add border radius or box shadows.
- **Don't** lay moiré or line fields over product photography; fields sit around the canvas, never on it.
- **Don't** set more than one display-size type moment per page.
- **Don't** animate prices, or animate anything that hides content without a reduced-motion fallback.
