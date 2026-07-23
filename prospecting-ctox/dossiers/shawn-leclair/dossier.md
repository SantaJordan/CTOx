# Shawn Leclair — Research Dossier

Prepared 2026-07-23. Sources: FullEnrich API pull (aggregator — treated as uncorroborated until matched to public artifacts), Exa-indexed public web (LinkedIn profile/posts/recommendations, quantum5.ai, esi-q.quantum5.ai, Wikipedia, PRNewswire). No LinkedIn browsing was performed; LinkedIn content comes from Exa's public index. The FullEnrich pull for this CTO came back thinner than others (~9KB, no company metadata); gaps are flagged in "Unverified claims."

---

## Career arc

| Period | Role | Company | Stage / Industry | Evidence |
|---|---|---|---|---|
| 1993–1995 | Student | University of Massachusetts Amherst | — | LinkedIn profile + FullEnrich (degree/major not public) |
| Jan 1998 – Jan 1999 | Systems Manager | DeltaTrends, Inc. | Unknown — no public footprint found | LinkedIn profile + FullEnrich only |
| Jan 1999 – Dec 2024 | President & Principal Consultant | Leclair & Associates, Inc., Norton, MA | Boutique software consultancy; "tailored solutions for small to mid-sized businesses across various industries" | LinkedIn profile (own description) |
| Jan 2003 – Apr 2023 | Consultant (20 yrs 3 mo) | Leerink Swann LLC, Boston, MA | Healthcare-focused investment bank (founded 1995; became Leerink Partners 2014, SVB Leerink 2019, SVB Securities 2021, Leerink Partners again 2023 after the SVB collapse) | LinkedIn profile; company history per Wikipedia "Leerink Partners" |
| Apr 2023 – Dec 2025 | Senior Technical Program Lead | Quantum5 (now Ander LLC), Scottsdale, AZ | Automotive-retail training + workforce-analytics SaaS, founded ~2018–2020, 20–30 employees (-20% YoY per LinkedIn company data, 2026); rebranded to "Ander, the performance intelligence company" Apr 2026 | LinkedIn profile; quantum5.ai news pages; CBT News |
| Jan 2026 – present | President (Fractional CTO practice) | Leclair & Associates | Hands-on fractional CTO for startups & SMBs, Boston area | LinkedIn profile headline + his own 2026 posts |

Notes on the arc:

- **28+ years total experience** (his LinkedIn states "28 years and 4 months" as of mid-2026).
- The Leerink Swann engagement ran **inside** the lifetime of his consultancy — a single client relationship held for **20 years and 3 months**. It ended April 2023, the month after Silicon Valley Bank's parent filed Chapter 11 (March 17, 2023) and Leerink's parent entered its buyout upheaval (Wikipedia, dated). The same month he started at Quantum5. Timing is factual; causation is not claimed.
- Quantum5 context during his tenure: it had acquired **ESI Trends** (May 17, 2022, per quantum5.ai press release) — a 1996-founded research firm whose platform, rebranded **ESi-Q**, ingests "millions of payroll records and employee surveys" and produces the **NADA Dealership Workforce Study** (20,000–25,000 dealership employees surveyed per year, "hundreds of thousands of payroll records" analyzed, per Ander's LinkedIn post of 2025-10-23). It then acquired **Trivie** (Jan 29, 2024, PRNewswire) and partnered with GP Strategies (Jan 3, 2024, PRNewswire). He joined the month after the ESI Trends integration year and left shortly before the Ander rebrand (Apr 27, 2026).

## Proven fixes

Evidence here is deliberately conservative — his public footprint is small, so each fix cites exactly where it comes from.

1. **Took single-threaded ownership of an acquired legacy analytics application and modernized it in place (2023–2025).** A public LinkedIn recommendation from Tyler Morgan (fractional CTO, Dallas) states: "I worked with Shawn at Ander on the ESi-Q team, where he was responsible for a legacy application and we collaborated on modernizing parts of the stack… He isn't afraid to dig into complex problem spaces to build real understanding, which is especially valuable when working with legacy systems." The application in question is the former ESI Trends platform — a survey + payroll-records ETL/reporting system that carries a contracted annual industry study (NADA Dealership Workforce Study) with immovable delivery cycles. Source: LinkedIn recommendation on his profile; ESi-Q scale figures from Ander's LinkedIn post (2025-10-23) and quantum5.ai acquisition release (2022-05-17).
2. **Ran a 20-year embedded technical engagement at a healthcare investment bank (2003–2023).** The duration and client (Leerink Swann LLC, Boston) are on his public profile. A client of this type does not retain an outside consultant for two decades unless the systems he owns keep working. What exactly he built there is not public — see Unverified claims — but the retention itself is the demonstrable fact.
3. **Sustained a boutique consultancy for ~26 years (1999–2024) serving SMBs across industries.** His own profile description: "Delivered tailored solutions for small to mid-sized businesses across various industries. Oversaw client acquisition, project delivery and long-term support." Longevity verified by the profile dates; individual client outcomes are not public.
4. **Department leadership and process streamlining at Quantum5.** Second public recommendation (Chloe Lowe): "he never hesitated to step in, often finding ways to streamline processes or innovate so both the team and the company could operate more effectively… incredibly patient and thoughtful when it comes to training." Source: LinkedIn recommendation.

## Industries & tech depth

- **Healthcare financial services / investment research** — 20 years embedded at a healthcare-only investment bank (Leerink). Domain-adjacent skills he self-lists (FullEnrich/LinkedIn skills, unverified individually): investment banking, equities, valuation, financial modeling, M&A, due diligence, corporate finance.
- **Workforce analytics / HR data SaaS** — 2.7 years owning the ESi-Q platform: employee surveys, payroll-record ETL, compensation/retention benchmarking, HRIS. "HRIS" appears in both his aggregator skills and his LinkedIn skill tags.
- **Automotive retail SaaS** — via Quantum5/Ander (dealership training + workforce intelligence, NADA/CADA study).
- **Core technical stack (self-listed, consistent across FullEnrich and LinkedIn; not independently demonstrated in public code — no GitHub found):** Microsoft SQL Server, T-SQL, SSIS, SSRS, ETL, data architecture/modeling/engineering, database design, .NET Framework, Python, PostgreSQL, AWS, Azure, cloud-native architecture, AI strategy.
- **Positioning in his own words** (LinkedIn About, retrieved 2026-07): companies where "technology works — but only because a few people are holding it together"; he stabilizes, scales, and professionalizes: architecture review, technical-debt and delivery-risk reduction, clear ownership and standards, leveling up engineering teams, founder decision support — "from reactive and fragile to predictable and well-run."

## Niche statement

Data-heavy B2B SaaS and services SMBs (workforce/benchmarking analytics, healthcare-finance back office) at the moment their SQL Server/SSIS-era legacy platform — often inherited through acquisition and understood by one or two people — must be stabilized and modernized in place without a rebuild or a full-time CTO; his angle is 25+ years as the embedded single-threaded owner of exactly such systems, including modernizing an acquired legacy analytics platform while its contracted reporting deadlines kept shipping.

## The EDP (Existential Data Point)

**Bus factor = 1 on the revenue-critical system.** When the platform carries contracted, calendar-fixed data deliverables (ESi-Q ships an annual industry study built from 20,000–25,000 surveys and hundreds of thousands of payroll records) and only one person understands the code, a single resignation drops delivery capacity to zero while the deadlines don't move — miss one reporting cycle and the anchor contract that funds the company is gone, and replacement hiring against an undocumented legacy stack typically costs two to four quarters of frozen roadmap before anyone can safely change the system again.

## Sources

- https://www.linkedin.com/in/shawn-m-leclair — profile: headline, About, experience dates, skills, recommendations (Tyler Morgan, Chloe Lowe). Retrieved via Exa index 2026-07-23.
- https://www.linkedin.com/posts/shawn-m-leclair_i-had-an-interesting-conversation-at-a-networking-activity-7473074682599235585-z8MC — his post on AI and the senior-talent pipeline, 2026-06-17.
- https://www.linkedin.com/posts/shawn-m-leclair_another-great-tech-event-in-boston-tech-activity-7467432041119215616-wvJ4 — Boston Tech Week post, 2026-06-02 (places him in the Boston ecosystem).
- https://quantum5.ai/news/quantum5-acquires-esi-trends-and-launches-esi-q — ESI Trends acquisition, 2022-05-17 (platform scope: payroll records, surveys, NADA study).
- https://www.linkedin.com/posts/ander-llc_automotiveretail-dealershipworkforce-employeeengagement-activity-7387246449442557952-gpxj — ESi-Q scale figures (20k–25k surveys/yr; "since 1996"), 2025-10-23.
- https://quantum5.ai/news/quantum5-transitions-to-ander — rebrand + product suite (Trivie, ESiQ, CalliQ), 2026-04-27.
- https://www.prnewswire.com/news-releases/quantum5-acquires-trivie-to-grow-automotive-retail-learning-opportunities-302046328.html — Trivie acquisition, 2024-01-29.
- https://en.wikipedia.org/wiki/Leerink_Partners — Leerink Swann history, SVB collapse timeline.
- FullEnrich API pull: /Users/jordan/Desktop/Claude Code/CTOx/prospecting-ctox/checkpoints/cto_enrich/shawn-leclair.json (aggregator data; used only where matched to public artifacts above).

## Unverified claims (database-only or inference — do not present as fact)

- **What he actually built at Leerink Swann.** Only the title ("Consultant"), dates, and location are public. The inference that he built/ran internal data and reporting systems rests on his self-listed skill set (SSIS/SSRS/T-SQL/HRIS + finance-domain skills) and the client's industry — no Leerink artifact names him. Treat any specific Leerink system claim as unverified.
- **DeltaTrends, Inc. (1998–99).** No public footprint of the company found via Exa; role known from profile/aggregator only.
- **UMass Amherst degree and field of study** — dates only; no degree or major public.
- **Individual skills** (e.g., Python, PostgreSQL, AWS, "AI Strategy") — self-listed; no public code, talks, or writing demonstrates them. No GitHub account, personal website, podcast, or conference talk was found (searched 2026-07-23).
- **Whether the Quantum5 role was remote from Massachusetts** — profile lists the role in Scottsdale, AZ while his 2026 activity is Boston-based; not resolved.
- **FullEnrich date discrepancy:** the pull shows Leclair & Associates ending Dec 2024 and restarting Jan 2026, leaving a 2025 gap that overlaps the Quantum5 tenure; LinkedIn shows the same two entries. The practical reading (consultancy dormant during full-time-equivalent Quantum5 work, relaunched Jan 2026 as a fractional CTO practice) is an inference.
- **Ander headcount trend (-20% YoY, 20–30 employees)** — from LinkedIn company-page enrichment data shown in Exa results, an aggregator figure; not confirmed by the company.
