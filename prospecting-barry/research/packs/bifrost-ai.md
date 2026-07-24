# Evidence pack: Bifrost AI
slug: bifrost-ai | domain: bifrost.ai | HQ: San Francisco, California US | employees(LI): 41 | founded: 2020 | stage_band: unknown
sources: vc:iqt
industry(LI): Software Development | specialties: vla, perception, ai, artificial intelligence, robotics data, world models, robotics evaluation, robotics policy, physical ai, humanoid, nvidia isaac lab, robotics, simulation, robotics testing, ego-centric data, synthetic data, usv, maritime
channel notes: Synthetic data and simulation for defense computer vision models (IQT portfolio, category AI)
own-language word count: ~1477

## Their own words (website via Exa, livecrawl-preferred)

URL: https://bifrost.ai
Bifrost · Simulation infrastructure for physical AI

BIFROST_SIM_v2.0

# Evaluate & ImprovePhysical AI

Discover what breaks your robot in 30 min using GPU-accelerated simulation.

Evaluate Manifold

Robot policy evaluations made easy, fast and insightful.

GET ACCESS LEARN MORE

Improve Stardust

Fix failures by generating photorealistic, multi-modal sensor data.

BOOK A DEMO LEARN MORE

## We’re getting AI into the physical world

01

### Codifying the hardest tasks in simulation

Turn demanding physical tasks into high-fidelity, multi-modal simulation.

02

### Evaluation Tasks defined by industry experts

To ensure reliability across complex industrial tasks domain experts define scenarios and SOPs

03

### Making simulation accessible to all

Open tools and synthetic data so any team can train, test, and evaluate physical AI.

We started where the stakes are highest, in production with the world’s most demanding teams.

NASA

BACKED BY

## A living library of physical work, across every domain

MARITIME

SPACE

AERIAL

OFF-ROAD

ROBOTICS

OPERATIONS

MANIFOLD

## The evaluation platform for robotics researchers

Run every major simulator benchmark in hours, not days, see exactly where your policy fails, and compare against verified baselines.

manifold-cli

$ manifold run █

GET EARLY ACCESS LEARN MORE

Open source release coming soon

One harness for every major simulator

ISAAC LABMUJOCOMANISKILLGENESISSTARDUST

// evaluation today

- ✕A single eval rollout takes 24 hours or more
- ✕Every team reinvents the harness for every policy and every benchmark
- ✕No CI. Reproducibility is nearly impossible

01Every benchmarkLIBERO, RoboCasa, or your own scenarios

028× fastersharded across GPUs by default

03Track the SOTAcompare against verified baselines

04Find failurescluster episodes by failure mode

STARDUST

## Synthetic data for perception and autonomy

Define a scenario in Python, or just describe it to your coding agent (Claude Code, Codex, any LLM). Stardust renders the rest: diverse, labeled, photorealistic data with rich time-series metadata, no 3D expertise required.

scene.ipynb

```
import bbi world = bbi.World()world.spawn("container_ship", quantity=12)world.spawn("buoy", quantity=30, scatter=True) world.ocean(sea_state=4)world.weather(fog=0.3, time="dusk")cam = world.camera(preset="maritime_eo") imgs = world.render(frames=4000)imgs.download(annotations=["bbox", "segmentation"])
```

BOOK A DEMO READ THE DOCS

SENSORS & LABELS

### Multi-domain, photorealistic data matching your operational requirements

One scene, rendered across modalities in perfect registration, with ground-truth labels generated automatically for every frame.

RGB Photorealistic visible spectrum

IR Infrared and thermal bands

DEPTH Per-pixel depth and range

SEGMENTATION + BBOXES Pixel-perfect masks and 2D/3D boxes

NEURAL RENDERING

### Realism and diversity with AI post-processing

A learned post-processing pass closes the domain gap and multiplies diversity. One scene, every condition: weather, lighting, and time of day, all photorealistic, so models transfer cleanly to the real world.

CLEAR OVERCAST FOG DAWN DUSK RAIN

3D ASSETS

### A 1,000+ object 3D asset library, and counting

Drag and drop from over a thousand production-ready, physically-accurate 3D assets, each tagged with real-world dimensions. Need something rare? Generate new assets with AI on demand, or request a custom asset from our 3D team.

Container ship 213 × 43 × 52 m

Container ship (Maersk) 400 × 60 × 73 m

Cruise ship 366 × 69 × 78 m

Response boat 14 × 4.7 × 8.1 m

Kayak 5.5 × 2.1 × 0.5 m

Monitoring buoy 1.0 × 1.0 × 1.1 m

Special mark buoy 2.8 × 2.6 × 6.1 m

Cardinal mark buoy 1.3 × 1.3 × 3.0 m

Cessna 208 Caravan 13 × 16 × 4.6 m

Pilatus PC-12 14 × 16 × 4.2 m

Harbor crane 12 × 28 × 29 m

Shipping port 912 × 1979 × 82 m

URL: https://manifold.bifrost.ai/
Manifold · The evaluation platform for robotics researchers

Open source release coming soon

MANIFOLD

# The evaluation platform for robotics researchers

Run every major simulator benchmark in hours, not days. See exactly where your policy fails. Compare against verified baselines.

GET EARLY ACCESS

Free for research partners

manifold-cli

$ manifold run █

STEP 01

## Test on every benchmark that matters

Evaluate broadly without spending weeks wiring up each new simulator. One harness runs LIBERO, RoboCasa, and your own scenarios across every major simulator.

Pick a policy and a benchmark. No per-simulator harness to build.

STEP 02

## Get results in a fraction of the time

Benchmarks come sharded across GPUs by default. LIBERO runs 8x faster than a single-GPU baseline, so an overnight job becomes a lunch break.

LIBERO-90, 1,000 rollouts: single GPU vs sharded across 8.

STEP 03

## Track progress over time and against the SOTA

Compare your daily performance against verified results from every major model, across every major benchmark. See your rank move against every published baseline, run over run.

Verified baselines on shared benchmarks. Every run gets a citable manifold:// URI.

STEP 04

## Discover where your policy fails

Cluster failed episodes by failure mode to see the specific task families and subtasks that break your policy, not just an aggregate score.

Run detail from manifold.bifrost.ai: score, per-task pass rates, clustered failure modes.

Open source release coming soon

## The standards layer can't be proprietary

Manifold's runner, harness, and leaderboard schema will be open, so results compound across the field instead of staying locked inside a single lab. We're opening it up soon. Get on the waitlist and we'll bring you in early.

JOIN THE WAITLIST

## Focus on the scienceManifold runs the evals

SIGN UP FOR EARLY ACCESS

Free for research partners

URL: https://bifrost.ai/stardust
Stardust · Photorealistic, multi-modal synthetic data · Bifrost

STARDUST

# Photorealistic, multi-modal synthetic data, in minutes

Describe a scenario and Stardust renders it: diverse, labeled, photorealistic data with rich time-series metadata. Generate in minutes what a fleet collects in months.

BOOK A DEMO READ THE DOCS

scene.ipynb

```
import bbi world = bbi.World()world.spawn("container_ship", quantity=12)world.spawn("buoy", quantity=30, scatter=True) world.ocean(sea_state=4)world.weather(fog=0.3, time="dusk")cam = world.camera(preset="maritime_eo") imgs = world.render(frames=4000)imgs.download(annotations=["bbox", "segmentation"])
```

## Real data alone will not get you there

// real data today

- ✕Real data is slow and expensive to collect and label
- ✕The long tail is missing: rare, dangerous, and edge-case scenarios never make the dataset
- ✕Sensor coverage is fixed to whatever hardware you flew, so you cannot test what you did not capture

SENSORS & LABELS

## Multi-domain, photorealistic data matching your operational requirements

One scene, rendered across modalities in perfect registration, with ground-truth labels generated automatically for every frame.

RGBPhotorealistic visible spectrum

IRInfrared and thermal bands

DEPTHPer-pixel depth and range

SEGMENTATION + BBOXESPixel-perfect masks and 2D/3D boxes

MULTIMODAL SENSOR SUPPORT

## One scene, multiple sensors

Render the same world across modalities in perfect registration, so you train and test the whole fusion stack, not just the camera.

AVAILABLE RGB Photorealistic visible spectrum

AVAILABLE IR Infrared and thermal bands

AVAILABLE Depth Per-pixel depth and range

IN DEVELOPMENT Radar Range-Doppler returns and clutter

RERUN

## Explore a real maritime scene, frame by frame

Every Stardust scene exports to Rerun. Pan and zoom the 3D world, scrub the timeline, and toggle sensor streams in registration. Live, interactive, real Stardust output.

Interactive viewer · loads a live recording from Rerun

NEURAL RENDERING

## Realism and diversity with AI post-processing

A learned post-processing pass closes the domain gap and multiplies diversity. One scene, every condition: weather, lighting, and time of day, all photorealistic, so models transfer cleanly to the real world.

CLEAR OVERCAST FOG DAWN DUSK RAIN

3D ASSETS

## A 1,000+ object 3D asset library, and counting

Drag and drop from over a thousand production-ready, physically-accurate 3D assets, each tagged with real-world

URL: https://bifrost.ai/robotics
Robot policy evaluation and synthetic data | Bifrost

MANIFOLD + STARDUST

# Improve your robot policies, faster

Manifold runs any policy on any benchmark and ranks it on a shared leaderboard, so you see exactly what improved and what regressed, run over run. Stardust generates the photorealistic, multi-modal data that trains the perception underneath. One pipeline, from training data to reproducible evaluation.

BOOK A DEMO READ THE DOCS

Open source. 1,000 rollouts per run. Any simulator.

## Robots pass in the lab and fail in the field

A policy that clears 90% in the lab can still fail in the field, because real test sets are small, static, and impossible to stage at scale. You cannot evaluate against the long tail of objects, grasps, lighting, and clutter that actually breaks a policy.

Bifrost closes both ends of that loop. Train perception on Stardust synthetic data that covers the long tail, then evaluate the trained policy on Manifold across every benchmark, at thousands of rollouts, with failure analysis you can act on. Evaluation leads, because you cannot improve what you cannot measure.

## Evaluation is the bottleneck

// evaluating robots today

- ✕A single sim eval rollout still takes 24 hours or more, and every benchmark needs a hand-built harness
- ✕Every policy and every benchmark has a different shape, so every lab rebuilds the harness from scratch and the work never compounds
- ✕Reproducibility is informal: no shared leaderboard, no CI, no citable run
- ✕Real-world test sets are broken, and there is no systematic way to evaluate robots at scale

MANIF

## LinkedIn about

Bifrost recreates the real world in simulation. Our simulation infrastructure enable the world’s largest robotics companies to train and evaluate systems at the speed of software, from helping NASA explore Mars autonomously to automating dangerous industrial work. Bifrost is a series A backed by Sequoia Capital, Lux Capital, and Airbus Ventures.

## News (Exa, top 3)
- Nextgen Federal awarded US Air Force BIFROST Enterprise ... (2026-06-12) https://orangeslices.ai/nextgen-federal-awarded-us-air-force-bifrost-enterprise-environmental-portal-e2p-ai-ml-support-contract/
  Nextgen Federal awarded US Air Force BIFROST Enterprise Environmental Portal (E2P) AI/ML Support contract | OrangeSlices AI

Opportunities

Agency Intel

Department of Defense

- Defense Health Agency
- US Air Force
- US Army
- US Navy

Federal Citizen Services

Federal Health

- Centers for Medicare & Medicaid Services
- Department of Health & Human Services
- Defense Health Agency
- Department of Veterans Affairs

Federal Financial

- Treasury Department
- Securities and Exchange Commission

-
- bifrost ai (2026-06-26) https://bifrost.ai/
  # Bifrost AI (Bifrost AI, Inc.)

Bifrost AI is a Software Development company. Bifrost is a simulation company that helps teams deploy AI systems faster and more safely for robotics and autonomous AI development with simulation, world models, and synthetic data. Bifrost AI employs 20 people (+4.9% YoY, +2 people) and has an annual revenue of $3M, founded in 2020. Headquartered in San Francisco, United States, with presence in Singapore. Its workforce is distributed across Singapore, United State
- Bifrost helps industrials speed up model training with its 3D data-generation platform | TechCrunch (2024-10-30) https://techcrunch.com/2024/10/30/bifrost-ai-raises-8m-for-its-3d-and-ai-data-generation-platform/
  Bifrost helps industrials speed up model training with its 3D data-generation platform | TechCrunch

Image Credits:Ariya Sontrapornpol / Getty Images

AI

Copy Share Link

# Bifrost helps industrials speed up model training with its 3D data-generation platform

Kate Park

7:00 AM PDT · October 30, 2024

Copy Share Link

For many companies working on AI models with applications in the physical world, data presents the biggest opportunity. It’s also the biggest hurdle they face, as nicely labeled 

## Open roles (Blitz, live)
- Technical Lead ({'city': None, 'country_code': 'SG'})
- Member of Technical Staff ({'city': 'Singapore', 'country_code': 'SG'})
- Frontend Engineer ({'city': 'Singapore', 'country_code': 'SG'})
- Robotics Developer Relations (DevRel) ({'city': 'San Francisco Bay Area', 'country_code': 'US'})
- Robotics Research Intern ({'city': 'San Francisco Bay Area', 'country_code': 'US'})
- Growth Lead (Robotics & World Models) ({'city': 'San Francisco Bay Area', 'country_code': 'US'})
- Growth Lead (Robotics & World Models) ({'city': 'San Francisco Bay Area', 'country_code': 'US'})
- Account Executive - Physical AI ({'city': None, 'country_code': 'US'})
- Growth Lead (Robotics & World Models) ({'city': None, 'country_code': 'US'})
- Growth Lead (Robotics & World Models) ({'city': 'San Francisco Bay Area', 'country_code': 'US'})

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
