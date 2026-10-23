// node trace.cjs <silhouette.png> -> prints {"w","h","d"} for the outer contour(s)
const potrace = require('potrace');
const file = process.argv[2];
potrace.trace(file, { turdSize: 60, optTolerance: 0.6, alphaMax: 1.0, threshold: 128 }, (err, svg) => {
  if (err) throw err;
  const w = Number(svg.match(/width="([\d.]+)"/)[1]);
  const h = Number(svg.match(/height="([\d.]+)"/)[1]);
  const d = svg.match(/ d="([^"]+)"/)[1].replace(/\s+/g, ' ').trim();
  console.log(JSON.stringify({ w, h, d }));
});
