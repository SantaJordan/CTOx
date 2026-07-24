# Evidence pack: TerraKinesis
slug: terrakinesis | domain: terrakinesis.com | HQ: Detroit, Michigan US | employees(LI): 3 | founded: 2026 | stage_band: preseed_seed
sources: exa-agent:tactical-mobile-edge-more
industry(LI): Embedded Software Products | specialties: embeddedsoftware, defense, software, commercial, scale, datameshes
channel notes: Pre-seed  dom: other status: pilot dod: TerraKinesis demonstrated PULSE software on TrellisWare radios during the U.S. Army's Dragon Nexus 26-01 bench test to improve tactical network scaling and connectivity. hq: Detroit, MI emp: 4 src: https://terrakinesis.com/
own-language word count: ~1391

## Their own words (website via Exa, livecrawl-preferred)

URL: https://terrakinesis.com
TerraKinesis — PULSE

Detroit, MI · Newlab

# PULSE

Distributed Computing up to 1,000 nodes. Real-time. No Servers. No SATCOM.

1,000+Nodes at Scale

<1msLocal Repair

95-99%Overhead Reduction

Backed by

Operational View

## Current State vs.Future State

Today, multi-domain command and control depends on centralized base stations and mandatory SATCOM links. When a link fails, the network fragments. PULSE replaces this with a distributed, self-healing mesh where every node communicates directly. SATCOM becomes optional.

What We Build

## Guaranteed MessagingWithout SATCOM

Today, distributed systems without servers crash at 20 nodes.

PULSE is a software microservice that guarantees message delivery — essential for distributed computing — across crewed, uncrewed, sensor, and dismount nodes in denied, degraded, intermittent, and limited bandwidth (DDIL) environments.

Two innovations make this possible. The NACK protocol — receivers signal only on missed messages — reduces network overhead by 95 to 99 percent. Beehive dynamic clustering groups nodes into self-healing colonies of 15 to 25, dropping scaling complexity from O(n²) to O(n).

PULSE runs on UDP/multicast. It deploys on the transport infrastructure already at the edge. Integration takes two to four weeks.

Explore the Architecture →

Defense

Multi-domain command and control for 1,000+ assets. Compatible with NGC2, TAK, Lattice, JBC-P, and C2FIX. Tested on commercial, public sector, and military radios.

▸

ITS / V2X

Guaranteed vehicle-to-vehicle messaging without the latency penalty of cellular hub-and-spoke. Enables connected infrastructure for autonomous vehicles.

▸

Software-Defined Vehicle

Replace kilometers of copper wiring with a self-healing wireless data mesh inside the vehicle. Faster than CAN bus. Redundant by design.

▸

Edge Computing

Drone swarms, manufacturing, warehouse robotics. Guaranteed delivery at 142 frames per second under 30 to 80 percent burst jamming.

▸

Team

## Built by Operators

Three co-founders with overlapping experience across the defense industrial base, automotive, and hyperscale cloud — from concept to contract.

Defense & Government

U.S. Army combat veteran. West Point. Top Secret clearance. Led programs at AWS generating $1B+ in defense revenue. Product leadership at Parry Labs on NGC2 architecture. Edge-native data synchronization at Ditto for contested operations.

Autonomy & AI

Production ADAS platforms across multiple vehicle lines at Big Three Automotive OEM. Embedded autonomy, vehicle motion control, and actuator integration at FCA. Pioneered real-time control, perception, and edge-cloud autonomy systems.

Enterprise Growth & Operations

Scaled a Series C defense unicorn software platform from inception to a near $1B+ valuation. Fortune-scale enterprise accounts at Salesforce. $80M/year channel territory at Zebra Technologies. $10M/year enterprise territory at Motorola Solutions.

Automotive & Strategy

Chicago Booth MBA. Systems engineering on large-scale safety-critical platforms at General Motors. Dual-use technology commercialization. Track record from prototype to $10M+ government contracts.

eSOF Scout Card

## Capability Overview

Scan to viewScout Card

Latest

## From the Substack

Substack · TerraKinesisHidden in Plain SightThe F-15E survival communications use case and what it reveals about the gap between today's C2 architecture and the distributed future. Read on Substack

Learn More

## Resources

⚙ArchitectureInteractive deep-dive into PULSE: beehive clusters, self-reconciling roll call, NACK aggregation, rotating shadow master.Explore

✎SubstackTechnical articles on PULSE architecture, defense applications, and commercial use cases.Read

▣eSOF Scout CardOne-page capability overview. Technical specs, integration details, and program alignment.View

👥LinkedInFollow TerraKinesis for product updates, demonstrations, and industry analysis.Follow

## See PULSE in Action

A ninety-second visualization of why acknowledgment-based protocols collapse at scale in DDIL, and what PULSE does instead. Narrated.

Watch the Demo →

Initiate Inquiry

[email protected]

Technical inquiries, partnership discussions, and demonstration requests.

URL: https://substack.com/@mustafaterrakinesiscom/note/p-193402044?r=7evom8&utm_source=notes-share-action&utm_medium=web
Hidden in Plain Sight - [email]

# [email]

SubscribeSign in

# Hidden in Plain Sight

### How a Downed Pilot in Iran Exposes the Architecture Problem PULSE Was Built to Solve

[email]

Apr 06, 2026

1

Share

# The Event

On April 3, 2026, an F-15E Strike Eagle from the 494th Fighter Squadron was shot down over southwestern Iran. Both crew members ejected. The pilot was rescued within hours. The weapons systems officer (WSO) was not.

The WSO landed alone in the Zagros Mountains. He carried a handgun, SERE training, and a Combat Survivor Evader Locator (CSEL) — an 800-gram satellite beacon integrated into his survival vest. The CSEL transmits encrypted location coordinates and short text messages to satellites. It uses rapid frequency hopping and ultra-short burst transmissions to reduce the probability of detection.

Thanks for reading! Subscribe for free to receive new posts and support my work.

Subscribe

But every transmission creates an emission. The CSEL operates in a spoke-and-hub topology. The WSO is the spoke. The satellite is the hub. Iranian electronic warfare units and IRGC ground forces were hunting him across a constrained search area. Military officials confirmed that aircrews are trained not to broadcast continuously because the beacon can be detected by the enemy. So he rationed his communications. Short bursts. Long silences. Predefined text messages — “injured,” “enemy nearby,” “ready for extraction” — and limited voice. He hid in a mountain crevice for over 36 hours while hundreds of Iranian soldiers closed in and Iranian state television called on civilians to turn him over for a bounty.

The rescue required hundreds of special operations forces, dozens of aircraft, CIA deception campaigns, Israeli air support, and U.S. attack aircraft dropping bombs on approaching Iranian convoys. Two Black Hawk helicopters took fire. An A-10 Warthog was shot down. Two C-130 transport planes became stuck on an improvised airstrip and were deliberately destroyed to deny the enemy access to sensitive systems. At least one special operations helicopter was also destroyed.

The WSO survived. The mission succeeded. But the cost was extraordinary — and the fundamental constraint remains unchanged. A downed warfighter today must choose between communication and concealment. The architecture forces that trade-off.

# The Problem

The CSEL is an impressive device. It does exactly what it was designed to do. 

URL: https://terrakinesis.com/
TerraKinesis — PULSE

Detroit, MI · Newlab

# PULSE

Distributed Computing up to 1,000 nodes. Real-time. No Servers. No SATCOM.

1,000+Nodes at Scale

<1msLocal Repair

95-99%Overhead Reduction

Backed by

Operational View

## Current State vs.Future State

Today, multi-domain command and control depends on centralized base stations and mandatory SATCOM links. When a link fails, the network fragments. PULSE replaces this with a distributed, self-healing mesh where every node communicates directly. SATCOM becomes optional.

What We Build

## Guaranteed MessagingWithout SATCOM

Today, distributed systems without servers crash at 20 nodes.

PULSE is a software microservice that guarantees message delivery — essential for distributed computing — across crewed, uncrewed, sensor, and dismount nodes in denied, degraded, intermittent, and limited bandwidth (DDIL) environments.

Two innovations make this possible. The NACK protocol — receivers signal only on missed messages — reduces network overhead by 95 to 99 percent. Beehive dynamic clustering groups nodes into self-healing colonies of 15 to 25, dropping scaling complexity from O(n²) to O(n).

PULSE runs on UDP/multicast. It deploys on the transport infrastructure already at the edge. Integration takes two to four weeks.

Explore the Architecture →

Defense

Multi-domain command and control for 1,000+ assets. Compatible with NGC2, TAK, Lattice, JBC-P, and C2FIX. Tested on commercial, public sector, and military radios.

▸

ITS / V2X

Guaranteed vehicle-to-vehicle messaging without the latency penalty of cellular hub-and-spoke. Enables connected infrastructure for autonomous vehicles.

▸

Software-Defined Vehicle

Replace kilometers of copper wiring with a self-healing wireless data mesh inside the vehicle. Faster than CAN bus. Redundant by design.

▸

Edge Computing

Drone swarms, manufacturing, warehouse robotics. Guaranteed delivery at 142 frames per second under 30 to 80 percent burst jamming.

▸

Team

## Built by Operators

Three co-founders with overlapping experience across the defense industrial base, automotive, and hyperscale cloud — from concept to contract.

Defense & Government

U.S. Army combat veteran. West Point. Top Secret clearance. Led programs at AWS generating $1B+ in defense revenue. Product leadership at Parry Labs on NGC2 architecture. Edge-native data synchronization at Ditto for contested operations.

Autonomy & AI

Production ADAS platforms across multiple vehicle lines at Big Three A

URL: https://terrakinesis.com/architecture/
PULSE Architecture — TerraKinesis

01 · Communications stack

## From firmwareto frequency.

Pulse Protocol today is a software bus — application logic riding on top of fixed WiFi silicon. The SDR roadmap takes ownership of MAC and PHY, which is what unlocks beehive scale, FHSS jamming resistance, slot-precise TDMA, and waveform agility.

Today

### Pulse on COTS MCU

Software-defined behavior on fixed WiFi silicon.

Application

Telemetry · FOTA · jammer detection

Pulse

Transport

UDP · custom retries

Pulse

Network

Static peer 

## LinkedIn about

TerraKinesis builds PULSE — embedded software that guarantees message delivery at scale across complex military and commercial edge environments. Modern tactical networks break under load. Standard solutions top out at roughly 20 nodes in self-healing mesh networks. NORM-based approaches cap near 150. Neither was designed for the scale, speed, or chaos of real-world edge operations. PULSE changes that. It delivers guaranteed messages in node complex meshes with 167–833x lower repair latency than existing alternatives, running on roughly lines of bare-metal code. PULSE is not a replacement for 

## News (Exa, top 3)
- PULSE Reduces Network Overhead by 60% at Fort Bragg | TerraKinesis posted on the topic | LinkedIn (2026-06-23) https://www.linkedin.com/posts/terrakinesis_casestudy-260623-activity-7475255419804774401-5XF-
  PULSE Reduces Network Overhead by 60% at Fort Bragg | TerraKinesis posted on the topic | LinkedIn

Agree & Join LinkedIn

By clicking Continue to join or sign in, you agree to LinkedIn’s User Agreement, Privacy Policy, and Cookie Policy.

# PULSE Reduces Network Overhead by 60% at Fort Bragg

https://www.linkedin.com/company/terrakinesis

TerraKinesis

206 followers

6d Edited

- Report this post

Last week at Fort Bragg, the U.S. Army documented an inconvenient truth: push TCP/IP past 20 nodes 
- Chrissy McGarry - Co-Founder, President & CEO | Defense Tech (2026-07-18) https://www.linkedin.com/in/ckmcgarry
  # Chrissy McGarry

Co-Founder, President & CEO | Defense Tech | Edge C2 | Autonomy

Detroit Metropolitan Area (US)

500 connections • 6,109 followers

## About

Hi, I’m Chrissy McGarry — a proven operator, board leader, and former Chief Operating Officer of Second Front (2F), a venture-backed national security software company. I helped scale the business from inception to now a $750M+ valuation, transforming from what began as a services-led offering evolved into a software solution and ultimat
- terrakinesis (2026-06-20) https://terrakinesis.com/
  # TerraKinesis

TerraKinesis is a Embedded Software Products company. TerraKinesis employs 4 people, founded in 2026. Headquartered in Detroit, Michigan, United States.

## About

TerraKinesis builds PULSE — embedded software that guarantees message delivery at scale across complex military and commercial edge environments.

Modern tactical networks break under load. Standard solutions top out at roughly 20 nodes in self-healing mesh networks. NORM-based approaches cap near 150. Neither was desi

## Open roles
(no jobs data found)

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
