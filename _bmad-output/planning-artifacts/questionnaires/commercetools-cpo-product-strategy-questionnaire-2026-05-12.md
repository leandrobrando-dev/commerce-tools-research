---
type: strategic-conversation-questionnaire
counterparty: commercetools — CPO (Chief Product Officer)
date: 2026-05-12
author: Mary (Business Analyst)
purpose: Pre-conversation prep + structured questions for a product-strategy discussion with commercetools' CPO. Outcomes pursued: (1) precisely scope what commercetools will build vs partner for in AI / operator-tooling / experimentation; (2) test the MC Custom Application architecture as the canonical extension pattern; (3) understand customer-feedback themes that drive their roadmap; (4) probe Agentic Jumpstart's downstream evolution; (5) clarify the storefront-authoring boundary specifically.
related_artifacts:
  - _bmad-output/planning-artifacts/research/market-golden-path-architecture-cdp-positioning-research-2026-05-12.md
  - _bmad-output/planning-artifacts/commercetools-ceo-strategic-conversation-questionnaire-2026-05-12.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/prd.md
suggested_format: "60–75 minute working session, virtual preferred (architecture-level questions benefit from screen-sharing). Technical conversation; expect deep dives. Off-the-record framing welcome."
---

# Strategic Conversation Questionnaire — commercetools CPO

## 0 · Pre-Conversation Framing

### Why we're talking

The CPO conversation is where the product-strategy detail lives. The CEO conversation establishes whether commercetools' direction collides or complements ours; the CPO conversation establishes **exactly where the boundaries are** — which capabilities they're shipping, which they're explicitly leaving to partners, and what the technical patterns are for ISV co-existence. Per our market research (2026-05-12), **the single highest-stakes question is whether commercetools intends to ship a storefront-authoring product themselves**. Most public signals say no — Agentic Jumpstart, AgenticLift, and Cora AI all sit at adjacent surfaces — but the CPO is the person who actually decides this.

### Hypotheses we want to test

1. **commercetools' product roadmap explicitly excludes operator-driven storefront authoring** — this is partner-territory by design.
2. **MC Custom Application + Connect packaging is the canonical extension pattern** for ISVs in 2026–2027; ApplicationShell investment is sustained.
3. **commercetools' AI investment is concentrated on Agentic Jumpstart + Cora + AgenticLift** — operator-facing AI in Merchant Center is Cora's scope; storefront-side AI is partner-territory.
4. **CDP layer is explicitly delegated to partners** (consistent with Foundry docs); commercetools will not build a CDP component.
5. **Top customer-feedback themes that drive roadmap include time-to-go-live, frontend velocity, and AI-readiness** — frontend velocity is the most commonly under-served need.

### Pre-conversation prep

Before the meeting, confirm the following:

- Current CPO and tenure ([Shiri Mosenzon Erez](https://commercetools.com/about-us) is the CPO per recent press; verify if changed)
- Recent product-launch announcements (last 90 days): Agentic Jumpstart (Nov 2025), AgenticLift + Cora AI (NRF 2026), any post-NRF launches
- Public statements / interviews / podcast appearances on roadmap, AI, partnerships within last 6 months
- Any commercetools developer documentation updates relevant to MC Custom Application architecture (`@commercetools-frontend/application-shell` major-version bumps, Connect packaging changes, `entryPointUriPath` changes)

### Conversation tone guidance

Technical and product-strategic. **The CPO will respect specificity** — come prepared with concrete architectural references (MC Custom App pattern, ApplicationShell v27, `useMcQuery`/`useMcMutation`, `oAuthScopes`, FlopFlip feature flags, CT Custom Objects). Demonstrate that we've architected against their canonical patterns; this is not a generic ISV asking for guidance, this is a sophisticated partner asking informed questions. Pitch is not appropriate here either — share architectural reasoning, not feature lists.

---

## 1 · Storefront / Frontend Strategy — The Boundary Question

### Section purpose

This section is the most important. Pin down whether operator-driven storefront authoring is in or out of scope for commercetools' own roadmap. Get specifics, not generalities.

### Questions

1. **Operator-driven storefront authoring — drag-and-drop canvas, governed component library, AI-assisted page completion — has been an open category in the commercetools ecosystem for years. Is there a product roadmap item where commercetools ships that capability natively, or is it explicitly partner-territory?**
   - *Hypothesis being tested:* explicitly partner-territory.
   - *What we learn:* **the single most important answer in the entire conversation.** Direct answer either green-lights our positioning or surfaces a roadmap collision.
   - *Follow-up if answer is hedged:* "What would have to change in the market for that to flip — would it be a customer-feedback signal, a competitive move, or a technology shift?"

2. **Frontastic was acquired in 2022 and the integration was completed by 2024–2025. Frontastic Studio's tastic / page-composition surface had operator-authoring DNA. When you decided what to keep and what to retire from Frontastic Studio, what was the strategic logic?**
   - *Hypothesis being tested:* commercetools kept the headless commerce primitives (Frontastic-flavored APIs, Studio backend) but did not double down on the operator-facing authoring UX.
   - *What we learn:* signals on whether storefront authoring is an active or dormant ambition.

3. **Looking at the Solution Hub today, the Personalisation, CMS/DXP, and PIM categories have many partners but no clear category leader for "AI-native operator storefront authoring." Is that a gap commercetools intends to fill via marketplace (an ISV becomes the leader), or via product (you ship something native), or is it not seen as a gap?**
   - *Hypothesis being tested:* gap intentionally filled via marketplace partner, not via native product.
   - *What we learn:* whether the marketplace path is the right one for us, and whether commercetools would actively support a designated ISV.

---

## 2 · Agentic Jumpstart, Cora, AgenticLift — Capability Boundaries

### Section purpose

Map exactly what each product does and what they explicitly DON'T do. The boundaries between Agentic Jumpstart's AI Hub, Cora AI's operator assistance, and AgenticLift are not fully clear from public docs.

### Questions

4. **Agentic Jumpstart launched with AI Hub + Agent Gateway. Six months in, what surprised you about how customers are using it? What use cases emerged that weren't in the original product brief, and what didn't land that you expected to?**
   - *Hypothesis being tested:* discovery + check-out via AI agents is delivering; deeper personalization or content workflows haven't emerged.
   - *What we learn:* the lived feedback loop on Agentic Jumpstart's scope.

5. **Cora AI is positioned as an operator-side AI assistant for Merchant Center, with Vertex-powered intelligent search. How do you see Cora's scope evolving — is it primarily query / answer / search, or are you investing in agentic workflows where Cora takes actions on behalf of the operator?**
   - *Hypothesis being tested:* Cora stays in query/search/insight territory in 2026; agentic-workflow Cora is 2027+.
   - *What we learn:* whether Cora and our AI Site Builder will eventually overlap. **Material question.**

6. **AgenticLift was announced as a "standalone agentic offering." How does it fit alongside Agentic Jumpstart — is AgenticLift the lighter-weight SKU, the verticalized offering, or something else? What's the customer profile that picks AgenticLift over Jumpstart?**
   - *Hypothesis being tested:* AgenticLift is packaging differentiation, not a new product surface.
   - *What we learn:* the breadth of commercetools' agentic-commerce SKU strategy.

7. **The protocols Agentic Jumpstart supports — MCP (Model Context Protocol), A2A, AP2 (Google Agent Payments), ACP (Agentic Commerce Protocol with OpenAI/Stripe) — represent strong bets. Of those, which is the most strategically important to commercetools, and where do you see the standards landscape consolidating in the next 12 months?**
   - *Hypothesis being tested:* ACP (OpenAI/Stripe co-developed) is the most strategically locked-in; the others are insurance bets.
   - *What we learn:* the protocol-level alignment we should architect against.

---

## 3 · MC Custom Application + Connect Packaging — Extension Pattern

### Section purpose

Validate that the MC Custom App pattern is canonical and supported long-term. Probe ApplicationShell investment, version stability, and any breaking-change risk.

### Questions

8. **The MC Custom Application pattern — `@commercetools-frontend/application-shell` v27 + Connect packaging + `mcAccessToken` HttpOnly cookie + `useMcQuery`/`useMcMutation` + FlopFlip — has emerged as the canonical ISV extension pattern. Is this architecture stable for the next 18–24 months, or is there a migration / major-version transition planned?**
   - *Hypothesis being tested:* stable for 18–24 months; ApplicationShell v28 is on the horizon but backward-compatible.
   - *What we learn:* confidence in our architectural baseline (per ADR-003 in our architecture document).

9. **For ISVs building MC Custom Apps, what's the most common architectural mistake or anti-pattern you see — something that gets shipped and then has to be re-architected because it ignored a Connect / ApplicationShell convention?**
   - *Hypothesis being tested:* re-implementing auth (Clerk-instead-of-MC-session), reimplementing Apollo/Redux/i18n that ApplicationShell already provides, or skipping `entryPointUriPath` configuration patterns.
   - *What we learn:* what NOT to do — direct input into our architecture decisions.

10. **The Connect packaging model — `connect.yaml` with `merchant-center-custom-application` + `service` + `event` types — is recent. Is there active investment in the Connect runtime, or is it stable infrastructure? Are there `service` / `event` patterns you wish ISVs used more?**
    - *Hypothesis being tested:* Connect is being actively invested in; commercetools wants more `event` subscribers (Subscriptions API), fewer `service` overcomplications.
    - *What we learn:* the right pattern for our async work (AI inference, behavioral ingestion, experimentation).

11. **Does commercetools have a specific posture on ISVs that ship browser-side scripts onto live storefronts? The Custom Application runs inside Merchant Center, but the storefront layer is downstream. Are there guardrails or recommendations for ISVs that want to instrument the storefront — especially around Core Web Vitals, consent, and the Red Zone / governed-checkout boundary?**
    - *Hypothesis being tested:* commercetools is increasingly opinionated about checkout-flow integrity (PCI scope) and storefront performance; expects ISVs to coordinate.
    - *What we learn:* the platform's appetite for our SDK's footprint on the storefront. Direct input to Epic 5 (Behavioral Data Infrastructure) story scope.

---

## 4 · Data / CDP / Identity — The Boundary Question (Layer Two)

### Section purpose

Test whether commercetools' Foundry guidance ("the CDP is the obvious place where customer records are mastered") is durable, or whether commercetools intends to bring CDP-like features native.

### Questions

12. **commercetools' Foundry documentation explicitly delegates customer mastering to "the CDP" when one exists. Is that an active architectural opinion, or a default that could shift if a CDP-leader gap emerges in your customer base?**
    - *Hypothesis being tested:* active and durable opinion — composable thesis applies to data-mastering as well as commerce-mastering.
    - *What we learn:* whether identity resolution / CDP-like features are off the roadmap, or just deprioritized.

13. **The CDP category is splintering — Adobe RT-CDP and Salesforce Data Cloud at one end (suite-bundled), RudderStack and Snowplow at the other (warehouse-first, dev-led). When you see commercetools customers on each path, do you observe one path leading to better commerce outcomes than the other?**
    - *Hypothesis being tested:* warehouse-first / dev-led CDPs (RudderStack, Snowplow, Hightouch) align better with the composable thesis; suite-bundled CDPs come with suite-bundled commerce platforms (Adobe Commerce, Commerce Cloud) that compete with commercetools.
    - *What we learn:* whether commercetools has a soft preference signal for our co-exist partnership lane.

14. **For an ISV building experimentation + behavioral analytics on commercetools, what's the canonical pattern for behavioral-event capture? Should we (a) ship our own client-side SDK, (b) accept events from the customer's CDP via destination adapter, or (c) consume commercetools Subscriptions for commerce events and let the CDP handle pre-purchase behavior?**
    - *Hypothesis being tested:* commercetools recommends (c) — Subscriptions for commerce events; pre-purchase behavior is partner / ISV territory; (a) and (b) are both acceptable depending on the ISV's positioning.
    - *What we learn:* validation of our pre-mortem decision (own SDK + CDP source-adapters + commercetools Subscriptions direct for commerce events).

---

## 5 · Customer Feedback & Roadmap Pressure

### Section purpose

Surface what commercetools customers are actually asking for that's not yet on the roadmap. The gaps tell us where ISV traction is highest.

### Questions

15. **Of the asks you hear from large enterprise customers in QBRs and roadmap reviews, which three come up most consistently — and which of those is hardest for commercetools to deliver natively, making it most likely to land with a partner?**
    - *Hypothesis being tested:* frontend velocity / time-to-market, AI-driven authoring, and unified analytics are the top asks; frontend velocity is hardest for commercetools to deliver natively.
    - *What we learn:* high-leverage signal on which ISV problem we should prioritize most heavily. **Material question.**

16. **What's the single roadmap conflict — the priority tradeoff that's most contentious internally — that you'd want external perspective on? (Asked carefully; the goal is to surface a real strategic question, not extract proprietary roadmap detail.)**
    - *Hypothesis being tested:* ambiguous; useful answer is information-rich either way.
    - *What we learn:* a real product-strategy puzzle commercetools is actively wrestling with — useful for both relationship-building and our own scenario planning.

17. **Has the rise of agentic commerce shifted the customer-feedback themes you hear? Are operators starting to ask "how do I make my storefront discoverable to AI agents," and if so, what's the roadmap response?**
    - *Hypothesis being tested:* yes — that's exactly why Agentic Jumpstart launched; the next ask is "how do I make my storefront *better* in front of AI agents," which is downstream-of-storefront-authoring (our scope).
    - *What we learn:* whether the agentic commerce wave is creating natural pull for storefront-experience platforms like ours.

---

## 6 · Partnership Mechanics

### Section purpose

Understand the concrete mechanics of becoming a recognized ISV partner — beyond marketplace listing, what does deep partnership look like?

### Questions

18. **Beyond marketplace listing, what does the deepest tier of ISV partnership with commercetools look like? Are there structures — early-access to roadmap, joint customer pilots, technical advisory boards, co-engineering — that you offer to ISVs delivering on a strategic gap?**
    - *Hypothesis being tested:* yes — there's a tiered partnership structure with early-access, joint-pilots, and technical-advisory tiers; access is gated on customer references + technical certification + co-marketing.
    - *What we learn:* the concrete steps from marketplace-listed to deep-partnership status.

19. **Of the SI partners launching Agentic Jumpstart — Accenture/Song, EPAM, Orium, Valtech — do any of them currently have a frontend-authoring or experimentation product offering that they sell alongside their services delivery?**
    - *Hypothesis being tested:* Orium and Valtech have the most pre-built IP; Accenture and EPAM lean on services delivery. None has a clear AI-storefront-authoring offering today.
    - *What we learn:* which SI partner is the most natural channel for us, and whether any has competing IP we'd need to navigate.

---

## 7 · Closing — Vision & Follow-Up

### Questions

20. **Where do you want commercetools' product surface to land 3 years from now — what's the strongest version of the product you're building toward?**
    - *Hypothesis being tested:* the answer surfaces what they consider native vs partner-territory in the long run.
    - *What we learn:* durable scope boundaries.

21. **If we're successful in landing on the marketplace as the AI-storefront-authoring + experimentation ISV, what would 'great' look like from your seat — what behaviors and outcomes would tell you we'd done it right? What would tell you we'd done it badly?**
    - *Closing move:* invites the CPO to articulate success criteria for our partnership; gives us a decision framework rather than a pitch response.

### Optional ask (only if natural opening appears)

> *"As we build, we'd value the chance to share architectural reviews and roadmap alignment with the commercetools product team — even informally. Is there a working session, advisory board, or design-partner program that supports that for ISVs at our stage?"*

---

## 8 · What to Listen For (Beyond the Answers)

| Signal | What it tells us |
|---|---|
| CPO **specifies the storefront-authoring boundary clearly** in Q1 — names it as partner-territory | Our positioning is safe; proceed with confidence |
| CPO **hedges** on Q1 ("we're considering...") or pivots to Cora's roadmap when answering | Storefront authoring is closer to native than public docs suggest; **highest-priority risk to track** |
| CPO **recommends specific architectural patterns** in Sections 3 and 4 — concrete answers about Subscriptions, ApplicationShell, Connect | High-trust technical conversation; long-term partnership-relevant |
| CPO **demurs on roadmap detail** ("we don't share that publicly") even on simple questions | Relationship is at marketplace-arms-length; deeper partnership needs more proof |
| CPO names **specific customers or partners** in the answers | Conversation has crossed an informality threshold; relationship is warming |
| CPO references **internal debates** (Q16) | Real product-strategy candor; conversation is going well |
| CPO redirects to **Solution Hub team / partner program manager** for Q18 | Partnership mechanics are real and structured; follow-up has a clear next step |

## 9 · Post-Conversation

Within 24 hours of the conversation:

1. Capture verbatim quotes for any answer to the boundary questions (Q1, Q5, Q12)
2. Update the strategic synthesis (`market-golden-path-architecture-cdp-positioning-research-2026-05-12.md`) Section 5 (Threat / Partnership Map) with new evidence
3. If Q1 answer was hedged, immediately escalate this as the primary risk and adjust roadmap accordingly
4. If Q19 answer named a competing SI offering, adjust channel-partner targeting
5. Send a personal thank-you note within 48 hours; reference one specific architectural detail from the conversation to demonstrate signal-quality reception

---

## 10 · Cross-Conversation Coordination with the CEO Conversation

If both CEO and CPO conversations occur within the same 30-day window, **coordinate the question sets to avoid duplication and to triangulate answers:**

- Reserve the **strategic-vision questions** (5-year framing, M&A appetite, suite competition) for the CEO conversation
- Reserve the **product-roadmap detail and architectural depth** for the CPO conversation
- Ask the **storefront-authoring boundary question (Q1) of both** — triangulating the answer is the highest-value cross-check in the entire program
- Ask the **CDP / data-layer question (Q12, Q14) of CPO only** — too detailed for CEO
- Ask the **AI scope question (CEO Q7 + CPO Q5)** of both — different framing, same hypothesis

If the CPO conversation comes first, use the answers to **refine** the CEO questionnaire — drop questions whose answers are already known and substitute deeper strategic-frame questions.

---

*Prepared by Mary, Business Analyst, 2026-05-12. This is a substantive technical-strategic conversation; the CPO will respect a focused 8–10 question deep-dive over a wider but shallower set. Optimize for boundary-question precision (Q1, Q5, Q12, Q14, Q15) over breadth.*
