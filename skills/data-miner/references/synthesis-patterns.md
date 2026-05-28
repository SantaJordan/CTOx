# Synthesis Patterns — turning sources into signals competitors can't copy

A single source is a list. Anyone can buy it. The defensible, high-converting targeting comes from
**combining 2+ sources in a non-obvious way** so that the *intersection* reveals a company in pain that
neither source shows alone.

Rule of thumb: **every recommended target list should combine at least two sources joined on a shared key**
(domain, legal name + address, license ID, or an entity ID you can map). If your output is a single-source
pull, you haven't finished.

Use these eight patterns. For each: what it is, the shape of the combination, and an example.

---

### 1. Cross-reference (presence in A ∩ B)
Match the same entity across two datasets so that being in *both* is the signal.
- **Shape:** `Source A (the population) × Source B (the qualifier)`, joined on a key.
- **Example:** licensed facilities (state board) × facilities with an open safety citation (regulator) =
  *licensed operators currently in trouble.*

### 2. Temporal correlation (A happened, B is now likely)
One dated event predicts a near-future need.
- **Shape:** `event in Source A at time T → expected pain at T + Δ`.
- **Example:** new license/registration filed last month → company in onboarding/setup pain *now.*

### 3. Velocity (rate of change as the signal)
The *speed* of a change matters more than the level.
- **Shape:** compare two snapshots of the same source over time; flag the fastest movers.
- **Example:** locations added per quarter (maps data, month over month) = who's scaling and feeling growth
  pain right now.

### 4. Absence as signal (in A but missing from B)
What a company *lacks* is the pain.
- **Shape:** `Source A (everyone) MINUS Source B (those who have the thing)`.
- **Example:** licensed contractors (board) NOT present in the certification registry = unaccredited
  operators, or operators missing a credential their peers have.

### 5. Threshold crossing (approaching a limit / deadline)
A value nearing a known cliff.
- **Shape:** filter Source A where `field` is within Δ of a regulatory/contractual threshold.
- **Example:** licenses/accreditations expiring in the next 90 days = a dated, time-boxed reason to call.

### 6. Geographic clustering (proximity / density)
Where entities sit relative to each other or to an event.
- **Shape:** join Source A to a location dataset; flag clusters or proximity to a trigger location.
- **Example:** facilities within N miles of a newly-opened competitor or a recent closure = local
  disruption pain.

### 7. Benchmark deviation (outlier vs peers)
A company that diverges from its cohort.
- **Shape:** compute a peer baseline from Source A; flag rows that deviate beyond a band.
- **Example:** ratings/violation counts far worse than same-category peers in the same region = a struggling
  operator, visible only once you've built the benchmark.

### 8. Lifecycle convergence (multiple clocks expiring together)
Several dated obligations landing in the same window.
- **Shape:** union of expiration/renewal dates across Sources A, B, C; flag overlaps.
- **Example:** license renewal *and* certification *and* a permit all due the same quarter = a company about
  to be very busy and very receptive to help.

---

## How to apply

1. From your scored sources, label each as a **trigger source** (carries pain) or a **join-key/enrichment
   source** (carries identity/coverage).
2. Pick a trigger source and a complementary source.
3. Choose the pattern above that fits the pain, and name the **join key** that connects them.
4. State the resulting segment as one sentence: *"[company type] where [Source A trigger] AND [Source B
   condition], joined on [key]."*
5. Sanity-check: could a competitor reproduce this exact combination cheaply? If yes, layer a third source
   or a less-obvious pattern until the answer is no.

> The output of synthesis is not "a bigger list." It's a **smaller, sharper list** of companies you can
> prove are in pain — built from cheap sources, hard for anyone else to copy.
