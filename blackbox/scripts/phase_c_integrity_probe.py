#!/usr/bin/env python3
import json, os, shutil, urllib.request, urllib.error
from pathlib import Path
BASE = os.environ.get("SDOS_BASE", "http://127.0.0.1:8000")
ANCHOR = Path(os.environ.get("SDOS_LEDGER_ANCHOR_PATH", "/tmp/sdos_stage2_anchor/ledger_anchor.json"))
OUT = Path(os.environ.get("OUT", "blackbox/results/phase_c.json"))
def get(path):
    try:
        with urllib.request.urlopen(BASE + path, timeout=5) as r:
            return r.status, r.read(512).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(512).decode("utf-8", "replace")
    except Exception as e:
        return None, str(e)
results = []
st, body = get("/ready")
results.append({"step": "ready_before", "status": st, "body": body[:200]})
if ANCHOR.exists():
    shutil.copy2(ANCHOR, str(ANCHOR) + ".bak")
    ANCHOR.write_text('{"count": 999999, "hmac_sha256": "deadbeef"}', encoding="utf-8")
    results.append({"step": "anchor_corrupted", "path": str(ANCHOR)})
else:
    results.append({"step": "anchor_missing", "path": str(ANCHOR)})
st2, body2 = get("/ready")
results.append({"step": "ready_after_anchor_tamper", "status": st2, "body": body2[:200], "pass": st2 == 503})
bak = Path(str(ANCHOR) + ".bak")
if bak.exists():
    shutil.move(str(bak), str(ANCHOR))
    results.append({"step": "anchor_restored"})
OUT.parent.mkdir(parents=True, exist_ok=True)
open(OUT, "w", encoding="utf-8").write(json.dumps(results, indent=2, ensure_ascii=False))
print(json.dumps(results, indent=2, ensure_ascii=False))
print("pass", all(r.get("pass", True) for r in results if "pass" in r))
