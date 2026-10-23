// Usage: node shoot.mjs <out.png> <url> <width> <height>  — waits for document.title === 'READY'.
import { writeFileSync } from 'node:fs';
const [out, url, w, h] = process.argv.slice(2);
const tab = await (await fetch('http://127.0.0.1:9333/json/new?about:blank', { method: 'PUT' })).json();
const ws = new WebSocket(tab.webSocketDebuggerUrl);
let id = 0; const pending = new Map();
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); } };
await new Promise((r) => (ws.onopen = r));
const send = (method, params = {}) => new Promise((r) => { pending.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });
await send('Emulation.setDeviceMetricsOverride', { width: +w, height: +h, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url });
for (let i = 0; i < 120; i++) {
  const r = await send('Runtime.evaluate', { expression: 'document.title' });
  if (r.result.value === 'READY') break;
  await new Promise((r) => setTimeout(r, 500));
}
const shot = await send('Page.captureScreenshot', { format: 'png' });
writeFileSync(out, Buffer.from(shot.data, 'base64'));
await fetch(`http://127.0.0.1:9333/json/close/${tab.id}`);
process.exit(0);
