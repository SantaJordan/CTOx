# Evidence pack: JuliaHub
slug: juliahub | domain: juliahub.com | HQ: Cambridge, Massachusetts US | employees(LI): 99 | founded: 2015 | stage_band: unknown
sources: vc:aei-horizonx
industry(LI): Software Development | specialties: modeling, technical computing, julia language, simulation, machine learning, high performance computing, artificial intelligence, cloud computing, julialang
channel notes: cloud platform for Julia scientific computing
own-language word count: ~1495

## Their own words (website via Exa, livecrawl-preferred)

URL: https://juliahub.com
# AI-powered engineering platform built for the age of Software-Defined Machines

Hardware Engineering at the Speed of Software

Explore Dyad ›

Explore JuliaHub ›

Products

## AI-Native Simulation, Modeling, and Computing

AI powered platforms that transform how engineers simulate, model, and deploy complex physical systems

### Dyad

Dyad Agent is an AI agent for physics-based modeling and simulation. Describe what you want to build - it derives equations, assembles models, runs simulations, and verifies correctness.

Explore Dyad ›

### JuliaHub

Cloud-native technical computing platform providing secure, scalable infrastructure for high-performance scientific computing and AI workloads

Explore JuliaHub ›

Real-World Results

## Transforming engineering workflows with measurable results

We accelerate innovation at the world's leading aerospace, pharmaceutical, and technology companies

View Case Studies ›

- 500x Instron optimized the design of its catapult 500x, speeding up its process from days to minutes, while reducing the BOM cost by 30% Instron Case Study ›
- 50% ASML saw a 50% reduction in development cycle time across 700+ engineers using JuliaHub for cross-functional collaboration ASML Keynote JuliaCon 2024 ›
- <2% Mitsubishi Electric (MERL) used novel state estimation techniques to achieve <2% error in predicting unmeasurable quantities such as refrigerant mass using Dyad MERL Case Study ›
- -3yrs Boeing built a guidance, navigation, and control system in 2 years instead of 5 years Boeing Keynote JuliaCon 2024 ›
- 15,000x NASA's RECURSAT mission planning was transformed into quick resolutions that ran 15,000x faster See NASA Video Demo ›
- 50x William Racing modeled a 50x more accurate prediction for its F1 car velocity and angle, with 4x faster execution, for better in-lap insights Williams Case Study ›

Open Source Foundation

## Built for Speed and Scale with Julia

Julia delivers 50x faster performance than Python, MATLAB, and R while maintaining ease of use—powering our AI-native platforms with unmatched speed and productivity

About Julia ›

Install Julia ›

100M+

Downloads

Install Julia ›

1M+

Users

Julia Community ›

13K+

Packages

Julia Packages ›

1,500+

Universities

Julia at Universities ›

Blog

## The latest from JuliaHub

Technical insights, customer stories, and industry developments that matter to engineering teams

View our blog ›

Read More Jul 21, 2026 • Company News JuliaHub at JuliaCon Global 2026

Jasmine Chokshi

Read More Jul 20, 2026 • Research & Innovation GPT-5.6 vs Claude Fable 5 for Physical AI, which performs best?

Dr. Chris Rackauckas

Anas Abdelrehim

Anshul Singhvi

Read More Jul 17, 2026 • Technical Tutorials Tradespace Exploration with the Dyad Agent

David Dinh

## Contact Sales

Learn about our products, pricing, implementation, and how JuliaHub can help your business

We’ll use your information to respond to your inquiry and, if applicable, classify your interest for relevant follow-up regarding our products. If you'd like to receive our newsletter and product updates, please check the box above. You can unsubscribe at any time. Learn more in our Privacy Policy.

### Get a Demo

Discover how Dyad, JuliaHub, and Pumas can improve your modeling and simulation workflows.

### Enterprise Support

Leverage our developers, engineers and data scientists to help you build new solutions.

### Custom Solutions

Have a complex setup that needs a custom solution? We are here to help.

The Dyad Dispatch July Edition Newsletter - View it Here

---

## Navigation

- Dyad
- JuliaHub
- JuliaHub in Pharma
- Pumas
- Julia
- Blog
- Events
- Videos
- Courses
- Case Studies
- Data Sheets
- White Papers
- Publications
- Documentation
- About
- Media
- Contact Us
- Careers
- LinkedIn
- YouTube
- X
- Terms of Service
- Privacy Policy
- EULA
- Trust and Security
- BLOG
- Contact Us ›
- Login ›

URL: https://juliahub.com/products/dyad
Dyad

# The first AI that thinks in physics

Dyad Agent is an AI agent for physics-based modeling and simulation - go from natural language to validated model faster than ever before

Dyad Pricing ›

Download Dyad ›

Read the docs ›

FrictionBrakeComponents

Can you help me model a component that provides a brake torque based on frictional characteristics and outputs the heat from braking to the disk and pad?

Searching

Search

1 query

Yes I'll create a formulation that captures the essential physics: friction converts mechanical power to heat, which is partitioned between disk and pad thermal masses, with convective cooling to ambient. The brake torque opposes rotation and depends on normal force, friction coefficient, and effective radius.

Reading, Read, 7 items, Reflecting, Reflect

Now I'll create the Dyad files with a test harness and analysis:

Writing, Write, 2 files, Creating, FrictionBrake.dyad, Created, FrictionBrake.dyad, Creating, SimplePowertrain.dyad, Created, SimplePowertrain.dyad, Compiling, Compile, 2 files, Ask Dyad Agent…, 2 Files Changed, src, FrictionBrake.dyad

```
# Friction brake component that converts mechanical power to heat# Provides brake torque based on normalized command and outputs heat to disk and padcomponent FrictionBrake  # Mechanical interface - rotational connection  shaft = Spline() [{"Dyad": {"placement": {"icon": {"x1": 950, "y1": 450, "x2": 1050, "y2": 550}}}}]  # Thermal interfaces - heat outputs (per wheel)  disk = Node() [{"Dyad": {"placement": {"icon": {"x1": 200, "y1": -50, "x2": 300, "y2": 50}}}}]  pad = Node() [{"Dyad": {"placement": {"icon": {"x1": 700, "y1": -50, "x2": 800, "y2": 50}}}}]  # Control input - normalized brake command (0 to 1)  brake_command = RealInput() [{"Dyad": {"placement": {"icon": {"x1": -50, "y1": 450, "x2": 50, "y2": 550}}}}]  # Geometric parameters  # Effective friction radius [m]  parameter R_effective::Length = 0.15  # Number of friction surfaces (1=single-sided, 2=double-sided)  parameter N_surfaces::Integer = 2  # Number of wheels with identical brakes  parameter N_wheels::Integer = 4  # Actuation parameter  # Maximum normal force per wheel [N]  parameter F_normal_max::Force = 5000  # Material properties  # Base coefficient of friction [-]  parameter μ_0::Real = 0.4  # Temperature coefficient of friction [1/K]  parameter α_T::Real = 0.0005  # Reference temperature [K]  parameter T_ref::Temperature = 293.15  # Heat partition parameter  # Heat partition fraction to disk [-]  par

URL: https://juliahub.com/products/juliahub
JuliaHub

# Cloud Platform for High-Performance Scientific Computing

Start Using JuliaHub ›

Request a Demo ›

A unified environment for technical computing, AI-powered simulation, and collaborative enterprise tools designed for Julia: the world's most performant language.

Julia Cloud IDE

## Managed Julia Dev Environment Made for Parallelism and Performance

Cloud-based Julia development environment with VSCode integration. Features interactive REPL, intelligent code completion, scalable computing resources, and access to 10,000+ scientific packages

Start for Free ›

Julia IDE Docs ›

Projects, Files, Datasets, Git, Cloud Hosted VS Code IDE, Compute, Packages, Permissions, Analytics

#### Coroutines

That allow suspending and resuming computations for I/O, event handling, producer-consumer processes, communicating via multiple channels, and scheduling tasks on several threads.

#### Composable Multi-threading

To schedule tasks simultaneously on more than one thread or CPU core with shared memory. Julia’s multi-threading is composable.

#### Distributed Computing

Runs multiple Julia processes with separate memory spaces. These can be on the same computer or multiple computers.

#### Julia GPU Compiler

Provides the ability to run Julia code natively on GPUs. There is a rich ecosystem of Julia packages that target GPUs on JuliaGPU.org.

Pluto.jl

## Advanced, Cloud-hosted Interactive Notebooks

Jump right into Pluto notebooks to explore data with Julia, share and work together with your team, and build interactivity with web components — all in the cloud.

Pluto.JL Docs ›

Pluto.JL Github ›

#### Reactivity

Pluto understands variable links between code cells, and will re-run a cell when a dependency changes, giving you a fast and fun way to experiment with your model.

#### Web Components

Pluto allows users to embed HTML, CSS and Javascript as well as share and render a notebook as a website. All available free on JuliaHub.

#### GUI Elements

Pluto lets you bind a Julia variable to a GUI element with common widgets like sliders, textfields and buttons. Combined with reactivity, this is a very powerful tool.

#### No Hidden State

Unlike Jupyter or MATLAB, there is no mutable workspace - the program state is completely described by the code you see. This eliminates hidden bugs and ensures reproducibility.

JuliaHub Transforms Workflows for Engineers

Packed with Developer Features

## Built for Team Productivity

Projects

### Enhance Team Collaborat

URL: https://juliahub.com/case-studies
Blog

Events

Videos

Courses

Case Studies

Data Sheets

White Papers

Publications

Documentation

# Case Studies

Read More Sep 4, 2025 • Energy Advancing the Goals of the ARPA-E’s DIFFERENTIATE Program with Julia

Read More Jul 9, 2024 • Industrials Improved HVAC Diagnostics

Read More Jan 2, 2024 • Industrials Instron: 500x Faster Design for Auto Crash Simulation

Read More Jan 2, 2024 • Technology Emergency Medical Supplies by Drone

Read More Jan 2, 2024 • Industrials Williams Racing Unlocks SciML Using Dyad

Read More Jan 2, 2024 • Energy Protecting the Electrical Grid with Fugro Roames

Read More Nov 6, 2023 • Pharmaceuticals Pfizer Accelerates Drug Development with Julia for 115x Gains

Read More Nov 6, 2023 • Pharmaceuticals United Therapeutics: Pharmaceutical Modeling with JuliaHub

Read More Nov 6, 2023 • Pharmaceuticals AstraZeneca Predicts Drug Toxicity with Julia & BNNs

Read More Jan 2, 2023 • Energy LAMPS Powers U

## LinkedIn about

JuliaHub’s mission is to empower those tackling the world’s toughest scientific and technical challenges with cutting-edge tools in a seamless, secure environment. JuliaHub combines advanced mathematical computing and machine learning expertise to enable scientific machine learning (SciML) techniques, Digital Twin modeling, and next-generation modeling and simulation in pharmaceutical, aerospace, automotive and other industrial verticals. Our product Dyad (formerly JuliaSim) is a leading solution for multi-physics modeling and simulation, combining traditional techniques with modern SciML appr

## News (Exa, top 3)
- Julia Computing Receives DARPA Award to Accelerate Electronics Simulation by 1,000x (2021-03-04) https://juliahub.com/blog/julia-computing-receives-darpa-award-to-accelerate-electronics-simulation-by-1000x
  Home

Blog

Julia Computing Receives DARPA Award to Accelerate Electronics Simulation by 1,000x

‹

›

Company News

# Julia Computing Receives DARPA Award to Accelerate Electronics Simulation by 1,000x

Date Published

Mar 4, 2021

Contributors

JuliaHub

Share

Cambridge, MA – Julia Computing has been awarded funding by the US Defense Advanced Research Projects Agency (DARPA) to accelerate simulation of Analog and Mixed-Signal circuit models using state of the art machine learning and artifici
- Julia Computing Receives DARPA Award to Build AI-Based Digital Phased Arrays with GPUs (2021-08-23) https://info.juliahub.com/blog/julia-computing-receives-darpa-award-to-build-ai-based-digital-phased-arrays-with-gpus
  Julia Computing Receives DARPA Award to Build AI-Based Digital Phased Arrays with GPUs
[The 2024 Julia User & Developer Survey is now open! Click here to participate.![](https://juliahub.com/assets/img/arrow-forward-black.svg)](https://form.jotform.com/241373057274355)
[Webinar: Modeling and Execution of Discrete-Time Controllers and State Machines in JuliaSim![](https://juliahub.com/assets/img/arrow-forward-black.svg)](https://juliahub.com/company/resources/discrete-time-controllers-and-state-m
- Government Modeling, Simulation & Scientific Computing () https://juliahub.com/offerings/government
  ---
title: Government - JuliaHub Customers
description: "Secure, high-performance computing platform for government R&D. JuliaHub Air provides air-gapped deployment, faster ATO approval, and mission-critical simulation capabilities. Trusted by NASA, DARPA, DOE, and US Air Force."
published: "Jun 10, 2026, 9:37 AM UTC"
---

Government

# Accelerating Government Research and Development

Julia’s high-performance capabilities, native parallelism, and GPU support allow agencies like NASA, US Air For

## Open roles (Blitz, live)
- Senior Lead - Modeling and Simulation (Dyad) (Remote) ({'city': 'Boston', 'country_code': 'US'})
- Senior Solutions Architect - Modeling and Simulation (Dyad) ({'city': 'Boston', 'country_code': 'US'})
- Compiler Engineer – Synchronous Programming (Dyad) ({'city': None, 'country_code': 'US'})
- Compiler Engineer – Synchronous Programming (Dyad) ({'city': 'Boston', 'country_code': 'US'})
- Senior Sales Account Executive - Pharma/ Biotech ({'city': 'Bengaluru', 'country_code': 'IN'})

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
