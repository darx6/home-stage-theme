# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Two audiences, in this order:

1. **Small home and furniture brand owners** (US, UK, Canada, Australia) who sell on Shopify and are judging whether our studio can upgrade their product pages. They arrive from a link in an email, a video audit, a forum reply or a job proposal, usually on a phone, and spend a minute or two deciding whether this is the quality they want on their own store.
2. **Their shoppers**, simulated: someone choosing a made-to-order sofa, bedding or ceramics who needs to see real colours and fabrics, know whether it fits their room, and know when it will arrive before committing $1,500–3,500.

## Product Purpose
HomeStage is a demo Shopify store for a fictional, mid-price, made-to-order home brand (sofas, linen bedding, ceramics). It exists to show, on a real working store, the studio's fixed-price product page upgrade: fabric/finish swatches with "order a sample", a dimensions block that answers "will it fit?", honest made-to-order lead times, a 3D/AR viewer and restrained, crafted motion. Success: a brand owner who sees it replies, or accepts a proposal, because the page looks like what they want for their own store.

Built to Shopify Theme Store standards so it can later become a sellable home & interiors theme.

## Positioning
Crafted by hand, not templated or AI-generated. The upgrade sections are self-contained so they can be added to a merchant's existing theme (Dawn, Horizon or others) for a fixed price in about six working days, rather than selling them a new theme.

## Operating Context
- Shopify Online Store 2.0 theme on the Skeleton base (sections + JSON templates), dev store `homestage-uqutijpv.myshopify.com`.
- Merchants edit everything in the Shopify theme editor; content comes from product metafields (swatches, dimensions, lead time).
- Prospects view it on mobile first; the page is also screen-recorded for 2-minute video audits and 20-second portfolio clips.
- Three product pages share the same sections: sofa (first), linen bedding, ceramics.

## Capabilities and Constraints
- Market: US. USD, US spelling, inches first with a switch to centimetres.
- Brand: mid-price, made to order; sofas roughly $1,500–3,500, made to order in 6–10 weeks.
- 3D/AR through Shopify's native product media; no third-party 3D libraries on product pages.
- Theme Store rules from `CLAUDE.md`: Lighthouse performance ≥ 60 and accessibility ≥ 90, no fake urgency or stock counts, no app dependencies, original code only (never Dawn or Horizon).
- Undecided: final product names, exact prices and lead times per product, the HomeStage logo.

## Brand Commitments
- Name: HomeStage (fictional). Clearly labelled as a concept store; it must never imply it is a real brand or a paid client.
- No AI-generated design or imagery.
- Visual direction is a baseline the studio's designer will refine.
- Must not resemble Formula, the studio's supplement theme (`../first-theme`): no heavy condensed uppercase grotesk display, no ink-on-white hairline rules and spec grids, no numbered label grammar. The first HomeStage direction (op-art gallery, Oct 2026) was rejected for drifting into that family.
- Preferred feel (user, Oct 2026): warm and tactile, distinctive but usable; a shopper understands the page at once.

## Evidence on Hand
- None yet for HomeStage: no products, photos, 3D models or copy exist.
- Imagery will come from free, licence-clear sources (Unsplash, Pexels photos; a CC0 3D sofa model, for example from Poly Haven), credited where required.
- Do not fabricate reviews, ratings, press mentions, customer counts or delivery statistics.

## Product Principles
1. Answer the shopper's real questions on the page: what it looks like in this fabric, will it fit, when will it arrive.
2. Every upgrade section must be portable to a client's theme and editable by a non-technical merchant.
3. Honest information over persuasion tricks: real lead times, no urgency, no invented proof.
4. Craft is visible in the details and restraint, not in effects.
5. Fast on a mid-range phone; motion never costs usability.

## Accessibility & Inclusion
WCAG 2.1 AA as required by the Theme Store: keyboard access, visible focus, 4.5:1 text contrast, 24×24px touch targets, swatches with text labels (never colour alone), full `prefers-reduced-motion` support.
