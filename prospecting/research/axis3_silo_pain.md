# Axis 3 — Silo Pain Detection & Scoring Rubric

**Axis definition:** Evidence that staff manually re-type or re-report data from one system to another, with no single source of truth. This is the pain a system integration would directly remove. The fractional CTO sells the cure; this axis scores how acute the disease is, from public signals only.

**Core mechanic of the pain:** A human is acting as the API between two systems. Wherever a person copies, re-keys, reconciles, or "pulls a report and pastes it into another tool," there is integration revenue.

---

## 1. Signal Source → Phrases Table

| Signal Source | What to look for | High-signal phrasing (verbatim patterns) |
|---|---|---|
| **Job postings — responsibilities** | The job *is* the integration glue a human is doing by hand | "manual data entry", "double entry / dual entry", "re-key / rekey / re-enter data", "copy and paste between systems", "transfer data between [X] and [Y]", "reconcile data across systems", "key in invoices/orders", "update both [system A] and [system B]", "manually export and import", "pull reports from [system] and load into [system]", "maintain spreadsheets to track…", "bridge the gap between [tool] and [tool]", "ensure data consistency across platforms" |
| **Job postings — titles** | Existence of the role implies the silo (see role list §1a) | "Data Entry Clerk", "Data Entry Specialist", "Order Entry Clerk", "Billing Coordinator", "Reconciliation Analyst", "Operations Analyst", "RevOps / Sales Ops Analyst", "Data Coordinator", "Reporting Analyst", "Systems Administrator (no eng)", "Implementation Specialist" (non-API), "EDI Coordinator", "Data Integrity Specialist", "Master Data Coordinator" |
| **Job postings — tooling tells** | Stack named as disconnected silos | "proficiency in Excel/VLOOKUP/pivot tables required", "advanced Excel", "experience with [CRM] AND [ERP] AND [billing]" listed as separate tools with no iPaaS/integration tool mentioned, "QuickBooks + Salesforce + spreadsheets" |
| **G2 / Capterra reviews — cons** | Customers describing the product as a silo | "doesn't integrate with…", "no integration with [tool]", "had to export to Excel", "manual export/import", "no API", "doesn't sync", "have to enter the same data twice", "no two-way sync", "data silos", "we use a separate system for…", "wish it talked to our [CRM/ERP]", "lots of manual workarounds", "we built a spreadsheet to bridge" |
| **G2 / Capterra reviews — workflow context** | Reviewer admits a human bridge | "we copy/paste from [A] to [B]", "re-enter everything into…", "reconcile at month-end by hand", "our ops team manually updates…" |
| **Company website / About / homepage** | Aspirational language admitting current state, OR product copy if they sell the cure (treat carefully, see §4) | "single source of truth" (as a *promise to themselves* in careers/about = pain; as a *product claim* = false positive), "connect your disconnected systems", "stop re-keying data", "eliminate manual data entry", "end of spreadsheets" |
| **Careers / culture pages** | Self-aware admissions | "we're scaling fast and our systems haven't kept up", "help us move off spreadsheets", "build the integrations we don't have", "modernize our tech stack", "our processes are manual today" |
| **News / funding / blog** | Growth that outpaces systems | "rapid growth", "doubled headcount", "post-acquisition integration", "merging two systems", "ERP migration", "digital transformation initiative" |

### 1a. Job Titles Whose Existence Implies Silo Pain

These roles exist primarily *because* systems don't talk. The denser the cluster, the higher the score.

- **Pure re-keying:** Data Entry Clerk/Specialist/Operator, Order Entry Clerk, Order Processor, Keying Specialist
- **Reconciliation glue:** Reconciliation Analyst, Billing Coordinator, Billing Specialist, AR/AP Clerk (when described as cross-system), Accounts Reconciliation Specialist
- **Reporting glue:** Reporting Analyst, BI Analyst (spreadsheet-based), Operations Analyst, Business Analyst (manual reporting)
- **Ops/RevOps glue:** RevOps Analyst, Sales Operations Analyst, Marketing Ops Coordinator, Operations Coordinator (when JD = "keep systems in sync")
- **Data-plumbing-by-hand:** Data Coordinator, Data Steward, Master Data Coordinator, Data Integrity Specialist, EDI Coordinator/Specialist
- **Integration-less "implementation":** Implementation Specialist / Onboarding Specialist whose JD is manual config + CSV uploads, with no API/engineering component

> Rule of thumb: a posting for a *new* data-entry/reconciliation/ops-analyst role is a stronger buy signal than an established one — it means the manual burden is *growing*.

---

## 2. Flat Keyword / Phrase List (lowercase, scan-ready)

Use for substring/regex scanning of scraped site text + job descriptions. Group A = strong, Group B = moderate, Group C = role titles, Group D = weak/contextual.

### Group A — strong silo phrases
```
manual data entry
manual entry
double entry
dual entry
double data entry
re-key
rekey
re-keying
re-enter data
re-enter the same data
enter data twice
enter the same data twice
copy and paste between systems
copy/paste between systems
copy data from one system
transfer data between systems
reconcile across systems
reconcile data across systems
manual reconciliation
no single source of truth
single source of truth
disconnected systems
disconnected tools
data lives in silos
data silos
siloed data
siloed systems
systems don't talk
systems that don't talk to each other
no integration between
doesn't integrate with
lack of integration
manual export
manual import
export to excel
export to spreadsheet
manual workaround
no two-way sync
no api
doesn't sync
keeping systems in sync
ensure data consistency across
swivel chair
```

### Group B — moderate / supporting
```
manual reporting
manual process
manual processes
spreadsheet
spreadsheets
excel
vlookup
pivot tables
google sheets
maintain spreadsheets
track in a spreadsheet
month-end reconciliation
data integrity
data cleanup
data hygiene
update both systems
pull reports
generate reports manually
bridge the gap between
patchwork of tools
tech stack hasn't kept up
move off spreadsheets
eliminate manual
stop re-keying
modernize our systems
legacy systems
fragmented data
fragmented systems
```

### Group C — role-title keywords
```
data entry clerk
data entry specialist
order entry clerk
order processor
billing coordinator
billing specialist
reconciliation analyst
operations analyst
operations coordinator
revops analyst
sales operations analyst
reporting analyst
data coordinator
data steward
master data coordinator
data integrity specialist
edi coordinator
implementation specialist
onboarding specialist
```

### Group D — weak/contextual (only count alongside A/B)
```
rapid growth
scaling fast
doubled headcount
digital transformation
erp migration
post-acquisition
systems integration
process improvement
operational efficiency
```

---

## 3. Scoring Rubric (0–5)

Score the company on the *strongest combined evidence* across all sources. Anchors are cumulative — a higher score generally requires the lower-score conditions plus more.

| Score | Label | Concrete anchor |
|---|---|---|
| **0** | No signal | No Group A/B/C hits. Company sells/uses well-integrated stack or no public ops signals at all. |
| **1** | Faint | Only Group D context (rapid growth, digital transformation) or a single isolated Group B word ("spreadsheets") with no manual-process framing. Could be anything. |
| **2** | Plausible | One Group B/C hit with mild context: e.g., an established "Operations Analyst" or "Reporting Analyst" role, or a careers line about "manual processes," but no explicit re-keying/reconciliation language. |
| **3** | Probable | One clear Group A phrase OR (a Group C re-keying/reconciliation title + a Group B support phrase). E.g., job posting says "reconcile data across systems" once; or a Data Entry Clerk req that also lists Excel-heavy duties. Single confirmed instance of a human bridging two systems. |
| **4** | Strong | Multiple Group A hits, OR one Group A phrase corroborated across **two** source types (e.g., JD says "re-key invoices" + a G2 review says "no integration, we export to Excel"). Named systems that visibly don't connect (CRM + ERP + billing listed, no iPaaS). A *newly opened* data-entry/reconciliation role. |
| **5** | Acute / textbook | Explicit "no single source of truth" / "data lives in silos" language **plus** a human-bridge role being hired **plus** corroborating cons in reviews; OR clear narrative of double entry across ≥2 named systems with manual reconciliation. The integration pitch writes itself — quantifiable wasted FTE hours implied. |

**Scoring procedure**
1. Scan all available sources, tally Group A/B/C/D hits per source.
2. Note how many *distinct source types* corroborate (jobs / reviews / site).
3. Apply the highest anchor whose conditions are met.
4. Cap at 3 if all evidence comes from a single sentence or a single source type with no corroboration (avoids over-scoring a stray keyword).

---

## 4. False Positives / Caveats

- **Vendors selling the cure (biggest trap).** A company whose *product marketing* says "eliminate manual data entry," "single source of truth," "stop re-keying," "connect disconnected systems" is describing their customers' pain, not their own. iPaaS/integration/ERP/automation vendors (Workato, Celigo, Zapier, MuleSoft clones, Boomi, etc.) will light up Group A hard. **Mitigation:** treat homepage/product/marketing copy as *negative or neutral* evidence for the company itself; only count site language when it appears in **About/careers/internal** context, and discount entirely if the company's category is integration/iPaaS/automation/data-pipeline.
- **Software review wording is about the product, not the buyer.** A G2 con "doesn't integrate with X" means the *reviewed product* has the gap — which scores *the reviewer's* company, not the product's vendor. Make sure you attribute the pain to the right entity.
- **"Single source of truth" is bidirectional.** It's a pain admission in careers/about ("we need to get to a single source of truth") but a product claim on a homepage. Context decides; default to false positive unless framed as a current shortcoming.
- **Excel / spreadsheets alone ≠ silo pain.** Spreadsheets are ubiquitous (finance, analysis, modeling). Only score when paired with cross-system framing (export/import, reconcile, "to bridge," "because [system] doesn't…"). Group B is support-only, never a standalone 3+.
- **Data Analyst / Data Engineer / Data Scientist roles** are often building *legitimate* pipelines — not evidence of manual silo pain (may even mean they're solving it in-house, reducing CTO opportunity). Distinguish from Data *Entry* / Data *Coordinator* / Data *Steward*.
- **Compliance/regulatory reconciliation** (e.g., financial close, SOX) can require manual reconciliation by design/audit, not because of missing integration — softer opportunity.
- **EDI Coordinator** can indicate either established integration (good EDI = connected) or manual EDI gap-filling; read the JD.
- **Generic "digital transformation" / "modernize"** (Group D) is marketing filler; never score above 1 on its own.
- **Staffing/consulting/RPA firms** post data-entry and reconciliation roles *on behalf of clients* or as services — the pain isn't theirs. Check whether the hiring entity is an outsourcer.
- **Recency matters.** Old cached reviews/JDs may describe a pain since solved. Prefer signals < 12 months old; weight a *currently open* req higher than a closed one.
