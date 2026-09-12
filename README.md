# hello-world

## Prana Mandala

`mandala.html` is an interactive 3D mandala rendered as glowing orbs of energy
(Three.js / WebGL). Concentric rings, lotus petals, and radial spokes are drawn
as luminous linework with plasma-cored orbs at every node.

- **Drag** to orbit the void, **scroll / pinch** to zoom, **click / tap** to send
  a pulse of light rippling outward through the rings.
- Switch pigment palettes (Sand · Aurora · Ember), adjust glow, and toggle rotation.

Because `app.rb` serves any top-level `.html` by name, the page is available at
`/mandala` once the app is running (`bundle exec rackup`). It is also a
self-contained file you can open directly in a browser.
