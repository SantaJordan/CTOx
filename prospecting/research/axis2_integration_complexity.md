# Axis 2 — Integration Complexity / Tech-Enablement

**Purpose:** Score how strongly a company runs MULTIPLE platforms that must talk to each other, implying heavy API/integration work. This is Carl's sweet spot (fractional CTO selling integration / technical leadership).

**Inputs:** Company `Industry`, `Description`, `Specialties`, and website copy (homepage, product, integrations/partners, developer/API pages).

**Core question the axis answers:** *Does this company have an integration surface area big enough that a fractional integration-CTO is valuable?*

---

## 1. Categorized Signal List

### STRONG signals (each ~ +2 toward a high score)
A clear, concrete integration surface. Hard to fake with marketing fluff.

| Signal | Example phrases |
|---|---|
| Explicit integrations/marketplace page | "integrations directory", "app marketplace", "200+ integrations", "browse our integrations", "connect your apps" |
| Named third-party connectors | "syncs with Salesforce, HubSpot, QuickBooks, NetSuite", "works with Shopify, Stripe, Slack" |
| "integrates / connects / syncs with" language | "integrates with your existing stack", "two-way sync with", "bi-directional sync", "connects to your CRM/ERP" |
| Data pipeline / ETL / middleware | "ETL", "ELT", "reverse ETL", "data pipeline", "iPaaS", "middleware", "message queue", "event bus", "CDC / change data capture" |
| API-first / developer platform | "API-first", "REST/GraphQL API", "developer portal", "webhooks", "SDK", "build on our platform", "developer docs" |
| Embedded / white-label integration | "embedded integrations", "white-label", "embed our widget", "OEM", "powered by", "embedded fintech/payments" |
| Real-time data sync across systems | "real-time sync", "real-time data", "keep your systems in sync", "single source of truth across tools" |
| System-of-record consolidation | "unify data from all your tools", "360-degree view", "consolidate disparate systems", "break down data silos" |

### MEDIUM signals (each ~ +1)
Implies multiple systems but less explicit; could be aspirational copy.

| Signal | Example phrases |
|---|---|
| Multiple product lines / suite | "platform of products", "product suite", "modules", "our products: X, Y, Z", "all-in-one platform" |
| Workflow automation across tools | "workflow automation", "automate across your tools", "no-code workflows", "triggers and actions", "Zapier-style" |
| Partner / app ecosystem | "partners page", "technology partners", "partner program", "ecosystem", "certified integrations" |
| Multi-platform / omnichannel ops | "omnichannel", "multi-channel", "cross-platform", "across web, mobile, POS" |
| SSO / identity plumbing | "SSO", "SAML", "SCIM", "OAuth", "directory sync" |
| Data warehouse / BI connectivity | "connect to Snowflake/BigQuery/Redshift", "sync to your warehouse", "BI integrations" |
| Legacy + modern coexistence | "modernize legacy systems", "connect legacy and cloud", "wrap your mainframe", "bridge old and new" |

### WEAK signals (each ~ +0.5, only count if corroborated)
Common boilerplate; alone they prove little.

| Signal | Example phrases |
|---|---|
| Generic "seamless" claims | "seamless integration", "plays nicely with", "fits your workflow" |
| Single named integration | "integrates with Google Calendar" (one connector ≠ integration surface) |
| Vague "platform" usage | "the platform for X" (marketing, not architecture) |
| "API available" footnote | "we have an API" with no developer surface |
| Cloud/SaaS mention | "cloud-based", "SaaS" (necessary not sufficient) |

---

## 2. Flat Keyword / Phrase List (lowercase, CSV-filter ready)

```
integrations
integration
integrate with
integrates with
connects with
connects to
syncs with
sync with
two-way sync
bi-directional sync
real-time sync
real time sync
data sync
keep in sync
single source of truth
integration marketplace
app marketplace
app directory
integrations directory
connect your apps
connect your tools
connect your stack
existing stack
your tech stack
api-first
api first
rest api
graphql
graphql api
public api
open api
developer portal
developer platform
developer docs
api documentation
webhooks
webhook
sdk
sdks
embed
embedded
white-label
white label
oem
powered by
ipaas
etl
elt
reverse etl
data pipeline
data pipelines
middleware
message queue
event bus
event-driven
change data capture
cdc
data warehouse
snowflake
bigquery
redshift
workflow automation
no-code workflow
triggers and actions
automate across
zapier
make.com
salesforce
hubspot
netsuite
quickbooks
shopify
stripe
slack
sso
saml
scim
oauth
directory sync
technology partners
partner program
partner ecosystem
app ecosystem
certified integrations
product suite
all-in-one platform
modules
omnichannel
multi-channel
cross-platform
unify your data
unify data
break down silos
data silos
disparate systems
360-degree view
360 view
modernize legacy
legacy systems
connect legacy
```

---

## 3. 0–5 Scoring Rubric

Score the company on its integration surface. Use the highest anchor whose criteria are clearly met; signal counts are a guide, not a vote tally.

| Score | Anchor | Typical evidence |
|---|---|---|
| **0** | Single simple product, no integration surface. | One product, no API mention, no integrations page, no third-party connectors. (e.g., a static brochure site, a single-purpose mobile app.) |
| **1** | One product with token connectivity. | Mentions "an API" or one named integration; "seamless" boilerplate only. No marketplace, no developer surface. |
| **2** | Some integration intent, lightly evidenced. | A handful of named connectors OR "integrates with your tools" + workflow automation language, but no dedicated integrations page/dev portal. |
| **3** | Real integration surface forming. | Dedicated integrations or partners page; several named connectors; OR public API + webhooks/SDK. Clearly expects to talk to other systems. |
| **4** | Multi-platform with strong integration surface. | Multiple product lines/modules AND an integrations marketplace OR developer platform; real-time/two-way sync; data pipeline or warehouse connectivity. |
| **5** | Clearly multi-platform with explicit, broad integration surface. | 2+ STRONG signals stacked: large integrations marketplace (dozens+), developer portal + webhooks + SDK, embedded/white-label, ETL/iPaaS/middleware language, and explicit multi-system data sync. A fractional integration-CTO has obvious, ongoing work. |

**Quick scoring heuristic (for CSV automation):**
- Count STRONG (×2), MEDIUM (×1), WEAK (×0.5) keyword hits in Industry+Description+Specialties.
- Raw = sum; cap WEAK contribution at 1.0 total.
- Map: raw 0 → 0; 0.5–1.5 → 1; 2–3 → 2; 3.5–5 → 3; 5.5–7 → 4; 7+ → 5.
- Tie-break upward only if at least one STRONG signal is present (prevents WEAK-keyword inflation).

---

## 4. False Positives / Caveats

**The big one — "IS the integration platform" vs. "NEEDS integrations":**
Carl sells *to* companies that struggle to make their multiple systems talk. A company whose entire product *is* iPaaS/ETL/integration tooling (e.g., a Workato/Mulesoft/Fivetran-type vendor) will trip every STRONG keyword but is a poor fit — they already have deep integration expertise in-house and likely don't buy a fractional integration-CTO. **Flag any company where integration is the core product, not a need.** Tell from: "the integration platform", "we connect X to Y for our customers", "iPaaS", positioning integration as the value prop rather than a feature.
  - Action: demote 2–3 points, or route to a separate "integration vendor — likely not ICP" bucket.

**Other caveats:**
- **Marketing boilerplate inflation.** "Seamless integration" and lone "we have an API" are weak; don't let stacked weak phrases reach a 3+. Require a STRONG signal to clear score 3.
- **Single connector ≠ surface.** "Integrates with Google Calendar" is one connector; integration complexity needs *multiplicity*.
- **Aspirational roadmap language.** "Coming soon: integrations", "we're building an API" describes intent, not current surface. Treat as MEDIUM at most.
- **Agencies / consultancies / dev shops.** They list every tech ("we integrate Salesforce, SAP, AWS...") as service capabilities, not their own product complexity. They are sellers of integration labor — possible competitor or channel, not ICP. Flag service-firm Industry values (IT services, software development agency, consulting).
- **Generic "platform" / "all-in-one."** Common SaaS positioning; only counts when paired with named connectors, modules, or a developer surface.
- **Marketplaces (commerce) vs. integration marketplaces.** "Marketplace" can mean a buyer/seller platform (e-commerce) with no integration meaning. Disambiguate: "app marketplace / integrations marketplace" = signal; "shop our marketplace" = not.
- **Heavy verticals that imply integration without saying it.** Some ICP companies (healthcare, fintech, logistics) clearly run many systems but use little integration vocabulary. Don't over-penalize a 0 — let Axis 2 stay low but lean on vertical/other axes; consider a small floor (min 1) for industries known to be system-dense.

---

*Build note: run keyword matching case-insensitively on concatenated Industry + Description + Specialties + scraped page text. Always apply the "integration vendor" demotion filter BEFORE finalizing the score.*
