---
date: 2026-05-12
project: Tutorial (commerce-tools-research / NextGen Frontend)
focus: Epic 3 → Epic 4 progression — bootstrap zero-to-full-site with prefilled templates landing in Epic 3, shorten time to Epic 4
stepsCompleted:
  - step-01-document-discovery
  - step-02-prd-analysis
  - step-03-epic-coverage-validation
  - step-04-ux-alignment
  - step-05-epic-quality-review
  - step-06-final-assessment
filesIncluded:
  prd:
    - _bmad-output/planning-artifacts/prd.md
  architecture:
    - _bmad-output/planning-artifacts/architecture.md
    - _bmad-output/planning-artifacts/adr-002-positioning-amplitude-statsig.md
  epics:
    - _bmad-output/planning-artifacts/epics.md
  stories:
    - _bmad-output/planning-artifacts/stories.md
  ux:
    - _bmad-output/planning-artifacts/ux-design-specification.md
    - _bmad-output/planning-artifacts/epic-1-foundation-workspace-wireframes.html
    - _bmad-output/planning-artifacts/epic-2-component-library-wireframes.html
    - _bmad-output/planning-artifacts/epic-3-editor-wireframes.html
    - _bmad-output/planning-artifacts/epic-4-ai-builder-migrator-wireframes.html
    - _bmad-output/planning-artifacts/epic-5-behavioral-data-wireframes.html
    - _bmad-output/planning-artifacts/epic-6-enterprise-admin-wireframes.html
    - _bmad-output/planning-artifacts/epic-8-experience-engine-wireframes.html
    - _bmad-output/planning-artifacts/epic-9-retail-pos-wireframes.html
  supplemental:
    - _bmad-output/planning-artifacts/briefs/product-brief-commercetools-next-gen-frontend-aci-2026-05-04.md
    - _bmad-output/planning-artifacts/competitive-analysis-site-builders-behavioral-analytics-ab-testing-2026-05-11.md
    - _bmad-output/planning-artifacts/implementation-readiness-report-2026-05-05.md
notes:
  - .md files treated as canonical; .html files are rendered twins (confirmed by user)
  - Epic 7 was merged into Epic 4 (confirmed by user) — Epic 4 scope is therefore expected to be heavier than original
---

# Implementation Readiness Assessment Report

**Date:** 2026-05-12
**Project:** Tutorial (commerce-tools-research / NextGen Frontend)
**Focus:** Epic 3 → Epic 4 progression — bootstrap zero-to-full-site with prefilled templates landing in Epic 3, shorten time to Epic 4

## Step 1 — Document Discovery

### Inventory

**PRD:** `prd.md` (canonical)

**Architecture:** `architecture.md` (canonical), `adr-002-positioning-amplitude-statsig.md` (ADR)

**Epics & Stories:** `epics.md`, `stories.md` (canonical)

**UX:** `ux-design-specification.md` (canonical), per-epic wireframes for epics 1, 2, 3, 4, 5, 6, 8, 9

**Supplemental:** product brief, competitive analysis (2026-05-11), prior readiness report (2026-05-05)

### Resolutions

- `.md` confirmed canonical; `.html` are rendered twins — no duplicate conflict
- Epic 7 merged into Epic 4 — accounts for the missing `epic-7-*-wireframes.html`. Epic 4 scope is expected to carry the additional weight; this will be a key area of scrutiny for the Epic 3 → Epic 4 progression

---

## Step 2 — PRD Analysis

### Functional Requirements (51 total)

**Storefront Authoring (FR1–FR6)**
- **FR1:** Operators view/navigate live storefront structure in a visual canvas editor
- **FR2:** Operators add/remove/reorder Green Zone components on the canvas
- **FR3:** Operators edit content properties (copy, images, colors, layout variants) within Green Zone constraints
- **FR4:** Operators preview storefront in desktop, tablet, mobile viewports before publish
- **FR5:** Operators preview storefront in B2C, B2B, dealer portal contexts before publish
- **FR6:** Operators access the editor from a mobile device

**AI-Assisted Creation (FR7–FR12)**
- **FR7:** Operators describe a storefront intent in natural language and receive a governed AI-generated draft
- **FR8:** AI drafts compose exclusively from the tenant's approved Green Zone component library
- **FR9:** Operators view AI reasoning and component selection intent before draft application
- **FR10:** Operators accept, modify, or reject individual AI component placements
- **FR11:** Operators manually edit/replace any AI-generated component within Green Zone constraints
- **FR12:** Real-time streaming progress feedback during AI draft generation

**Governance & Publishing (FR13–FR20)**
- **FR13:** Developers designate components as Green Zone (operator-editable) or Red Zone (platform-protected)
- **FR14:** Developers configure which component properties are operator-editable per Green Zone component
- **FR15:** Platform enforces Red Zone — operator/AI cannot modify Red Zone components or commerce logic
- **FR16:** Operators publish to staging for review
- **FR17:** Brand Publishers publish staged storefronts to live production
- **FR18:** Platform validates governance compliance before publish; blocked publishes surface specific violations
- **FR19:** Platform deploys atomically — no partial state visible to live traffic
- **FR20:** All publish actions recorded with author, timestamp, content diff in immutable audit log

**Autonomous Commerce Intelligence — ACI Phase 1 (FR21–FR28)**
- **FR21:** ACI Analysts/Operators view session behavioral heatmaps overlaid on the live storefront canvas
- **FR22:** Platform calculates and displays engagement scores per storefront section
- **FR23:** ACI Analysts flag low-performing sections and notify Operators
- **FR24:** Operators navigate from an ACI flag to the relevant component in the editor
- **FR25:** Behavioral events collected asynchronously without impacting render performance
- **FR26:** Behavioral data withheld until end-consumer cookie consent; collection stops on withdrawal
- **FR27:** ACI Analysts view page-level performance metrics (load time, scroll depth, exit rate)
- **FR28:** IT Admins configure ACI behavioral data retention period (default 13 months rolling)

**Developer & Component Management (FR29–FR33)**
- **FR29:** Developers create/configure/publish a governed component library via Developer Console
- **FR30:** Developers define field-level edit permissions for each Green Zone component
- **FR31:** Developers simulate operator access in the Console to verify governance enforcement
- **FR32:** Developers update component library definitions without full platform redeployment
- **FR33:** Platform restricts AI draft generation to components in the tenant's published library

**Migration & Onboarding (FR34–FR39)**
- **FR34:** Developers connect an existing commercetools project via API credentials
- **FR35:** Platform proposes a Green Zone component mapping scaffolded from existing template/codebase structure
- **FR36:** Developers review/adjust/publish the scaffolded component mapping
- **FR37:** Platform migrates existing page configurations to the storefront canvas format
- **FR38:** Platform measures and reports Core Web Vitals baseline for an existing storefront pre-migration
- **FR39:** Platform validates migrated pages for completeness; renders a readiness report before go-live

**Platform & Administration (FR40–FR46)**
- **FR40:** IT Admins configure tenant SSO via SAML 2.0 or OIDC
- **FR41:** IT Admins automate user provisioning/deprovisioning via SCIM 2.0
- **FR42:** IT Admins assign platform roles (IT Admin, Developer, Brand Publisher, Brand Editor, ACI Analyst, Cross-brand Admin)
- **FR43:** IT Admins configure per-brand access boundaries for multi-brand tenants
- **FR44:** IT Admins select EU or US data residency at tenant provisioning
- **FR45:** IT Admins generate and download a Data Processing Agreement within the platform
- **FR46:** IT Admins view a usage dashboard (sessions, AI generations, storefronts) vs. tier limits

**Compliance & Data Privacy (FR47–FR51)**
- **FR47:** End consumers withdraw behavioral consent → platform immediately stops ACI collection for that session
- **FR48:** IT Admins submit right-to-erasure for a consumer's behavioral data; fulfilled within 30 days
- **FR49:** Platform enforces PCI DSS boundary — ACI scripts blocked in checkout and payment capture flows
- **FR50:** All platform-provided Green Zone components meet WCAG 2.1 AA by default
- **FR51:** Platform surfaces accessibility warnings when operator edits may violate WCAG 2.1 AA prior to publish

**Total FRs: 51**

### Non-Functional Requirements (23 total)

**Performance (NFR1–NFR6)**
- **NFR1:** Editor actions visible response within 500 ms
- **NFR2:** AI draft generation completes within 30 s end-to-end; streaming progress after 2 s
- **NFR3:** Publish (governance + deploy) within 15 s for storefronts ≤500 KB
- **NFR4:** Storefront LCP <2.5 s mobile, <1.5 s desktop; CLS <0.1; INP <200 ms (CWV pass)
- **NFR5:** ACI heatmap overlay loads within 3 s after canvas section navigation
- **NFR6:** commercetools API sync (catalog, pricing, inventory) propagates to live storefronts within 60 s

**Security (NFR7–NFR14)**
- **NFR7:** TLS 1.3+ in transit
- **NFR8:** AES-256 at rest
- **NFR9:** Red Zone enforcement at platform layer — cannot be bypassed by API tampering, payload manipulation
- **NFR10:** ACI scripts blocked in checkout/payment via CSP scope audit + runtime enforcement
- **NFR11:** Multi-tenant isolation enforced at ORM layer; cross-tenant queries impossible even with compromised credentials
- **NFR12:** Immutable audit log for all platform actions (login, publish, component update, data access)
- **NFR13:** Secrets via platform vault; no plaintext storage/logging
- **NFR14:** External integrations validate TLS certs; reject self-signed/expired

**Scalability (NFR15–NFR20)**
- **NFR15:** 10× concurrent operator sessions with <10 % perf degradation
- **NFR16:** ACI ingestion 100 K events/s with <500 ms latency
- **NFR17:** Horizontal scaling — linear throughput up to 1 M concurrent storefront sessions
- **NFR18:** Per-tenant API budget; circuit breaker at 10 K calls/min
- **NFR19:** Pooled DB connections; auto-scale within per-tenant limits (e.g., 100/Enterprise)
- **NFR20:** CDN edge handles geographic distribution; origin fallback only on CDN failure

**Accessibility (NFR21–NFR23)**
- **NFR21:** Editor meets WCAG 2.1 AA (keyboard, screen reader, contrast 4.5:1 text / 3:1 UI)
- **NFR22:** All platform-provided Green Zone components meet WCAG 2.1 AA by default
- **NFR23:** Publish validation warns on accessibility violations before confirmation

**Total NFRs: 23**

### Additional Requirements / Constraints

**Compliance:** GDPR (data processor model, DPA, right-to-erasure, 13-mo retention default, EU residency); ePrivacy/Cookie Consent (CMP integration via IAB TCF 2.0, native consent banner, DNT respect); PCI DSS (SAQ-A posture, hard ACI/payment scope separation, annual pen tests); WCAG 2.1 AA (editor + components).

**Multi-tenant:** Strict data-layer isolation; tenant offboarding with full purge in 30 days.

**commercetools API compliance:** Per-tenant API budgeting; least-privilege scoping (read-only catalog/pricing/inventory); no API ToS violations.

**SOC 2 Type II:** Architected for compliance Day 1; report target within 12 months of launch.

**Integrations (MVP):** commercetools Composable Commerce REST API; commercetools Merchant Center SSO+Shell; Okta/Azure AD/Google (SAML 2.0, OIDC, SCIM 2.0); CDN (Vercel Edge / Cloudflare); CMPs (OneTrust, Cookiebot, Didomi via IAB TCF 2.0).

**Implementation:** Edge rendering required for CWV; ISR or subscription-based cache invalidation within 60 s; AI generation latency budget 30 s e2e; ACI script must add 0 ms measurable LCP impact; zero-downtime publishes (blue/green or canary).

### PRD Completeness Assessment

**Strengths:**
- Requirements traceable to Journey scenarios (1, 2 → AI/auth/publish; 3 → Developer Console; 4 → ACI; 5 → Tenant/SSO/RBAC; 6 → Migration)
- Coverage spans all six journeys; FR/NFR numbering disciplined and referenceable
- MVP/Growth/Vision phasing explicit; deferral list spelled out
- Compliance posture defined (GDPR, ePrivacy, PCI, WCAG, SOC 2) with concrete mitigations

**Gaps relevant to Epic 3 → 4 focus:**
- FR7 (describe → draft) and FR35 (component scaffolding from codebase) are the two pillars for "zero-to-full-site bootstrap with prefilled templates" — but **the PRD does not define a "starter template" or "site bootstrap" capability separate from AI generation**. The bootstrap requested may need an explicit FR (e.g., "FR-NEW: Operators can instantiate a full-site starter from a curated template gallery as a pre-AI shortcut") — to be confirmed against epics in Step 3.
- "Time to first publish" success metric exists (same business day) but no FR mandates a **sample/seed storefront or pre-populated templates at tenant provisioning**. The bootstrap goal is implicit, not requirements-backed.
- No FR on **iterative AI refinement** (multi-turn conversation with the AI to revise a draft) — relevant if Epic 4's AI Builder is meant to handle refinement loops.

---

## Step 3 — Epic Coverage Validation

### Coverage Matrix (PRD FR1–51 → Epics)

| FR | Topic | Epic Coverage | Status |
|----|-------|---------------|--------|
| FR1–FR6 | Canvas authoring + viewport/context preview + mobile editor | Epic 3 | ✅ Covered |
| FR7 | AI describe → governed draft | Epic 4 | ⚠️ **Semantic drift** — PRD says "describe → AI generates draft" (generation); epics rewrite as "operator begins editing → AI infers intent → offers completion" (completion). These are fundamentally different products. |
| FR8 | AI drafts only from approved Green Zone library | Epic 4 | ✅ Covered (verbatim) |
| FR9 | View AI reasoning before draft applied | Epic 4 | ✅ Covered (re-routed via Commerce Intelligence Drawer / ConfidenceCard) |
| FR10 | Accept/modify/reject individual AI placements | Epic 4 | ✅ Covered |
| FR11 | Manual edit/replace any AI component | Epic 4 | ✅ Covered |
| FR12 | Streaming progress feedback during AI gen | Epic 4 | ✅ Covered (renamed "completion" — same UX) |
| FR13–FR14 | Green/Red Zone designation + field-level perms | Epic 2 | ✅ Covered |
| FR15 | Red Zone enforcement | Epic 3 | ✅ Covered |
| FR16–FR20 | Publish flow + governance validation + atomic deploy + audit log | Epic 3 | ✅ Covered |
| FR21–FR28 | ACI behavioral analytics | Epic 5 | ✅ Covered (UI re-routed inline on canvas — no separate dashboard) |
| FR29–FR32 | Developer Console + library mgmt | Epic 2 | ✅ Covered |
| FR33 | AI restricted to library | Epic 3 | ✅ Covered |
| FR34–FR39 | Migration: connect, scaffold, migrate pages, CWV baseline, validation | Epic 4 (was Epic 7 — dissolved) | ✅ Covered — but FR35 expands to 3 migration paths (Frontastic, Custom Next.js, Monolith) |
| FR40 | SAML/OIDC SSO | Epic 1 (basic) + Epic 6 (full) | ✅ Covered (split) |
| FR41 | SCIM 2.0 | Epic 6 | ✅ Covered |
| FR42 | Role assignment | Epic 1 (basic) + Epic 6 (full UI) | ✅ Covered (split) |
| FR43–FR46 | Per-brand boundaries, residency, DPA, usage dashboard | Epic 6 | ✅ Covered |
| FR47–FR49 | Consent withdrawal, right-to-erasure, PCI boundary | Epic 5 | ✅ Covered |
| FR50 | Platform components WCAG AA | Epic 2 | ✅ Covered |
| FR51 | Accessibility warnings before publish | Epic 3 | ✅ Covered |

### Net-New FRs Introduced in Epics (Not in PRD)

The epics added **24 FRs (FR52–FR75)** beyond the PRD's 51:

- **FR52–FR65 (Epic 8 — AI Experience Engine):** experiment hypotheses, two-horizon measurement (Horizon 1/2), recommendation panel, progressive rollout, GitHub PR generation for beyond-Green-Zone changes, rollback alerts, failure taxonomy, Tenant Intelligence Score, first-10-experiments-free, historical data import, campaign workspace, Commerce Intelligence Drawer dual-mode (Create/Optimize)
- **FR66–FR75 (Epic 9 — Physical Retail POS):** POS within MC shell, inventory reservations to storefront, unified CT order pipeline, catalog search via CT API, fiscal receipts (partner-handled), POS RBAC via CASL, in-store behavioral ingestion to ACI, AI assisted-selling, POS Green/Red Zone, offline transaction queue

### ⚠️ Critical PRD ↔ Epics Drift

1. **FR7 paradigm shift (Epic 4 — directly impacts your Epic 3 → 4 goal):**
   - **PRD model:** "describe → AI generates governed draft" (Lovable-style cold-start generation)
   - **Epics model:** "operator begins editing → AI infers intent → offers completion" (warm-start completion)
   - **Implication:** The Epics' Create mode requires the operator to *already have a canvas with content to edit before AI can help*. A new tenant on a blank canvas cannot describe-to-storefront. **This conflicts directly with your "zero-to-full-site bootstrap with prefilled templates on Epic 3" goal** — neither doc establishes how a tenant gets to a non-empty canvas in the first place.

2. **No "starter template" / "site bootstrap" capability in either doc:**
   - PRD: implicit in journey 1 (Sofia describes a campaign), but no explicit FR for "instantiate a full-site starter from a curated template gallery"
   - Epics: FR35 only covers scaffolding from an *existing* storefront (migration); no greenfield bootstrap path
   - **Your stated Epic 3 goal "bootstrap creation from zero to full site with prefilled templates" has no requirements coverage today.** This is a gap that needs an explicit FR before stories can be written.

3. **PRD has not been re-versioned to reflect epics changes:**
   - Epics introduce FR52–75 — these need to be back-propagated into the PRD as authoritative requirements
   - Epics rewrite of FR7 should appear in the PRD as a deliberate trade-off (currently invisible)
   - PRD FRs and Epic FRs should be the same source of truth

4. **Epic 4 is overloaded for "shorten time Epic 3 → Epic 4":**
   - Epic 4 now covers: AI Site Builder (FR7–12) + 3 migration paths (FR34–39 with Frontastic + Custom Next.js + Monolith) + historical data import (FR63) + Commerce Intelligence Drawer Create mode (FR65) = **14 FRs across 5 distinct sub-capabilities**
   - With Epic 7 dissolved, the original "small Epic 4" became a multi-month combined epic
   - Sequencing notes P2 mentions "Frontastic path first" but no formal slicing of Epic 4 into deliverable phases

### Coverage Statistics

- **PRD FRs:** 51
- **PRD FRs covered in epics:** 51 (100 %)
- **Net-new FRs in epics not in PRD:** 24 (FR52–FR75)
- **Total FRs in epics:** 75
- **Coverage %:** 100 % of PRD FRs traced; PRD lags epics by 24 FRs (back-propagation needed)
- **Semantic-drift FRs:** 1 critical (FR7 — paradigm shift)
- **Goal-vs-coverage gap:** "Zero-to-full-site bootstrap with prefilled templates" — **0 covering FRs**

### Missing Requirements (Critical for User's Stated Focus)

**Critical Missing FRs (to add to PRD + Epic 3):**

- **FR-NEW-A:** Operators can instantiate a full-site starter template from a curated, brand-tokenizable template gallery at tenant onboarding — establishing a non-empty canvas without requiring AI generation or migration
  - **Impact:** Without this, "zero-to-full-site" is not a supported workflow. The current Epic 4 Create mode requires existing canvas content; the current Epic 4 Migrator requires an existing storefront to migrate from. Greenfield tenants have no path to a populated canvas.
  - **Recommendation:** Add to Epic 3 (editor surface) — template gallery is a publish-pipeline-adjacent feature, not an AI feature. This unblocks Epic 3 → Epic 4 sequencing because Epic 4's AI completion now has something to complete.

- **FR-NEW-B:** The platform ships a default starter template library (single-brand B2C, multi-locale B2C, B2B-with-account-portal, B2X-multi-context) that any new tenant can select before defining their own component library
  - **Impact:** Without seed templates, every tenant must wait for Epic 2 (Developer Console) component library setup before Epic 3 can produce a usable canvas. This serializes Epic 2 → Epic 3 hard.
  - **Recommendation:** Add to Epic 2 (component library) — platform-shipped default templates as part of the Day-1 governed library.

**High Priority — Resolve Drift:**

- **FR7 must be reconciled:** Either revert epics to the PRD's "describe → generate" model, or update PRD to match the epics' "infer → complete" model. Both cannot stand. **Recommendation:** with FR-NEW-A above, the epics' completion model becomes viable (canvas is no longer empty for greenfield tenants), so the path of least resistance is updating the PRD to match epics — but explicitly noting the bootstrap dependency.

---

## Step 4 — UX Alignment

### UX Document Status

**Found.** Canonical: `ux-design-specification.md`. Per-epic wireframe HTML files exist for epics 1, 2, 3, 4, 5, 6, 8, 9. Earlier exploration in `ux-design-directions.html` (HTML only) — superseded.

### UX ↔ PRD Alignment

✅ **Aligned:**
- Operator chrome inherits commercetools Merchant Center tokens — consistent with PRD FR40/FR42 (MC SSO + native shell)
- Three operator journeys defined in UX (AI Creation, Direct Edit, First Publish) map cleanly to PRD Journeys 1, 2, 3
- Two-zone governance UX (ComponentSlot Green/Red Zone) maps to PRD FR13–FR15
- AI reasoning-before-action (AIReasoningCard) maps to PRD FR9
- ACI plane defined as separate dashboard within MC nav — but PRD FR21–FR27 are operator-facing

⚠️ **Drift between UX spec and PRD:**
- **Mobile editor (FR6 vs UX 1280px hard minimum):** UX spec sets `min-width: 1280px` as a hard constraint and shows a "use desktop" message below; PRD FR6 mandates "Business Operators can access the storefront editor from a mobile device" + Journey 2 (Sofia's Black Friday 6am crisis recovery) is explicitly a mobile-fix-on-phone scenario. **Direct conflict.** Either FR6 needs to be downscoped to "view-only / approve from mobile" or UX needs a mobile editing mode.
- **ACI placement (FR21 vs UX architecture):** PRD FR21 says heatmaps "overlaid directly on the live storefront canvas"; UX spec defines ACI as a **separate top-level section in the MC nav** with its own dashboard ("Commerce Signals", "Product Intelligence", "Experiments"). Epics later resolve this by saying "ACI dissolved into the canvas — no separate dashboard". **The UX spec is out of date relative to the epics on this point.**

### UX ↔ Epics Alignment

⚠️ **Major naming + architecture drift:**

| Concept | UX Spec | Epics | Status |
|---------|---------|-------|--------|
| AI panel | `AIPanel` | `Commerce Intelligence Drawer` | **Renamed** — epics' dual-mode drawer is more sophisticated than UX's chat-only panel |
| AI transparency card | `AIReasoningCard` | `ConfidenceCard` (Optimize) + `AIReasoningCard` (Create) | **Split** — epics introduce two card variants tied to mode |
| AI interaction model | "describe → AI shows reasoning → materialize on canvas" (Lovable-aligned) | "operator begins editing → AI infers intent → offers completion" (warm-start) | **Different paradigm** — UX matches PRD, epics diverged |
| ACI surface | Dedicated MC nav section (3 dashboards) | Inline canvas overlays + canvas-anchored recommendation panel | **Architecturally different** — epics chose inline; UX still describes dashboards |
| First-time use | "Guided Creation" wizard (Direction 6) for new operator's first page | No equivalent — closest is Epic 8's "Data Ramp Onboarding" empty state | **Gap** — UX spec's onboarding pattern is not in epics |
| Recommendation panel | Not in UX spec (predates Epic 8) | UX-DR26 + Epic 8 FR56 | UX requirements **were retro-added** (UX-DR26–UX-DR31) but the spec body is unchanged |

✅ **Aligned:**
- StorefrontCanvas, ContextBar, ComponentSlot, ContextSwitcher, GovernanceBadge, PublishAction, FirstPublishCelebration — all defined in both
- 8px grid, MC token inheritance, Radix UI primitives
- Per-epic wireframes exist (epics 1, 2, 3, 4, 5, 6, 8, 9) — not visually validated by me but the file presence indicates they were produced

### UX Architecture Support (PRD ↔ UX feasibility)

- **Performance:** UX spec is silent on performance budgets; PRD NFR1 (500 ms editor response) and NFR2 (30 s AI generation with 2 s streaming start) are not reflected as UX commitments. **Gap** — designers should know the timing budget so loading states, skeletons, and progress indicators are designed around it.
- **Accessibility:** UX spec defines comprehensive WCAG 2.1 AA testing (axe-core in CI, VoiceOver, NVDA, keyboard-only journeys). Strong alignment with PRD NFR21–NFR23 and FR50–FR51.
- **Keyboard nav:** UX spec defines `⌘↑/↓` for section reordering, `⌘Z` undo, `⌘/` panel toggle, `⌘K` command palette (Phase 2). All consistent with epics UX-DR16, UX-DR23.

### UX Coverage of Your Epic 3 → Epic 4 Goal

**Critical:** The UX spec does **not** define a "starter template gallery" or "prefilled site bootstrap" flow either. Closest references:

- **Direction 6 — "Guided Creation"** (in `ux-design-directions.html`, since superseded): described as "step-by-step wizard, AI generates preview at each step". This is implementation as **AI generation**, not template instantiation.
- **Journey 3 — First Publish:** also assumes AI generates the first page; no template selection step.
- **No explicit "blank state → choose template → populated canvas" journey is documented.**

This confirms the gap from Step 3: zero-to-full-site bootstrap is implicit in journeys (Sofia describes a campaign and AI generates it), but never broken out as a separate, lower-risk path that doesn't depend on AI quality. **For the user's stated focus, this is the single largest UX gap.**

### UX Warnings

- ⚠️ **UX spec is older than epics** — written before Epic 7 dissolved into Epic 4 and before Epic 8 (Experience Engine) added FR52–65. The retroactive UX-DR26–UX-DR31 entries in `epics.md` are not reflected in `ux-design-specification.md` body. **Recommendation:** treat the epics' UX requirements as authoritative, and either update the UX spec or formally mark it as the foundational direction with addenda.
- ⚠️ **Mobile editor (FR6) vs 1280px constraint** — material conflict; pick one and update the other.
- ⚠️ **ACI placement drift** — UX still shows dedicated dashboards; epics moved to inline canvas overlays. UX spec body needs revision.
- ⚠️ **No starter-template / site-bootstrap flow** — confirmed gap aligned with the user's Epic 3 → Epic 4 goal.
- ⚠️ **Performance budgets not surfaced in UX spec** — designers don't know the 500 ms / 30 s / 15 s NFR targets they should design around.

---

## Step 5 — Epic & Story Quality Review (Epic 3 + Epic 4 deep dive)

### Architecture Surfacing — Critical Discovery

The architecture document's first capability bullet (line 34) explicitly lists **"template library"** as part of "Storefront Creation & Editing": *"Visual storefront editor with drag-and-drop interface, **template library**, B2X rendering..."* — but neither the PRD FR list nor the epics/stories include any story-level coverage of a template library or starter site. **The capability is named in the architecture and lost on the way down to FRs and stories.**

The architecture also still describes the **PRD's Lovable model** of FR7 ("describe your storefront, AI generates governed draft") on line 36 — confirming that the original product intent was cold-start describe-to-storefront, and the epics-side "warm-start completion" pivot did not propagate back through architecture or PRD.

### Architecture Drift (separate from Epic 3 → 4 focus, but material)

- **Tech stack:** Architecture's `Core Architectural Decisions` (line 213+) names Clerk for auth, tRPC for API, `create-next-app` as the starter. Epics rewrite this to MC Custom Application (`@commercetools-frontend/application-shell` v27, `useMcQuery`/`useMcMutation`, `create-mc-app` starter-typescript template). **Architecture is one architectural pivot behind the epics.**
- **Starter template requirement (workflow check):** The bmad-check-implementation-readiness Step 5 explicitly checks if Architecture specifies a starter template → if YES, Epic 1 Story 1 must be "Set up initial project from starter template". Architecture says `create-next-app`; Story 1.1 (`MC Custom Application Scaffold & Connect Packaging`) uses `create-mc-app starter-typescript` instead. **Story 1.1 is correct for the actual chosen platform; the architecture wording is stale.**

### Epic Quality Assessment (User-Value Focus)

| Epic | User-centric? | Value Proposition | Verdict |
|------|--------------|-------------------|---------|
| Epic 1 — Platform Foundation & Operator Workspace | Mixed — title says "operator workspace" but most content is foundation infrastructure | A signed-in operator can navigate the platform; behavioral collection starts | ⚠️ **Partially technical milestone.** Stories 1.1–1.3, 1.5, 1.6 are pure foundation (scaffold, schema, RBAC wiring, CI/CD, observability). Only 1.4 and 1.7 deliver direct operator value (sign-in, procurement-gate skeleton). Acceptable for a foundation epic if labeled as such, but the user-value framing is thin. |
| Epic 2 — Governed Component Library | ✅ Yes — "Developer can publish a governed library" | Developers ship a governed library that operators consume in Epic 3 | ✅ Clean |
| Epic 3 — Storefront Editor & Publishing | ✅ Yes — "Operators can build and publish" | Direct operator-facing value | ✅ Clean |
| Epic 4 — AI Site Builder & Migrator | ✅ Yes — but bundles two distinct value props | (a) AI-assisted completion; (b) migration from existing storefront | ⚠️ **Two separate value propositions in one epic** — site builder ≠ migrator. Splitting would let migrator ship without blocking on AI inference quality. |
| Epic 5 — Behavioral Data Infrastructure | ⚠️ Half-half — collection infra is technical; canvas-anchored heatmaps are user-value | "Operators see behavioral signals inline" | ⚠️ **Hybrid epic.** Story 5.1 is pure infrastructure; 5.3–5.10 are operator-facing. The "behavioral collection starts at Epic 1" prose is a contradiction — the FRs are tracked in Epic 5 but the work begins in Epic 1. **Coverage map drift** between epic narrative and story location. |
| Epic 6 — Enterprise Administration & Compliance | ✅ Yes | IT Admin onboards tenant fully | ✅ Clean |
| Epic 8 — AI Experience Engine | ✅ Yes | Operators run experiments, get recommendations | ✅ Clean — possibly biggest epic but well user-framed |
| Epic 9 — Physical Retail POS | ⚠️ Research epic by design — research deliverables vs. user-value deliverables not separated | TBD pending partner selection | ⚠️ Epic 9 has FR mappings but **no stories defined yet** (verified — no `### Story 9.x` entries). Acceptable for a research epic; needs to be clearly labeled as such until partner ADR completes. |

### Epic Independence Check

- ✅ **Epic 1 stands alone** — no forward dependency.
- ✅ **Epic 2 → needs Epic 1** (CASL, tenancy, RBAC) — fine.
- ⚠️ **Epic 3 → needs Epic 1 + Epic 2 strictly.** Epic 3 stories (3.1, 3.2, 3.3) require the published component library schema from Epic 2 to function. The PRD's "MVP Resource Requirements" mentions Epic 2 + Epic 3 in parallel under P1, but **the editor cannot render slots without a defined component library**. Sequence is hard, not parallel.
- ⚠️ **Epic 4 → needs Epic 1, Epic 2, AND Epic 3.** Epic 4's Site Builder writes its AI completions to the canvas defined by Epic 3. Story 4.5 (`Governed AI Completion Application`) explicitly dispatches `APPLY_AI_COMPLETION` to the canvas state manager — which only exists once Story 3.1 (`StorefrontCanvas Foundation`) ships. **No way to start Epic 4 work without Epic 3's canvas.** Migration paths (4.9–4.11) also require Epic 2's component library to map into.
- ⚠️ **Epic 5 → contradiction.** Epic prose says "behavioral collection starts at Epic 1 project connection — moat begins accumulating before any operator UI is built." But all behavioral-collection FR-mapped stories live in Epic 5 (5.1, 5.2). Either Story 1.x needs to include a basic event collection scaffold, or the prose needs to be corrected.
- ⚠️ **Epic 8 → needs Epic 5 (live behavioral data) AND Epic 4's drawer (Optimize mode extends Create mode drawer infrastructure).** Sequencing P3 says Epic 8 MVP comes after Epic 4 — consistent with stories.

### Story-Level Quality — Epic 3 (14 stories)

✅ **Strengths:**
- All stories use clear "As-a / I-want / So-that" + numbered ACs that are testable and specific
- ACs reference concrete tech (Inngest job names, Prisma table names, CASL permissions) — implementable as written
- Dependencies declared on every story
- Complexity tagged (XL/L/M)

⚠️ **Issues found:**

1. **Story 3.1 is XL with 7 ACs covering: rendering + governance overlay + 4 explicit canvas states + ARIA live region + AI tint badge + WCAG audit.** Should be split into two: (a) canvas + slot rendering + governance overlay; (b) keyboard navigation + ARIA + WCAG audit + AI-tint badge. **One XL story is high-risk for a foundation story** — its delay blocks every other Epic 3 story.

2. **Story 3.7 (Mobile Editor) directly contradicts UX spec.** UX spec says "min-width: 1280px hard constraint, below shows 'use desktop' message". Story 3.7 builds a touch-optimized editor at <768 px with bottom-sheet drawers. **Either UX spec or Story 3.7 must be corrected before implementation.** Recommend keeping Story 3.7 (matches PRD FR6 + Journey 2 Black Friday recovery scenario) and updating UX spec.

3. **Story 3.8 (Real-time Collaboration with Liveblocks) is marked L but is independently complex.** Liveblocks room auth, presence, conflict toast, graceful degradation, custom auth endpoint. Reasonable as one story, but has a large surface and is not strictly required for MVP — could defer.

4. **Story 3.9 (Storefront Branches) is marked L and deeply scoped — Git-model branches for storefront pages with three-way diff and merge.** This is a very heavy capability for "MVP — easy to migrate, satisfying to build". **Not in PRD as an FR.** Likely should be deferred to post-MVP.

5. **No Epic 3 story covers prefilled-template / starter-site bootstrap.** Confirmed gap — the most critical for the user's stated goal.

### Story-Level Quality — Epic 4 (13 stories)

✅ **Strengths:**
- Stories well-decomposed by function (drawer infra, inference engine, reasoning card, application, per-row actions, streaming)
- Migration paths separated (Frontastic / Custom Next.js / Monolith) — allows incremental delivery
- AC use specific tech names (OpenRouter, Zod, Inngest events) — implementable
- Story 4.11 explicitly marked as "available without full platform activation" → pre-sales tool, smart business move

🔴 **Critical issue — Circular dependency on migration path stories:**

- Story 4.9 (Frontastic Migration) declares dependency on **Story 4.12** (Migration Review UI)
- Story 4.10 (Custom Next.js Migration) declares dependency on **Story 4.12**
- Story 4.11 (Monolith Migration) declares dependency on **Story 4.12** AND **Story 4.13**
- Story 4.12 (Migration Review UI) declares dependency on **Story 4.9 OR 4.10 OR 4.11**

**This is a literal circular dependency.** Implementation cannot start. Resolution: either Story 4.12 should depend on at least one migration path completing first (then enhances for the others), or the migration path stories should produce the mapping JSON output without needing the review UI to exist.

⚠️ **Additional Epic 4 issues:**

6. **Story 4.2 (Drawer Infrastructure) and 4.3 (AI Intent Inference Engine) are both XL.** 4.3's ACs include the entire AI inference pipeline: edit observation hook + Inngest function + OpenRouter integration with governance prompt + streaming + 30 s timeout + Zod schema validation. **One story should not own the entire AI integration surface area.** Suggest splitting 4.3 into: (a) edit-observation hook + Inngest event firing (4.3a), (b) OpenRouter integration with governance prompt (4.3b), (c) Zod validation + Inngest streaming wiring (4.3c).

7. **Three migration paths (4.9, 4.10, 4.11) are all XL.** Each is a major effort. Frontastic (parser + auto-mapper + semantic matching), Custom Next.js (GitHub App + codebase analysis + LLM extraction), Monolith (sitemap + LLM canvas generation + CWV baseline). **Per Priority Sequencing P2 ("Frontastic path first"), recommend slicing Epic 4 to ship Frontastic + Story 4.13 first, defer 4.10 and 4.11 to Epic 4 phase 2.**

8. **AI Site Builder (Stories 4.2–4.7) and AI Migrator (Stories 4.9–4.13) are independent capability tracks.** They share Story 4.1 (CT project connection) and Story 4.12 (review UI for migrations) but otherwise. **Splitting Epic 4 into Epic 4a (Migrator-Frontastic) and Epic 4b (Site Builder Create mode) directly serves the user's goal of shortening Epic 3 → Epic 4 progression** — Migrator could ship before Site Builder is complete.

9. **No Epic 4 story covers cold-start "describe → generate full site"** (the PRD's original FR7). Stories 4.2–4.7 implement only the warm-start completion model (must observe operator edits first). For greenfield tenants on a blank canvas, **there is no AI path to a populated canvas**.

### Cross-Story Coverage Analysis

| Capability | PRD FR | Epic FR Map | Story | Status |
|-----------|--------|-------------|-------|--------|
| Operator describes intent → AI generates draft from blank canvas | FR7 (PRD) | FR7 rewritten | None | 🔴 **Not implemented** — would need a "Story 4.0: Cold-start describe-to-page" that doesn't exist |
| Operator selects from prefilled site template | None — gap | None — gap | None | 🔴 **Architecture mentions; no FR; no story** — confirmed primary gap for user's stated goal |
| Operator inherits a default Day-1 component library so canvas is non-empty | Implicit | None | None | 🔴 **Gap** — Epic 2 expects developers to define library; no platform-shipped default starter library |
| Operator begins editing → AI completes from observed edits | FR7 (epics) | Epic 4 | Stories 4.2, 4.3, 4.4, 4.5, 4.6, 4.7 | ✅ Covered |
| Migration from Frontastic | FR34–37 | Epic 4 | Story 4.9 | ⚠️ Covered but circular dependency on 4.12 |
| Migration from Custom Next.js | FR34–37 | Epic 4 | Story 4.10 | ⚠️ Covered but circular dependency on 4.12 |
| Migration from monolith + CWV baseline | FR34–39 | Epic 4 | Story 4.11 | ⚠️ Covered but circular dependency on 4.12 + 4.13 |
| Editor canvas + Green/Red Zone | FR1–FR3, FR15 | Epic 3 | Stories 3.1–3.3 | ✅ Covered |
| Mobile editor | FR6 | Epic 3 | Story 3.7 | ⚠️ Covered but conflicts with UX spec 1280px constraint |

### Quality Findings — Severity Summary

#### 🔴 Critical Violations (block implementation as written)

1. **Circular dependency in Epic 4:** Stories 4.9/4.10/4.11 ↔ Story 4.12 — must be untangled before sprint planning
2. **Zero coverage of "zero-to-full-site bootstrap with prefilled templates"** — your stated focus has no FR, no story, no implementation path. Architecture mentions "template library" but it never propagated to PRD/epics/stories
3. **PRD FR7 (cold-start describe → generate) has no implementing story.** Either revise PRD to match epics' warm-start model or add a cold-start story to Epic 4

#### 🟠 Major Issues

4. **UX spec ↔ Story 3.7 mobile editor conflict** — pick one, document the other as superseded
5. **Epic 4 is overloaded** — Site Builder + 3 Migration Paths + Historical Data Import + Drawer = 13 stories, two distinct value propositions; sequencing P2 mentions "Frontastic path first" but no formal slicing plan
6. **Story 3.1 and Story 4.3 are XL with broad scope** — XL stories on critical-path foundations (canvas + AI inference) are high-risk for sprint commitment
7. **PRD ↔ Epics drift on FR7 paradigm** (cold-start vs warm-start) and PRD missing 24 net-new FRs (FR52–75)
8. **Architecture document is one pivot behind** the epics (Clerk/tRPC/create-next-app vs. MC Custom Application / ApplicationShell / create-mc-app)
9. **Epic 5 prose ↔ story location contradiction** — "behavioral collection starts at Epic 1" but no Epic 1 story implements it

#### 🟡 Minor Concerns

10. Epic 1 user-value framing is thin — most stories are foundation infrastructure. Consider relabeling as "Foundation" epic explicitly so it's clear it's not user-feature-driven.
11. Story 3.9 (Storefront Branches) is heavy for MVP — not PRD-required, defer to post-MVP
12. Story 3.8 (Real-time Collaboration via Liveblocks) is marked L but independently complex — defer or simplify for MVP
13. Epic 9 has FRs (FR66–75) but no stories yet — acceptable for a research epic, but should be flagged as "stories pending partner ADR" until then.
14. Epic 4 Migration paths use OpenRouter heavily (4.9 semantic matching, 4.10 codebase extraction, 4.11 monolith canvas generation) — three separate LLM-quality dependencies in one epic; failure rates compound

---

## Step 6 — Summary and Recommendations

### Overall Readiness Status

🟠 **NEEDS WORK** — particularly around the user's stated focus area (Epic 3 → Epic 4 progression).

The plan has strong bones: 100 % of PRD FRs are mapped to epics, the architecture and tech-stack pivot to the MC Custom Application is sound, story decomposition is detailed with implementable ACs, and the Epic 8 (Experience Engine) and Epic 9 (POS) extensions are well-conceived. **But on the specific path the user wants to optimize — bootstrap zero-to-full-site on Epic 3, and accelerate the Epic 3 → Epic 4 increment — the plan has critical structural gaps.**

### Critical Issues Requiring Immediate Action (specific to your stated focus)

1. **[BLOCKER for stated goal] Zero-to-full-site bootstrap with prefilled templates has no requirements coverage.**
   - Architecture mentions "template library" (line 34) but it never propagated into PRD FRs, epics, or stories.
   - Greenfield tenants today have **no path to a populated canvas** unless they go through migration (Epic 4) or describe-to-AI (which Epic 4 broke into a warm-start completion model that requires existing canvas content). Both paths require something to exist first.
   - **Action:** Add **FR-NEW-A** (`Operators can instantiate a full-site starter from a curated template gallery`) to the PRD and a corresponding story to Epic 3, plus **FR-NEW-B** (platform-shipped default starter library) added to Epic 2 so a new tenant has Day-1 component coverage. This is the unblocker for "zero-to-full-site on Epic 3".

2. **[BLOCKER] Circular dependency in Epic 4 migration stories.**
   - Stories 4.9, 4.10, 4.11 all declare a dependency on Story 4.12, but 4.12 declares a dependency on at least one of 4.9/4.10/4.11. **Implementation cannot start.**
   - **Action:** Untangle by either (a) making 4.12 enhance after one path lands first, or (b) producing the migration mapping JSON without requiring the unified review UI. Recommend making 4.12 buildable against a stub mapping fixture, then 4.9 (Frontastic-first per Priority Sequencing P2) can run in parallel.

3. **[BLOCKER for FR7] PRD ↔ Epics paradigm conflict on FR7 not reconciled.**
   - PRD says "describe → AI generates governed draft" (Lovable cold-start). Epics say "operator begins editing → AI infers from observed edits → completes" (warm-start). UX spec aligns with the PRD; epics rewrote it without back-propagating.
   - **Action:** Decide deliberately. With FR-NEW-A above (template gallery) plus the warm-start completion model, the epics' approach becomes coherent (canvas is non-empty for greenfield tenants). Update PRD FR7 to match epics, document the trade-off, and update UX spec.

### Recommended Next Steps — Concrete Slicing to Shorten Epic 3 → Epic 4

To directly serve the user's stated goal of "**bootstrap creation from zero to full site with prefilled templates on Epic 3, and shorten the time to increment Epic 3 to Epic 4**", the following slicing is recommended:

**Phase A — Add the missing pieces (target: 1 sprint of planning + early Epic 2 work):**
1. Update PRD: add FR-NEW-A (starter gallery) and FR-NEW-B (default platform library); reconcile FR7 to the warm-start completion model and document the cold-start gap explicitly closed by FR-NEW-A
2. Update Architecture: rewrite tech-stack section to match epics (MC Custom Application, ApplicationShell, create-mc-app starter); fix "template library" reference to point to FR-NEW-A
3. Update UX spec: remove 1280 px hard constraint conflict (resolve with Story 3.7); update ACI placement description (inline canvas overlays, not dedicated dashboard); ensure Direction 6 "Guided Creation" maps to the new template-gallery flow

**Phase B — Re-slice Epic 3 (target: smaller, shippable):**
4. Add **Story 3.0: Starter Template Gallery** — operator selects from a default gallery on first canvas open; selection populates the canvas with default Green Zone components and brand-tokenizable copy. *This is the unblocker — once shipped, the canvas is never empty.*
5. Split **Story 3.1** (XL → 2 stories) — separate canvas-rendering + governance-overlay from keyboard/ARIA/AI-tint
6. **Defer Story 3.8 (Liveblocks collaboration) and Story 3.9 (Storefront Branches) to Epic 3 phase 2 (post-MVP).** Neither is PRD-mandated; both add weeks of surface area
7. Result: Epic 3 ships with **9 user-facing stories** (3.0, 3.1a/b, 3.2–3.7, 3.10–3.14) instead of 14 — leaner, ships sooner, hands off cleanly to Epic 4

**Phase C — Split Epic 4 (target: ship Migrator before Site Builder):**
8. Rename Epic 4 → **Epic 4a: Migrator** (Stories 4.1, 4.9 Frontastic, 4.12 review-with-stub-fixture, 4.13 readiness, 4.8 historical import)
9. Add **Epic 4b: AI Site Builder** (Stories 4.2 drawer, 4.3a/b/c inference engine split, 4.4 reasoning card, 4.5 governed application, 4.6 per-row, 4.7 streaming)
10. **Defer Stories 4.10 (Custom Next.js) and 4.11 (Monolith) to Epic 4c (phase 2)** — they are XL each, share LLM-quality risk, and per Priority Sequencing P2 only Frontastic is the highest-urgency ICP
11. With FR-NEW-A in Epic 3 producing a populated canvas, the warm-start completion model in Epic 4b is now coherent for greenfield tenants on Day 1

**Phase D — Foundation cleanup parallel to Phase B/C:**
12. Resolve Epic 5 prose ↔ story location contradiction — either move behavioral collection scaffolding to a Story 1.x, or rewrite Epic 5 prose to say "behavioral UI surfaces in Epic 5; behavioral collection scaffolding in Story 1.x"
13. Mark Epic 9 explicitly as "research epic — partner ADR pending" until vendor selected

### Specific Document Updates Required

| Document | Update | Why |
|---|---|---|
| `prd.md` | Add FR-NEW-A (starter gallery), FR-NEW-B (default platform library), FR52–FR75 (back-prop from epics); reconcile FR7 to warm-start | Close the bootstrap gap; bring PRD up to date with the 24 net-new FRs introduced in epics |
| `architecture.md` | Rewrite Core Architectural Decisions section (Clerk → MC session auth, tRPC → useMcQuery/Mutation, create-next-app → create-mc-app); document template gallery requirement | Architecture is one pivot behind the implementing plan |
| `ux-design-specification.md` | Resolve mobile editor 1280 px conflict; update ACI placement (canvas-anchored, not dashboards); add starter-gallery flow; surface NFR1/NFR2/NFR3 performance budgets so designers know what to design around | Three known drift points + missing performance budgets |
| `epics.md` | Add Story 3.0 (starter gallery) to Epic 3; split Epic 4 into 4a/4b/4c (Migrator / Site Builder / Phase 2 migration paths); fix Epic 5 collection-vs-UI prose; resolve circular dependency on 4.9/4.10/4.11 ↔ 4.12 | Direct enablers for shortening Epic 3 → Epic 4 |
| `stories.md` | Add Story 3.0; split Story 3.1; split Story 4.3; resolve 4.9/4.10/4.11 ↔ 4.12 dependency wording; add Story 4.0 (cold-start describe → AI on populated canvas) if cold-start retained anywhere; add Epic 9 stories once partner ADR completes | Story-level execution of epic re-slice |

### Risk-Adjusted Reading

The user's stated goal is shippable but **not as currently planned**. The "bootstrap zero-to-full-site on Epic 3" capability is structurally absent and must be added; the Epic 4 circular dependency means implementation cannot start without untangling. **However**, with the four-phase slicing above, the gap from Epic 3 to a working Epic 4 phase 1 (Migrator-Frontastic + Site Builder MVP completion mode) shortens materially — Phase B drops 5 stories from Epic 3, Phase C drops 4 stories from Epic 4 phase 1. **The critical path goes from ~27 stories down to ~14 stories for an Epic 3 + Epic 4a-MVP delivery.**

### Final Note

This assessment identified **14 issues across 5 categories** (3 critical, 6 major, 5 minor). The three critical issues (template-gallery gap, circular dependency, FR7 paradigm conflict) **must be resolved before sprint planning**; the major and minor issues should be tracked as PRD/architecture/UX maintenance debt and addressed in the order they constrain implementation.

The plan is well-conceived strategically — the gaps are mostly drift from rapid evolution (Epic 7 dissolved, Epic 8 added, MC Custom Application pivot, ACI inline UI rework) where downstream documents weren't updated. **A focused 1-sprint sync of PRD/Architecture/UX to match the epics, plus the slicing plan above, gets you to "READY" status.**

---

**Assessor:** John (Product Manager) — bmad-check-implementation-readiness workflow
**Date:** 2026-05-12
**Focus:** Epic 3 → Epic 4 progression (zero-to-full-site bootstrap; shortened increment)
**Comparison baseline:** prior `implementation-readiness-report-2026-05-05.md`



