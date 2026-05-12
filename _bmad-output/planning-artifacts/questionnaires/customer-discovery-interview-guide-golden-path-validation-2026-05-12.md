---
type: customer-discovery-interview-guide
counterparty: prospective commercetools enterprise customers (n=15 cohort)
date: 2026-05-12
author: John (Product Manager) — operationalizes Mary's market research recommendation (Phase 1 validation gate)
purpose: |
  Validate the two-sales-motion thesis surfaced by the 2026-05-12 Golden Path market research before GTM resources commit to either motion.
  Specifically:
  (1) test whether the Consolidation motion is real for Legacy-Trapped Enterprise (lead pitch: "replace fragmented stack");
  (2) test whether the Integration motion lands for CDP-mature segments (lead pitch: "experience-and-decisioning layer above your CDP");
  (3) surface unexpected pain points and buyer behaviors that the secondary research couldn't see.
related_artifacts:
  - _bmad-output/planning-artifacts/research/market-golden-path-architecture-cdp-positioning-research-2026-05-12.md
  - _bmad-output/planning-artifacts/decisions/adr-004-tracking-layer-architecture.md
  - _bmad-output/planning-artifacts/prd.md (FR78–FR82)
  - _bmad-output/planning-artifacts/briefs/elevator-pitch-commercetools-next-gen-frontend-2026-05-05.md (Section 0 — sales-motion guidance)
suggested_format: "45-minute virtual conversation per interviewee. Audio-recorded with consent for synthesis. NOT a sales pitch — a discovery conversation."
target_n: 15
target_cohort: |
  Five interviews per segment, three segments:
  - Legacy-Trapped Enterprise (consolidation thesis)
  - Digital-Native B2B Scale-up (integration thesis, dev-led tracking maturity)
  - AI-Forward Innovator (integration thesis, AI-native tracking maturity)
---

# Customer Discovery Interview Guide — Golden Path Validation (n=15)

## 0 · Pre-Interview Framing

### Why we're talking to these customers

The 2026-05-12 Golden Path market research surfaced a strategic recommendation that **the platform should co-exist with the customer's CDP rather than replace it**, because 81 % of >$10B-revenue commercetools customers already run one. Two sales motions emerge from that finding: an **Integration motion** for the 5 of 6 CDP-mature ICP segments (default, production-grade) and a **Consolidation motion** for Legacy-Trapped Enterprise (provisional, pending customer-interview validation).

This guide validates the second claim. **Without primary evidence, we cannot commit GTM resources to the Consolidation motion.** Five Legacy-Trapped interviews tell us whether the consolidation pitch wins deals or just sounds appealing. Five interviews each in the two CDP-mature segments tell us whether the Integration pitch is on-thesis — or whether we've misjudged what those buyers actually want from us.

### What "validated" means (decision criteria for synthesis)

| Motion | Validated if... | Falsified if... |
|---|---|---|
| **Consolidation (Legacy-Trapped)** | ≥ 3 of 5 interviews surface explicit pain around fragmented tracking AND would buy a "tracking + storefront in one platform" pitch over a CDP-first stack | ≤ 1 of 5 — the consolidation pitch is theoretical; collapse to single (Integration) sales motion and refine ICP. **Update the strategic synthesis accordingly.** |
| **Integration (Digital-Native + AI-Forward)** | ≥ 4 of 5 interviews per segment confirm: (a) they will not displace their CDP, (b) they will pay for a layer that reads commercetools commerce context their CDP can't, (c) they want experiment outcomes flowing back to their CDP | ≤ 2 of 5 per segment — the Integration motion is mis-pitched; surface what they actually want and re-frame |
| **Both motions** | The two-motion split holds: Legacy-Trapped responds to consolidation, CDP-mature responds to integration, and the responses don't overlap | The split blurs (e.g., CDP-mature also wants consolidation, or Legacy-Trapped also wants integration) — the segmentation is wrong; revisit ICP definitions |

### Conversation tone guidance

- **NOT a sales pitch.** Do not show product mockups. Do not name the platform. Do not pre-empt their answers.
- **Stay curious, ask "why," ask "tell me more about that."** Use the 5 Whys when you hit a surface answer.
- **Do not validate hypotheses by leading.** Let them say what they think; don't suggest answers.
- **Track tracking-maturity language.** Note whether they say "our analytics stack," "our CDP," "our data warehouse," "our experimentation tool" — vocabulary signals tracking architecture maturity.
- **Off-the-record framing welcome.** Use "We're doing some research on commercetools customer pain points" if they ask. Be honest if pressed about commercial intent: we're early-stage product research, not a sales call.
- **45 minutes hard cap.** Better to have a tight, focused conversation than a sprawling one.

### Pre-interview research per interviewee

Before every call:

1. **Confirm segment classification.** Look at their public stack signals (BuiltWith, Wappalyzer, job postings mentioning specific tools, conference talks, engineering blog). Validate they fit the segment you booked them in.
2. **Note any specific tools they're known to use.** If they're public RudderStack / Segment / Snowplow customers, you'll be testing the Integration thesis with concrete vendor specificity. If they have nothing visible (Legacy-Trapped signal), prepare to ask broader questions about how they handle tracking today.
3. **Note their commercetools tenure.** New CT customers (< 12 months) and mature ones (> 24 months) will give different answers. Adjust expectations.
4. **Note their commerce model.** B2C-only vs B2B-only vs B2X — affects what pain points surface.
5. **Have a 1-paragraph preamble ready** to introduce yourself, the research scope, and the consent ask for recording. Send it in advance via email/Slack.

---

## 1 · Common Opening (all 15 interviews — 7 minutes)

### Section purpose

Establish rapport, set the conversation contract, and capture baseline context. Same questions for all 15 — this is the control surface for cross-segment synthesis.

### Questions

1. **"Tell me about your role and what your team is responsible for in commerce."**
   - *Listening for:* role title, team size, what they actually own day-to-day vs what they're nominally accountable for.

2. **"Walk me through how a customer discovers your products today, from first touch to repeat purchase."**
   - *Listening for:* their actual customer-journey understanding, where they drop in technical detail vs. business detail, what they notice about the journey.

3. **"What's the single biggest commerce-stack frustration that's eating your time right now?"**
   - *Listening for:* unprompted mention of fragmented tools, tracking gaps, frontend velocity, AI/personalization, data silos. **Do not lead. Just listen.**

4. **"On a scale of 0 to 10, how confident are you that you understand what your customers do on your storefront before they buy?"**
   - *Listening for:* the score itself + the rationale. A score of 7 with "we have great tools but no one synthesizes the data" is different from a score of 4 with "we just don't have the instrumentation."

### What this tells us

- The **vocabulary they use unprompted** signals their tracking maturity (vocabulary is more revealing than the answers).
- **Where they mention CDP/tracking** unprompted vs. where you have to prompt them in Section 2.
- **Their pain-point ranking** — does fragmented tracking even make their top three? If not, that's a signal about the consolidation pitch's salience.

---

## 2 · Tracking Architecture Today (all 15 interviews — 10 minutes)

### Section purpose

Pin down their actual tracking architecture without leading. The answers here determine whether you stay on the Consolidation track (Section 3a) or shift to the Integration track (Section 3b) for the rest of the interview.

### Questions

5. **"Walk me through how data flows from a customer's browser to whatever team needs to see it. Take it slowly — start at the click, end at the dashboard or the team that uses the data."**
   - *Listening for:* SDK / pixel / CDP / warehouse / BI tool vocabulary. **Critical: let them describe it. Don't supply terms.**
   - *Follow-up if they say "GA4" or "Adobe Analytics" only and stop:* "What about behavioral data — clicks, scrolls, that level of detail?"
   - *Follow-up if they mention a CDP:* "How long has that been in place? What did it replace?"

6. **"Who owns this pipeline today — engineering, marketing ops, data, or somewhere else?"**
   - *Listening for:* the buying-committee shape (per Mary's market research: CDP buyer is joint CMO + CTO/CDO; DXP buyer is VP Digital + CTO).
   - *Critical: ask "and who do they report into?"* — surfaces the actual decision-maker.

7. **"If you wanted to add a new tool that needed to read your behavioral data, what would the conversation look like internally?"**
   - *Listening for:* whether the answer is "we'd plug it into our CDP as a destination" (Integration thesis confirmation) or "we'd evaluate replacing one of our existing tools" (Consolidation thesis confirmation) or "we'd build custom integration" (Legacy-Trapped signal).

8. **"What's the pain you have with your current tracking architecture? Anything where you've thought 'this should be different'?"**
   - *Listening for:* CDP-specific pain (cost, complexity, identity-resolution gaps), fragmented-tools pain (data silos, manual reconciliation), or no-tracking pain (operational blindness).
   - *Don't move on until you've heard a specific pain. Probe with "what's that look like in a typical week?" if they go vague.*

### Branching logic

After Section 2, classify the interview into one of three buckets:

| If they describe... | They are... | Continue with... |
|---|---|---|
| A CDP they actively run (RudderStack, Segment, Snowplow, Adobe RT-CDP, Salesforce Data Cloud, Tealium, etc.) AND clear pipeline ownership | **CDP-mature (Integration thesis)** | Section 3b — Integration motion validation |
| Multiple unintegrated analytics tools (ContentSquare, Amplitude, Optimizely, Hotjar, GA4 + others) and no CDP, with explicit pain about fragmentation | **Legacy-Trapped (Consolidation thesis)** | Section 3a — Consolidation motion validation |
| Mostly GA4 + no other behavioral analytics, or "we don't have much yet" | **Tracking-immature** | Section 3a — Consolidation motion validation, but flag the interview as edge-case (might not fit Legacy-Trapped Enterprise either; could be a different segment) |

**If they describe both a CDP AND fragmented tools** (e.g., "we have RudderStack but also still pay for ContentSquare and Optimizely directly"), this is a hybrid case — run **both** Section 3a and 3b but at half-depth each, and flag the interview as a useful counter-signal for the strict two-motion split.

---

## 3a · Consolidation Motion Validation — Legacy-Trapped (15 minutes — only for the right cohort)

### Section purpose

Test whether a "tracking + storefront in one platform" pitch wins them as a customer.

### Questions

9. **"If a single platform let you author your storefront, run your experiments, and capture behavioral data — bundled into your commercetools subscription — would that be interesting? Walk me through what would have to be true."**
   - *Listening for:* enthusiasm + specific conditions. "Yes if it integrates with [tool X]" is a softer signal than "yes if it consolidates and we drop [tool X]."
   - *Critical follow-up:* "What concerns or risks would you flag in that conversation internally?"

10. **"What's the typical procurement story for a tool like this in your org? Who has to say yes?"**
    - *Listening for:* buying committee shape. CFO/Procurement involvement = TCO-consolidation pitch lands. Marketing-only = it doesn't.

11. **"If you've ever evaluated a tool that promised to consolidate analytics + experimentation, what made it work or not work?"**
    - *Listening for:* prior exposure to tools like Optimizely Full Stack, Amplitude+Statsig, Adobe Experience Cloud. Whether they've lived through the "all-in-one" pitch before — and what soured them on it.

12. **"How do you think about the risk of betting on a single platform for tracking + storefront vs. keeping them separate?"**
    - *Listening for:* explicit single-vendor risk language vs. operational-simplicity preference. This is the heart of the Consolidation motion's viability — is single-vendor seen as risk or as simplification?

13. **"Imagine your team asks you 'should we replace [their main current analytics tool] with a single platform?' What's your honest answer?"**
    - *Listening for:* the visceral reaction. Hesitation = consolidation is theoretical even if appealing. Quick "yes" = consolidation is real for them.

### Listening signals

| Strong consolidation signal | Weak consolidation signal |
|---|---|
| Names specific dollar amounts they're paying across tools, unprompted | Talks about "we have some tools" without specifics |
| Mentions a recent failed integration project as evidence of fragmentation pain | Acknowledges fragmentation but is "fine for now" |
| Procurement-driven CFO involvement signals on Q10 | Marketing-only buyer signals |
| Explicit "we'd love to consolidate, we just haven't found the right tool" | "We'd consider it but it's not urgent" |

---

## 3b · Integration Motion Validation — CDP-Mature (15 minutes — only for the right cohort)

### Section purpose

Test whether the "experience-and-decisioning layer above your CDP" pitch lands.

### Questions

9. **"You mentioned [their CDP]. If a tool wanted to layer experimentation and AI-driven storefront experiences on top of your existing CDP — without touching the CDP itself — would that be interesting? Walk me through what would have to be true."**
   - *Listening for:* enthusiasm + specific integration concerns. "Yes if it sources events from [their CDP] and emits outcomes back" is the strongest validation signal.

10. **"What does your CDP NOT do well that you wish it did?"**
    - *Listening for:* gaps the platform's experience-and-decisioning layer can fill — particularly around storefront-side decisioning, experiment outcomes, commerce-context awareness, AI activation that goes beyond predictive scoring.
    - *Critical:* if they say "actually our CDP does all that," validate the answer with "tell me about a recent decision your CDP helped with" — concrete examples reveal whether the CDP really delivers what they claim.

11. **"How does your team currently run experiments at the storefront layer? What's that workflow look like?"**
    - *Listening for:* reliance on Optimizely / VWO / Statsig as separate tools, custom in-house experimentation, or absence of systematic experimentation.

12. **"Your CDP probably gives you predictive traits, audience scoring, recommendation traits — products like Twilio Segment AI or Snowplow Signals. How do you use those today, and what do you wish was different?"**
    - *Listening for:* awareness + actual usage. Many tenants pay for these features and don't use them. Knowing why is valuable: complexity, no clear surface, lack of governance, or "we don't trust the model."
    - *This is the encroachment-risk question.* If they're heavy users of CDP AI activation today, the platform's Experience Engine has to win against active competition. If they're skeptical, the platform's governance + commerce-context differentiation wins easier.

13. **"Imagine I told you a new commercetools-native tool reads your existing CDP's events as a source, runs storefront experiments using your governed component library, and emits experiment outcomes back to your CDP for downstream attribution. Would that get a yes from your CTO and your data team?"**
    - *Listening for:* concerns about double-instrumentation, schema compatibility, identity-resolution boundaries, who owns the outcome events. **These are the real integration concerns**; surface them.

14. **"What would have to be true for you to choose this over a CDP-vendor's own evolving experience-layer offering (e.g., Twilio Segment AI's recommendation traits)?"**
    - *Listening for:* commercetools-native specificity, governance, commerce-context, specific use cases their CDP can't address. Their answer is the moat sharpener.

### Listening signals

| Strong integration signal | Weak integration signal |
|---|---|
| Articulates specific gaps in their CDP that the platform fills | "Our CDP does what we need" without specifics |
| Mentions concrete pain with running experiments on the storefront layer | Says experiments are "fine" or "not a priority" |
| CTO + Data team buying-committee involvement on Q13 | Marketing-only buyer signals |
| Names CDP-vendor AI features they don't trust or don't use | Heavy reliance on CDP-vendor AI without complaint |

---

## 4 · Common Future-State Questions (all 15 interviews — 8 minutes)

### Section purpose

Surface decision criteria, pricing sensitivity, and timeline. These cut across both motions and inform how either pitch needs to be packaged commercially.

### Questions

15. **"If you were going to evaluate a new tool in this space in the next 12 months, what's the trigger? Why now versus next year?"**
    - *Listening for:* implicit timing — frontend EOL, contract renewal, AI mandate from leadership, board-level competitive pressure, etc.

16. **"What's your default procurement timeline for a tool like this? Walk me from first conversation to signed contract."**
    - *Listening for:* sales-cycle reality vs. our market research benchmarks (CDP enterprise: 90–180 days; commerce platform: longer post-signature implementation). Validate or refute the benchmark.

17. **"What single proof point — case study, pilot, demo — would move you from interested to advocating for purchase internally?"**
    - *Listening for:* the lighthouse customer profile they want to see (a peer brand? a similar commerce model? a published outcome?) — directly informs our case-study GTM strategy.

18. **"If this kind of platform existed today and you had to pitch it to your CFO, what would you say?"**
    - *Listening for:* their natural framing of the value. The phrases they use are the phrases that work in their org's vocabulary. **Steal them.**

---

## 5 · Wrap (all 15 interviews — 5 minutes)

### Questions

19. **"What didn't I ask that you think I should have?"**
    - *Listening for:* the unprompted insight that the interview missed. Often the most valuable answer of the conversation.

20. **"Who else in your network — at peer companies, not at your own — should I talk to?"**
    - *Use sparingly.* Only ask if the conversation went well; never pressure. Referrals are the highest-quality lead source for follow-up interviews.

21. **"Would you be willing to do a 30-minute follow-up if I have specific product mockups to test in 6–8 weeks?"**
    - *Listening for:* willingness signals continued engagement; reluctance signals the interview was net-negative.

### Closing line

> *"This conversation was incredibly valuable. I'll send you a personal note within 48 hours summarizing what I heard. If anything in our conversation triggered a thought you want to add later, my email is [yours]. Thank you."*

---

## 6 · Post-Interview Synthesis Template

Within 24 hours of every interview, capture the following in a per-interview note:

```yaml
---
interviewee: [name + role + company]
segment_classification: [Legacy-Trapped | Digital-Native B2B | AI-Forward Innovator | other]
date: YYYY-MM-DD
duration_min: 45
recording_url: [link to recording]
---

## Section 1 — Opening signals
- Pain points named unprompted: [...]
- Score on confidence-in-customer-understanding: X/10
- Vocabulary signals (CDP-mature / Legacy-Trapped / mixed): [...]

## Section 2 — Tracking architecture
- Current stack (verbatim): [...]
- Pipeline owner: [team + reports to whom]
- Most acute pain: [...]

## Section 3 — Motion validation
- Motion tested: [Consolidation | Integration | hybrid]
- Validation signal strength: [Strong | Medium | Weak | Counter-signal]
- Key quote: "..."
- Specific objections raised: [...]

## Section 4 — Future state
- Trigger that would prompt evaluation: [...]
- Procurement timeline: [N weeks]
- Lighthouse-customer profile they'd want to see: [...]
- Their CFO-pitch language (verbatim): "..."

## Section 5 — Wrap
- Question they think we missed: [...]
- Referrals provided: [N]
- Follow-up willing: [yes / no]

## Synthesis flags
- 🟢 Validating: [hypothesis it supports + how strongly]
- 🔴 Falsifying: [hypothesis it challenges + how strongly]
- 🟡 Surprising / off-script: [insight that didn't fit any hypothesis]
- ❓ Follow-up needed: [questions to come back to]
```

### Cohort-level synthesis (after all 15 interviews complete)

Consolidate per-interview notes into a single synthesis document covering:

1. **Decision-criteria roll-up.** Are the validation thresholds met? (≥3/5 Legacy-Trapped for Consolidation; ≥4/5 each for Integration in CDP-mature segments)
2. **Quoted pain points** by segment — the verbatim language to use in PRD updates and pitch materials.
3. **Surprising findings** that didn't fit the pre-interview hypotheses — flag for re-running the strategic synthesis.
4. **Buying-committee shape per segment** — validate or refute Mary's market research framework.
5. **Recommended GTM next steps** — which motion gets resources, which gets parked, what proof points the lighthouse-customer GTM needs.
6. **Updated decision log:**
   - Consolidation motion: validated / falsified / mixed
   - Integration motion: validated / falsified / mixed
   - Two-motion split: holds / blurs / new motion needed

The cohort synthesis is the single artifact handed back to the strategy/PM track for **decision lock** — feeds an update to ADR-004 (revisit conditions) and the strategic synthesis section of the Golden Path market research.

---

## 7 · Interview Logistics Checklist

### Recruiting

- [ ] **Source list compiled.** Outbound list of 30+ prospects per segment (assume 3:1 ask:scheduled ratio).
- [ ] **Outreach copy approved.** Email + LinkedIn templates, peer-introduction templates, no-sales-pitch language clearly framed.
- [ ] **Incentive structure decided.** None for peer-introductions; $100–$250 gift card (or charitable donation alternative) for cold prospects per segment-norm research.
- [ ] **Calendar scheduling tool ready.** Calendly link + 45-min default; buffers between calls.

### Conversation logistics

- [ ] **Recording consent template ready.** Inform of recording at the start of every call, get verbal yes before proceeding.
- [ ] **Transcription pipeline ready.** Auto-transcription tool (Otter, Fathom, or Riverside) configured.
- [ ] **Note-taking template prepped.** Per-interview note doc pre-created from the Section 6 YAML template.
- [ ] **5-Why probe practiced.** Have your follow-up phrases ready: "Tell me more about that." "What does that look like in practice?" "Why is that the case?" "What would change if that were different?"

### Synthesis logistics

- [ ] **Cohort tracking spreadsheet.** Per-interview row with classification, validation signal, key quote — sortable.
- [ ] **Decision-log doc ready.** Standing template for the post-cohort synthesis with Section 6's 6-point structure.
- [ ] **Strategic-synthesis update draft.** Pre-author the "what changes if Consolidation is falsified" / "what changes if Integration is mis-pitched" branches before the data lands — so synthesis is a quick decision rather than a weeks-long write-up.

### Schedule

- **Week 0 (this week):** Source list compiled, outreach launched.
- **Weeks 1–4:** 15 interviews completed. Schedule no more than 4 per week (Tue–Thu cluster) to leave time for per-interview synthesis.
- **Week 5:** Cohort synthesis written. Decision recommendations to leadership.
- **Week 6:** Strategic-synthesis updates landed in ADR-004 + research artifact + PRD if motion-set changes.

---

## 8 · What This Validates and What It Doesn't

### Validates

- ✅ Whether the two-motion split is real (Consolidation for Legacy-Trapped + Integration for CDP-mature)
- ✅ Whether the Consolidation pitch wins deals (or just sounds appealing)
- ✅ Whether the Integration pitch lands with CDP-mature buyers (or whether we've misjudged what they want)
- ✅ Buying-committee shape per segment (validates or refutes the secondary research)
- ✅ Procurement timeline benchmarks (90–180 days vs commerce-platform 6–12 months)
- ✅ Specific objections that need addressing in PRD/architecture/pitch

### Does NOT validate

- ❌ Pricing sensitivity to specific dollar amounts (different research method needed: pricing surveys, conjoint analysis, quote-stage feedback)
- ❌ Feature-level prioritization within Epic 5/6/8 (different research method: cardsort, RICE prioritization, beta feedback)
- ❌ International / non-English-speaking ICP (the n=15 will likely skew US/Western Europe; APAC and LATAM gap remains)
- ❌ Buyer behavior under direct competitive pitch (different research method: competitive-bake-off interviews after we have lighthouse customers)
- ❌ Long-term retention / expansion behavior (only post-customer behavior validates this — e.g., NPS surveys + churn analysis at 6/12-month milestones)

---

## 9 · Hand-Off

After cohort synthesis (Week 5), the deliverables for downstream artifact updates are:

| Deliverable | Owner | Format | Updates |
|---|---|---|---|
| **Cohort synthesis document** | John (PM) | New artifact in `_bmad-output/planning-artifacts/research/` | Verbatim quotes, segment-by-segment validation, recommended GTM next steps |
| **Updated ADR-004 monitoring/revisit** | John (PM) | Edit existing ADR | Revisit-condition #4 ("Customer-interview validation of the Consolidation motion fails") gets resolved one way or the other |
| **Strategic synthesis updates** | Mary (Analyst) — optional handoff | Edit Section 5 of `market-golden-path-architecture-cdp-positioning-research-2026-05-12.md` | If motion-set changes; otherwise note the validation outcome inline |
| **PRD / epic / story updates** | John (PM) | Edits to PRD, epics.md, stories.md if motion-set changes | E.g., if Consolidation falsified, Story 6.10 Phase 2 (native CAPI fallback) might be deprioritized or removed |
| **Updated elevator pitch + interview narrative** | John (PM) | Edits to briefs/ | Section 0 sales-motion guidance refined or simplified based on results |

---

*Prepared by John, Product Manager, 2026-05-12. This guide operationalizes the n=15 Phase-1 validation gate Mary recommended in the Golden Path market research. Run on time-bounded schedule (target completion Week 5) so the strategic decision-lock can happen before significant GTM resources commit.*
