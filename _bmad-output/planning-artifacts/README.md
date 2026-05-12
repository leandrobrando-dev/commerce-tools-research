# Planning Artifacts — Index

This directory holds the planning artifacts for the **commercetools Next-Gen Frontend** project. Source-of-truth documents (Markdown) live alongside their typed companions; rendered HTML twins and HTML-native artifacts live under `html/`.

**Last reorganized:** 2026-05-12

---

## Layout

```
planning-artifacts/
├── README.md                             ← this file
│
├── prd.md                                ← canonical PRD
├── architecture.md                       ← canonical architecture
├── epics.md                              ← canonical epics
├── stories.md                            ← canonical stories
├── ux-design-specification.md            ← canonical UX spec
│
├── briefs/                               ← product briefs, elevator pitch, interview narratives, 30-60-90
├── research/                             ← market + technical research artifacts
├── decisions/                            ← ADRs
├── reports/                              ← implementation readiness reports
├── competitive/                          ← competitive analyses
├── questionnaires/                       ← exec / discovery conversation prep
│
└── html/                                 ← all HTML twins + HTML-native artifacts
    ├── 00-bmad-journey-map.html          ← front door — start here
    ├── doc-reader-styles.css             ← shared stylesheet
    ├── _doc-reader-header.html           ← build-time scaffold template
    ├── _doc-reader-footer.html           ← build-time scaffold template
    │
    ├── prd.html / architecture.html / epics.html / stories.html / ux-design-specification.html
    ├── adr-002-positioning-amplitude-statsig.html
    ├── implementation-readiness-report-2026-05-05.html
    ├── competitive-analysis-...-2026-05-11.html
    ├── competitive-comparison-amplitude-statsig.html
    ├── ux-design-directions.html
    ├── interactive-prototype.html
    ├── org-chart-12month-2026-05-05.html
    ├── epic-{1,2,3,4,5,6,8,9}-...-wireframes.html
    │
    ├── briefs/                           ← mirrors planning-artifacts/briefs/
    └── research/                         ← mirrors planning-artifacts/research/
```

## Conventions

- **Markdown is source of truth.** Every `.md` here drives the corresponding `.html` (when one exists). Edit MDs; HTMLs are rendered.
- **Canonical specs live at the root** — PRD, architecture, epics, stories, UX spec. These are the documents the team works in daily.
- **Typed subdirectories** group supporting material so the root stays readable.
- **HTMLs are self-contained renderers.** Each `.html` embeds its source markdown inline in a `<script type="text/markdown">` tag, so any HTML can be opened directly in a browser without a build step. The shared `doc-reader-styles.css` provides typography and the `00-bmad-journey-map.html` is the navigation hub.

## What lives where

| Directory | What | Examples |
|---|---|---|
| `briefs/` | Strategic narrative — vision documents, pitches, interview narratives | `product-brief-...`, `elevator-pitch-...`, `30-60-90-day-plan-...` |
| `research/` | Market + technical research that informs PRD scope and positioning | `market-ai-native-...`, `market-golden-path-...`, `technical-commercetools-frontend-...` |
| `decisions/` | Architecture Decision Records — durable strategic decisions with rationale | `adr-002-positioning-amplitude-statsig.md` |
| `reports/` | Periodic assessments — readiness checks, retros, status snapshots | `implementation-readiness-report-2026-05-05.md`, `...-2026-05-12.md` |
| `competitive/` | Vendor and category competitive analyses | `competitive-analysis-site-builders-behavioral-analytics-ab-testing-2026-05-11.md` |
| `questionnaires/` | Conversation prep for strategic / discovery / partnership meetings | `commercetools-ceo-strategic-conversation-questionnaire-...`, `commercetools-cpo-product-strategy-questionnaire-...` |
| `html/` | Rendered HTML twins of MD sources + HTML-native artifacts (wireframes, prototype, journey map) | All `.html` files; the navigation hub at `html/00-bmad-journey-map.html` |

## Navigation

- **Start at [`html/00-bmad-journey-map.html`](html/00-bmad-journey-map.html)** for the visual journey through the planning artifacts. It links to every rendered HTML doc.
- **For source editing:** open the canonical `.md` files at the root.
- **For deep context:** read the briefs first, then the research, then the PRD/architecture/epics/stories.

## When HTMLs are rendered

There is no automated pipeline that regenerates HTMLs on every MD edit (yet). Some HTMLs may lag behind their MD sources after edits. Where a divergence matters, the MD is authoritative. Manual HTML regeneration is performed periodically.

**Known lagging HTMLs (as of 2026-05-12):** `prd.html`, `epics.html`, `stories.html`, `architecture.html` — all reflect 2026-05-08 content; the MDs were updated 2026-05-12. UX spec HTML still matches.

## Conventions for new artifacts

- **Naming:** lowercase-kebab-case, ending in date `-YYYY-MM-DD` for time-stamped artifacts (research, reports, competitive analyses, questionnaires)
- **Frontmatter:** YAML at the top of every MD; include `type`, `date`, `author`, and `inputDocuments` when relevant
- **Cross-references:** use full project-relative paths (`_bmad-output/planning-artifacts/<dir>/<file>.md`) in frontmatter; use relative links in body prose where natural
- **Rendered HTMLs:** when adding a new MD with a paired HTML, place the MD in its typed directory and the HTML at the corresponding location under `html/`
