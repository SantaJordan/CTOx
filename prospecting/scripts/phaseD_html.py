#!/usr/bin/env python3
"""Build a PUBLIC-SAFE HTML playbook from companies_by_pain_PUBLIC.csv (NO PII:
no names/emails/phones). Output: prospecting/carl_leads_playbook.html"""
import csv, os, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def p(*a): return os.path.join(ROOT, *a)
SRC = p("companies_by_pain_PUBLIC.csv")   # redacted source — no contact PII
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
TOP = rows[:75]
n = len(rows)
no_cto = sum(1 for r in rows if r.get("has_full_time_cto") == "no")
jobpain = sum(1 for r in rows if (r.get("jobs_pain_score") or "0") not in ("", "0"))

def td(s): return f"<td>{html.escape(str(s))}</td>"
trs = []
for r in TOP:
    trs.append("<tr>" + "".join([
        td(r["rank"]), td(r["pain_score"]),
        f"<td><b>{html.escape(r['company'])}</b><br><span class=dim>{html.escape(r['industry'][:32])}</span></td>",
        td(r["integration_opportunity"]),
        f"<td>{'<span class=red>no full-time CTO</span>' if r['has_full_time_cto']=='no' else 'has CTO'}"
        f"<br><span class=dim>{html.escape(str(r['tech_count']))} eng · ratio {html.escape(str(r['technical_ratio']))}</span></td>",
        f"<td class=dim>{html.escape(r['why_i_believed'])}</td>",
        f"<td class=op>{html.escape(r['opener'])}</td>",
    ]) + "</tr>")

HTML = f"""<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Series A Integration-Gap Target List — Blueprint GTM</title>
<style>
body{{background:#0d1117;color:#e6edf3;font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:24px}}
h1{{font-size:24px;margin:0 0 4px}} .sub{{color:#7d8590;margin-bottom:20px;max-width:820px}}
.stats{{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:24px}}
.stat{{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:14px 18px;min-width:120px}}
.stat b{{font-size:26px;display:block;color:#58a6ff}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border-bottom:1px solid #21262d;padding:8px 10px;text-align:left;vertical-align:top}}
th{{color:#7d8590;position:sticky;top:0;background:#0d1117}}
.dim{{color:#8b949e;font-size:11px;max-width:300px}} .red{{color:#f85149;font-weight:600}}
.op{{max-width:340px;color:#adbac7;font-size:12px}} tr:hover{{background:#161b22}}
.foot{{color:#7d8590;font-size:12px;margin-top:18px}}
</style></head><body>
<h1>Series A Integration-Gap Target List</h1>
<div class=sub>Series A, tech-enabled companies that depend on a key system-of-record, run multiple
platforms, show data-silo pain, and are thin on technical leadership — the profile a fractional
CTO unlocks. Scored on a 4-axis pain rubric. Contacts are delivered privately; this public view
is redacted. Built with Blueprint GTM.</div>
<div class=stats>
<div class=stat><b>{n}</b>qualified companies</div>
<div class=stat><b>{no_cto}</b>no full-time CTO</div>
<div class=stat><b>{jobpain}</b>hiring-signal pain</div>
<div class=stat><b>4</b>scoring axes</div>
</div>
<h2>Top 75 by pain</h2>
<table><thead><tr>
<th>#</th><th>Pain</th><th>Company</th><th>Integration opportunity</th><th>Tech leadership</th>
<th>Why it's a fit</th><th>Opener (message = redescription of targeting)</th>
</tr></thead><tbody>
{''.join(trs)}
</tbody></table>
<div class=foot>Redacted public view ({n} companies total; top 75 shown). Methodology: niche → 4-axis
rubric → TAM filter → enrich → pain-sort. No personal contact data published.</div>
</body></html>"""
out = p("carl_leads_playbook.html")
open(out, "w", encoding="utf-8").write(HTML)
print("wrote", out, f"({len(HTML)} bytes, {len(TOP)} rows shown of {n}) — PUBLIC-SAFE, no PII")
