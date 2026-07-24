# Evidence pack: Prelude Security
slug: prelude-security | domain: preludesecurity.com | HQ: ,   | employees(LI): 40 | founded:  | stage_band: unknown
sources: vc:new-north
industry(LI): Computer and Network Security | specialties: asca, threat exposure management, security control validation, security control monitoring
channel notes: continuous security testing
own-language word count: ~1457

## Their own words (website via Exa, livecrawl-preferred)

URL: https://preludesecurity.com
Looking for Prelude Security? You're looking for Origin.

# Looking for Prelude Security?

You found the right page. We are now Origin, the endpoint AI observability platform for the agent workforce running today.

Already running Prelude Monitor? Nothing changes for you. Same product. Same team. Same way of getting in touch with us.

Contact us

Whether you’re running Prelude Monitor today or sizing up Origin for the first time, we look forward to hearing from you.

I agree to Origin’s Privacy Policy and understand that I can unsubscribe at any time.*Get in touch →

What Origin does

## Endpoint AI observability, built for the work agents actually do.

The agents your team deployed write code, touch files, call APIs, and spend budget, often faster than anyone can track by hand.

Origin runs at the endpoint, where the work happens. Nothing upstream sees it the same way.

How it works

## Ask Origin.

Find every agent and MCP server across the fleet, approved and unapproved alike.

01 DiscoveryWhere are our agents?02 SecurityWhat are they doing?03 SpendWhere is our intelligence going?

Ask Origin · DiscoveryWhere are our agents?K

You

Show every AI agent and MCP server across the fleet in the last 7 days. Group by endpoint, owner, and install path.

Routing · fleet discovery

analytics_query· done

1,284 agents · 612 endpoints · 91 shadow installs

Claude Code38%

Cursor31%

MCP servers19%

Browser agents12%

1,284 agents across 612 endpoints. 91 are shadow installs not in MDM. The biggest gap is personal Cursor installs on engineering laptops, followed by local MCP servers connected to GitHub.

Ask Origin · DiscoveryWhich endpoints run unsanctioned MCP servers?K

You

Which endpoints are running local MCP servers that aren't in the sanctioned catalog?

mcp_inventory· 47 matches

personal_install ∧ ¬in(sanctioned_catalog)

ENG-MBP-22github-mcp · supabase-mcp

LAPTOP-R180TR52postgres-mcp

ENG-MBP-14slack-mcp · linear-mcp

ENG-MBP-08github-mcp · custom-rag

47 endpoints running 21 distinct MCP servers outside the catalog. Most-touched targets: GitHub, internal Postgres, Slack. None hit the secrets vault — yet.

Ask Origin · DiscoveryWho installed an agent this week?K

You

/audit new agents this week — who, what, where, and is it sanctioned?

Routing · audit · 7d

audit· 214 events

first_observed_within(7d) ∩ kind=agent_install

diego.alvarezCodex · ENG-MBP-22 · personal

kevin.wrightCursor 3.3.30 · MBP-KW · sanctioned

ben.taylorClaude Code · HR-LAPTOP-04 · sanctioned

priya.shahCopilot · FINANCE-PC-07 · sanctioned

214 first-time agent installs this week. 18 are personal / unsanctioned. 196 came through the standard install path; the rest were side-loaded.

Ask Origin · DiscoveryShow agent density by team.K

You

Break down agent installs by team — which orgs are highest density?

analytics_query· done

agents_per_endpoint by org

Engineering64%

Customer Eng48%

Product31%

Security22%

Engineering averages 4.7 agents per laptop — highest density in the company. Customer Engineering is second at 3.2. Marketing and Sales sit below 1.

Ask Origin · DiscoveryPersonal-GitHub connections?K

You

Any agents on the fleet connecting to GitHub from personal accounts?

Routing · attribution

session_trace· 9 sessions

agent.git_auth ≠ user.sso_email

Cursor · ENG-MBP-22auth: diego.gh ≠ diego.alvarez@

Claude · ENG-MBP-08auth: a-singh-dev ≠ aaron.singh@

Copilot · LAPTOP-R180TR52auth: mwong-side ≠ wong.m@

9 active agent ↔ GitHub auth pairs where the agent's commit identity doesn't match the SSO identity. All on Engineering machines.

Ask Origin · DiscoveryWhere are our agents?K

You

Show every AI agent and MCP server across the fleet in the last 7 days. Group by endpoint, owner, and install path.

Routing · fleet discovery

analytics_query· done

1,284 agents · 612 endpoints · 91 shadow installs

Claude Code38%

Cursor31%

MCP servers19%

Browser agents12%

1,284 agents across 612 endpoints. 91 are shadow installs not in MDM. The biggest gap is personal Cursor installs on engineering laptops, followed by local MCP servers connected to GitHub.

Ask Origin · DiscoveryWhich endpoints run unsanctioned MCP servers?K

You

Which endpoints are running local MCP servers that aren't in the sanctioned catalog?

mcp_inventory· 47 matches

personal_install ∧ ¬in(sanctioned_catalog)

ENG-MBP-22github-mcp · supabase-mcp

LAPTOP-R180TR52postgres-mcp

ENG-MBP-14slack-mcp · linear-mcp

ENG-MBP-08github-mcp · custom-rag

47 endpoints running 21 distinct MCP servers outside the catalog. Most-touched targets: GitHub, internal Postgres, Slack. None hit the secrets vault — yet.

Ask Origin · DiscoveryWho installed an agent this week?K

You

/audit new agents this week — who, what, where, and is it sanctioned?

Routing · audit · 7d

audit· 214 events

first_observed_within(7d) ∩ kind=agent_install

diego.alvarezCodex · ENG-MBP-22 · personal

kevin.wrightCursor 3.3.30 · MBP-KW · sanctioned

ben.taylorClaude Code · HR-LAPTOP-04 · sanctioned

priya.shahCopilot · FINANCE-PC-07 · sanctioned

214 first-time agent installs this week. 18 are personal / unsanctioned. 196 came through the standard install path; the rest were side-loaded.

Ask Origin · DiscoveryShow agent density by team.K

You

Break down agent installs by team — which orgs are highest density?

analytics_query· done

agents_per_endpoint by org

Engineering64%

Customer Eng48%

Product31%

Security22%

Engineering averages 4.7 agents per laptop — highest density in the company. Customer Engineering is second at 3.2. Marketing and Sales sit below 1.

Ask Origin · DiscoveryPersonal-GitHub connections?K

You

Any agents on the fleet connecting to GitHub from personal accounts?

Routing · attribution

session_trace· 9 sessions

agent.git_auth ≠ user.sso_email

Cursor · ENG-MBP-22auth: diego.gh ≠ diego.alvarez@

Claude · ENG-MBP-08auth: a-singh-dev ≠ aaron.singh@

Copilot · LAPTOP-R180TR52auth: mwong-side ≠ wong.m@

9 active agent ↔ GitHub auth pairs where the agen

URL: https://preludesecurity.com/
Looking for Prelude Security? You're looking for Origin.

# Looking for Prelude Security?

You found the right page. We are now Origin, the endpoint AI observability platform for the agent workforce running today.

Already running Prelude Monitor? Nothing changes for you. Same product. Same team. Same way of getting in touch with us.

Contact us

Whether you’re running Prelude Monitor today or sizing up Origin for the first time, we look forward to hearing from you.

I agree to Origin’s Privacy Policy and understand that I can unsubscribe at any time.*Get in touch →

What Origin does

## Endpoint AI observability, built for the work agents actually do.

The agents your team deployed write code, touch files, call APIs, and spend budget, often faster than anyone can track by hand.

Origin runs at the endpoint, where the work happens. Nothing upstream sees it the same way.

How it works

## Ask Origin.

Find every agent and MCP server across the fleet, approved and unapproved alike.

01 DiscoveryWhere are our agents?02 SecurityWhat are they doing?03 SpendWhere is our intelligence going?

Ask Origin · DiscoveryWhere are our agents?K

You

Show every AI agent and MCP server across the fleet in the last 7 days. Group by endpoint, owner, and install path.

Routing · fleet discovery

analytics_query· done

1,284 agents · 612 endpoints · 91 shadow installs

Claude Code38%

Cursor31%

MCP servers19%

Browser agents12%

1,284 agents across 612 endpoints. 91 are shadow installs not in MDM. The biggest gap is personal Cursor installs on engineering laptops, followed by local MCP servers connected to GitHub.

Ask Origin · DiscoveryWhich endpoints run unsanctioned MCP servers?K

You

Which endpoints are running local MCP servers that aren't in the sanctioned catalog?

mcp_inventory· 47 matches

personal_install ∧ ¬in(sanctioned_catalog)

ENG-MBP-22github-mcp · supabase-mcp

LAPTOP-R180TR52postgres-mcp

ENG-MBP-14slack-mcp · linear-mcp

ENG-MBP-08github-mcp · custom-rag

47 endpoints running 21 distinct MCP servers outside the catalog. Most-touched targets: GitHub, internal Postgres, Slack. None hit the secrets vault — yet.

Ask Origin · DiscoveryWho installed an agent this week?K

You

/audit new agents this week — who, what, where, and is it sanctioned?

Routing · audit · 7d

audit· 214 events

first_observed_within(7d) ∩ kind=agent_install

diego.alvarezCodex · ENG-MBP-22 · personal

kevin.wrightCursor 3.3.30 · MBP-KW · sanctioned

ben.taylorClaude Code · HR-LAPTOP-04 

URL: https://preludesecurity.com/blog
Looking for Prelude Security? You're looking for Origin.

# Looking for Prelude Security?

You found the right page. We are now Origin, the endpoint AI observability platform for the agent workforce running today.

Already running Prelude Monitor? Nothing changes for you. Same product. Same team. Same way of getting in touch with us.

Contact us

Whether you’re running Prelude Monitor today or sizing up Origin for the first time, we look forward to hearing from you.

I agree to Origin’s Privacy Policy and understand that I can unsubscribe at any time.*Get in touch →

What Origin does

## Endpoint AI observability, built for the work agents actually do.

The agents your team deployed write code, touch files, call APIs, and spend budget, often faster than anyone can track by hand.

Origin runs at the endpoint, where the work happens. Nothing upstream sees it the same way.

How it works

## Ask Origin.

Find every agent and MCP server across the fleet, approved and unapproved alike.

01 DiscoveryWhere are our agents?02 SecurityWhat are they doing?03 SpendWhere is our intelligence going?

Ask Origin · DiscoveryWhere are our agents?K

You

Show every AI agent and MCP server across the fleet in the last 7 days. Group by endpoint, owner, and install path.

Routing · fleet discovery

analytics_query· done

1,284 agents · 612 endpoints · 91 shadow installs

Claude Code38%

Curs

## LinkedIn about

Organizations of all sizes depend on Prelude to know with certainty that their defenses will protect them against the latest threats. Prelude\'s security control validation platform provides the essential and continuous visibility into the state of your security controls, their configuration, and how they map against the latest threats. With actionable insights into how to maximize the tools you already have, Prelude ensures you get the most out of your security controls, align to compliance, and stay protected. Learn more: preludesecurity.com

## News (Exa, top 3)
- Prelude Security Announces Additional $16M Investment ... (2025-09-25) https://www.businesswire.com/news/home/20250925489179/en/Prelude-Security-Announces-Additional-%2416M-Investment-Led-by-Brightmind-Partners-Along-With-Sequoia-Capital-and-Insight-Partners-To-Build-the-Next-Generation-of-Endpoint-Security
  Prelude Security Announces Additional $16M Investment Led by Brightmind Partners, Along With Sequoia Capital and Insight Partners, To Build the Next Generation of Endpoint Security

Sep 25, 2025 10:30 AM Eastern Daylight Time

# Prelude Security Announces Additional $16M Investment Led by Brightmind Partners, Along With Sequoia Capital and Insight Partners, To Build the Next Generation of Endpoint Security

Share

---

NEW YORK--(BUSINESS WIRE)--Prelude Security, the next generation endpoint pro
- Prelude Security Raises Additional $16M in Funding (2025-09-25) https://www.finsmes.com/2025/09/prelude-security-raises-additional-16m-in-funding.html
  Prelude Security Raises Additional $16M in Funding

Sign in Join

Sign in

Welcome!Log into your account

your username

your password

Forgot your password?

Create an account

Sign up

Welcome!Register for an account

your email

your username

A password will be e-mailed to you.

Password recovery

Recover your password

your email

Search

FinSMEs The Website About Venture Capital News

FinSMEs The Website About Venture Capital News

Search

Home USA Prelude Security Raises Additional $16M i
- Continuing the Prelude Mission Through our $24mm ... (2022-04-22) https://www.preludesecurity.com/blog/continuing-the-prelude-mission-through-our-24mm-series-a-financing
  Looking for Prelude Security? You're looking for Origin.

# Looking for Prelude Security?

You found the right page. We are now Origin, the endpoint AI observability platform for the agent workforce running today.

Already running Prelude Monitor? Nothing changes for you. Same product. Same team. Same way of getting in touch with us.

Contact us

Whether you’re running Prelude Monitor today or sizing up Origin for the first time, we look forward to hearing from you.

I agree to Origin’s Privacy 

## Open roles (Blitz, live)
- Sales Operations ({'city': None, 'country_code': 'US'})
- AI-Native Marketer ({'city': None, 'country_code': 'CA'})
- AI-Native Marketer ({'city': None, 'country_code': 'US'})
- Sales Operations ({'city': None, 'country_code': 'US'})
- Sales Operations ({'city': None, 'country_code': 'CA'})
- Talent Acquisition Specialist ({'city': None, 'country_code': 'CA'})
- Sales Operations Specialist ({'city': None, 'country_code': 'US'})
- Talent Acquisition Specialist ({'city': None, 'country_code': 'US'})
- Sales Operations Specialist ({'city': None, 'country_code': 'CA'})
- Technical Account Manager ({'city': None, 'country_code': 'CA'})

---
# Context for the scoring agent (do not re-search)

## Barry Hess niche
Defense and intelligence technology companies in the $5M-$10M range whose proven prototype is stuck between demo and fielded deployment, guided by a CTO who fielded a patented tactical Android app platform with operators in theater and now engineers deployment architecture and acquisition advocacy from day one.

**EDP:** When months-to-field exceeds the funded months remaining on the contract, the program dies in the DoD valley of death - and for a $5M-$10M defense tech company, one dead transition is often the company.

## Deployed-reality checklist (score absence against this)
- **DDIL**: denied/disconnected/intermittent/low-bandwidth comms. Canonical example: an AI
  crowd-detection startup streamed 30fps video; the contested environment had bandwidth for
  1 frame every 5 seconds. One architecture change (frame-rate decoupling) saved the project.
- **SWaP-C**: size, weight, power, cost on the platform actually carried/mounted.
- **ATO/RMF**: Authority to Operate on government networks; STIGs, POA&Ms, IL4/IL5.
- **CMMC / NIST 800-171**: company-level compliance before the contract dies.
- **ITAR/export**: controlled data handling.
- **Operator training & sustainment**: who trains the E-5, who fixes it in the field, spares,
  battery logistics, GFE integration.
- **Advocacy chain**: a champion above the operator level; operators loving it is not adoption.
- **Prime/flow-down mechanics**: subcontract structure, government back-end integration.
- **TAK ecosystem**: if it touches situational awareness and never mentions ATAK/TAK, ask why.


## Doctrine
# Targeting doctrine brief (inject into every dossier & company agent — do NOT re-read the corpus)

Distilled from Jordan Crawford's Cannonball/Blueprint corpus, 2026-07-23.

1. **Pain-Qualified Segment beats ICP.** Never target firmographics ("50-200 person SaaS").
   Target companies in an observable painful SITUATION right now. The situation must be
   provable from public data.
2. **Existential Data Point (EDP).** For each niche, name the single number that kills the
   company if the problem stays unfixed (e.g. equipment utilization 60% vs 80% margins;
   fleet utilization <70% = crisis). Every dossier must state the EDP of its CTO's target
   situation: "what does it cost a company, in what metric, to leave this unfixed?"
3. **Jobs are confessions.** A job posting is a company publicly describing its own pain.
   We match jobs whose EXISTENCE signals a problem the CTO has already fixed — not jobs the
   CTO would apply to. "First Head of Engineering" = no technical leadership. "Integration
   Engineer (Epic, HL7)" = drowning in healthcare plumbing.
4. **The message is a redescription of the targeting.** If targeting is precise, the message
   writes itself by describing what we found. The reader should think "how do they know that?"
5. **Message-as-gift (GTM Shift letter standard).** Conversational, unhurried, 4–6 short
   sentences. Opens with a verified surprising fact. Every claim traces to a named public
   source. Valuable even if never answered. One light question, under 15 words. Bans: "I
   noticed", flattery, "hope you're well", meeting asks, personal details about the recipient
   as the opener. Lead with the CTO's expertise matched to the company's evident problem.
6. **Niche = Industry × Situation × Unique Angle** — all three specific (Ben Horowitz
   principle: not best botanist; best Japanese botanist specializing in Zen gardens).
7. **Insight tests**: counterintuitive (would other CTOs argue?), specific (exact tools/
   patterns), quantifiable (before/after numbers), demonstrable (showable in 5 minutes).
8. **Evidence honesty.** Actions > words > database records. Aggregator/API data (Blitz,
   FullEnrich) never corroborates itself — load-bearing claims need the person's or
   company's OWN public artifacts. Date every claim; label estimates as estimates.
9. **Dropping a bad fit is success.** Never pad a list to hit a count.
