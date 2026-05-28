# Data Miner 🪏

**Describe your vertical. Get the best data sources for it — ranked.**

Data Miner is a self-contained Claude skill that helps you find the data sources that reveal **which
companies in your niche are in pain right now** (a trigger, a violation, an expiration, a gap), verifies the
data is actually there, and **scores every source on 7 criteria** — always pushing toward the *cheapest
high-quality* option.

It's built for GTM, sales, and research work where the bottleneck isn't "find a list of companies" — it's
"find the data that proves a specific company needs me this week, without overpaying for it."

## What it does

1. **Intake** — narrows you to one company type, the specific pain/trigger, geography, and the join key you
   need (domain, address, contact).
2. **Discovery** — sweeps 7 source categories (government, licensing boards, industry/accreditation bodies,
   maps data, open datasets, commercial APIs, data marketplaces).
3. **Verification** — actually opens each source and confirms the fields exist. No assuming.
4. **Scoring** — rates every source on **Quality, Scale, Price, Freshness, Accessibility, Granularity, and
   Pain-signal strength**, ranking cheap + high-quality first.
5. **Synthesis** — shows how to combine 2+ sources into a pain-qualified target list competitors can't
   cheaply copy.
6. **Report** — a ranked Data Source Report with a recommended 2–3 source build stack and the costs you can
   cut.

## How to use it

- In Claude Code: run `/data-miner`, or just say *"find data sources for [your vertical]"* and the skill
  auto-triggers.
- Anywhere else: paste `SKILL.md` into your assistant and describe your vertical.

## What you need

- **A web search tool.** [Exa MCP](https://exa.ai) is recommended (semantic search + page contents +
  `findSimilar`). Plain web search or Firecrawl also work.
- **Your own API keys**, set as environment variables (e.g. `EXA_API_KEY`). **This skill never contains or
  asks you to paste a key into a file.**

## Files

```
data-miner/
├── SKILL.md                       # the skill (start here)
├── README.md                      # this file
└── references/
    ├── scoring-rubric.md          # the 7 criteria + weights + a worked example
    ├── source-categories.md       # the 7 categories + public example sources + how to search
    └── synthesis-patterns.md      # 8 ways to combine sources into a copy-proof signal
```

## Principles (the short version)

- Hard data beats soft signals.
- Mine for pain, not firmographics.
- Verify, never assume.
- Cheap + high-quality wins.
- One source is a list; two sources is a moat.

---

*Built by Jordan Crawford · [blueprintgtm.com](https://blueprintgtm.com). Public and free to use.*
