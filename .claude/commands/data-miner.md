# Data Miner — find the best data sources for a vertical

Load and run the **Data Miner** skill at `skills/data-miner/SKILL.md`, plus its references in
`skills/data-miner/references/`.

## First: confirm you have a search tool

This skill mines the live web. You need a semantic web-search + page-contents capability.

- **Recommended:** Exa MCP (`mcp__exa__web_search_exa`, `findSimilar`, contents). Do a quick test (e.g.
  query "healthcare data registry", 1 result).
- If Exa isn't available, any web search + fetch tool works. If you have **no** search tool at all,
  **stop and tell the user what to enable** — do not invent sources or field names from memory.

## Then: run the skill

Follow `SKILL.md` end to end:

1. **Phase 0 — Intake.** Pin down ONE company type, the specific pain/trigger, geography, the customer's
   customer, what they already use, and the join key they need. Push back on vague answers; restate the
   brief in one sentence before searching.
2. **Phase 1 — Discover** across the 7 source categories (`references/source-categories.md`).
3. **Phase 2 — Verify** every candidate — open it, confirm the real fields and a join key. Discard or label
   anything unverified.
4. **Phase 3 — Score** each surviving source on the 7 criteria (`references/scoring-rubric.md`); rank
   cheap + high-quality first.
5. **Phase 4 — Synthesize** at least one 2-source combination (`references/synthesis-patterns.md`).
6. **Deliver** the ranked Data Source Report.

Be a ping-pong partner: this is done WITH the user. Lead with the *trigger*, not firmographics, and always
flag where a cheaper source matches an expensive one.
