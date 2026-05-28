---
name: who-do-i-want-to-be-when-i-grow-up
description: >-
  Walk any independent professional — consultant, fractional executive, agency
  owner, solo founder, advisor — from a fuzzy "I help everyone" identity to an
  ultra-specific niche AND a pain-sorted list of real prospects with
  decision-maker contacts and tailored openers. This is the full
  niche-discovery → testable-ICP → prospecting pipeline (the same one built for
  fractional CTO Carl Maloney in this repo). Trigger this skill whenever the
  user says "who do I want to be when I grow up", "who should I be when I grow
  up", "help me find my niche", "I don't know who my customer is", "who exactly
  should I sell to", "help me figure out my positioning / ICP", "who needs what
  I do right now", "build me a target list for my consulting/fractional/agency
  practice", or any variant where someone selling their own expertise needs to
  (a) figure out their edge and (b) find who's in the situation that needs it.
  Use it even when the person doesn't explicitly say "niche" — if they're an
  independent professional unsure of their positioning or who to prospect, this
  is the skill.
---

# Who Do I Want to Be When I Grow Up?

A guided journey from "I can help anyone" to a sharp niche and a list of real
people who need you *right now*, with openers written for them. It works for any
independent professional — consultant, fractional exec, agency, advisor, solo
founder — not just CTOs.

The spine of the method is one rule from Jordan Crawford's Blueprint GTM
methodology:

> **The message is a redescription of the targeting.** If your targeting is
> precise, the outreach writes itself.

So we spend most of the energy getting the targeting right. The message falls
out for free at the end.

## How to run this (the 6 steps)

1. **Soul interrogation** — Socratic grilling to find their edge → an
   ultra-specific niche (Industry × Situation × Unique Angle). *This is the
   heart of the skill. Don't rush it.*
2. **Collect grounding inputs** — their LinkedIn + any real sales/intro **call
   transcripts or notes**. The niche must be grounded in evidence, not vibes.
3. **Niche down → a testable ICP** — convert the niche into 3–4 *detectable*
   signals/axes with a 0–5 scoring rubric.
4. **Find the pool** — use the **`data-miner`** skill to discover the best data
   source(s) / TAM for their vertical.
5. **Research at scale** — clone **Blueprint-Swarm** as a sibling repo and use
   it (plus Exa + Blitz where available) through the Claude Code harness to
   score and enrich the candidate list.
6. **Deliver** — a pain-sorted target list + decision-maker contacts + a
   tailored opener per target.

The reference implementation of steps 3–6 already lives in this repo under
`prospecting/` (scripts) and `prospecting/research/` (the rubric axes). Point at
those rather than reinventing them. **Don't duplicate sibling skills — reference
them by name.**

---

## Step 1 — Soul interrogation (the heart)

Your job here is to be an aggressive-but-collaborative ping-pong partner. You
push HARD against generic answers, because a generic answer makes the rest of
the pipeline impossible — you cannot deploy messaging against a signal you can't
detect in data. Mirror the tone of the sibling `ctox-niche-discovery` skill
(read `../../../skills/ctox-niche-discovery.md` for the full triangulation
method and pushback ladders — it's CTO-flavored but the framework is universal).

Ask **one or two questions at a time**, wait for the answer, then push on the
weakest part of it. Never dump the whole question bank at once — this is a
conversation, not a form.

**The destination:** a single sentence they can complete —

> "I help **[SPECIFIC INDUSTRY]** who are **[SPECIFIC SITUATION / trigger]** by
> **[UNIQUE ANGLE most peers would argue with]**."

All three slots must be specific. Missing any one = too generic. (Ben Horowitz:
you may not be the world's best botanist, but you can be the world's best
*Japanese* botanist specializing in *Zen gardens*.)

### Question bank (pull from these, don't recite them)

**Who EXACTLY can you help?** (Industry)
- "What industry do you know better than 95% of your peers?"
- "If you walked into one conference and people assumed you were *the* expert in
  the room, which conference is it?"
- "Where would you be *embarrassed* not to have the answer?"
- Pushback: "'Healthcare' is too broad. Payers? Providers? EHR vendors?
  Telehealth? Which one could you write the textbook on?"
- Pushback: "'SaaS' is not an industry — it's a delivery model. What industry
  does that SaaS *serve*?"

**How do you help them — the mechanism?** (this becomes the Unique Angle)
- "What's the actual *thing* you do? Not the outcome — the mechanism."
- "When you watch a peer solve this problem, what makes you cringe?"
- "What do you know works that most people in your field would argue against?"
- Pushback: "'Best practices' aren't a mechanism — everyone claims them. What do
  you do that *isn't* the textbook answer?"
- Pushback: "If I searched for people who do [X], I'd get 10,000 results. What
  narrows it to 50?"

**When do they call you — the trigger?** (Situation)
- "What's happening in their business *at the exact moment* they pick up the
  phone?"
- "Is this *chronic* pain (always there, can be deferred forever) or *episodic*
  pain (sudden onset, deadline attached)?" — episodic is far better, because it
  has a trigger event you can *detect in public data*.
- Pushback: "'Growth' isn't a situation. When in their growth? What specifically
  *breaks*?"

**The embarrassment / edge test**
- "Where would you be embarrassed NOT to have the answer?"
- "Finish this: 'Most people in my field believe ___, but I've found ___.'"
- If their answer wouldn't make a knowledgeable peer say "actually, I disagree…"
  — it's not yet an edge. Keep pushing.

### Red flags — push back every time you hear them

| Red flag | Push back with |
|---|---|
| "I can help anyone." | "If everyone's your customer, no one is. Who do you help *10x* better than the rest?" |
| "I'm good at [generic competence]." | "That's table stakes. What's the take that makes a peer uncomfortable?" |
| "Modern best practices." | "What do you do that *isn't* best practice — and works anyway?" |
| "I work across industries." | "Which ONE do you know an order of magnitude better than the others?" |
| "Companies that need to scale." | "Scaling *what*, *when*? What's the specific thing that snaps?" |

**Success check:** the niche is ready when (a) you could name 100 companies that
fit the industry, (b) the situation has a *trigger event detectable in public
data*, (c) the angle would make some peers argue, and (d) the person is slightly
*uncomfortable* with how narrow it feels. If they're comfortable, it's not
narrow enough yet.

---

## Step 2 — Collect grounding inputs

A niche asserted from memory drifts toward flattery. Ground it in evidence.

Ask for:
1. **Their LinkedIn URL** (you'll read the About/Experience to confirm where
   they actually have depth — and to catch the gap between what they *say* they
   do and what their history *proves* they do).
2. **Recent sales / intro CALL transcripts or notes** — paste them, or give a
   file path. These are gold: the exact words a real prospect used to describe
   the pain *become* your detection keywords later. (In the Carl build, three
   evaluation-call transcripts defined the entire reference persona.)
3. **2–3 worked examples / past clients** — what was the trigger, what did you
   build/fix, what changed (ideally with a number).

Read these, then *re-run the weakest part of Step 1* against the evidence. If
the transcripts say the pain is "my team re-keys data between two systems by
hand," that phrase is now a targeting signal — note it. Jordan's rule: *"Did
your customer say this on a whim? Go find who else matches that pattern."*

---

## Step 3 — Niche down to a testable ICP (the rubric)

Now translate the niche into something a computer can *detect*. The pattern,
proven in `prospecting/research/`, is **3–4 scoring axes, each 0–5, each with a
keyword bank AND an explicit false-positives section.** Read
`../../../prospecting/research/axis1_key_integrations.md` (and `axis2_*`,
`axis3_*`) as worked templates before drafting theirs — they show the exact
shape: a signal→keyword mapping table, a 0–5 anchor ladder, and a
false-positives list.

Draft a rubric for **their** niche along these four lever types:

| Axis type | What it detects | Carl example | Your job |
|---|---|---|---|
| **Key situation** | The trigger — they're in the moment NOW | Missing a growth-unlocking integration to a system-of-record | Define the trigger from Step 1's Situation |
| **Complexity / fit** | Enough surface area that the work is real | Running multiple platforms that must talk | What makes a prospect *substantial* enough to need you |
| **Pain** | Hard evidence the problem is live | Staff manually re-keying data (a human as the API) | The smoking-gun signal — often visible in job posts |
| **Decision-maker gap (booster)** | They'd actually *hire out* for this | No full-time CTO to own the build | Who's missing such that they'd bring you in |

For each axis write: a 0–5 anchor ladder, a keyword/phrase bank (use the
prospect's *own words* from Step 2 transcripts), and a **false-positives**
section. The single most important guard, learned the hard way in the Carl
build: **demote anyone who IS the cure or who merely SELLS the cure.** (For
Carl, an iPaaS/ETL vendor lights up every integration keyword but is the worst
possible fit.) Always include that demotion rule, adapted to their niche.

Two scoring guards to bake into any rubric you hand off:
- **Word-boundary keyword matching**, never raw substring — `"api"` must not
  match "ther*api*st", `"edi"` must not match "m*edi*a". Use a regex like
  `(?<![a-z0-9])term(?![a-z0-9])`.
- **Score from cheap text first** (industry + description + specialties from the
  TAM CSV) before spending any API call. This collapses a huge corpus to a few
  hundred real candidates for free.

End this step with a written rubric (one markdown file per axis, mirroring
`prospecting/research/`) the user signs off on.

---

## Step 4 — Find the pool (use the `data-miner` skill)

You now know the *type* of company. Find where they live as data. **Invoke the
`data-miner` skill** (installed in this repo — run `/data-miner` or load
`../data-miner/SKILL.md`). It mines the live web across source categories,
verifies real fields + a join key on every candidate source, scores each source
on cost/quality, and returns a ranked Data Source Report. Lead with the
*trigger*, not firmographics.

Default starting TAM if their vertical is broadly "US software / SaaS": Eric
Nowoslawski's GrowthEngineX **`coldoutboundskills`** repo bundles a free
~173k-company US SaaS list (domain, LinkedIn, industry, headcount, funding band,
description) — clone it as a sibling and let the rubric do the qualifying rather
than paying for a list. For non-SaaS verticals, let `data-miner` find the right
registry/association/marketplace source.

---

## Step 5 — Research at scale with Blueprint-Swarm + the harness

Score the rubric across the pool and enrich the survivors. Split the work by
type, exactly as the reference pipeline does:

- **Deterministic, high-volume API work** (scoring, contact/email/phone lookup,
  team counts, job-post pulls) → **concurrent Python**, checkpointed to JSONL so
  reruns are cheap. See `../../../prospecting/scripts/` (`stage1_filter_score.py`,
  `phaseA_enrich.py`, `phaseB_jobs.py`, `phaseD_assemble.py`) as the reference
  implementation — adapt, don't rewrite from scratch.
- **Qualitative judgment** (pain narrative, keep/drop call, opener) → **agent
  fan-out**, ~15–20 companies per agent.

### Bring in Blueprint-Swarm

Blueprint-Swarm is Jordan's open agent-swarm for GTM customer intelligence
(understanding *why* customers buy/churn in their own words). Clone it as a
**sibling** directory and drive it from the Claude Code harness — reference it,
don't vendor it into this repo:

```bash
# from ~/Desktop/Claude Code/  (sibling to this repo)
git clone https://github.com/SantaJordan/Blueprint-Swarm.git
```

If that URL 404s, **stop and ask the user for the correct Blueprint-Swarm URL**
— do not guess. Follow Blueprint-Swarm's own README for setup; run its agents
through the harness over the candidate list to enrich each company with
voice-of-customer pain language, which feeds directly into the openers in Step 6.

### Search / enrichment engines

Use whatever is configured; the reference build used:
- **Exa** (semantic search) — confirm a company truly fits the trigger, pull
  recent news, find lookalikes from one URL.
- **Blitz** (people engine) — decision-makers, email + phone, team
  count/ratio, leadership-gap detection. (Note: Blitz holds people +
  firmographics only — *no* funding/stage data; get funding from the TAM CSV.)

**Two enrichment guards from the reference build, always apply:**
- **Email domain-match guard** — if a returned email's domain ≠ the company's
  domain, flag it (`email_domain_ok = no`); it's almost always the wrong person.
- **No silent drops** — log every company you skip (no jobs found, no contact,
  etc.) so the user can audit, never delete it quietly.

### Secrets — non-negotiable, this is a public repo

All API keys live ONLY in a **gitignored `.env`**, referenced **by name** in
code, never hardcoded and never printed. The repo's `.env` defines these names
(values are not shown anywhere): `BLITZ_API_KEY`, `EXA_API_KEY`,
`OPENWEB_NINJA_API_KEY`, `SERPER_API_KEY`, `FULLENRICH_API_KEY`,
`FULLENRICH_WORKSPACE_ID`, `APIFY_TOKEN`. Before any commit, grep the working
tree for key patterns and confirm `git check-ignore .env` passes. Any skill that
carries its own credentials (e.g. a publishing skill) is invoked **in place from
its global location — never copied into this repo.**

---

## Step 6 — Deliver

Produce three artifacts, mirroring `prospecting/output/`:

1. **Pain-sorted company list** — every kept company ranked by a composite
   **pain score** (the situation/complexity/pain axes + job signal, with the
   decision-maker-gap axis as a booster). Columns: rank, pain score, per-axis
   scores, the specific opportunity, the evidence (with URLs), firmographics,
   and whether a relevant leader is missing. Drop (and log) anyone with no real
   pain evidence.
2. **Decision-maker contact list** — company, person, role, title, email,
   `email_domain_ok`, phone, LinkedIn.
3. **A tailored opener per target** + a "why I believed" rationale. Write the
   opener as a **redescription of why the company scored** — that's the whole
   point of getting the targeting precise. Grade openers (Eric's
   `cold-email-copy-grader` works well) and revise low scorers before shipping.
   Optionally render an HTML playbook (publish it with existing publishing
   tooling invoked *in place* — keep its credentials out of this repo).

The output is an **engine, not a one-off list**: rerun it monthly and the pains
re-sort as companies post new jobs, raise rounds, and lose (or fail to hire)
their key leader.

---

## Pointers (read these as needed)

- `../../../skills/ctox-niche-discovery.md` — full niche-triangulation method +
  pushback ladders for Step 1.
- `../../../skills/ctox-insight-validator.md` — four-test insight quality check
  (counterintuitive / specific / quantifiable / demonstrable) for sharpening the
  Unique Angle.
- `../../../prospecting/research/axis{1,2,3}_*.md` — worked rubric templates for
  Step 3.
- `../../../prospecting/scripts/` — reference scoring + enrichment scripts for
  Steps 3 & 5.
- `../../../CASE_STUDY.md` — the full Carl Maloney narrative end to end.
- `../data-miner/SKILL.md` — source discovery for Step 4.

---

*Built on the Blueprint GTM methodology by Jordan Crawford —
[blueprintgtm.com](https://blueprintgtm.com).*
