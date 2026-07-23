# Daniel Kirichanski — Research Dossier

Prepared 2026-07-23. Every claim is dated and sourced. Self-reported metrics are labeled as such.
Research method: Exa search + page crawls only. LinkedIn content quoted below comes from Exa's crawl
of the public profile (snapshot dated 2026-07-09) — his own published words, not aggregator data.

## Career arc (companies, stages, industries, dates)

| Period | Role | Company | Stage / context | Industry |
|---|---|---|---|---|
| Jun 2026 – present | Founder & CTO | Prime Path Global (Austin, TX) | Solo fractional CTO practice for Series A–C and PE-backed companies | Fractional CTO / advisory |
| Jan 2024 – present | IT Advisor (parallel engagement) | Independent (via expert networks) | Tech due diligence + advisory for PE/VC firms | Advisory |
| Apr 2025 – Jun 2026 | Head of Infrastructure Platform and Reliability Engineering | Tricentis | ~1,700-person private software-testing company; post-acquisition org consolidation during his tenure | DevTools / QA software |
| Sep 2024 – Aug 2025 | Head of Cloud Operations, IT and Information Security | Avathon (formerly SparkCognition) | ~250-person company mid-rebrand (Oct 2024) and mid-transition to SaaS Industrial AI platform | Industrial AI |
| Apr 2024 – Jan 2025 | AI Trainer Advisor | Outlier (Scale AI) | Gig/advisory: LLM training and fine-tuning | AI |
| Jan 2022 – Apr 2024 | Head of Platform Engineering | Ripple | Late-stage crypto payments; RippleNet infrastructure | Blockchain payments / fintech |
| Jan 2019 – Jan 2022 | Sr. Engineering Manager, Developer & Platform Services | PayPal | Public company; internal CI/CD platform serving 9,000+ developers | Payments / fintech |
| Jan 2017 – Dec 2018 | Senior Product Manager (Technology Leadership Program) | PayPal | Executive rotation program: mobile app launch, Canada market entry, cybersecurity corporate VC | Payments / fintech |
| Jul 2015 – Jan 2017 | Engineering Manager (Cyber Security) | PayPal | Post-acquisition integration of CyActive (Israeli predictive-security startup PayPal bought Mar 2015, reported ~$60M) | Payments / security |
| Dec 2013 – Jul 2015 | Senior Technical Lead, QA (Global Data Science) | PayPal | Fraud-system test automation | Payments / fraud |
| 2016 – 2017 | Co-Founder | VerumView | Seed-stage Israeli real-time-KYC startup (existence corroborated; his role database-only — see Unverified) | Fintech / KYC |
| Jul 2012 – Dec 2013 | Senior Automation Engineer, Tech Lead | Dell | Clustered storage file-system testing (database-only detail) | Hardware / storage |
| Feb 2010 – Jul 2012 | QA Team Lead | NICE Actimize | Fraud-prevention systems for financial institutions (database-only detail) | Financial crime software |

Location: Austin, TX. Languages: English, Hebrew, Russian (database). Total experience: self-stated "20+ years"
(profile shows 22y 9m). Note the Avathon/Tricentis overlap (Apr–Aug 2025) — both listed this way on his own profile.

**Aggregator staleness note:** the FullEnrich pull (checkpoints/cto_enrich/daniel-kirichanski.json) still shows
Tricentis as his current role. His live profile (crawled 2026-07-09) shows Tricentis ended Jun 2026 and Prime Path
Global founded Jun 2026. The practice is ~1 month old at research time.

## Proven fixes (specific problems, with evidence + source)

All bullets below are **self-reported on his own public artifacts** (LinkedIn profile experience section,
snapshot 2026-07-09; primepath.global). None are independently audited numbers.

1. **Cloud cost reduction at payments scale.** Ripple (2022–2024): "reducing cloud costs by 35%" while running
   infrastructure for "over 6 billion annual transactions" on Kubernetes/AWS/GCP. His site claims "$8M annual
   cloud and vendor spend I cut at a large payment business, a program I owned outright." [LinkedIn profile;
   primepath.global]
2. **Deployment velocity via internal developer platform.** Ripple: GitOps-based internal developer platform,
   "decreasing deployment cycles from hours to minutes." PayPal (2019–2022): led 12-engineer team delivering the
   CI/CD platform for 9,000+ developers, migrated it to Kubernetes on GCP within 12 months; "increased deployment
   frequency by 30% and reduced build times by 20%." [LinkedIn profile]
3. **AI-driven SRE / incident response.** Tricentis (2025–2026): "deploying AI Agents for automated incident
   detection, root cause analysis, and on-call response. Reducing MTTR by ~40%." Site claims "40% production
   stability gain, leading a team that brought AI into operations and site reliability engineering" and "30%
   efficiency gain across a Fortune 500 engineering org after I improved its SDLC with AI." [LinkedIn profile;
   primepath.global]
4. **Post-acquisition technical integration — done twice as operator.** PayPal (2015–2017): led post-acquisition
   integration of a predictive-security acquisition (CyActive — acquisition independently confirmed by TechCrunch/
   ZDNet, Mar 2015) into PayPal's global security ecosystem "within 12 months while navigating tech stack mismatch,
   cross-cultural alignment, and enterprise security compliance." Tricentis (2025–2026): "drove organizational
   transformation post-acquisition, restructuring 5 engineering teams from siloed, misaligned functions into a
   cohesive org." [LinkedIn profile; techcrunch.com 2015-03-10]
5. **Services-to-SaaS platform transition.** Avathon (2024–2025): "led enterprise transformation to a SaaS-based
   Industrial AI platform," modernizing AWS/GCP infrastructure with microservices; ran IT, CloudOps, DevOps/MLOps,
   and Security. The company rebranded from SparkCognition during his tenure (PRNewswire, 2024-10-17). [LinkedIn
   profile; prnewswire.com]
6. **Standing up engineering leadership where there was none.** Profile About section: "I've stood up engineering
   leadership where there was none, turned around underperforming teams, modernized legacy platforms." Site sells
   this as "Interim Engineering Leadership" and "Org Design & Turnaround." [LinkedIn profile; primepath.global]
7. **Live advisory practice with a public point of view.** Active LinkedIn essayist (44 posts, 2,478 followers as
   of Jul 2026): the "Verification Tax"/implementer-vs-arbiter argument against reflex AI hiring (2026-07-02,
   citing the METR 2025 study and Sonar developer survey); AI agents shipped without an evaluation harness
   (2026-07-07); AWS root-account governance failure as the real lesson of cloud horror stories (2026-06-25);
   zombie dev-tool spend as both budget leak and vendor-durability red flag — sourced from two paid expert-network
   engagements in one week (2026-05-26); "AI engineer with FinTech experience is two job descriptions stapled
   together" (2026-05-19). [linkedin.com/posts/daniel-kirichanski_*]

## Industries & tech depth

- **Payments / fintech (deepest):** ~11 years across PayPal (4 roles, 2013–2022) and Ripple (2022–2024), plus
  NICE Actimize fraud prevention and VerumView KYC earlier. Understands regulated delivery (SOX/SOC 2 references
  in his own posts and role descriptions).
- **Platform engineering / SRE / cloud:** the through-line of every senior role — Kubernetes, AWS, GCP, Azure,
  Terraform, GitOps CI/CD, internal developer platforms, cloud cost optimization, reliability engineering.
  (FullEnrich adds ArgoCD, HashiCorp Vault, Istio mTLS, OpenCost, Kafka, SOC 2 — see Unverified.)
- **Applied AI in operations:** AI agents for incident response (Tricentis), LLM training work (Outlier,
  2024), Medium tutorial on self-hosting n8n (2025-02-10), sustained public writing on AI engineering
  economics (2026). Certified Blockchain Expert (Blockchain Council, issued 2024-06-16).
- **Security:** PayPal InfoSec engineering management, Avathon InfoSec ownership, zero-trust patterns.
- **What he is NOT (per his own positioning):** not a product-zero-to-one CTO, not a consumer-app builder, not a
  hands-on ML researcher. His material targets companies that already have a product and revenue but whose
  engineering org, platform, or cloud economics broke during growth or M&A.

## Niche statement

Fractional CTO for Series A–C and PE-backed B2B software companies — heaviest in fintech/payments — at the
moment engineering becomes the growth constraint (post-acquisition stack collision, cloud spend climbing
unexplained, headcount doubled but shipping flat), fixed with the platform-engineering/SRE playbook he ran at
PayPal and Ripple: developer-platform + GitOps delivery, FinOps-grade cost control, and AI-in-operations with
verification capacity funded before more implementers.

- **Industry:** growth-stage B2B software, fintech/payments-weighted; PE-backed platforms in M&A mode.
- **Situation:** engineering-as-bottleneck inflection — first real engineering leadership gap, post-acquisition
  integration, runaway cloud spend, reliability/on-call breakdown, stalled AI adoption.
- **Unique angle:** payments-scale platform operator (6B+ transactions self-reported) who treats AI as an
  operations and verification problem, not a hiring problem — cut costs and MTTR with the same playbook twice.

## The EDP (existential data point)

**Engineering cost per unit shipped:** when a Series A–C company's cloud + engineering spend keeps compounding
(~30%+/yr cloud growth, headcount doubled) while delivery throughput stays flat, gross margin and runway erode
until the next round is unraisable — every month of unfixed platform drag or unintegrated acquisition is burn
with zero shipped differentiation, and his own anchor numbers ($8M spend cut, 35% cloud reduction, 40% MTTR
reduction, deploys hours→minutes) are the before/after of exactly that number.

## Sources

- https://www.linkedin.com/in/daniel-kirichanski — public profile, Exa crawl snapshot 2026-07-09 (headline,
  About, full experience section; primary source for self-reported metrics)
- https://primepath.global — Prime Path Global site (services, anonymized track-record claims)
- https://www.linkedin.com/posts/daniel-kirichanski_ai-speeding-up-your-engineers-is-not-a-reason-activity-7478462617284669440-cPGN (2026-07-02)
- https://www.linkedin.com/posts/daniel-kirichanski_a-team-im-working-with-runs-several-ai-agents-activity-7480274497858863104-4lBN (2026-07-07)
- https://www.linkedin.com/posts/daniel-kirichanski_a-founder-got-locked-out-of-his-own-aws-account-activity-7475925811930316800-5E11 (2026-06-25)
- https://www.linkedin.com/posts/daniel-kirichanski_two-firms-paid-me-this-week-to-answer-the-activity-7465057608908038146-XaEn (2026-05-26)
- https://www.linkedin.com/posts/daniel-kirichanski_ai-engineer-with-fintech-experience-is-activity-7462519454107815936-iDsj (2026-05-19)
- https://www.linkedin.com/posts/daniel-kirichanski_most-engineering-orgs-i-walk-into-are-optimizing-activity-7465786224763465728-VrL7 (2026-05-28)
- https://medium.com/@daniel.krs — Medium ("Deploying n8n on the Cloud," 2025-02-10)
- https://officehours.com/dan-k — Office Hours advisory profile
- https://certificates.blockchain-council.org/457a31e9-9348-4eb7-a035-2120fdb7490a — Certified Blockchain Expert, 2024-06-16
- https://techcrunch.com/2015/03/10/paypal-confirms-acquisition-of-cyactive-plans-to-open-new-security-hub-in-israel/ — CyActive acquisition
- https://www.zdnet.com/article/paypal-to-pay-60m-for-israeli-security-startup-cyactive/ — CyActive price report (2015-03-09)
- https://www.prnewswire.com/news-releases/avathon-launches-the-first-system-level-industrial-ai-platform-302278510.html — SparkCognition→Avathon rebrand (2024-10-17)
- FullEnrich API pull: checkpoints/cto_enrich/daniel-kirichanski.json (aggregator; used for pre-2015 roles and noted as stale on current role)

## Unverified claims (database-only or self-reported without external corroboration)

- **VerumView co-founder role (2016–2017):** company existence and seed round corroborated (FintechWeekly, CB
  Insights), but his association appears only in the FullEnrich pull; CB Insights lists a different person
  ("Maxim P.") as Founder/Director. Our profile crawl truncated before this era. Treat as unverified.
- **NICE Actimize (2010–2012) and Dell (2012–2013) details:** FullEnrich-only in this research (profile crawl
  truncated); dates plausible, not directly captured from his own artifact.
- **GLG and AlphaSights "Technology Expert/Advisor" roles (2024–2025):** FullEnrich-only as named engagements,
  though his 2026-05-26 post about paid expert-network requests corroborates the activity in general.
- **Ripple title variant "Head of Platform Engineering (RippleNet Infrastructure)":** appears on Wiza (another
  aggregator); his live profile says "Head of Platform Engineering" only.
- **Specific stack details at Ripple (ArgoCD, HashiCorp Vault, Istio mTLS, OpenCost, SOC 2 attainment, "10M+
  monthly cross-border transactions"):** FullEnrich role description only; his live profile omits these.
- **All performance metrics** ($8M spend cut, 35% cloud cost reduction, ~40% MTTR reduction, 30% deployment
  frequency gain, 20% build-time reduction, 6B+ annual transactions, 250M app users, $10M Canada revenue):
  self-reported on his own profile/site; no independent audit found. Presented on stage they should be framed
  as "he claims," not established fact.
- **No talks, podcasts, or press appearances found.** His public footprint is LinkedIn writing, one Medium
  tutorial, an Office Hours page, and his company site — no conference talks or interviews surfaced via Exa.
