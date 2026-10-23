# Linden two-seat sofa: asset sources

All media for the Linden demo product is derived from CC0 (public domain) assets. No credit is legally required; credit is kept here for honesty.

| Asset | Source | Licence |
|---|---|---|
| 3D model (geometry, wood and base fabric textures) | [Sofa 01](https://polyhaven.com/a/Sofa_01) by Kirill Sannikov, Poly Haven | CC0 |
| Swatch textures | Poly Haven fabrics: [caban](https://polyhaven.com/a/caban), [wool_boucle](https://polyhaven.com/a/wool_boucle), [velour_velvet](https://polyhaven.com/a/velour_velvet), [rough_linen](https://polyhaven.com/a/rough_linen), [poly_wool_herringbone](https://polyhaven.com/a/poly_wool_herringbone), [ribbed_corduroy](https://polyhaven.com/a/ribbed_corduroy) | CC0 |

## How the files were made
- `recolour.py`: masks the upholstery in the sofa's diffuse texture by lightness and recolours it per fabric; recolours a centre crop of each Poly Haven fabric texture the same way (closer crops for herringbone and corduroy so the weave reads at swatch size) so swatch and sofa average to the same colour (`fabrics.json`, measured).
- Fabric 02 uses the `wool_boucle` texture, which is a houndstooth tweed, so it is named "Moss houndstooth".
- `outlines/`: front and side silhouettes from shadowless, near-orthographic renders (`flat.html`, 6° lens), traced to vector paths with `potrace@2.1.8` (`outlines/trace.cjs`). Stored on the product as the `homestage.outline_front` and `outline_side` JSON fields and drawn by the theme at one shared inch scale.
- `models/linden_<fabric>.glb`: the glTF with that fabric's texture, packed with `@gltf-transform/cli@4.1.0 copy`.
- `renders/linden_<fabric>_{34,front,side}.jpg`: rendered from the GLB with `@google/model-viewer@3.5.0` (neutral environment, neutral tone mapping, exposure 0.8) in headless Brave (`view.html`, `shoot.mjs`), trimmed and centred on white at 2000×1500.

Real size of the model: 157 × 66 × 80 cm (62 × 26 × 31 in). Product dimensions must use these values so AR shows the true size.
These are 3D renders, not photographs; label them as renders on the store.

Every raster here embeds its origin (`impeccable embed-prompt --read <file>`).
