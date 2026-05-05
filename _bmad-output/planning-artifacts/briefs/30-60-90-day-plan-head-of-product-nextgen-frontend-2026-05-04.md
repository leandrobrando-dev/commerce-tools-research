# 30-60-90 Day Plan: Head of Product – Next-Gen Frontend
**Leandro Palazzo | commercetools | Version 2.0 | 2026-05-05**

---

## Context & Intent

This is not a generic onboarding plan. The architecture is defined, the epics are sequenced, and 80 stories are written. The product direction is set. The job in the first 90 days is to translate that into: committed design partners, a validated MLP shipping to private beta, and a team that can execute the full 12-month roadmap without becoming a bottleneck.

The biggest risks are not technical. They are organizational: who has authority over scope, which SI partners become allies vs. threats, and whether the right accounts are in the room for design partner validation. Speed of trust-building is the rate-limiting variable.

The architecture is documented. What is unknown is the human terrain.

---

## Days 1–30: Orient, Validate, Recruit

### Objective

Achieve full internal alignment, complete competitive landscape mapping, recruit 3–5 committed design partners, and lock the MLP scope against Epic priority sequencing.

---

### Week 1: Internal Intelligence

**The goal this week is not to read documentation. It is to build a map of the humans, the politics, and the open decisions — using the documentation as the baseline.**

**Day 1: Full document review.**

Architecture is documented in `architecture.md`. Epics are sequenced in `epics.md`. All 80 stories are written in `stories.md`. Read all three on Day 1. The reading goal is not "understand what exists" — it is "understand what's been decided vs. what remains genuinely open."

**What IS decided (do not re-open):**
- Ships as MC Custom Application via commercetools Connect — lives inside the Merchant Center shell
- Auth: `mcAccessToken` HttpOnly cookie via ApplicationShell v27 — no new auth infrastructure
- Hosting: Vercel (Next.js App Router, RSC-first, ISR on-demand revalidation)
- Database: Neon (PostgreSQL 18.3, branch-per-PR, RLS multi-tenancy)
- Behavioral events: ClickHouse Cloud (100K events/sec, <500ms query latency)
- Async jobs: Inngest 4.2.6
- Real-time collaboration: Liveblocks 3.18
- AI completions: OpenRouter (anthropic/claude-3.5-sonnet)
- Feature flags: FlopFlip (built into ApplicationShell)
- RBAC: CASL 6.x wired to ApplicationShell oAuthScopes
- B2X context switching: URL `?ctx=b2c|b2b|dealer` + RSC re-render (ADR-001)
- AI quality threshold: ≥90%
- Primary button color: MC primary blue

**What is NOT yet decided (these are the real Week 1 questions):**
- SI partner program structure: which SIs, what commercial terms, what access model?
- Design partner selection criteria: who qualifies, what do we ask, what do they get?
- Attach rate targets: what does leadership consider a win at 12 months?
- AI Experience Engine pricing gates: who sets the consumption model and first 10 experiments free policy?
- Tenant Intelligence Score transparency: visible in free tier or only for AI Engine subscribers?
- Org reporting: does this team report to Product or Engineering, and what does that mean for headcount authority?

**Days 2–5 schedule:**

| Day | Activity |
|-----|----------|
| 2 | 1:1s with CTO and CPO. Goal: their personal definition of success, their biggest worry about this product, any landmines in the org. |
| 3 | 1:1s with Engineering lead(s). Understand current team capacity, existing commitments, and what Epic 1 (platform foundation) work is already in flight. |
| 4 | 1:1s with Sales and Solutions Engineering leadership. Map which enterprise accounts are already in conversation. Identify the 10–15 design partner candidates. |
| 5 | 1:1 with Marketing. Understand current messaging, any analyst briefings scheduled, and how the "Next-Gen Frontend" story is being told externally today. |

**Week 1 deliverable:** A written internal memo (shared with CPO and CTO) listing: (1) open decisions and proposed owners, (2) 10–15 design partner candidates with rationale, (3) any gaps between `epics.md` and `stories.md`, (4) the biggest organizational risk in the first 90 days.

---

### Week 2: Competitive Landscape + Design Partner Outreach

**Competitive landscape (self-directed, 2 days):**

Map the current state of: Contentful Studio, Builder.io, Uniform, Shogun, Makeswift, and Sanity (Presentation). The evaluation framework:

- Visual editing model: page-centric vs. component-centric vs. section-centric
- Commerce integration depth: product data binding, pricing, inventory
- B2B support: account catalogs, contract pricing, approval workflows
- Behavioral analytics: built-in, third-party, or absent
- AI capabilities: generation, optimization, or marketing only
- CT customer overlap: which of these do our target accounts already use?

Goal: identify (1) the two or three genuine differentiators the current architecture makes possible that competitors cannot easily replicate, and (2) the displacement narrative for each competitor a design partner is likely already using.

**Design partner outreach begins:**

From the Week 1 candidate list of 10–15 accounts, begin first outreach. The message: "We are defining the future of the Merchant Center frontend experience and want to build it with customers who have the most to gain. We are looking for 3–5 teams who will get early access, direct input into the roadmap, and a dedicated implementation path. The ask is 2–3 hours/month from a product or digital lead."

**Design partner selection criteria (to lock by end of Week 2):**
- Active commercetools customer on a current contract
- Has a storefront in production or in active build
- Has meaningful B2B complexity OR meaningful experimentation/personalization ambition
- Has internal technical capability to participate (not 100% dependent on SI for all decisions)
- Geographic and vertical diversity across the cohort (at least two verticals, at least two geos)
- Ideally: at least one account currently using ContentSquare or Amplitude (behavioral data displacement story)

**Week 2 deliverable:** Design partner candidate shortlist with rationale, outreach sent to all 10–15, competitive landscape first draft.

---

### Week 3: Discovery Calls + Internal Synthesis

**Discovery calls — structured 60-minute sessions:**

1. Their current storefront stack (10 min) — what they built, what they hate, what they wish existed
2. Their current experimentation/personalization setup (10 min) — what tools, who owns it, what's the activation rate
3. Their B2B complexity (10 min) — account structures, pricing models, approval workflows
4. Their biggest operational pain (10 min) — what takes too long, what requires a developer when it shouldn't
5. Their read on AI in commerce (10 min) — hype or real, what would they actually use
6. Pitch + ask (10 min) — share the vision, ask for the design partner commitment

**Key point to communicate in discovery calls:** Connecting their project to the platform starts accumulating behavioral intelligence immediately, before the AI Experience Engine is live. The Tenant Intelligence Score begins building from Day 1 of connection — before experiments are possible. This is a concrete reason to connect early.

**Internal synthesis:**

Write a structured synthesis:
- Where is there genuine alignment between CPO, CTO, and Sales on what this product is?
- Where is there hidden disagreement (especially on scope, pricing, and what "success" means at 12 months)?
- Which SI partners are already in conversation and what is their current posture — curious, threatened, or actively lobbying against?
- What is the current team's honest capacity assessment for Epic 1 work?

**Week 3 deliverable:** Discovery call notes synthesized into a "customer voice" brief (3–5 pages, shareable with Engineering and Design), internal alignment synthesis memo (leadership-only).

---

### Week 4: Design Partner Commitment + MLP Hypothesis

**Lock design partners:**

Target: 3 committed, 5 in conversation. "Committed" means: light design partner agreement signed (shared roadmap access, monthly calls, logo rights for case study, no pricing commitment required), and a named internal champion identified.

**MLP hypothesis — present to CPO and CTO:**

This is not a new architecture debate. It is a scope and sequencing conversation. The proposal:

**P0 (Months 1–3):**
- Epic 1: Platform foundation — MC Custom Application scaffold, ApplicationShell v27 auth, CASL RBAC, Neon multi-tenancy, CI/CD pipeline
- Epic 5: Behavioral data infrastructure — ClickHouse event ingestion, consent layer, event taxonomy, activated at project connection
- Epic 6-skeleton: SSO, SCIM, data residency basics

**P1 (Months 3–5):**
- Epic 2: Governed component library
- Epic 3: Storefront editor + publishing (StorefrontCanvas, ComponentSlot, ContextBar with B2X switching, PublishAction, Green/Red Zone governance)

**P2 (Months 5–7):**
- Epic 4: AI site builder + migrator (≥90% quality gate)

**P3 (Months 7–9):**
- Epic 8 MVP: AI Experience Engine

**P4 (Months 9–12):**
- Epic 8 full

**P5 (Months 12+):**
- Epic 6 full

**The moat story to communicate to leadership:** Behavioral Data Infrastructure ships at P0, not P2. ClickHouse event ingestion starts at project connection. Design partners who connect early will have the richest Tenant Intelligence Score data when AI experiments go live in P3. The moat starts on Day 1.

**Week 4 deliverable:** MLP proposal document, design partner roster (3 committed), alignment meeting with CPO/CTO to lock P0 scope.

---

## Days 31–60: MLP Definition, Team Assembly, Implementation Planning

### Objective

Lock the P0 MLP spec to story level, assemble the core team, establish sprint cadence, and get Epic 1 + Epic 5 groundwork in active development.

---

### Weeks 5–6: MLP Specification

The architecture is decided. What engineering planning in this phase IS about: implementation sequencing, component library depth, storefront template scope, and AI Experience Engine feature gating. Not architecture debates.

**Epic 1 — Platform Foundation (P0, Months 1–3):**

The scaffold. Everything else depends on it being clean.

- MC Custom Application registered in CT Connect marketplace
- ApplicationShell v27 integration, `mcAccessToken` HttpOnly cookie auth wired end-to-end
- CASL 6.x RBAC bound to ApplicationShell `oAuthScopes` — roles: IT Admin, Storefront Developer, Brand Publisher, Brand Editor, ACI Analyst, Cross-brand Admin
- Neon PostgreSQL: multi-tenant schema, row-level security, branch-per-PR workflow
- CI/CD: Vercel preview deployments on every PR, Neon branch provisioned automatically, destroyed on merge
- FlopFlip feature flags integrated — all new capabilities behind flags from Day 1
- Inngest 4.2.6 configured for async job processing

**Definition of done for Epic 1:** A design partner can connect their CT project, authenticate via ApplicationShell, and see their project data — with full audit logging and RBAC enforced.

**Epic 5 — Behavioral Data Infrastructure (P0, Months 1–3):**

This is not a nice-to-have. It is P0 because the AI Experience Engine has no intelligence without behavioral history. Every week of delay is a week of moat not being built.

- ClickHouse Cloud cluster provisioned and validated at 100K events/sec ingestion target with <500ms query latency
- Event taxonomy v1 defined (page views, component interactions, add-to-cart, checkout funnel, B2B-specific events — account switches, approval queue interactions)
- Client-side event SDK instrumented in the StorefrontCanvas
- Consent layer integrated (GDPR-compliant, opt-out surfaced in ContextBar, immediate stop on withdrawal)
- `user_hash` is HMAC-SHA256 of sessionId — never raw userId in ClickHouse
- Tenant Intelligence Score calculation defined, algorithm reviewed with design partners, first score visible to admins in the Custom Application
- **Hard target:** All design partners flowing events to ClickHouse within 14 days of project connection

**Epic 6-skeleton — Enterprise Compliance (P0, Months 1–3):**

- SSO: SAML 2.0 + OIDC, delegated to ApplicationShell where possible
- SCIM: user provisioning/deprovisioning
- Data residency: EU/US region selection at project creation
- PCI DSS boundary: ACI tracking scripts blocked from executing in checkout/payment flows

**Epic 2 — Governed Component Library (P1, Months 3–5):**

Key specification decision for Week 5: how many components ship in the initial library, and what does "governed" operationally mean?

- Green Zone: components editors can drag, drop, configure, and publish without developer involvement. Guardrails enforced by `executor.ts`.
- Red Zone: components requiring SI/developer involvement to modify (custom business logic, third-party integrations, checkout flows). Criteria must be objective (security risk, checkout integrity) — not commercial SI interest.
- **Critical:** Green/Red Zone criteria must be published in developer documentation before beta. Establish the governance standard before SIs can lobby to expand Red Zone boundaries.
- ComponentSlot contracts published to SI developer portal, backward-compatible, versioned.
- Component depth for P1: 20–30 production-ready Green Zone components covering hero, product grid, product detail, navigation, cart, and B2B-specific components (account selector, approval status).

**Epic 3 — Storefront Editor + Publishing (P1, Months 3–5):**

- StorefrontCanvas: drag-and-drop RSC canvas. RSC-first; client components only where interactivity is required.
- ComponentSlot: Green Zone mounting points, slot contracts enforced by executor.
- ContextBar: B2X/locale switcher — URL `?ctx=b2c|b2b|dealer` + RSC re-render (ADR-001). One click switches B2B/B2C/dealer view; canvas re-renders immediately; switching never discards unsaved draft changes.
- PublishAction: staged → live with full audit log, draft, review, approve, publish. Vercel ISR on-demand revalidation on publish.
- Green/Red Zone governance: `executor.ts` is the chokepoint. No component renders on canvas unless it passes zone validation.
- Liveblocks 3.18: real-time multi-user editing, presence indicators, conflict resolution on canvas.

**Behavioral analytics surface (inline with P1 — NOT the AI Experience Engine):**

The analytics surface in the editor makes behavioral data visible before AI experiments are live:

- Engagement score badges inline on canvas (component-level, updated from ClickHouse on canvas load)
- Session heatmaps overlaid on live canvas (hotspot visualization per component slot)
- Page-level performance metrics: bounce rate, scroll depth, conversion funnel drop-off

**NOT in MLP, NOT in P1:** AI Experience Engine experiments, ConfidenceCard recommendations, hypothesis generation, GitHub PR generation from AI. Those are P3 (Months 7–9). Setting this boundary explicitly prevents scope creep.

---

### Weeks 7–8: Team Assembly + Sprint Zero

**Team assembly — identify by Week 8:**

- 2 senior frontend engineers (RSC/Next.js App Router depth required — this is not a React SPA team)
- 1 backend/data engineer (Neon + ClickHouse ownership)
- 1 designer (product design, owns the canvas UX end-to-end)
- 1 solutions engineer embedded from SE org (design partner liaison, implementation support)

If headcount is not yet approved, this is the forcing function conversation with CPO. Make the trade-off explicit in writing: approve headcount or adjust Epic delivery timelines accordingly.

**Sprint zero — complete before first sprint starts:**

- GitHub repo structure agreed and documented
- PR template with Neon branch + Vercel preview requirements in place
- Feature flag naming convention established (FlopFlip)
- Event taxonomy v1 reviewed and signed off by at least two design partners
- Definition of Done agreed: RBAC validation, event instrumentation, Green/Red Zone annotation, accessibility baseline (WCAG 2.1 AA)
- Backlog groomed to at least 3 sprints ahead for Epic 1 stories
- Design partner communication cadence live (async channel + weekly sync)

**Weeks 7–8 deliverable:** Team staffed or hiring plan approved, Sprint Zero complete, Epic 1 development actively running, design partner communication cadence live.

---

## Days 61–90: Build, Validate, Prep Public Launch

### Objective

Epic 1 + 5 in private beta with design partners. First real behavioral data flowing to ClickHouse. Design partners experiencing the product, not just hearing about it. Public launch readiness assessed.

---

### Weeks 9–10: Private Beta Foundation

- Epic 1 complete: at least 2 design partners have connected their CT project, authenticated via ApplicationShell, and are operating inside the MC Custom Application
- Epic 5 live: ClickHouse receiving events from at least 2 design partners. Validate at event level — actual events from actual storefront interactions, not test data.
- Tenant Intelligence Score visible in admin UI for connected projects. Brief design partners on what the score means and what it will unlock when AI experiments go live in P3.
- **First behavioral data review with design partners:** Share the heatmap and engagement data they are already generating. This is the moment the product stops being a demo and becomes real.
- RBAC validated end-to-end: all six roles tested with real design partner team members in real roles.

---

### Weeks 11–12: Editor Preview + Green/Red Zone Governance

- StorefrontCanvas available to design partners in preview mode
- At least 1 design partner has used PublishAction to push a staged change to live
- Green/Red Zone documentation published to SI developer portal before SI partner briefings
- ComponentSlot contracts v1 published — at least 1 SI partner has reviewed and provided feedback
- ContextBar functioning: at least 1 design partner has used B2X context switching to preview a page in both B2B and B2C context
- Liveblocks multi-user editing tested with design partner teams (2+ simultaneous editors on one canvas)

---

### Weeks 13–16: Iteration + Public Launch Readiness Assessment

**Design partner iteration:**

- Monthly design partner review sessions in place (rotating lead: Leandro chairs Month 1, SE lead chairs Month 2+)
- Bug and friction backlog triaged and prioritized weekly — design partner feedback is the primary input to sprint planning in this phase
- At least 1 design partner has decommissioned or flagged for decommission a third-party analytics tool in favor of the behavioral data surface in the editor
- Tenant Intelligence Score: design partners targeting score 20+ within 60 days of project connection

**Public launch readiness criteria (assessed at Day 90, not necessarily met at Day 90):**

- Is Epic 1 stable enough for public beta? (Zero critical auth or RBAC bugs in 2-week window)
- Is Epic 5 ingesting reliably from all design partners? (No dropped events, consent layer validated)
- Is the SI developer documentation complete enough to onboard a net-new SI without white-glove support?
- Is the Green/Red Zone governance criteria clear and defensible?
- Is the AI Experience Engine pricing model agreed internally?
- Is the Tenant Intelligence Score transparency policy agreed?

Public beta announcement should not happen until all the above are green. Day 90 is the checkpoint, not the deadline.

---

## Success Metrics by Day 90

### Design Partner Metrics

| Metric | Target |
|--------|--------|
| Design partners committed (signed agreement, named champion) | 3 minimum, 5 in conversation |
| Design partners with CT project connected and Epic 1 live | 2 minimum |
| Design partners flowing events to ClickHouse | All connected partners, within 14 days of connection |
| Tenant Intelligence Score | ≥20 for connected design partners within 60 days of connection |
| Design partners who have used PublishAction in production | 1 minimum |
| Design partner who has flagged a third-party analytics tool for decommission | 1 minimum |

### Product Metrics

| Metric | Target |
|--------|--------|
| Epic 1 stability (auth + RBAC + multi-tenancy) | Zero critical bugs in 2-week window before public beta |
| Epic 5 event ingestion reliability | <0.1% dropped events, validated at ClickHouse |
| B2X context switching operational | ContextBar live, `?ctx=` switching validated with at least 1 design partner |
| Green/Red Zone documentation published | Complete, reviewed by at least 1 SI partner |
| ComponentSlot contracts v1 published | Yes |

### Organizational Metrics

| Metric | Target |
|--------|--------|
| MLP scope locked (written, signed by CPO + CTO) | Done by Day 28 |
| Core team assembled or hiring plan approved | Done by Day 45 |
| Sprint Zero complete | Done by Day 56 |
| SI partner program structure defined | Draft by Day 60, final by Day 75 |
| AI Experience Engine pricing model agreed | Agreement by Day 75 |
| Tenant Intelligence Score transparency policy | Agreed by Day 75 |

### Forward-Looking Targets (Set at Day 90, Measure Later)

| Metric | Target |
|--------|--------|
| AI-generated drafts publishable with minor edits (P2 launch gate) | ≥90% at P2 launch |
| First GitHub PR generated by AI Experience Engine | P3 milestone (Months 7–9) |
| ContentSquare/Amplitude displacement at design partner | At least 1 account by Month 6 |
| SI co-sells at 12 months | 3 minimum |
| Reference customers live at 12 months | 10 minimum |

---

## Key Decisions to Lock Before Day 1

| Decision | Stakes | Recommended Owner | Target Date |
|----------|--------|------------------|-------------|
| **MLP Scope Authority** — who has final call on what's in/out of P0 and P1? | If unclear, every stakeholder becomes a veto | CPO | Day 1 |
| **Design Partner Selection Criteria** — what qualifies an account, what do we ask of them, who approves? | Wrong design partners = validation theater. Right ones = real signal. | Leandro + Sales | Day 14 |
| **SI Partner Strategy** — which SIs get early access, what are commercial terms, what does "SI Developer" role get them? | SIs can be fastest distribution channel or biggest source of Green/Red Zone governance friction | CPO + CRO | Day 21 |
| **Org Reporting and Headcount Authority** — does this team have independent headcount or is it borrowing from existing roadmap teams? | Borrowed time is not a team — affects delivery dates for every Epic | CPO + CTO | Day 14 |
| **Marketing and GTM Ownership** — who owns the "Next-Gen Frontend" external story, analyst briefings, and launch messaging? | Product and Marketing need to operate from the same narrative | CPO + CMO | Day 21 |
| **AI Experience Engine Pricing Gates** — who sets the consumption model and the first 10 experiments free policy? | Affects design partner adoption of P3 and attach rate story at 12 months | CPO + Revenue | Day 45 |
| **Tenant Intelligence Score Transparency** — visible to customers in free tier or only AI Engine subscribers? | Determines product-led growth hook vs. premium upsell story | CPO + Leandro | Day 45 |

---

## Red Flags and Contingency Plans

### Red Flag 1: Scope Creep from Internal Stakeholders
**Signal:** Engineering planning conversations in Weeks 5–6 keep re-opening architecture decisions that are already documented in `architecture.md`.
**Response:** The architecture is decided. If a stakeholder is relitigating it, find out why — is it a legitimate new constraint, or change aversion? If the latter: surface it to CPO in writing. Do not let architecture debates absorb engineering time.

### Red Flag 2: No Design Partner Commitments by Day 30
**Signal:** Outreach to 10–15 accounts, no signed agreements by Day 30.
**Response:** Diagnose: are candidates saying "not the right time" (deal timing), "we don't see the fit" (positioning problem), or "we need to check with our SI" (SI is blocking)? Each requires a different response. If SI blocking is the pattern, escalate the SI partner strategy conversation immediately.

### Red Flag 3: Behavioral Event Ingestion Not Flowing Within 7 Days of Project Connection
**Signal:** ClickHouse is not receiving events from a connected design partner storefront within 7 days of project connection.
**Response:** This is an Epic 5 implementation issue, not a design partner problem. Escalate immediately — the Tenant Intelligence Score cannot accumulate without live event data. Every day of delay is a day of AI Experience Engine readiness lost. Assign a named engineering owner to unblock within 48 hours. Do not let this slip into the next sprint.

### Red Flag 4: Green/Red Zone Boundary Disputes with SI Partners
**Signal:** SI partners requesting that more components be labeled Red Zone in documentation, expanding the boundary beyond what is technically justified.
**Response:** This is governance being gamed for commercial reasons — Red Zone protects SI implementation revenue. The criteria for Red Zone must be based on objective security risk, not SI commercial interest. If boundary disputes emerge post-publication, treat them as product governance issues, not commercial negotiations.

### Red Flag 5: Core Team Not Assembled by Day 45
**Signal:** Headcount approvals not received or hiring pipeline empty at the 6-week mark.
**Response:** Leadership escalation, not a hiring process issue. Present the trade-off in writing: either approve headcount or adjust Epic delivery timelines accordingly. Do not absorb the slack by overcommitting a borrowed team.

### Red Flag 6: Design Partner Discovery Calls Reveal Misaligned Expectations
**Signal:** Design partners in Week 3 describe pain points that the current P0 scope does not address.
**Response:** Valuable signal, not a crisis. Document the gap explicitly. If multiple design partners surface the same misalignment, bring it to the Week 4 MLP proposal conversation. A scope adjustment at Day 28 is manageable. A scope adjustment at Day 90 is a crisis.

### Red Flag 7: ContextBar / B2X Context Switching Friction in Design Partner Testing
**Signal:** Design partners testing ContextBar find the `?ctx=` URL parameter approach disorienting or inconsistent with their existing storefront URL structure.
**Response:** ADR-001 resolved the technical approach. If UX friction emerges, this is a design problem, not an architecture re-open. Assign design sprint to ContextBar UX, validate with design partner, ship iteration.

---

## Communication Plan

**Internal (Every Friday):**
- All-hands product update (5 min): what shipped, what's next, one key learning
- Leadership sync: metrics, blockers, decisions needed

**Design Partners (Weekly):**
- Product call on Monday: what's coming, feedback loop
- Engineering office hours on Wednesday: questions, bug reports, feature requests
- Reference documents: `architecture.md`, `epics.md`, `stories.md` always available to design partners

**Sales & SI Partners (Bi-weekly):**
- Pipeline review: who's showing interest, what objections are surfacing
- SI partner check-in: how are they thinking about the product and the GitHub PR workflow?

**GTM & Marketing (Bi-weekly):**
- Go-to-market readiness check-in: launch materials, analyst interaction, comms timeline

---

## Contingency Plans

**If Design Partner Timeline Slips 1 Month:**
- Push public beta announcement to Week 20–21
- Use the extra time to refine based on extended beta feedback
- Do not skip the public launch — momentum matters

**If One Design Partner Churns Before Going Live:**
- Recruit a replacement from the next tier of prospects
- Reflect on why they left — scope mismatch, timeline, or product misfit?
- Incorporate learnings into the onboarding process for remaining partners

**If SI Partners Are Not Co-Selling Post-Launch:**
- Reframe: position the product as "customer self-service first" rather than "requires SI for implementation"
- Consider a 30% implementation revenue share for SIs who adopt it into their proposals
- Invest in SI enablement: component extension starter packages, training, certification program

---

## What Success Looks Like at Day 90

At Day 90, the test is not whether the plan was followed. It is whether these five things are true:

**1. The right design partners are in the room.**
Three accounts have signed design partner agreements. They have real B2B complexity or real experimentation ambition. At least two have their CT project connected and behavioral data flowing to ClickHouse.

**2. The product is real, not a demo.**
At least one design partner has used PublishAction to push a change to production. At least one has switched B2X context in ContextBar and seen their storefront respond. The Green Zone/Red Zone governance is documented and a real SI has reviewed it. The Tenant Intelligence Score is visible in the admin UI and accumulating real data.

**3. The team can execute without me being the bottleneck.**
The sprint cadence is self-sustaining. The Definition of Done is agreed and enforced. The design partner feedback loop is running. Engineering is two sprints ahead in backlog grooming.

**4. The organizational ambiguities are resolved.**
MLP scope authority is clear. Headcount is approved or the trade-off is documented. SI partner program structure is drafted. AI Experience Engine pricing model is agreed. Tenant Intelligence Score transparency policy is decided.

**5. The moat is being built.**
The behavioral data infrastructure is live. Design partners are generating Tenant Intelligence Score data that will make their AI Experience Engine experiments better than any competitor's at P3 launch. The moat is not the AI. The moat is the 9 months of behavioral history that makes the AI useful. That history starts accumulating now, or it doesn't accumulate at all.

If all five are true at Day 90, the next 90 days — P1 delivery, SI onboarding, and preparing for the AI Experience Engine MVP — are executable. If they are not, the right move is to say so clearly and adjust, not to accelerate into a foundation that isn't solid.

---

**Document Version:** 2.0 | Plan Date: 2026-05-05 | Start Date: [Hiring Date + onboarding buffer]

*Architecture is decided. The human terrain is not. Use this plan as your north star for the human and organizational work — the product decisions are already made.*
