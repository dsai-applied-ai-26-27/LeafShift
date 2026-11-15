"""Local click-through review for the PlantDoc images in the mapped classes.

Run from the project root:

    .venv\\Scripts\\python.exe src\\review_plantdoc.py

It serves a page on http://127.0.0.1:8765, shows one image at a time, and writes
each decision straight into data/processed/plantdoc_review.csv in the existing
column order. No extra dependencies, standard library only.

Scope defaults to the images in the 9 mapped classes (990 rows), because those
are the only PlantDoc images that enter the cross-dataset evaluation. Pass
--scope all to walk the full 2,922.
"""

from __future__ import annotations

import argparse
import csv
import json
import mimetypes
import os
import socket
import sys
import threading
import webbrowser
from datetime import date
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PROJECT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = PROJECT / "data" / "processed" / "plantdoc_review.csv"
DEFAULT_ROOT = PROJECT / "data" / "raw" / "plantdoc"
DEFAULT_MAPPING = PROJECT / "data" / "processed" / "week7_class_mapping_counts.csv"

REVIEWER = "Emin Hadziabdic"
VALID = {"keep", "uncertain", "remove"}


# --------------------------------------------------------------------------- data
class Store:
    """Owns the CSV rows and writes them back after every decision."""

    def __init__(self, csv_path: Path, root: Path, mapping_path: Path, scope: str):
        self.csv_path = csv_path
        self.root = root
        self.lock = threading.Lock()

        with open(csv_path, newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            self.fieldnames = list(reader.fieldnames or [])
            self.rows = [dict(row) for row in reader]

        if not self.fieldnames:
            raise SystemExit(f"{csv_path} has no header row")

        # canonical class per PlantDoc folder, for display and scoping
        self.folder_to_class: dict[str, str] = {}
        if mapping_path.exists():
            with open(mapping_path, newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    folder = (row.get("plantdoc_folder") or "").strip()
                    canonical = (row.get("canonical_class") or "").strip()
                    if folder and canonical:
                        self.folder_to_class[folder] = canonical

        if scope == "all":
            self.scope_ids = list(range(len(self.rows)))
        else:
            self.scope_ids = [
                index
                for index, row in enumerate(self.rows)
                if row.get("original_label", "").strip() in self.folder_to_class
            ]

    def state(self) -> dict:
        items = []
        for index in self.scope_ids:
            row = self.rows[index]
            label = row.get("original_label", "").strip()
            items.append(
                {
                    "id": index,
                    "rel": row.get("relative_path", ""),
                    "label": label,
                    "canonical": self.folder_to_class.get(label, ""),
                    "split": row.get("relative_path", "").split("/")[0],
                    "decision": (row.get("decision") or "").strip().lower(),
                    "reason": row.get("reason", ""),
                    "final_label": row.get("final_label", ""),
                }
            )
        return {"items": items, "reviewer": REVIEWER, "scope": len(items)}

    def decide(self, index: int, decision: str, reason: str, final_label: str) -> dict:
        with self.lock:
            if index not in self.scope_ids:
                raise ValueError("row is outside the review scope")
            row = self.rows[index]
            decision = (decision or "").strip().lower()
            if decision and decision not in VALID:
                raise ValueError(f"unknown decision {decision!r}")
            if decision in {"uncertain", "remove"} and not reason.strip():
                raise ValueError("a reason is required for uncertain and remove")

            row["decision"] = decision
            row["reason"] = reason.strip()[:400]
            row["final_label"] = final_label.strip()[:120]
            if decision:
                row["reviewer"] = REVIEWER
                row["review_date"] = date.today().isoformat()
            else:
                row["reviewer"] = ""
                row["review_date"] = ""

            self._flush()
            return {
                "id": index,
                "decision": row["decision"],
                "reason": row["reason"],
                "final_label": row["final_label"],
            }

    def _flush(self) -> None:
        tmp = self.csv_path.with_suffix(".csv.tmp")
        with open(tmp, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=self.fieldnames)
            writer.writeheader()
            for row in self.rows:
                writer.writerow({key: row.get(key, "") for key in self.fieldnames})
        os.replace(tmp, self.csv_path)


# --------------------------------------------------------------------------- page
PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PlantDoc review - LeafShift</title>
<style>
  :root {
    --bg: #12141a;
    --panel: #1b1f27;
    --panel-2: #232833;
    --line: #2e3543;
    --text: #e9ecf1;
    --muted: #98a1b0;
    --keep: #3ddc84;
    --uncertain: #f5b942;
    --remove: #ef5f5f;
    --accent: #6aa9ff;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; height: 100%; }
  body {
    background: var(--bg); color: var(--text);
    font: 15px/1.45 "Segoe UI", system-ui, -apple-system, sans-serif;
    display: flex; flex-direction: column;
  }
  header { padding: 12px 18px 10px; border-bottom: 1px solid var(--line); }
  .bar { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
  .bar h1 { font-size: 15px; margin: 0; font-weight: 600; letter-spacing: .2px; }
  .counts { color: var(--muted); font-size: 13px; display: flex; gap: 12px; }
  .counts b { color: var(--text); font-variant-numeric: tabular-nums; }
  .spacer { flex: 1; }
  .mode { display: flex; gap: 4px; background: var(--panel); padding: 3px; border-radius: 8px; }
  .mode button {
    background: none; border: 0; color: var(--muted); padding: 5px 11px;
    border-radius: 6px; cursor: pointer; font-size: 13px;
  }
  .mode button[aria-pressed="true"] { background: var(--panel-2); color: var(--text); }
  .track { height: 3px; background: var(--panel-2); margin-top: 10px; border-radius: 2px; overflow: hidden; }
  .track div { height: 100%; width: 0; background: var(--keep); transition: width .2s ease; }

  main { flex: 1; display: flex; min-height: 0; }
  .stage {
    flex: 1; display: flex; align-items: center; justify-content: center;
    padding: 16px; min-width: 0; background: #0d0f13;
  }
  .stage img { max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 6px; }
  .missing { color: var(--remove); font-size: 14px; text-align: center; }

  aside {
    width: 330px; flex: 0 0 330px; border-left: 1px solid var(--line);
    padding: 16px; display: flex; flex-direction: column; gap: 14px; overflow-y: auto;
  }
  .class { font-size: 17px; font-weight: 600; }
  .folder { color: var(--muted); font-size: 12.5px; word-break: break-all; margin-top: 3px; }
  .pill {
    display: inline-block; font-size: 11px; letter-spacing: .4px; text-transform: uppercase;
    padding: 2px 7px; border-radius: 20px; background: var(--panel-2); color: var(--muted);
  }
  label { font-size: 12px; color: var(--muted); display: block; margin-bottom: 5px; }
  input[type="text"], textarea {
    width: 100%; background: var(--panel); color: var(--text); border: 1px solid var(--line);
    border-radius: 8px; padding: 9px 10px; font: inherit; font-size: 13.5px; resize: vertical;
  }
  input[type="text"]:focus, textarea:focus { outline: none; border-color: var(--accent); }
  .chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 7px; }
  .chips button {
    background: var(--panel); border: 1px solid var(--line); color: var(--muted);
    border-radius: 20px; padding: 4px 10px; font-size: 12px; cursor: pointer;
  }
  .chips button:hover { color: var(--text); border-color: var(--accent); }
  .actions { display: grid; grid-template-columns: 1fr; gap: 8px; margin-top: auto; }
  .actions button {
    border: 1px solid var(--line); background: var(--panel); color: var(--text);
    padding: 12px; border-radius: 9px; font: inherit; font-weight: 600; cursor: pointer;
    display: flex; justify-content: space-between; align-items: center;
  }
  .actions button span { font-weight: 400; color: var(--muted); font-size: 12px; }
  .actions button:hover { border-color: currentColor; }
  #b-keep:hover { color: var(--keep); }
  #b-uncertain:hover { color: var(--uncertain); }
  #b-remove:hover { color: var(--remove); }
  .nav { display: flex; gap: 8px; }
  .nav button {
    flex: 1; background: none; border: 1px solid var(--line); color: var(--muted);
    padding: 8px; border-radius: 8px; font: inherit; font-size: 12.5px; cursor: pointer;
  }
  .nav button:hover { color: var(--text); }
  .hint { font-size: 12px; color: var(--muted); min-height: 17px; }
  .hint.bad { color: var(--uncertain); }
  .done { text-align: center; padding: 30px 10px; }
  .done h2 { font-size: 18px; margin: 0 0 8px; }
  .done p { color: var(--muted); font-size: 13.5px; margin: 0 0 18px; }
  .done button {
    background: var(--keep); color: #0d1a12; border: 0; padding: 10px 18px;
    border-radius: 8px; font: inherit; font-weight: 600; cursor: pointer;
  }
  @media (max-width: 820px) {
    main { flex-direction: column; }
    aside { width: auto; flex: 0 0 auto; border-left: 0; border-top: 1px solid var(--line); }
    .stage { min-height: 45vh; }
  }
</style>
</head>
<body>
<header>
  <div class="bar">
    <h1>PlantDoc review</h1>
    <div class="counts">
      <span><b id="c-done">0</b>/<span id="c-total">0</span> reviewed</span>
      <span style="color:var(--keep)">keep <b id="c-keep">0</b></span>
      <span style="color:var(--uncertain)">uncertain <b id="c-uncertain">0</b></span>
      <span style="color:var(--remove)">remove <b id="c-remove">0</b></span>
    </div>
    <div class="spacer"></div>
    <div class="mode" id="mode">
      <button data-mode="pending" aria-pressed="true">To review</button>
      <button data-mode="all" aria-pressed="false">Everything</button>
    </div>
  </div>
  <div class="track"><div id="prog"></div></div>
</header>

<main>
  <div class="stage" id="stage"></div>
  <aside>
    <div>
      <div class="class" id="f-class">-</div>
      <div class="folder" id="f-folder">-</div>
      <div style="margin-top:8px"><span class="pill" id="f-split">-</span>
        <span class="pill" id="f-pos">-</span></div>
    </div>

    <div>
      <label for="reason">Reason <span id="reason-req"></span></label>
      <textarea id="reason" rows="2" placeholder="short, e.g. not a leaf / two diseases"></textarea>
      <div class="chips" id="chips"></div>
    </div>

    <div>
      <label for="final">Final label, optional</label>
      <input type="text" id="final" placeholder="leave empty to keep the folder label">
    </div>

    <div class="hint" id="hint"></div>

    <div class="nav">
      <button id="b-undo">Undo</button>
      <button id="b-skip">Skip</button>
    </div>

    <div class="actions">
      <button id="b-keep">Keep <span>1</span></button>
      <button id="b-uncertain">Uncertain <span>2</span></button>
      <button id="b-remove">Remove <span>3</span></button>
    </div>
  </aside>
</main>

<script>
const CONFIG = __CONFIG__;
const state = { items: [], byId: new Map(), queue: [], pos: 0, mode: 'pending', history: [] };
const el = id => document.getElementById(id);

const CHIPS = {
  remove: ['not a leaf', 'wrong crop', 'wrong disease', 'unreadable', 'collage or screenshot', 'stock photo watermark'],
  uncertain: ['two diseases visible', 'symptoms unclear', 'label unsure', 'too dark or blurry', 'stock photo watermark']
};

function counts() {
  let keep = 0, unc = 0, rem = 0;
  for (const it of state.items) {
    if (it.decision === 'keep') keep++;
    else if (it.decision === 'uncertain') unc++;
    else if (it.decision === 'remove') rem++;
  }
  return { keep, unc, rem, done: keep + unc + rem };
}

function refreshCounts() {
  const c = counts();
  el('c-done').textContent = c.done;
  el('c-total').textContent = state.items.length;
  el('c-keep').textContent = c.keep;
  el('c-uncertain').textContent = c.unc;
  el('c-remove').textContent = c.rem;
  el('prog').style.width = state.items.length ? (100 * c.done / state.items.length) + '%' : '0';
}

function buildQueue() {
  state.queue = state.items
    .filter(it => state.mode === 'all' || !it.decision)
    .map(it => it.id);
  state.pos = 0;
}

function current() {
  if (state.pos >= state.queue.length) return null;
  return state.byId.get(state.queue[state.pos]) || null;
}

function render() {
  refreshCounts();
  const it = current();
  const stage = el('stage');

  if (!it) {
    stage.innerHTML = '<div class="done"><h2>Nothing left in this view</h2>' +
      '<p>Switch to "Everything" to revisit decisions, or close this tab and rerun the notebook.</p>' +
      '<button id="b-open-all">Open Everything</button></div>';
    const openAll = document.getElementById('b-open-all');
    if (openAll) {
      openAll.onclick = () => {
        const all = el('mode').querySelector('[data-mode="all"]');
        if (all) all.click();
      };
    }
    el('f-class').textContent = '-';
    el('f-folder').textContent = '';
    el('f-split').textContent = '-';
    el('f-pos').textContent = '-';
    return;
  }

  const src = '/img?id=' + it.id + '&t=' + Date.now();
  stage.innerHTML = '<img alt="" src="' + src + '">';
  const img = stage.querySelector('img');
  img.onerror = () => { stage.innerHTML = '<div class="missing">image file not found on disk<br>' + it.rel + '</div>'; };

  el('f-class').textContent = it.canonical || it.label;
  el('f-folder').textContent = it.rel;
  el('f-split').textContent = it.split;
  el('f-pos').textContent = (state.pos + 1) + ' / ' + state.queue.length;
  el('reason').value = it.reason || '';
  el('final').value = it.final_label || '';
  setHint('');
  renderChips();
  el('reason').focus({ preventScroll: true });
}

function renderChips() {
  const kind = el('chips').dataset.kind || 'remove';
  const box = el('chips');
  box.innerHTML = '';
  for (const text of CHIPS[kind]) {
    const b = document.createElement('button');
    b.textContent = text;
    b.onclick = () => { el('reason').value = text; el('reason').focus(); setHint(''); };
    box.appendChild(b);
  }
}

function setHint(text, bad) {
  const h = el('hint');
  h.textContent = text || '';
  h.className = 'hint' + (bad ? ' bad' : '');
}

async function decide(decision) {
  const it = current();
  if (!it) return;
  const reason = el('reason').value.trim();
  const finalLabel = el('final').value.trim();

  if ((decision === 'uncertain' || decision === 'remove') && !reason) {
    el('chips').dataset.kind = decision;
    renderChips();
    el('reason-req').textContent = '(required for ' + decision + ')';
    setHint('Pick a chip or type a reason first.', true);
    el('reason').focus();
    return;
  }

  const before = { id: it.id, decision: it.decision, reason: it.reason, final_label: it.final_label };
  const response = await fetch('/api/decide', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: it.id, decision, reason, final_label: finalLabel })
  });
  if (!response.ok) {
    const detail = await response.text();
    setHint('Not saved: ' + detail, true);
    return;
  }

  state.history.push(before);
  it.decision = decision;
  it.reason = reason;
  it.final_label = finalLabel;
  el('reason-req').textContent = '';

  if (state.mode === 'pending') {
    state.queue.splice(state.pos, 1);
    if (state.pos >= state.queue.length) state.pos = state.queue.length;
  } else {
    state.pos++;
  }
  render();
}

async function undo() {
  const last = state.history.pop();
  if (!last) { setHint('Nothing to undo.', true); return; }
  const response = await fetch('/api/decide', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: last.id, decision: last.decision, reason: last.reason, final_label: last.final_label })
  });
  if (!response.ok) { setHint('Undo failed.', true); return; }
  const it = state.byId.get(last.id);
  it.decision = last.decision;
  it.reason = last.reason;
  it.final_label = last.final_label;
  buildQueue();
  const at = state.queue.indexOf(last.id);
  state.pos = at >= 0 ? at : Math.max(0, state.queue.length - 1);
  render();
}

function skip() {
  if (!current()) return;
  state.pos = (state.pos + 1) % Math.max(1, state.queue.length);
  render();
}

el('b-keep').onclick = () => decide('keep');
el('b-uncertain').onclick = () => { el('chips').dataset.kind = 'uncertain'; decide('uncertain'); };
el('b-remove').onclick = () => { el('chips').dataset.kind = 'remove'; decide('remove'); };
el('b-undo').onclick = undo;
el('b-skip').onclick = skip;

el('mode').onclick = event => {
  const button = event.target.closest('button[data-mode]');
  if (!button) return;
  state.mode = button.dataset.mode;
  for (const b of el('mode').querySelectorAll('button')) b.setAttribute('aria-pressed', String(b === button));
  buildQueue();
  render();
};

document.addEventListener('keydown', event => {
  if (event.target.tagName === 'TEXTAREA' && event.key !== 'Escape') {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      const kind = el('chips').dataset.kind || 'remove';
      decide(kind === 'uncertain' ? 'uncertain' : 'remove');
    }
    return;
  }
  if (event.key === '1' || event.key === 'k') { event.preventDefault(); decide('keep'); }
  else if (event.key === '2' || event.key === 'u') { event.preventDefault(); el('chips').dataset.kind = 'uncertain'; decide('uncertain'); }
  else if (event.key === '3' || event.key === 'r') { event.preventDefault(); el('chips').dataset.kind = 'remove'; decide('remove'); }
  else if (event.key === 'Backspace' || event.key === 'ArrowLeft') { event.preventDefault(); undo(); }
  else if (event.key === 'ArrowRight') { event.preventDefault(); skip(); }
});

async function boot() {
  const response = await fetch('/api/state');
  const data = await response.json();
  state.items = data.items;
  state.byId = new Map(state.items.map(it => [it.id, it]));
  buildQueue();
  render();
}
boot();
</script>
</body>
</html>
"""


# ------------------------------------------------------------------------ server
class Handler(BaseHTTPRequestHandler):
    store: Store
    page: bytes

    def log_message(self, fmt, *args):  # keep the console quiet
        pass

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send(HTTPStatus.OK, self.page, "text/html; charset=utf-8")
            return
        if parsed.path == "/api/state":
            body = json.dumps(self.store.state()).encode("utf-8")
            self._send(HTTPStatus.OK, body, "application/json")
            return
        if parsed.path == "/favicon.ico":
            self._send(HTTPStatus.NO_CONTENT, b"", "image/x-icon")
            return
        if parsed.path == "/img":
            query = parse_qs(parsed.query)
            try:
                index = int(query.get("id", ["-1"])[0])
            except ValueError:
                self._send(HTTPStatus.BAD_REQUEST, b"bad id", "text/plain")
                return
            if not 0 <= index < len(self.store.rows):
                self._send(HTTPStatus.NOT_FOUND, b"no such row", "text/plain")
                return
            path = self.store.root / self.store.rows[index]["relative_path"]
            if not path.is_file():
                self._send(HTTPStatus.NOT_FOUND, b"file missing", "text/plain")
                return
            content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            self._send(HTTPStatus.OK, path.read_bytes(), content_type)
            return
        self._send(HTTPStatus.NOT_FOUND, b"not found", "text/plain")

    def do_POST(self):
        if urlparse(self.path).path != "/api/decide":
            self._send(HTTPStatus.NOT_FOUND, b"not found", "text/plain")
            return
        length = int(self.headers.get("Content-Length") or 0)
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = self.store.decide(
                int(payload.get("id")),
                payload.get("decision", ""),
                payload.get("reason", "") or "",
                payload.get("final_label", "") or "",
            )
        except Exception as exc:  # report the message, do not crash the server
            self._send(HTTPStatus.BAD_REQUEST, str(exc).encode("utf-8"), "text/plain")
            return
        self._send(HTTPStatus.OK, json.dumps(result).encode("utf-8"), "application/json")


def free_port(preferred: int) -> int:
    for port in range(preferred, preferred + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise SystemExit("no free port found")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--scope", choices=["mapped", "all"], default="mapped")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    if not args.csv.is_file():
        raise SystemExit(f"review file not found: {args.csv}")
    if not args.root.is_dir():
        raise SystemExit(f"image folder not found: {args.root}")

    store = Store(args.csv, args.root, args.mapping, args.scope)
    page = PAGE.replace("__CONFIG__", json.dumps({"scope": len(store.scope_ids)})).encode("utf-8")

    handler = type("BoundHandler", (Handler,), {"store": store, "page": page})
    port = free_port(args.port)
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    url = f"http://127.0.0.1:{port}/"

    pending = sum(1 for i in store.scope_ids if not (store.rows[i].get("decision") or "").strip())
    print(f"Review file:  {args.csv}")
    print(f"Image root:   {args.root}")
    print(f"In scope:     {len(store.scope_ids)} images, {pending} still undecided")
    print(f"Open:         {url}")
    print("Stop with Ctrl+C. Decisions are written to the CSV as you click.")

    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    sys.exit(main())
