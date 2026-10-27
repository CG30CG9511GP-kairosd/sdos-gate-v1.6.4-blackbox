#!/usr/bin/env python3
import json, os, time, urllib.request, urllib.error
BASE = os.environ.get("SDOS_BASE", "http://127.0.0.1:8000")
out = []
def post(body, headers):
    req = urllib.request.Request(BASE + "/v1/gateway/analyze-batch", data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, r.read(256).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(256).decode("utf-8", "replace")
    except Exception as e:
        return None, str(e)
cases = [
    ("no_headers", b"{}", {}),
    ("bad_key", b"{}", {"Content-Type": "application/json", "X-SDOS-API-Key": "wrong-key-xxxxxxxxxxxxxxxxxxxxxxxx"}),
    ("bad_sig", b"{}", {"Content-Type": "application/json",
        "X-SDOS-API-Key": os.environ.get("SDOS_API_KEY", "test-key-that-is-long-enough-32-bytes"),
        "X-SDOS-Timestamp": str(int(time.time())), "X-SDOS-Nonce": "bb-nonce-1",
        "X-SDOS-Signature": "AA==", "X-SDOS-Tenant-ID": "default"}),
]
for name, body, h in cases:
    st, body_r = post(body, h)
    rec = {"case": name, "status": st, "body_prefix": body_r[:120], "pass": st in (401, 403)}
    out.append(rec)
    print(json.dumps(rec, ensure_ascii=False))
path = os.environ.get("OUT", "blackbox/results/phase_b.json")
os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
open(path, "w", encoding="utf-8").write(json.dumps(out, indent=2, ensure_ascii=False))
print("all_pass", all(x["pass"] for x in out))
