---
date: 2026-05-12
version: v2
project: Tutorial (commerce-tools-research / NextGen Frontend)
focus: Verification re-run after closing all three blockers from the 2026-05-12 v1 report (FR76/FR77 added + FR7 reconciled + Epic 4 circular dependency untangled + UX spec brought current)
priorReport: _bmad-output/planning-artifacts/reports/implementation-readiness-report-2026-05-12.md
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
    - _bmad-output/planning-artifacts/decisions/adr-002-positioning-amplitude-statsig.md
    - _bmad-output/planning-artifacts/decisions/adr-004-tracking-layer-architecture.md
  epics:
    - _bmad-output/planning-artifacts/epics.md
  stories:
    - _bmad-output/planning-artifacts/stories.md
  ux:
    - _bmad-output/planning-artifacts/ux-design-specification.md
    - _bmad-output/planning-artifacts/html/epic-1-foundation-workspace-wireframes.html
    - _bmad-output/planning-artifacts/html/epic-2-component-library-wireframes.html
    - _bmad-output/planning-artifacts/html/epic-3-editor-wireframes.html
    - _bmad-output/planning-artifacts/html/epic-4-ai-builder-migrator-wireframes.html
    - _bmad-output/planning-artifacts/html/epic-5-behavioral-data-wireframes.html
    - _bmad-output/planning-artifacts/html/epic-6-enterprise-admin-wireframes.html
    - _bmad-output/planning-artifacts/html/epic-8-experience-engine-wireframes.html
    - _bmad-output/planning-artifacts/html/epic-9-retail-pos-wireframes.html
  supplemental:
    - _bmad-output/planning-artifacts/reports/implementation-readiness-report-2026-05-12.md
    - _bmad-output/planning-artifacts/reports/implementation-readiness-report-2026-05-05.md
notes:
  - This is a verification re-run scoped to confirming the v1 report's three blockers are fully closed and surfacing any drift the closing edits introduced.
  - Same canonical inventory as v1; no new artifacts added since 2026-05-12 v1 except this report.
---

# Implementation Readiness Assessment Report — v2

**Date:** 2026-05-12
**Version:** v2 (verification re-run)
**Project:** Tutorial (commerce-tools-research / NextGen Frontend)
**Focus:** Confirm closure of v1 blockers; surface any new drift from the closing edits.
**Comparison baseline:** [implementation-readiness-report-2026-05-12.md](_bmad-output/planning-artifacts/reports/implementation-readiness-report-2026-05-12.md) (v1)

## Step 1 — Document Discovery

### Inventory

**PRD:** `prd.md` (canonical) — edited 11x this session for FR7 warm-start reconciliation + FR76/FR77 starter-template gallery + default platform library.

**Architecture:** `architecture.md` (canonical), `adr-002-positioning-amplitude-statsig.md`, `adr-004-tracking-layer-architecture.md`.

**Epics & Stories:** `epics.md`, `stories.md` — Story 4.12 edited (AC8 added, Dependencies restructured into labelled clauses).

**UX:** `ux-design-specification.md` (canonical) — 15 edits this session: ACI plane rewritten, AIPanel→CommerceIntelligenceDrawer with dual-mode, AIReasoningCard scoped + new ConfidenceCard, new StarterTemplateGallery component, new Performance Design Budgets section, Direction 6 reframed, Journey 3 rewritten. Plus 8 per-epic wireframes (epics 1, 2, 3, 4, 5, 6, 8, 9).

**Supplemental:** Prior readiness reports (2026-05-05, 2026-05-12 v1).

### Resolutions

- `.md` confirmed canonical; `.html` are rendered twins (regenerated 2026-05-12 via `scripts/regenerate_html_twins.py`).
- No duplicates, no missing required documents.
- ADR-004 (tracking layer architecture) is now part of the architecture inventory — was not in v1's scan because it had not been promoted to a tracked artifact.

### Discovery Outcome

✅ All required documents present, no duplicates, inventory unchanged from v1 except the addition of ADR-004 to the architecture set.

---

## Step 2 — PRD Analysis

### Functional Requirements (58 total list-items, FR1–FR82)

**Storefront Authoring (FR1–FR6)** — unchanged from v1.

**AI-Assisted Creation (FR7–FR12)** — **FR7 reconciled to warm-start completion model.** Now reads: *"Business Operators editing a populated canvas can have the AI infer their completion intent from observed edits (minimum three distinct edit events) and offer a governed completion for the remaining sections, drawn from the tenant's approved Green Zone component library. The canvas is populated either by a starter template (FR76), a migration (FR34–FR39), or prior published state. Cold-start describe-to-storefront from a blank canvas is not supported in MVP — bootstrap is owned by FR76/FR77."* — closes the v1 Critical PRD↔Epics drift on FR7.

**Governance & Publishing (FR13–FR20)** — unchanged.

**ACI Phase 1 (FR21–FR28)** — unchanged.

**Developer & Component Management (FR29–FR33)** — unchanged.

**Migration & Onboarding (FR34–FR39)** — unchanged (Epic 4 covers 3 migration paths).

**Platform & Administration (FR40–FR46)** — unchanged.

**Compliance & Data Privacy (FR47–FR51)** — unchanged.

**🆕 Site Initialization & Starter Templates (FR76–FR77)** — closes v1 BLOCKER #1.
- **FR76:** Starter template gallery during tenant onboarding — at least 4 starter shapes (single-brand B2C, multi-locale B2C, B2B with account portal, B2X multi-context) producing populated canvas.
- **FR77:** Default platform-shipped Green Zone component library covering all FR76 starter templates so a new tenant has Day-1 component coverage before defining its own developer-governed library.

**🆕 Tracking Layer & CDP Co-Exist (FR78–FR82)** — added since v1 baseline (FR78 cross-session stitching for auth customers; FR79 CDP destination-adapter pattern; FR80 experiment-outcome event emission; FR81 hybrid Pixel+CAPI playbook; FR82 Tenant Intelligence Score moat-narrative surface).

### FR52–FR75 — back-propagation status

The PRD references FR55, FR61, and FR62 inline (inside FR78/FR82 prose) but **does not redefine FR52–FR75 in the PRD's own FR list**. Net-new FRs FR52–FR65 (Epic 8 — AI Experience Engine) and FR66–FR75 (Epic 9 — POS) remain epic-only.

**Verdict:** This is the same v1 Major issue ("PRD lags epics by 24 FRs") and is still open. Severity unchanged. Less urgent than v1's three blockers; tracked as documentation debt.

### Non-Functional Requirements (23 total)

Unchanged from v1: NFR1–NFR6 (performance), NFR7–NFR14 (security), NFR15–NFR20 (scalability), NFR21–NFR23 (accessibility). Notably **NFR2 was reworded this session** to reflect the warm-start model: "AI completion job (intent inference + governed completion offer applied to canvas) completes within 30 seconds end-to-end, with streaming progress shown after 2 seconds."

### Additional Requirements / Constraints

Unchanged from v1: GDPR, ePrivacy/Cookie Consent, PCI DSS, WCAG 2.1 AA, multi-tenant isolation, commercetools API compliance, SOC 2 Type II target, MVP integrations, edge rendering, ACI script LCP 0ms, zero-downtime publishes.

### PRD Completeness Assessment

**Strengths (changed since v1):**
- ✅ FR7 paradigm contradiction resolved across PRD (11 edits this session — Success Criteria, MVP Scope, Subscription tiers, Implementation Considerations, MVP Phase 1, NFR2, Journey 1 narrative, Journey Capabilities Summary).
- ✅ FR76/FR77 add explicit greenfield bootstrap path.
- ✅ FR78–FR82 introduce CDP co-exist posture with tracking-layer detail.
- ✅ Journey 1 (Sofia's Valentine's Day campaign) rewritten to model starter-template + warm-start completion — narrative now consistent with the FR-level definition.

**Strengths (carry-over from v1):**
- 100 % of original PRD FRs traceable to journeys.
- MVP/Growth/Vision phasing explicit; deferral list spelled out.
- Compliance posture defined with concrete mitigations.

**Gaps (still open):**
- PRD does not define FR52–FR75 in its own FR list — these live only in epics.md. Same as v1; severity unchanged (Major).
- A handful of narrative passages still use "AI creation" / "AI generation" phrasing where they describe operator perception (Journey 6 Diego's marketing lead, Innovation Analysis line 365). These are storytelling, not requirements; deliberately left in place during this session's edits to preserve emotional weight.

---

## Step 3 — Epic Coverage Validation

### Coverage Matrix (PRD FR1–82 → Epics)

| FR Range | Topic | Epic Coverage | Status |
|---|---|---|---|
| FR1–FR6 | Canvas authoring + viewport/context preview + mobile editor | Epic 3 | ✅ Covered |
| **FR7** | **AI warm-start completion (warm-start)** | **Epic 4 — Stories 4.2, 4.3a/b/c, 4.4–4.7** | **✅ Covered. Drift closed in v2 — PRD and epics now use the same warm-start completion language.** |
| FR8 | AI drafts only from approved Green Zone library | Epic 4 | ✅ Covered |
| FR9 | View AI reasoning before draft applied (Commerce Intelligence Drawer) | Epic 4 | ✅ Covered |
| FR10–FR12 | Accept/modify/reject + manual edit + streaming | Epic 4 | ✅ Covered |
| FR13–FR14 | Green/Red Zone designation + field-level perms | Epic 2 | ✅ Covered |
| FR15 | Red Zone enforcement | Epic 3 | ✅ Covered |
| FR16–FR20 | Publish flow + governance + atomic deploy + audit | Epic 3 | ✅ Covered |
| FR21–FR28 | ACI behavioral analytics (canvas-anchored, no separate dashboard) | Epic 5 | ✅ Covered |
| FR29–FR32 | Developer Console + library mgmt | Epic 2 | ✅ Covered |
| FR33 | AI restricted to library | Epic 3 (cross-cutting) | ✅ Covered |
| FR34–FR39 | Migration: connect, scaffold (3 paths), migrate, CWV baseline, validation | Epic 4 (Epic 7 dissolved) | ✅ Covered |
| FR40 | SAML/OIDC SSO | Epic 1 (basic) + Epic 6 (full) | ✅ Covered (split) |
| FR41 | SCIM 2.0 | Epic 6 | ✅ Covered |
| FR42 | Role assignment | Epic 1 (basic) + Epic 6 (full UI) | ✅ Covered (split) |
| FR43–FR46 | Per-brand boundaries, residency, DPA, usage dashboard | Epic 6 | ✅ Covered |
| FR47–FR49 | Consent withdrawal, right-to-erasure, PCI boundary | Epic 5 | ✅ Covered |
| FR50 | Platform components WCAG AA | Epic 2 | ✅ Covered |
| FR51 | Accessibility warnings before publish | Epic 3 | ✅ Covered |
| FR52–FR65 | Experiments, recommendations, Horizon-1/2, GitHub PR, rollback, "Tried and Retired", Tenant Intelligence Score, First 10 Free, historical import, campaigns, Drawer dual-mode | Epic 8 (AI Experience Engine) | ✅ Covered |
| FR66–FR75 | POS in MC shell, inventory sync, unified CT Order pipeline, fiscal receipts, POS RBAC, in-store ACI ingestion, AI assisted-selling, POS Green/Red Zone, offline queue | Epic 9 (research epic — partner ADR pending) | ⚠️ Mapped, but stories deferred until partner ADR completes (acceptable for research epic — flagged in epic prose). |
| **FR76** | **Starter template gallery (greenfield bootstrap)** | **Epic 3 — Story 3.0** | **✅ Covered. Closes v1 BLOCKER #1.** |
| **FR77** | **Default platform-shipped Green Zone library** | **Epic 2 — Story 2.10** | **✅ Covered. Closes v1 BLOCKER #1.** |
| FR78 | Auth-customer cross-session stitching | Epic 5 — Story 5.11 | ✅ Covered |
| FR79 | CDP destination-adapter pattern (RudderStack, Segment, Snowplow) | Epic 5 — Story 5.12 | ✅ Covered (Phase 2 adapters; MVP own-SDK only) |
| FR80 | Experiment-outcome event emission to customer destinations | Epic 8 — story integrated with experiment runner | ✅ Covered |
| FR81 | Hybrid Pixel + CAPI playbook (Meta, Google, TikTok) | Epic 5 (docs); Epic 8 (Phase 2 native CAPI) | ✅ Covered (MVP = playbook; Phase 2 = native emission) |
| FR82 | Tenant Intelligence Score moat-narrative surface | Epic 8 — Tenant Intelligence Score in nav | ✅ Covered |

### FR7 Drift Verification (v2-specific check)

Cross-checked the FR7 reconciliation across PRD ↔ epics ↔ stories:

| Document | FR7 statement |
|---|---|
| **PRD** ([prd.md:600](_bmad-output/planning-artifacts/prd.md#L600)) | "Business Operators editing a populated canvas can have the AI infer their completion intent from observed edits (minimum three distinct edit events) and offer a governed completion for the remaining sections..." |
| **Epics** ([epics.md:37](_bmad-output/planning-artifacts/epics.md#L37)) | "Business Operators can begin editing a canvas and receive an AI completion offer — the AI infers intent from observed edits and offers to complete remaining sections using the governed component library" |
| **Stories** (Story 4.3a/b/c) | Edit-observation hook + Inngest event + OpenRouter integration (warm-start completion engine) |

✅ **No paradigm drift.** The three documents now state the same warm-start completion model. The "minimum three distinct edit events" specificity is in the PRD only — recommend adding to the epics' FR7 statement for tighter alignment, but not a blocker.

### Net-New FRs Assessment

- **FR76, FR77, FR78–FR82** are now full first-class FRs in both PRD and epics — back-propagation since v1 brings these to parity.
- **FR52–FR75** remain epic-defined; PRD references them by number but does not redefine. Same status as v1.

### Coverage Statistics

- **PRD FRs (list-defined):** 58 list-items spanning FR1–FR82 with FR52–FR75 referenced inline only.
- **Epic FRs (list-defined):** 82 (FR1–FR82, contiguous).
- **PRD FRs covered in epics:** 58 / 58 list-items = **100%**.
- **Epic FRs not in PRD's own list:** 24 (FR52–FR75) — same as v1 ("PRD lags epics by 24 FRs").
- **Semantic-drift FRs:** 0 (down from 1 in v1 — FR7 reconciled).
- **Goal-vs-coverage gap (greenfield bootstrap):** 0 covering FRs in v1 → **2 covering FRs in v2** (FR76, FR77). Closed.

### Missing Coverage

🔴 **None blocking.** All v1 critical missing FRs (FR-NEW-A, FR-NEW-B) are now landed as FR76 and FR77 with corresponding stories.

🟡 **Documentation debt:** PRD's own FR list does not redefine FR52–FR75. Same as v1.

---

## Step 4 — UX Alignment

### UX Document Status

✅ **Found and significantly updated since v1.** Canonical: `ux-design-specification.md`. Per-epic wireframes for epics 1, 2, 3, 4, 5, 6, 8, 9.

### v1 → v2 UX Edit Summary

15 edits applied this session:

1. **Mobile editor (Story 3.7) drift** — already reconciled before this session: tablet 768–1279px is review-only; mobile <768px is crisis-recovery editor (Sofia Black Friday journey); desktop ≥1280px is primary authoring. Closes v1's UX↔PRD FR6 conflict.
2. **Direction 6 reframed** — "Guided Creation" is no longer a wizard; it's the StarterTemplateGallery (FR76/Story 3.0) populating the canvas with brand-tokenized governed components.
3. **Journey 3 (First Publish) rewritten** — starter gallery → operator edits → AI Site Builder warm-start completion → publish → celebration. Mermaid diagram replaced.
4. **🆕 StarterTemplateGallery component** added as Phase 1 MLP critical with 4 starter shapes (single-brand B2C, multi-locale B2C, B2B with account portal, B2X multi-context); validates components against tenant's published library; ties to FR76/FR77/Story 3.0.
5. **StorefrontCanvas updated** with "empty" state deep-linking to StarterTemplateGallery via "Start from template" CTA.
6. **AIPanel → CommerceIntelligenceDrawer** with documented dual-mode architecture (Create observes operator edits → completion offer; Optimize surfaces canvas-anchored behavioral recommendations); auto-switches based on data availability.
7. **AIReasoningCard scoped to Create mode** (warm-start completion transparency).
8. **🆕 ConfidenceCard** added for Optimize mode (recommendation + behavioral evidence + expected outcome + confidence + Horizon badge ⚡/📈 + progressive rollout apply with rollback).
9. **Implementation Roadmap updated** — MLP Phase 1 component list reflects new components; Phase 1+ adds ConfidenceCard + Optimize mode.
10. **ACI Plane (entire section) rewritten** from "dedicated MC nav with 3 dashboards" to **canvas-dissolved** (heatmap toggle, engagement score badges, drop-off annotations, hesitation markers) + CommerceIntelligenceDrawer Optimize mode for recommendations + minimal **ACI Inbox** in MC nav for ACI Analyst chronological feed.
11. **🆕 Performance Design Budgets section** added between Visual Design Foundation and Design Direction Decision: NFR1/NFR2/NFR3/NFR4/NFR5/NFR6 budgets with designer's-job column, loading-state pattern table by duration, anti-patterns list. Closes v1's "performance budgets not surfaced in UX spec" finding.
12–15. **Six consistency lints** — `AI panel` / `AIPanel` → `CommerceIntelligenceDrawer` across implementation strategy, feedback patterns, navigation patterns, responsive section, accessibility focus management, accessibility focus trap.

### UX ↔ PRD Alignment

✅ **Aligned (post-v2 edits):**
- Three operator journeys (AI Creation, Direct Edit, First Publish) now reflect FR7 warm-start + FR76 starter gallery.
- ComponentSlot Green/Red Zone maps to FR13–FR15.
- StarterTemplateGallery maps to FR76/FR77.
- CommerceIntelligenceDrawer dual-mode maps to FR7 (Create) + FR56/FR65 (Optimize) + FR9 (reasoning before action).
- ConfidenceCard maps to FR56–FR60 (recommendation panel + Horizon badges + rollback + failure taxonomy).
- ACI canvas-anchored overlays map to FR21–FR27.
- Performance Design Budgets surfaces NFR1–NFR6 for designer use.
- Mobile editor (Story 3.7) responsive section reconciled with FR6 + Sofia Journey 2.

⚠️ **Residual minor drift in UX narrative passages (5 locations):**

| Line | Content | Severity | Recommendation |
|---|---|---|---|
| [93](_bmad-output/planning-artifacts/ux-design-specification.md#L93) | Critical Success Moment: "AI draft → publish in under an hour — Operator describes a campaign page or new storefront; AI generates a governed draft" | 🟡 Minor | Reword to model warm-start: "Operator picks starter template → edits → AI completion offer → publish in under an hour." This was missed in this session's edit pass. |
| [183](_bmad-output/planning-artifacts/ux-design-specification.md#L183) | "Lovable / Bolt / v0 / Framer AI" — "Reverse creation flow: describe → AI assembles → operator refines → publish" | ✅ OK | Historical context describing inspiration tools; cold-start describes Lovable accurately. Leave. |
| [214](_bmad-output/planning-artifacts/ux-design-specification.md#L214) | Anti-Patterns: "Generate-then-explain AI — AI acts first, explains after" | ✅ OK | This is a *do-not-do* anti-pattern — describing it from the cold-start perspective is correct context. Leave. |
| [224](_bmad-output/planning-artifacts/ux-design-specification.md#L224) | Design Inspiration Strategy: "Reverse creation flow: describe → assemble → refine → publish (Lovable)" | ✅ OK | Same — historical inspiration source. Leave. |
| [462](_bmad-output/planning-artifacts/ux-design-specification.md#L462) | Direction 6 row: "Step-by-step wizard, AI generates preview at each step" | ✅ OK | This is the *originally-explored* Direction 6, superseded by the FR76 reframe at L476. Historical context. Leave (the L476 reframe makes the inheritance clear). |
| [587](_bmad-output/planning-artifacts/ux-design-specification.md#L587) | Flow Optimization Principles: "Minimum path to publish = 3 interactions — describe → approve AI reasoning → publish" | 🟡 Minor | Reword to: "Minimum path to publish = 3 interactions — pick starter template → approve completion → publish." Consistent with Journey 1 + Journey 3 rewrites. |

**Net assessment:** L93 + L587 are surface-level minor lints that should be cleaned up in a follow-up pass. The other 3 are historical/contextual and correctly retain cold-start phrasing.

### UX ↔ Architecture Alignment

⚠️ **Architecture is one pivot behind** — this is the same v1 Major issue:
- Architecture's `Core Architectural Decisions` still names Clerk for auth, tRPC for API, `create-next-app` as starter.
- Epics now use MC Custom Application (`@commercetools-frontend/application-shell` v27, `useMcQuery`/`useMcMutation`, `create-mc-app starter-typescript`).
- UX spec's design system foundation references commercetools Merchant Center tokens — consistent with the implemented MC pivot.
- **The UX spec is correctly aligned with the implementation; the architecture document is the lagging artifact.**

### UX Coverage of v1 Goal (Epic 3 → 4 progression)

✅ **Confirmed.** Starter gallery (FR76 / Story 3.0) creates the populated canvas; Story 3.0 hands off cleanly to Epic 4's warm-start completion (FR7). The "zero-to-full-site bootstrap" gap from v1 has explicit UX coverage now.

### UX Warnings

- 🟡 L93 Critical Success Moment phrasing — minor cleanup needed
- 🟡 L587 Minimum-path-to-publish — minor cleanup needed
- ⚠️ Architecture document remains one pivot behind (carries over from v1)

---

## Step 5 — Epic & Story Quality Review

### Epic Quality Assessment (User-Value Focus) — v2 status

| Epic | v1 verdict | v2 verdict | Change |
|---|---|---|---|
| Epic 1 — Platform Foundation & Operator Workspace | ⚠️ Partially technical milestone | ⚠️ Partially technical milestone | Unchanged. Recommendation: explicitly relabel as "Foundation" epic. |
| Epic 2 — Governed Component Library | ✅ Clean | ✅ Clean — **plus Story 2.10 (default platform library, FR77) added** | **Improved.** Story 2.10's 9 ACs cover manifest + schema conformance + WCAG CI gate + immutable publish via Inngest + tenant auto-install + append-only extension semantics + version upgrade with dry-run preview + authoritative source for FR76 + TypeScript type export. Excellent quality. |
| Epic 3 — Storefront Editor & Publishing | ✅ Clean | ✅ Clean — **plus Story 3.0 (Starter Template Gallery, FR76) added** | **Improved.** Story 3.0's 9 ACs cover first-canvas detection + 4 starter cards from CT Custom Objects + library coverage validation + brand-token customization with WCAG contrast checks + transactional instantiation with rollback + CASL gating + audit log + a11y-compliant modal with focus trap. Excellent quality. |
| Epic 4 — AI Site Builder & Migrator | ⚠️ Two value props bundled + circular dep | ⚠️ Two value props bundled (no longer circular) | **Circular dependency CLOSED in v2** via Story 4.12 AC8 + restructured Dependencies. Bundling concern unchanged — Migrator + Site Builder still in one epic. Recommended split-into-4a/4b/4c remains optional. |
| Epic 5 — Behavioral Data Infrastructure | ⚠️ Hybrid epic + prose contradiction | ⚠️ Same | Unchanged. Prose ↔ story-location contradiction (FR21–28 in Epic 5 vs "collection starts at Epic 1" claim) still open. |
| Epic 6 — Enterprise Administration & Compliance | ✅ Clean | ✅ Clean | Unchanged. |
| Epic 8 — AI Experience Engine | ✅ Clean | ✅ Clean | Unchanged. |
| Epic 9 — Physical Retail POS | ⚠️ Research epic, no stories | ⚠️ Research epic, no stories (acceptable) | Unchanged. Pending partner ADR. |

### Epic Independence Check — v2 status

- ✅ **Epic 1 stands alone** — no forward dependency.
- ✅ **Epic 2 → needs Epic 1** — fine.
- ✅ **Epic 3 → needs Epic 1 + Epic 2** — Story 3.0 explicitly depends on Epic 2's Story 2.10 (FR77 default library); narrative now consistent.
- ⚠️ **Epic 4 → needs Epic 1, 2, 3** — same as v1 (no architectural change). Epic 4 stories write to Epic 3's canvas; Migrator paths map into Epic 2's library.
- ⚠️ **Epic 5 prose ↔ story location contradiction** — same as v1 ("behavioral collection starts at Epic 1 project connection — moat begins accumulating before any operator UI is built" still in Epic 5 prose; collection FRs still tracked in Epic 5 stories).
  - **Note:** epics.md line 325 (added in this session per a previous edit pass) clarifies: *"Epic 1 ships the Postgres behavioral events schema only (Story 1.2 AC4). The active collection pipeline (storefront snippet, /api/events ingestion endpoint, ClickHouse behavioral_events table, batching) ships in Epic 5 Story 5.1."* — this **partially closes** the contradiction.
- ✅ **Epic 8 → needs Epic 5 + Epic 4 drawer** — consistent.

### Story-Level Quality — Critical changes since v1

**Story 4.12 — Migration Scaffolded Component Mapping Review** *(rewritten in this session)*

| Aspect | v1 | v2 |
|---|---|---|
| Acceptance Criteria | 7 ACs | **8 ACs** — new AC8 explicitly defines the test fixture set (3 scenarios: happy-path, unmatched-component, field-type-mismatch), the file path (`tests/fixtures/migration-mapping-{frontastic\|nextjs\|monolith}.json`), and the seeding mechanism (`migration/seed-fixtures` Inngest function on `next dev` startup) |
| Dependencies | "Story 4.9 or 4.10 or 4.11 (any migration path), published component library CT Custom Object, Neon branch database" | **Three labelled clauses:** Build deps (fixtures + library + Neon); Forward consumers (4.9, 4.10, 4.11); **Not blocked by:** 4.9, 4.10, 4.11 |
| Cycle status | 🔴 Circular: 4.9/4.10/4.11 → 4.12 → 4.9/4.10/4.11 | ✅ **Acyclic** |

**Verified post-edit dependency graph:**

```
4.1 (CT project connection) ──┐
                              ├──> 4.9  (Frontastic) ─┐
                              ├──> 4.10 (Next.js)    ─┤
                              ├──> 4.11 (Monolith) ──┐│
                              └──> 4.12 ◄────────────┘├──> publishes mappings
fixtures (AC8) ───────────────────> 4.12              │
4.13 ◄────────────────────────────── 4.12 ◄───────────┘
```

✅ **No cycles.** Stories 4.9/4.10/4.11 declare a forward dependency on 4.12 only; 4.12's Build deps cite fixtures (per AC8) — not migration paths. 4.13 depends on 4.12 (forward only).

**Recommended Epic 4 sprint sequence:**
1. Phase 0 (parallel): Story 4.1 + fixture creation (per 4.12 AC8)
2. Phase 1: Story 4.12 ships against fixtures
3. Phase 2: Story 4.13 ships against 4.12's mapping schema
4. Phase 3 (Frontastic-first per Priority Sequencing P2): Story 4.9 wires real data through 4.12 + 4.13
5. Phase 4: Stories 4.10, 4.11 add the other migration paths

### Story-Level Quality — Other v1 issues

| v1 issue | v2 status | Notes |
|---|---|---|
| Story 3.1 XL with 7 ACs (canvas + governance + ARIA + AI tint + WCAG audit) | ⚠️ Same — split-into-3.1a/3.1b recommendation not yet applied | Still high-risk for sprint commitment but not blocking. Can split during Epic 3 sprint planning. |
| Story 3.7 vs UX spec mobile editor conflict | ✅ **Closed** — UX spec defines tablet review-only + mobile <768px crisis-recovery editor + desktop ≥1280px primary | Reconciliation already in UX spec L836–862. |
| Story 3.8 Liveblocks complexity | ⚠️ Same — still L, defer-or-simplify recommendation stands | Not in MVP critical path. |
| Story 3.9 Storefront Branches scope | ⚠️ Same — heavy, post-MVP recommended | Not in MVP critical path. |
| Story 4.3 XL covering entire AI inference pipeline | ⚠️ **Already split** in current stories.md into 4.3a/4.3b/4.3c (edit observation, OpenRouter integration, Zod validation + streaming) | Closed (improvement since v1). |
| FR7 cold-start describe→generate has no implementing story | ✅ **Closed** — PRD now explicitly states cold-start is not supported in MVP; FR76+Story 3.0 own bootstrap | Closed (per PRD L600 + Story 3.0). |

### Cross-Story Coverage Analysis — v2

| Capability | PRD FR | Epic FR Map | Story | v1 Status | v2 Status |
|---|---|---|---|---|---|
| Operator describes intent → AI generates draft from blank canvas | FR7 (PRD v1) | Cold-start removed | None | 🔴 Not implemented | ✅ Deliberately not in MVP — bootstrap by FR76 |
| Operator selects from prefilled site template | FR76 (NEW v2) | Epic 3 — Story 3.0 | Story 3.0 | 🔴 Not in any doc | ✅ Full implementation path |
| Default Day-1 component library | FR77 (NEW v2) | Epic 2 — Story 2.10 | Story 2.10 | 🔴 Gap | ✅ Full implementation path |
| Operator begins editing → AI completes from observed edits | FR7 (epics) | Epic 4 | Stories 4.2, 4.3a/b/c, 4.4–4.7 | ✅ Covered | ✅ Covered + paradigm-aligned |
| Migration from Frontastic | FR34–37 | Epic 4 | Story 4.9 | ⚠️ Circular dep | ✅ Acyclic |
| Migration from Custom Next.js | FR34–37 | Epic 4 | Story 4.10 | ⚠️ Circular dep | ✅ Acyclic |
| Migration from monolith + CWV baseline | FR34–39 | Epic 4 | Story 4.11 | ⚠️ Circular dep | ✅ Acyclic |
| Editor canvas + Green/Red Zone | FR1–FR3, FR15 | Epic 3 | Stories 3.1a/b–3.3 | ✅ Covered | ✅ Covered |
| Mobile editor | FR6 | Epic 3 | Story 3.7 | ⚠️ Conflicted with UX | ✅ Reconciled with UX |

### Quality Findings — v2 Severity Summary

#### 🔴 Critical Violations (block implementation as written)

**None.** All three v1 critical blockers are closed:
- ✅ Zero-to-full-site bootstrap with prefilled templates — FR76 + FR77 + Story 3.0 + Story 2.10 land it
- ✅ Circular dependency in Epic 4 — Story 4.12 AC8 + restructured Dependencies untangle it (graph verified acyclic)
- ✅ FR7 paradigm conflict — PRD + epics + stories all use warm-start completion

#### 🟠 Major Issues (carry-over from v1, severity unchanged)

1. **Architecture document one pivot behind** — still names Clerk/tRPC/`create-next-app`; should rewrite to MC Custom Application + ApplicationShell + `create-mc-app starter-typescript`. Largest remaining drift.
2. **Epic 4 overloaded** — 13 stories, two value props (Site Builder + Migrator). Optional split into 4a/4b/4c remains a recommendation, no longer a blocker.
3. **Story 3.1 XL not yet split** — split-into-3.1a/3.1b recommendation pending. Sprint-planning concern, not blocker.
4. **PRD lags epics by 24 FRs (FR52–75)** — same as v1. Documentation debt; PRD references some by number (FR55, FR61, FR62) inline but does not redefine.
5. **Epic 5 prose ↔ story location** — partially clarified by line 325 addition; could still be tightened.

#### 🟡 Minor Concerns

1. UX spec residual cold-start phrasing at L93 + L587 — surface lints, recommend fixing in next pass
2. Epic 1 user-value framing still thin — relabel as "Foundation" epic
3. Story 3.8 (Liveblocks) and Story 3.9 (Branches) — defer to post-MVP recommendation stands
4. Epic 9 stories pending partner ADR
5. Three migration paths still lean on OpenRouter — compounding LLM-quality risk (mitigation strategy in Epic 4 prose line 361)

---

## Step 6 — Summary and Recommendations

### Overall Readiness Status

🟢 **READY (with documentation debt)**

The three v1 critical blockers are demonstrably closed. The remaining open items are 5 majors and 5 minors — none of them block sprint planning, and most are documentation drift that can be fixed during a single one-sprint sync. Implementation can commence on Epic 1 + Epic 2 immediately; Epic 3 starts in parallel once Story 2.10 (FR77 default library) lands; Epic 4 can begin after Story 4.12 + 4.1 ship.

### v1 → v2 Closure Diff

| v1 Critical Blocker | v2 Status | Evidence |
|---|---|---|
| **Zero-to-full-site bootstrap with prefilled templates has no requirements coverage** | ✅ **CLOSED** | FR76 ([prd.md:660](_bmad-output/planning-artifacts/prd.md#L660)) + FR77 ([prd.md:661](_bmad-output/planning-artifacts/prd.md#L661)) define greenfield bootstrap; Story 3.0 ([stories.md:379](_bmad-output/planning-artifacts/stories.md#L379)) and Story 2.10 ([stories.md:355](_bmad-output/planning-artifacts/stories.md#L355)) implement it; UX spec adds StarterTemplateGallery component + rewrites Journey 3 + reframes Direction 6. |
| **Circular dependency in Epic 4 migration stories** | ✅ **CLOSED** | Story 4.12 AC8 explicitly defines fixture set; Dependencies restructured into labelled clauses (`Build deps:` / `Forward consumers:` / `Not blocked by:`); dependency graph verified acyclic. |
| **PRD ↔ Epics paradigm conflict on FR7 not reconciled** | ✅ **CLOSED** | PRD FR7 + 11 derived edits aligned to warm-start completion; epics.md FR7 statement matches; UX spec Journey 3 + Drawer dual-mode + Direction 6 reframe all consistent; NFR2 reworded. Cross-doc verification confirms no semantic drift. |

### Open Items (5 Major + 5 Minor) — Carry-over and New

| Severity | Issue | Source | Recommended Action |
|---|---|---|---|
| 🟠 Major | Architecture document one pivot behind (Clerk/tRPC/`create-next-app`) | v1 carry-over | One-sprint architecture sync to MC Custom Application + ApplicationShell + `create-mc-app starter-typescript`. **Largest remaining drift.** |
| 🟠 Major | PRD lags epics by 24 FRs (FR52–75 not redefined in PRD list) | v1 carry-over | Back-propagate FR52–75 from epics.md to prd.md FR list. Documentation debt. |
| 🟠 Major | Epic 4 overloaded (Site Builder + Migrator + 3 paths in one epic) | v1 carry-over | Optional split into Epic 4a/4b/4c. Improves shippability; not a blocker. |
| 🟠 Major | Story 3.1 XL not yet split | v1 carry-over | Split into 3.1a (canvas + governance overlay) + 3.1b (keyboard + ARIA + WCAG audit + AI tint). Sprint-planning concern. |
| 🟠 Major | Epic 5 prose ↔ story location partially clarified, not fully | v1 carry-over (improved) | Tighten prose wording; consider moving event collection scaffolding to Story 1.2 explicitly. |
| 🟡 Minor | UX spec L93 + L587 residual cold-start phrasing | NEW (v2 lint) | 2-line cleanup pass; both are surface lints that contradict the warm-start reconciliation. |
| 🟡 Minor | Epic 1 user-value framing thin | v1 carry-over | Relabel as "Foundation" epic so the technical-milestone framing is intentional. |
| 🟡 Minor | Story 3.8 Liveblocks complexity for MVP | v1 carry-over | Defer or simplify for MVP. Not blocking. |
| 🟡 Minor | Story 3.9 Storefront Branches scope heavy | v1 carry-over | Defer to post-MVP. Not blocking. |
| 🟡 Minor | Epic 9 stories pending partner ADR | v1 carry-over | Acceptable for research epic; flag in epic prose remains. |

### Recommended Next Steps (Priority Order)

1. **🟠 Architecture sync** *(largest remaining drift — recommended next session)* — rewrite `architecture.md` Core Architectural Decisions to reflect MC Custom Application pivot. The document is the only artifact still describing the pre-pivot stack; epics, stories, and UX spec are all aligned to the implemented architecture.

2. **🟡 UX spec cleanup pass** *(2-line fix)* — update L93 Critical Success Moment and L587 Minimum-path-to-publish to reflect warm-start completion + starter template flow. Quick win; closes the only NEW v2 finding.

3. **🟠 PRD FR back-propagation** *(documentation debt sprint)* — add FR52–FR75 as explicit list-items to prd.md. The cross-references inside FR78/FR82 work today; making them first-class brings the PRD to FR parity with epics.

4. **Optional refinements (not blocking implementation):**
   - Split Story 3.1 → 3.1a + 3.1b
   - Consider Epic 4 split into 4a/4b/4c
   - Relabel Epic 1 as "Foundation"
   - Tighten Epic 5 prose

### Implementation Sequencing — v2 Recommendation

Implementation can begin now with this order:

**Phase A (parallel — Foundation)**
- Epic 1 stories 1.1–1.7
- Epic 2 stories 2.1–2.10 (Story 2.10 = FR77 default library)

**Phase B (depends on Phase A)**
- Epic 3 Story 3.0 (Starter Template Gallery, depends on Epic 2 Story 2.10)
- Epic 3 stories 3.1a/3.1b–3.6 (canvas + governance + publish)
- Epic 4 Story 4.1 (CT project connection)
- Epic 4 fixture creation (per Story 4.12 AC8) — **parallel with 4.1**

**Phase C (depends on Phase B)**
- Epic 4 Story 4.12 (Migration Review UI — fixture-driven)
- Epic 4 Story 4.13 (Migrated Page Validation)
- Epic 5 Story 5.1 (Behavioral Event Collection Pipeline)

**Phase D (depends on Phase C)**
- Epic 4 Stories 4.2/4.3a/b/c/4.4–4.7 (AI Site Builder warm-start completion)
- Epic 4 Story 4.9 (Frontastic migration — first per P2)
- Epic 5 Stories 5.2–5.12 (ACI + CDP co-exist)
- Epic 6 (Enterprise Admin)

**Phase E (depends on Phase D)**
- Epic 4 Stories 4.10, 4.11 (Custom Next.js + Monolith migrations)
- Epic 8 (AI Experience Engine — Optimize mode)
- Epic 9 (POS — pending partner ADR)

### Final Note

This v2 assessment identified **5 major + 5 minor open items, 0 critical blockers**. All three v1 critical blockers are demonstrably closed across PRD, UX spec, epics, and stories. The remaining open items are mostly documentation debt — fixable in a single one-sprint sync without blocking implementation.

The plan is **READY for sprint planning and implementation kickoff**. The recommended next move is the architecture document sync (largest remaining drift), followed by the 2-line UX spec cleanup and the PRD FR back-propagation. After those, the readiness state will be 🟢 fully READY with no documentation debt.

---

**Assessor:** John (Product Manager) — bmad-check-implementation-readiness workflow (v2 verification re-run)
**Date:** 2026-05-12
**Focus:** Confirm closure of v1 blockers; surface drift from closing edits
**Comparison baseline:** [implementation-readiness-report-2026-05-12.md](_bmad-output/planning-artifacts/reports/implementation-readiness-report-2026-05-12.md) (v1)


