---
adr_id: ADR-004
type: technical-architecture
status: Accepted
date: 2026-05-12
author: Leandro Palazzo
related:
  - planning-artifacts/research/market-golden-path-architecture-cdp-positioning-research-2026-05-12.md
  - planning-artifacts/architecture.md (Pivot Notice + ADR-003 MC Custom Application Pivot)
  - planning-artifacts/prd.md (FR78–FR82, Tracking Layer & CDP Co-Exist section)
  - planning-artifacts/epics.md (Epic 5 + Epic 6 + Epic 8 narrative additions; Priority Sequencing P2.5 elevation)
  - planning-artifacts/decisions/adr-002-positioning-amplitude-statsig.md
---

# ADR-004: Tracking Layer Architecture — CDP Co-Exist Posture

**Status:** Accepted
**Date:** 2026-05-12
**Author:** Leandro Palazzo
**Type:** Technical Architecture (third inline/standalone architectural ADR; numbered after ADR-003 MC Custom Application Pivot)

---

## Context

On 2026-05-12, market research ([market-golden-path-architecture-cdp-positioning-research-2026-05-12.md](../research/market-golden-path-architecture-cdp-positioning-research-2026-05-12.md)) surfaced a structural fact previously absent from our worldview: **our ICP is overwhelmingly CDP-mature already.** The CDP Institute 2024 member survey reports 68 % of all respondents have a deployed CDP, rising to 81 % among firms with > $10 B revenue. Tealium's 2025 *State of the CDP* (n = 1,200) reinforces: CDP-equipped firms self-report a 14-point success delta over non-CDP peers.

Our prior architectural prose claimed a **"native intelligence loop — no ETL, no third-party handoffs, no data lag"** as the platform's primary moat. That claim survives only partially under Golden-Path scrutiny:

- The **typical commercetools enterprise customer** runs a Customer Data Platform (RudderStack, Twilio Segment, Snowplow, Adobe Real-Time CDP, Salesforce Data Cloud, Tealium, Hightouch, or equivalent) for legitimate architectural reasons: data ownership, PII transformation, identity resolution, ad-platform Event Match Quality, and frontend performance.
- commercetools' own Foundry documentation explicitly delegates customer mastering to "the CDP" when one exists — meaning our positioning either aligns with commercetools' architectural opinion or fights it.
- Forrester's *Identity Resolution Solutions Landscape Q4 2025* classifies CDPs as "martech table-stakes." Identity resolution carries ~20 % weighting on enterprise CDP RFPs (per Amperity / CDP.com frameworks).
- Twilio Segment AI (GA June 2025) and Snowplow Signals (GA May 2025) are actively encroaching on the AI-personalization / decisioning layer. The competitive position is **time-bounded** — a 12–24 month window before Class C dev-led CDPs may build storefront-decisioning surfaces of their own.

**The positioning posture is therefore not "replace the CDP" but "co-exist with the CDP at a different layer."** The platform is the *experience-and-decisioning* layer; the CDP is the *data-and-identity* layer. ADR-002 already established the vertical/horizontal positioning vs. Amplitude+Statsig+OpenAI; ADR-004 extends that frame to the broader CDP category by defining the technical architecture that makes co-existence operational.

---

## Decision

**The platform implements a deliberate co-exist architecture vs. the customer's Customer Data Platform — neither replacing it nor depending on it — with three distinct data paths, a scoped identity-resolution boundary, and out-of-scope decisions documented explicitly.**

The decision lands across PRD (FR78–FR82), epics (Epic 5 + Epic 6 + Epic 8 narratives), stories (Story 5.11, 5.12, 6.10, 8.19, 8.1 enhanced), and Priority Sequencing (Epic 8 elevated P3 → P2.5). This ADR is the durable record of the architectural reasoning behind those changes.

### The three data paths

| # | Data type | Source | Path | Owner |
|---|---|---|---|---|
| **1** | **Behavioral events** (clicks, scrolls, hovers, exposures, form abandonment, JS errors, performance metrics) | Storefront browser session | **Either** (a) platform-owned SDK → `/api/events` ingest → ClickHouse, **or** (b) customer's CDP (RudderStack / Segment / Snowplow) → CDP source-adapter `/api/cdp-events/{vendor}` → same ClickHouse pipeline | Platform receives; CDP may emit |
| **2** | **Commerce events** (orders, payments, customer lifecycle, catalog changes, inventory updates, pricing changes) | commercetools backend | commercetools Subscriptions → platform service → ClickHouse + Postgres | Platform reads directly from commercetools — **bypasses the CDP entirely** |
| **3** | **Experiment-outcome events** (variant ID, exposure count, conversion delta, statistical confidence, rollout state, Horizon-1 + Horizon-2 measurements) | Platform Experience Engine | Platform → customer-configured destination(s) (RudderStack / Segment / generic webhook) | Platform emits; CDP routes onward to customer's warehouse + ad platforms + BI |

### The identity-resolution boundary

| Identity scope | Who owns it | Mechanism |
|---|---|---|
| **Authenticated customer cross-session stitching** | **Platform (in scope)** | `Customer.externalId` → `HMAC-SHA256(externalId, TENANT_STITCH_SECRET)` → first-party `__aci_uid` cookie (Secure, HttpOnly, SameSite=Lax, 13-month expiry); Story 5.11 / FR78 |
| **Anonymous traffic stitching** (session-level only) | Platform | `session_id` only; events tagged `cohort: "anonymous"` |
| **Cross-device, cross-cookie identity-graph resolution** | **CDP (out of scope for platform)** | Delegated to customer's CDP partner; platform consumes the CDP's resolved identity if present (`userId` in CDP-emitted events → `user_hash`) |
| **PII transformation / hashing for ad-platform CAPI** | **CDP (out of scope for platform; documented playbook)** | Customer's CDP layer; platform ships integration recipes (Story 6.10 / FR81) but does not own EMQ scoring |

### The explicit out-of-scope decisions

The platform deliberately does **not** build:

1. **An identity graph for anonymous + cross-device traffic.** This is the CDP's structural value — building it ourselves would compete with the CDP layer and contradict the co-exist posture.
2. **Native EMQ scoring or Match Quality optimization.** Meta / Google / TikTok ad-platform Match Quality is a CDP-layer concern; the platform ships docs + reference implementations only (Story 6.10 / FR81 Phase 1) plus a Phase 2 native CAPI fallback for tenants without a CDP.
3. **A destination catalog for multi-tool fan-out.** The customer's CDP routes data to BigQuery, Snowflake, Meta CAPI, Google Ads, Slack, and 50+ other destinations. The platform does not replicate this.
4. **PII transformation, consent management, or GDPR/CCPA cookie banner replacement.** Consent management platforms (OneTrust, Cookiebot, Didomi) are well-established; the platform integrates with them via FR26 / Story 5.2 but does not replace them.

---

## Mechanism: how the architecture lands

### 1. Behavioral event ingestion — own SDK or CDP source-adapter (FR79 / Story 5.12)

The same ClickHouse `behavioral_events` table receives events from both paths:

```text
                  ┌───────────────────────────────────┐
                  │  ClickHouse `behavioral_events`   │
                  │  (tenant_id, session_id,          │
                  │   user_hash, event_type, source)  │
                  └─────────────────▲─────────────────┘
                                    │
            ┌───────────────────────┴───────────────────────┐
            │                                               │
   ┌────────┴─────────┐                          ┌──────────┴──────────┐
   │  Platform SDK    │                          │ CDP source-adapter  │
   │  (browser)       │                          │ (server-to-server)  │
   │  Story 5.1       │                          │ Story 5.12 (Phase 2)│
   │  source: "sdk"   │                          │ source: "cdp:{v}"   │
   └────────▲─────────┘                          └──────────▲──────────┘
            │                                               │
   ┌────────┴─────────┐                          ┌──────────┴──────────┐
   │ Live storefront  │                          │ Customer CDP        │
   │                  │                          │ (RudderStack /      │
   │ FR25 — async,    │                          │  Segment / Snowplow)│
   │ no LCP impact    │                          │ FR79 — Zod-validated │
   └──────────────────┘                          └─────────────────────┘
```

Both paths converge on the same Zod schema (`BehavioralEventSchema`) and the same ClickHouse column layout. Tenants choose their path at onboarding via the IT Admin dashboard; mixed-mode is supported (same tenant uses both during a CDP migration window).

### 2. Commerce event ingestion — commercetools Subscriptions direct (bypasses CDP)

Commerce events are read **directly from commercetools** via the Subscriptions API. The platform never relies on the CDP for commerce data because:

- **Schema fidelity.** commercetools Subscription payloads carry the full commerce context (account tier, contract pricing, approval workflow state, catalog segment, inventory state) that the CDP's flattened event model loses.
- **Freshness.** Direct Subscription delivery is lower-latency than CDP-routed commerce events.
- **Decoupling.** Commerce events flow even if the customer's CDP is misconfigured or under load; the platform's commerce-context decisioning remains operational.
- **Cost.** Routing commerce events through the CDP would charge against the customer's CDP MTU pricing.

```text
   ┌────────────────────┐    Subscriptions    ┌───────────────────────┐
   │ commercetools      │ ──────────────────▶ │  Platform commerce    │
   │ • Order            │  (real-time push,    │  service (Inngest)    │
   │ • Customer         │   <60s end-to-end)   │                       │
   │ • Cart             │                      │  → ClickHouse         │
   │ • Catalog          │                      │  → Postgres mirror    │
   │ • Pricing          │                      │  → ACI decisioning    │
   └────────────────────┘                      └───────────────────────┘
```

### 3. Experiment-outcome event emission — back to the customer's CDP (FR80 / Story 8.19)

Outcome events fan out to customer-configured destinations:

```text
   ┌─────────────────────┐                   ┌────────────────────────┐
   │ Experience Engine   │                   │ Customer's data infra  │
   │ (Epic 8)            │                   │                        │
   │                     │                   │  ┌──────────┐          │
   │ • Variant exposure  │ ────────────────▶ │  │ RudderStack│ ───┐   │
   │ • Horizon-1 result  │  outcome events   │  └──────────┘    │   │
   │ • Horizon-2 result  │                   │                  ├──▶ Warehouse + Ads + BI
   │ • Rollout gate      │                   │  ┌──────────┐    │   │
   │ • Rollback          │                   │  │ Segment  │ ───┤   │
   │ • Promote           │                   │  └──────────┘    │   │
   │                     │                   │                  │   │
   │ correlationId per   │                   │  ┌──────────┐    │   │
   │ event for idempotency│                  │  │ Webhook  │ ───┘   │
   │                     │                   │  └──────────┘          │
   └─────────────────────┘                   └────────────────────────┘
```

The platform owns the experiment surface and the tenant-intelligence model; the customer's CDP routes outcomes to their warehouse + ad platforms + BI. **No raw PII** crosses this boundary — outcome events carry HMAC-hashed `user_hash` per FR78, allowing the customer's CDP to join on its own identity graph without the platform exposing customer identifiers.

### 4. Identity resolution — split scope (FR78 / Story 5.11)

The platform builds **only** auth-customer cross-session stitching. Anonymous + cross-device + cross-cookie identity-graph resolution is delegated to the CDP partner. This is documented explicitly in customer-facing materials so non-CDP tenants understand which CLV signals are available to them:

| Cohort | Stitching | CLV measurement (FR55) |
|---|---|---|
| **Authenticated customer, single device** | Platform (`Customer.externalId` + first-party cookie) | ✅ Full Horizon 2 CLV |
| **Authenticated customer, multi-device** | Platform stitches sessions on devices the customer has authenticated on; cross-device pre-auth requires CDP | ✅ Full Horizon 2 CLV (post-auth) + 🟡 partial (pre-auth) |
| **Anonymous, single session** | `session_id` only; tagged `cohort: "anonymous"` | ❌ Not computed |
| **Anonymous, cross-session/cross-device** | **Out of scope — delegated to CDP** | ✅ Full Horizon 2 CLV (CDP-equipped tenants); ❌ Not computed (non-CDP tenants) |

### 5. EMQ-aware ad-platform integration (FR81 / Story 6.10)

Phase 1 (MVP) — documentation + reference implementations for hybrid Pixel + Conversions API integration with Meta, Google, TikTok via the customer's CDP layer. The platform does not own EMQ scoring.

Phase 2 — native CAPI emission for tenants without a CDP, gated on Consolidation-motion validation (per Golden Path market research). When shipped, the IT Admin dashboard exposes an "Ad Platform Integrations" surface with OAuth grants per platform; events flow directly from commercetools Subscriptions through the platform to the ad platforms' Conversions APIs.

### 6. Tenant Intelligence Score as moat-narrative surface (FR82 / Story 8.1 enhanced)

The five compounding signals — sessions collected, experiments completed, CLV cohort size, prediction accuracy, "tried and retired" library size — are surfaced in the MC nav rail with explicit "your data is compounding" framing. First-10-Experiments-Free (FR62) is reframed as a permanent moat-accumulation accelerator. **Tenant intelligence is the platform's primary long-term moat against CDP-vendor encroachment over the 12–24 month time-bounded window.**

---

## Consequences

### Expected positive outcomes

- ✅ **Aligned with the customer's existing architecture.** The 81 % of enterprise commercetools customers who already run a CDP are not asked to rip-and-replace; they get the experience-and-decisioning layer they don't have today.
- ✅ **commercetools-aligned posture.** commercetools Foundry documentation says "the CDP is the obvious place where customer records are mastered." We don't fight that opinion in our architecture.
- ✅ **Joint-pitch lane with Agentic Jumpstart SI partners.** The Accenture/Song, EPAM, Orium, Valtech channel that delivers Agentic Jumpstart can position us as the storefront-experience layer beneath the agentic surface (per market research recommendation) without forcing us to compete with commercetools' AI direction.
- ✅ **Smaller engineering scope vs. CDP-replacement.** We do not build identity graphs, destination catalogs, or PII pipelines — those are large bodies of work that compete with vendors who have years more infrastructure.
- ✅ **Clear out-of-scope language.** When customers ask "do you replace our CDP," we have a clear answer with rationale, not a hedged answer. RFPs are easier.
- ✅ **Tenant intelligence accumulation as primary moat.** Per ADR-002 + Golden Path research, the durable defensible position is the tenant-specific model — not the data path. This decision sharpens that focus.

### Risks accepted

- ⚠️ **Dependency on customer's CDP being correctly configured.** If a CDP-mature tenant misconfigures their CDP, our Experience Engine recommendations may be degraded. The customer perceives it as our product failing. Mitigation: Story 8.19's destination-status surface provides observable health; documentation explicitly frames the boundary; lighthouse-customer onboarding includes joint configuration.
- ⚠️ **Engineering surface bifurcation (own SDK + CDP source-adapters).** Maintaining the platform's own browser SDK alongside N CDP-destination adapters (RudderStack, Segment, Snowplow at minimum) is real maintenance overhead. Mitigation: ship-order is own-SDK first (Story 5.1, MVP) and CDP source-adapters in Phase 2 (Story 5.12); per-vendor adapters share a normalization layer; rate-limiting and Zod schema are unified across paths.
- ⚠️ **CDP vendors actively encroaching on decisioning layer.** Twilio Segment AI (June 2025) and Snowplow Signals (May 2025) ship predictive traits + intervention engines that overlap our Experience Engine. The 12–24 month time-bounded window matters. Mitigation: tenant-intelligence accumulation as primary moat (Epic 8 elevated to P2.5 priority); first-10-experiments-free as permanent moat-accelerator; speed-to-market on lighthouse customers.
- ⚠️ **Marketing language shift carries credibility cost.** Walking back "no third-party handoffs, no ETL, no data lag" from prior PRD/brief language requires stakeholder conversation. Mitigation: PRD and "What Makes This Special" already reframed (this commit); briefs and pitch deck updated in parallel; "the moat is the model, not the pipe" is a defensible reframing.
- ⚠️ **CLV measurement on anonymous traffic depends on CDP partner.** Tenants without a CDP get partial Horizon 2 CLV (auth cohort only). Mitigation: documented scope split; non-CDP tenants get a "connect a CDP for full anonymous-cohort CLV" CTA in the Tenant Intelligence Score panel.

### Unknowns to watch

- **commercetools' own AI direction.** Agentic Jumpstart (Nov 2025) targets agentic commerce, not storefront authoring (validated by 2026-05-12 research). If commercetools later extends Agentic Jumpstart "downward" into operator-facing storefront authoring, our positioning collides with their roadmap. Watch for any commercetools product launch in 2027 targeting storefront authoring or experience-layer AI.
- **CDP category consolidation.** Adobe + Salesforce + Tealium suite vendors vs. RudderStack + Snowplow + Hightouch dev-led tools — the CDP category is splintering. If a major M&A move consolidates further (Twilio Segment acquired by an analytics company, RudderStack acquired by a warehouse vendor), our co-exist surface area changes.
- **Ad-platform CAPI standardization.** Meta, Google, TikTok all have their own Conversions API implementations today. If a standard emerges (e.g., extending the IAB TCF / GPC framework to server-side events), Phase 2 native CAPI emission becomes simpler. Watch IAB / W3C activity.
- **Customer-interview validation of Consolidation motion.** The market research recommended n=15 customer interviews to validate the two sales motions (Integration default, Consolidation provisional). Until those interviews happen, the Consolidation-motion FR set (Story 6.10 Phase 2 native CAPI fallback) is best-guess.

---

## Rejected alternatives

### Alternative A — Build the CDP ourselves (replace RudderStack / Segment / Snowplow)

**Rejected.** Engineering scope explodes (full CDP + storefront + AI Site Builder + Experience Engine simultaneously). Forfeits commercetools' architectural endorsement of the CDP layer. Forrester calls CDP "martech table-stakes" — RFPs penalize platforms that ignore or replace it. 6 of 6 ICP segments either already have a CDP or expect one — replacement framing creates a rip-and-replace objection that doubles deal complexity. Class C dev-led CDPs (RudderStack, Snowplow) and Class D suite CDPs (Adobe RT-CDP, Salesforce Data Cloud) can out-execute us on data routing for years.

### Alternative B — Partner with one CDP exclusively (e.g., RudderStack-native commerce platform)

**Rejected as default; reserved as accelerator after Option B is established.** Forecloses ~75 % of our enterprise ICP (those running Segment, Adobe RT-CDP, Salesforce Data Cloud, Tealium, or in-house). Single-vendor dependency creates strategic risk if the partner is acquired or pivots (Twilio acquired Segment for $3.2 B; mParticle acquired by Rokt — M&A pressure on CDP vendors is real). Locks the developer-led segment but loses the analyst-leader segment. **Could revisit as a phase-2 GTM move with RudderStack or Hightouch after Option B has 2–3 lighthouse references.**

### Alternative C — Stay silent on the CDP layer in product architecture

**Rejected.** The Golden Path is the de-facto pattern for commercetools enterprise customers; ignoring it leaves customers to figure out the integration story themselves. Our product would feel architecturally incomplete; SI partners (Accenture, EPAM, Orium, Valtech) would need to write custom integration each time. Silence reads as either unawareness or weakness.

### Alternative D — Build a "CDP-lite" — selective destination support (3–5 destinations max) without claiming to be a CDP

**Rejected for now.** Fuzzy positioning; customers ask "is this a CDP or not" and we have to hedge. The clean co-exist line — "we are not a CDP; we are the experience-and-decisioning layer above one" — is sharper. CDP-lite could be revisited in a future ADR if customer behavior demands it.

---

## Monitoring / Revisit conditions

Revisit this ADR if any of the following occur:

1. **commercetools ships an operator-facing storefront authoring or experimentation product** (extends Agentic Jumpstart "downward" or launches a separate offering) — our positioning collides with their roadmap; our role may shift from primary ISV to commodity layer. **Highest-priority risk to track.**
2. **CDP vendor (Twilio Segment, RudderStack, Snowplow) ships a UI experimentation runner** that overlaps our Experience Engine surface — the 12–24 month window narrows; tenant-intelligence moat acceleration becomes more urgent.
3. **Adobe RT-CDP or Salesforce Data Cloud ships a commercetools-native connector** — they reach into our ICP via their existing customer relationships; co-exist motion needs sharper differentiation.
4. **Customer-interview validation of the Consolidation motion fails** (n=15 cohort indicates Legacy-Trapped Enterprise customers are not interested in tracking + storefront from one vendor) — collapse to single (Integration) sales motion; Story 6.10 Phase 2 native CAPI fallback may be deprioritized.
5. **Ad-platform CAPI standardization emerges** (cross-platform server-side event spec) — Phase 2 native CAPI fallback simplifies; reconsider whether the platform should own CAPI emission natively even for CDP-equipped tenants.
6. **commercetools acquires a CDP vendor** — would reframe our co-exist posture relative to commercetools' own data-layer ambitions; major repositioning required.
7. **A new CDP architecture pattern emerges** that supersedes the warehouse-first / suite-bundled split (e.g., a fully-decentralized event-bus pattern, or a return to first-party cookie-only tracking driven by privacy regulation) — our co-exist contract may need updating.

Scheduled revisit: **2026-11-12** (6 months), or sooner if any of the above occurs.

---

## References

- [Golden Path Architecture market research — 2026-05-12](../research/market-golden-path-architecture-cdp-positioning-research-2026-05-12.md) · the originating analysis
- [commercetools Foundry — Plan Integrations](https://docs.commercetools.com/foundry/blueprint/plan-integrations) · "the CDP is the obvious place where customer records are mastered"
- [Forrester Identity Resolution Solutions Landscape, Q4 2025](https://www.forrester.com/report/the-identity-resolution-solutions-landscape-q4-2025/RES190152) · CDP as martech table-stakes
- [Twilio Segment AI GA (June 2025)](https://www.twilio.com/en-us/changelog/2025/twilio-segment-ai-releases-general-availability) · CDP encroachment evidence
- [Snowplow Signals (May 2025)](https://snowplow.io/) · CDP encroachment evidence
- [CDP Institute 2024 Member Survey](https://www.cdpinstitute.org/news/customer-data-platform-growth-shifts-to-new-markets-cdp-institute-report/) · 81 % CDP adoption among > $10 B firms
- Planning artifacts:
  - [PRD](../prd.md) — FR78–FR82 (Tracking Layer & CDP Co-Exist section), Executive Summary + What Makes This Special updates
  - [epics.md](../epics.md) — Epic 5 + Epic 6 + Epic 8 narratives; Priority Sequencing P2.5 elevation
  - [stories.md](../stories.md) — Story 5.11, 5.12, 6.10, 8.19, 8.1 enhanced
  - [architecture.md](../architecture.md) — ADR-003 (MC Custom Application Pivot) + CDP Co-Exist Pattern data-flow section (added 2026-05-12)
  - [ADR-002](adr-002-positioning-amplitude-statsig.md) — Amplitude+Statsig vertical-vs-horizontal positioning (the strategic frame this ADR extends to the CDP category)
