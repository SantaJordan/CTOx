# Evidence pack: Ditto
slug: ditto | domain: ditto.com | HQ: San Francisco, California US | employees(LI): 208 | founded: 2018 | stage_band: series_a | LATE(151-300)
sources: exa-agent:tactical-mobile-edge-more|sbir
industry(LI): Technology, Information and Internet | specialties: peer-to-peer, crdt, edge sync, cloud-optional, offline database
channel notes: Series A / SBIR Phase III $45M Series A; multiple DoD SBIR Phase I/II awards and Phase III eligibility. dom: mobile status: fielded dod: Ditto states that its ATAK Edge Sync Plugin is used by USSOCOM and other DoD entities, following multiple SBIR awards for DoD use cases. hq: San Francisco, CA emp: 100-200 src: https://www.ditto.com/products/ditto-atak-plugin || SBIR PhII x2 [2023] Air Force latest: AFWERX FA8650-22-C-9222 Sequential Small Business Innovation Research (SBIR) Phase II - Decision Lens Accelerate hq: San Francisco,CA emp: 6
own-language word count: ~1442

## Their own words (website via Exa, livecrawl-preferred)

URL: https://ditto.com
Ditto - Resilient Edge Device Connectivity

# ResilientEdgeDeviceConnectivity.Servers&CloudOptional.The only offline-first database with built-in peer-to-peer networking

Ditto SDK v5: Built for Speed and Developer Experience Ditto SDK v5: Built for Speed and Developer Experience

Blog

Ditto SDK v5: Built for Speed and Developer Experience

Building an LLM Wiki for Ditto: How a Mac Mini Became My Second Brain Building an LLM Wiki for Ditto: How a Mac Mini Became My Second Brain

Blog

Building an LLM Wiki for Ditto: How a Mac Mini Became My Second Brain

We Built a Browser Robot Because Webflow's API Can't Handle a Code Block We Built a Browser Robot Because Webflow's API Can't Handle a Code Block

Blog

We Built a Browser Robot Because Webflow's API Can't Handle a Code Block

## Keep mission-critical systems online when it matters most

Ditto is the only edge-native, mobile database that can consistently support your business anytime, anywhere. Edge-native solutions are built specifically to thrive on mobile and edge devices, without relying solely on cloud-based services.

Build flexible operations that are both latency-sensitive and resilient without reliance on network hardware, edge servers, or the cloud

Decentralize your systems to remove single points of failure that lead to operational bottlenecks

Drive consistent revenue and customer service anywhere, regardless of connectivity or bandwidth

“When your POS goes down, that has a true financial cost to your business”

Once Ditto is installed in your applications, write a few simple queries, and watch your mobile and edge devices automatically form mesh networks and share data directly without the need for servers or access points.

## The Tech

Take a quick look at the core technology powering our peer-to-peer and cloud sync plans.

Foundational Technology

---

##### Offline-first mobile database

Even when devices are completely offline, they can always read, write, and process data

---

##### CRDT-powered conflict resolution

To resolve concurrency conflicts that appear in decentralized models, as well as enable delta-based sync, Ditto harnesses the power of conflict-free replicated data type (CRDT) technology

P2P Sync

Device Sync

---

##### Automatic Device Discovery and Mesh Networking

Devices running the same application automatically connect and maintain ad-hoc mesh networks without the need for manual pairing or configuration

---

##### Direct Peer-to-Peer Sync

Out-of-the-box support for BLE, P2P WiFi, LAN, and more enables real-time sync in disconnected or bandwidth-constrained environments

---

##### Opportunistic Cloud Sync

Anytime internet is available to one or more devices within the mesh, all devices sync with your existing cloud systems

---

##### Opportunistic Cloud Sync

Anytime internet is available, devices sync with your existing cloud systems

Success Stories

---

“Our Ditto partnership is providing real-time visibility for inflight devices”

"Our approach to developing frontline tools prioritizes close partnership with our flight attendants during each development step. Ditto has been a great partner in ensuring our tools are seamless for our flight attendants. With their help, we have supported our workgroup by providing visibility of one another’s inflight mobile device… in real-time"

Read More

Vikram BaskaranVP of IT

“Ditto moves key data quickly with no round trips to central services”

“Ditto moves key operational data between retail team members quickly, seamlessly and with no round trips to central services. The more control and information we can put in the hands of operators and their teams, the better they can care for customers.”

Read More

Chris TaylorRetail Ops Manager

“This technology truly revolutionizes the way crew members work”

Ditto's remarkable capabilities enable smooth and stable communication among crew devices, even without connectivity during flight. This allows our crew to shift from former manual operations to a more advanced and efficient working style and enables us to create more room for the crew to introduce new services to passengers. This technology truly revolutionizes the way crew members work.

Read More

Ms. Yu AbeDirector, IT Planning & Promotion Department

“Ditto ensures USAF's data remains as reliably agile as we are”

Ditto is our strategy to ensure that USAF's data remains as reliably agile as we are… with Ditto, married with these Apple Platforms… we can provide a seamless and mission-ready experience anywhere in the world, and under any circumstances.

Read More

Bryan AlleboneMajor 55th Wing / BOCKSCAR

### Harness the full power of your existing mobile and edge infrastructure

More WiFi isn’t the answer. Your mobile and edge devices are more powerful than you realize, capable of advanced networking without the need for new devices, hardware, or networking setups.

Bridge connectivity gaps without added hardware or complexity.

Once Ditto is installed in your applications, write a few simple queries, and watch your mobile and edge devices automatically form mesh networks and share data directly without the need for servers or access points.

Swift

KOTLIN

JAVASCRIPT

C#

C++

RUST

```
// initialize Ditto with your account credentials
    let ditto = Ditto(...)
    try ditto.startSync()
    
    // insert data into your local data store
    try await ditto.store.execute(
        query: "INSERT INTO cars DOCUMENTS ({ 'color': 'blue' })")
    
    // listen for change to your local data store
    try ditto.store.registerObserver(
        query: "SELECT * FROM cars"){ result in
            /* Update UI */
    };
    
    // sync only the data your device cares about
    try ditto.sync.registerSubscription(query: "SELECT * FROM cars")
```

```
// initialize Ditto with your account credentials
    val ditto = Ditto(DefaultAndroidDittoDependencies(context))
    ditto.startSync()
    
    // insert data into your local data store
    ditto.store.ex

URL: https://ditto.com/products/ditto-atak-plugin
Ditto ATAK Plugin 

INTEGRATIONSEdge Sync PLUGIN for atak

# Maintain Operational Connectivity in Any Environment

Ditto’s Edge Sync Plugin for ATAK (Android Team Awareness Kit for Civilian use or Android Tactical Assault Kit for military use) ensures real-time data sharing even in degraded, denied, or disconnected environments.

Powered by Ditto's Edge SDK - offline-first mobile database

Automatically sync peer-to-peer over any available transport

Ensure data consistency and security in DDIL environments

The Problem

---

Unreliable connectivity disrupts teams' CoP within ATAK

Maintaining a Common Operational Picture (CoP) is crucial to ensuring the effectiveness and safety of disconnected teams in degraded environments, but communications are prone to interruption and failure - even with MANET radios and TAK servers. Not to mention, mesh network mode for ATAK doesn't support sync without a local area network.

The Solution

---

Unlock resilient peer-to-peer sync in any environment

Ditto's Edge Sync Plugin for ATAK enables devices to maximize the use of their own inherent communication pipelines (WiFi, Bluetooth, P2P WiFi, etc.) in addition to MANET radios. This mesh data sync solution ensures resilient and redundant communication capabilities between connected nodes without unnecessary hardware.

## Unlock true offline power in ATAK

Long-Range Multi-Hop Sync

The plugin will automatically relay data across multiple devices, extending the communication range and enabling disconnected devices to exchange data.

Consistent CoP Without a Server

The plugin can synchronize data changes across all nearby team members without specialized hardware. Enhance coordination and situational awareness with the mobile devices you already have.

Transport and Platform Agnostic

Sync over Bluetooth Low Energy, WiFi Aware, MANET, SATCOM, and more. The plugin runs on all your platforms including mobile, web, server, and embedded hardware.

Fast Deployment

The plugin is already mission-ready. Compatible with ATAK 4.10+, a simple installation process you will have your team ready for deployment quickly and without complexity.

Powered by the Ditto Edge SDK

Learn More

---

## See the full picture, anytime, anywhere

Empower real-time decision-making everywhere, from the command center to the tactical edge, even in disconnected, denied or contested environments.

#### Sync between distant teams, even when offline

Even devices disconnected entirely from the cloud can 

URL: https://ditto.com/solutions/public-sector/propagate
Propagate

PRODUCTS

PROPAGATE

# Software-defined Networking for the Tactical Edge

Propagate by Ditto transforms any Commercial Off-The-Shelf (COTS) Android phone or tablet into a powerful edge network router, edge<->cloud gateway, and robotic controller — no custom hardware required.

- Edge network routing across multiple disparate terrestrial networks and IP-based peripherals
- Cloud gateway via any path the Android can reach — LTE, Starlink, WiFi, and more
- Robotic network interface control for UAS Ground Control Stations
- Deep ATAK integration with built-in TAK server and plugin

The Problem

---

## Custom hardware is the bottleneck at the tactical edge

Current battlefield edge networking relies on custom, kernel-configured End User Devices (EUDs) and expensive, bulky hardware for routing, bridging, and cloud connectivity. These purpose-built solutions create supply chain fragility, cost overruns, and fielding delays — limiting digital situational awareness to those with specialized equipment. With over 300,000 ATAK users across the DoD and allied forces, the custom EUD has become the limiting factor for capability fielding at scale.

The Solution

---

## A software-defined approach on the devices you already have

Propagate delivers a patent-pending userspace IP Stack that runs as a consumer-type app on any of the 3+ billion Androi

## LinkedIn about

Ditto is the only mobile database with built-in edge device connectivity and resiliency. 
Drive consistent revenue and build flexible operations at the edge without WiFi, Servers, or Cloud. Sell a product, deliver a service, and conduct operations anywhere without worrying about connectivity. 

## News (Exa, top 3)
- Contracts For Jul. 11, 2025 () https://www.war.gov/News/Contracts/Contract/Article/4242075/
  Contracts For Jul. 11, 2025 > U.S. Department of War > Contract | U.S. Department of War

Skip to main content (Press Enter).

NAVY

Rolls-Royce Corp., Indianapolis, Indiana, is awarded a $54,730,397 firm-fixed-price modification to previously awarded contract (N00024-25-C-2405) for production of 12 MT7 turboshaft engines, ancillary parts, and installation kits in support of the Ship to Shore Connector program, Landing Craft, Air Cushion 100 class craft. Work will be performed in Indianapolis, I
- US Air Force Awards $950M Contract to Ditto for Next- ... (2022-03-29) https://www.ditto.com/press-releases/us-air-force-awards-950m-contract-ditto-command-control
  US Air Force Awards $950M Contract to Ditto for Next-Generation Command and Control Network

Press Release

# US Air Force Awards $950M Contract to Ditto for Next-Generation Command and Control Network

Ditto will incorporate its Intelligent Edge platform to power the US Air Force Advanced Battlefield Management System (ABMS)

‍

March 29, 2022

SAN FRANCISCO, CA / ACCESSWIRE / March 29, 2022 / Ditto, creators of next-generation software infrastructure that enables apps to synchronize data in re
- Ditto - AFWERX Selects Ditto for Strategic Funding Increase (STRATFI) Opportunity up to $28M () https://www.ditto.com/blog/afwerx-selects-ditto-for-strategic-funding-increase-stratfi-opportunity-up-to-28m
  Ditto - AFWERX Selects Ditto for Strategic Funding Increase (STRATFI) Opportunity up to $28M

Published OnApril 1, 2025March 31, 2025

# AFWERX Selects Ditto for Strategic Funding Increase (STRATFI) Opportunity up to $28M

# Ditto has been selected for a Strategic Funding Increase (STRATFI) opportunity by AFWERX (or SpaceWERX) with funding of up to $28 million.

Adam Fish

Founder and CEO

Ditto, the only mobile database with built-in edge device connectivity, has been selected for a Strategic F

## Open roles (Blitz, live)
- Senior Software Engineer, Cloud ({'city': 'Seattle', 'country_code': 'US'})
- 2026 Ditto Intern Program (Fall) ({'city': 'Atlanta', 'country_code': 'US'})
- Senior Software Engineer, Portal ({'city': 'Atlanta', 'country_code': 'US'})
- PubSec Counsel ({'city': 'Seattle', 'country_code': 'US'})
- Senior Software Engineer, Portal ({'city': 'Atlanta', 'country_code': 'US'})
- Senior Software Engineer, Data Sync ({'city': 'Seattle', 'country_code': 'US'})
- Senior Software Engineer, Systems FDE ({'city': 'Seattle', 'country_code': 'US'})
- Senior Software Engineer, Portal ({'city': 'Atlanta', 'country_code': 'US'})
- Revenue Operations Lead ({'city': 'Atlanta Metropolitan Area', 'country_code': 'US'})
- Director of People Operations ({'city': 'Greater Seattle Area', 'country_code': 'US'})

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
