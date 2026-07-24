# Evidence pack: Q-Net Security
slug: q-net-security | domain: qnetsecurity.com | HQ: St Louis, Missouri US | employees(LI): 13 | founded: 2015 | stage_band: series_a
sources: exa-agent:defense-cyber
industry(LI): Computer and Network Security | specialties: data center security, encryption, network security, enterprise hardware, cybersecurity
channel notes: Series A Series A-stage company; additionally received an Air Force SBIR Phase III IDIQ award. dom: cyber status: fielded dod: Q-Net’s silicon-based cyber product won an Air Force SBIR Phase III IDIQ for protection of tactical-edge communications, including airborne WANs, air-to-air links, and mobile ad-hoc networks supporting Agile Combat Employment. hq: St. Louis, MO emp:  src: https://www.businesswire.com/news/home/20250819547305/en/Q-Net-Security-Secures-a-SBIR-Phase-III-IDIQ-Contract-with-the-U.S.-Air-Force-to-Protect-Tactical-Edge-Communications
own-language word count: ~1268

## Their own words (website via Exa, livecrawl-preferred)

URL: https://qnetsecurity.com
Home | Q-Net Security - Superior Security for Point-to-Point Communication

Silicon-based cybersecurity

# Enhanced security.Simplified management.Cost-effective.

As cyberattacks evolve — powered by AI and on the verge of quantum — traditional approaches struggle to keep up. Q-Net delivers seamlessly integrated, silicon-based protection built for the networks of today and the threats of tomorrow.

See the solution → Contact us

Why Q-Net

## Three problems. One device.

Simplified management

### Low maintenance, effortless deployment

- Plug-and-play integration — works with existing infrastructure, no rip-and-replace.
- Set and forget — no installs, upgrades, or patches.
- Automated keying — eliminates manual key management.
- No complexity — no firewall rules or endpoint agents.
- Streamlined network — cloaked IPs simplify management.

Unmatched cybersecurity

### Cryptographically enforced microsegmentation

- Secure silicon — immune to remote hacks, including AI-powered.
- Quantum-resistant encryption — protection against emerging quantum threats and beyond.
- Proactive defense — prevents lateral movement and exfiltration, not just detection.
- Compliance certified — FIPS-140 and NSA/NIST post-quantum guidelines.

Cost-effective

### Do more with less

- No infrastructure overhaul — integrates with your current network.
- Flexible adoption — replace redundant tools on your own schedule.
- Comprehensive protection — VPN- and firewall-class function without the complexity.

3

Day USCYBERCOMexercise

The only solution to remain unbroken — no Q-Net-protected endpoint was ever compromised over the three-day exercise.

— USCYBERCOM smart-city red-team exercise · Validated with NCCoE & NIST

1/5

### ... After carrying out the tests contemplated within this document, it can be concluded that the tool complies with the functionality it offers. The encryption added to data transmission between the protected points is of great power and after all the tests were carried out by the participating team, the device could not be breached and remained invisible (i.e., no information could about it could be obtained).

---

International Telecom Executive

2/5

### The configuration and administration of this solution is quite simple in striking contrast to the strength that it brings to operations. As a final consideration, Q-Net is an effective and powerful tool that has multiple deployment use cases in client environments.

---

International Telecom Executive

3/5

### Q-Net evaluate[d] uniquely and favorably, and reporting require[d] a separate section.

---

USCYBERCOMExercise Chief

4/5

### The gear we have in place at the plant is still operational and has been working properly without issue.

---

Major US UtilitySenior Network Administrator

5/5

### Q-Net Security is installed as a part of our reference architecture especially distributed renewables … and a good solution for handling grid-edge systems.

---

Power Industry ConsortiumPrincipal Cybersecurity Manager

URL: https://qnetsecurity.com/about
About us | Q-Net Security - Superior Security for Point-to-Point Communication

Who we are

# Security, rightthe first time.

Q-Net is built by the scientists and engineers who designed the technology — hardware-based encryption that protects on day one and for years to come.

Leadership

## A leadership team rooted in science and expertise

Our team stands behind our product — they've designed it from the ground up. Scientists, entrepreneurs, and engineers with decades of direct experience in technology and encryption, leading Q-Net Security to design and deploy groundbreaking technology in real commercial settings.

John Pyrovolakis

CEO

Deborah L. Wince-Smith

Board of Directors

Randall Cox

Board of Directors

Scott Chaney

COO

Andrew Quirin

Chief Architect

Contact

Advisors

## Insights & connections

Strong leadership for strong security. Q-Net's technology is backed by scientific, business, and financial leaders, and we count dozens of additional members among our advisors. When deploying the next generation of security, we believe our team needs to be driven by luminaries and leaders.

#### JOHN PYROVOLAKISCEO, Q-Net Security

Pyrovolakis founded the Innovation Accelerator Foundation (IAF), whose mission is to promote our nation's economic competitiveness by promoting our nation's innovation. The IAF hosts the Academic Venture Exchange, where a set of elite research and development American universities pool some of their premier innovation assets. It also hosts iBridgeNetwork, which is our nation's largest university intellectual property marketplace. Prior to founding the Innovation Accelerator, Pyrovolakis started iKaptivate - a software-as-a-service workflow tool - to a private equity firm. Before that Pyrovolakis was a mergers and acquisitions banker at Jesup & Lamont, a boutique investment bank based in New York. Prior to that, Pyrovolakis founded CollegeScape - a software as a service online college admissions platform - which he sold to Thomson-Reuters, a multinational conglomerate that trades on the New York Stock Exchange (“TOC”).

Pyrovolakis is a member of the Board of Trustees of The American College of Greece and a member of the Board of Directors at Atreyu Trading, TruBeacon, Q-Net Cybersecurity and the New Jersey Innovation Institute. Pyrovolakis was a judge at the MIT, Columbia, and Stonybrook Entrepreneurship competitions, and a member of the “Committee of Visitors” to the National Science Foundation.

#### DEBORAH L. WINCE-S

URL: https://qnetsecurity.com/the-solution
The Solution | Q-Net Security - Superior Security for Point-to-Point Communication

The Solution / Components

# Hardware on the wire.Policy off to the side.

Two components. The Q-Box encrypts every packet in silicon. The QPM decides who may talk. Nothing else ever touches your data.

The data journey

01

Plain-text in

Endpoint sends clear traffic into the Q-Box endpoint port.

›

02

Q-Box encrypts

AES-256-GCM in silicon, a fresh key as often as every packet.

›

03

Cipher on the wire

Only cipher-text crosses the untrusted network.

›

04

Q-Box decrypts

Peer Q-Box authenticates the source and decrypts.

›

05

Plain-text out

Clear traffic exits to the destination endpoint.

How it fits together

## The architecture

A secure overlay on the network you already run. Trust is created between protected endpoints across an untrusted path.

QPM

Control plane. Q-Boxes register themselves to the QPM, and the QPM pushes policy to registered Q-Boxes. No user traffic ever traverses the QPM.

DATA PLANE · POINT-TO-POINT

PROTECTED

SERVER

PLC / RTU

SENSOR

ANY IP ENDPOINT

PLAIN

Q-BOX

AES-256

UNTRUSTEDNETWORK

AES-256

Q-BOX

PLAIN

PROTECTED

SERVER

PLC / RTU

SENSOR

ANY IP ENDPOINT

Plain-text inside the perimeter · cipher-text on the wire · new keys used up to every packet

01 / The hardware

## Q-Box

A silicon encryption device — no processor, no OS, no software — that drops directly in line on the ethernet segment of the device it protects. A hardware barrier discards unauthorized data at line rate.

AES-256

GCM · IN SILICON

#7

0/142

PATENTED JUST-IN-TIME KEYING

2,000

CONNECTIONS / BOX

0

IP · AGENTS · SOFTWARE PATCHES

Q-BOX

ENDPOINT

PLAIN-TEXT

Q-BOX

NETWORK

CIPHER-TEXT

On the roadmap

We aren't done yet — increased throughput and more coming soon.

Contact us for details →

02 / The brain

## QPM

The Q-Net Policy Manager is where you describe what is allowed — bring-your-own-OS installable software, or available as a SaaS. It distributes policy; no user traffic ever passes through it.

Zero data path

Establishes secure connections only — never sees your traffic.

Thousands of boxes

Individual or group management with automated keying.

Instant revoke

Pull a Q-Box from the network if a unit is lost or captured.

Plane separation

Control plane fully separated from the data plane.

Deployment

## Bump-in-the-wire.Set & forget.

Drop in

Insert the Q-Box in line on the physical cable. No rip & replace, no IP changes, no agents.


URL: https://qnetsecurity.com/datasheets
Datasheets | Q-Net Security - Superior Security for Point-to-Point Communication

The Solution / Datasheets

# Datasheets

Download the latest technical specifications for the Q-Box encryption device.

Q-Box

MODEL QBX-100311

AES-256-GCM190 Mb/s2,000 CONNSFIPS 140-2

Silicon encryption device — bump-in-the-wire, hardware AES-256-GCM, per-packet keying. DPI-compatible via Traffic Mirroring.

Download PDF ↓ 1 PAGE

Looking for how it all fits together? Read the solution overview →

## LinkedIn about

Q-Net Security produces hardware that creates an impenetrable barrier between defined endpoints within your existing network. QNS is national intelligence-grade, quantum-resistant security that is more powerful than any other cybersecurity solution in the world. We drop into existing networks with minimal configuration, and render brute force decryption attacks nigh-impossible.

## News (Exa, top 3)
- Q-Net Security Secures a SBIR Phase III IDIQ Contract with ... (2025-08-19) https://www.businesswire.com/news/home/20250819547305/en/Q-Net-Security-Secures-a-SBIR-Phase-III-IDIQ-Contract-with-the-U.S.-Air-Force-to-Protect-Tactical-Edge-Communications
  Q-Net Security Secures a SBIR Phase III IDIQ Contract with the U.S. Air Force to Protect Tactical Edge Communications

-

# Q-Net Security Secures a SBIR Phase III IDIQ Contract with the U.S. Air Force to Protect Tactical Edge Communications

Share

---

ST. LOUIS--(BUSINESS WIRE)-- Q-Net Security, who is pioneering the field of silicon-based cybersecurity, has been awarded a contract by the United States Air Force to help develop technologies and requirements aimed at securing communications at
- Q-Net Security wins USAF SBIR Phase III to secure military ... (2025-08-20) https://www.airforce-technology.com/news/q-net-security-usaf/
  Q-Net Security wins USAF SBIR Phase III to secure military comms

Q-Net Security enhances data transit security with silicon-based cybersecurity solutions for defence and enterprise networks. Credit: Gorodenkoff/Shutterstock.com.

Q-Net Security has received the US Air Force (USAF) Small Business Innovation Research (SBIR) Phase III indefinite delivery, indefinite quantity (IDIQ) contract to enhance security of military communications.

The contract involves the development of technologies and s
- US Air Force Taps Q-Net for Advanced Tactical ... (2025-08-22) https://thedefensepost.com/2025/08/22/us-communication-systems-qnet/
  US Air Force Taps Q-Net for Advanced Tactical Communication Systems

Soldier operates a computer system during a field training exercise. Photo: Lance Cpl. Jonathan Willcox/US Marine Corps

Missouri-based Q-Net Security has signed a US Air Force contract to help make battlefield communications faster, safer, and more reliable in domains where every second and signal counts.

The project builds on the firm’s earlier work with the service centering on the development and fielding of airborne wide-

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
