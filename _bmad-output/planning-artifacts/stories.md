---
generatedDate: "2026-05-05"
inputDocuments:
  - "_bmad-output/planning-artifacts/epics.md"
  - "_bmad-output/planning-artifacts/prd.md"
  - "_bmad-output/planning-artifacts/architecture.md"
epicsIncluded: [1, 2, 3, 4, 5, 6, 8]
status: "complete"
---

# Tutorial - User Stories

## Epic 1: Platform Foundation & Operator Workspace

### Story 1.1: MC Custom Application Scaffold & Connect Packaging

**As a** platform IT Admin
**I want** a fully scaffolded MC Custom Application deployed via commercetools Connect into Merchant Center
**So that** the platform is accessible as a native Merchant Center application without any external authentication or separate login flow

**Acceptance Criteria:**
1. The application is bootstrapped using `create-mc-app` with the TypeScript template; the root component wraps the entire application in `<ApplicationShell>` from `@commercetools-frontend/application-shell` v27, with `applicationName`, `entryPointUriPath`, and `cloudIdentifier` props correctly set from environment variables.
2. A valid `connect.yaml` is present at the repository root, declaring at minimum one `merchant-center-custom-application` deployment type (with `entryPointUriPath` matching the env var) and one `service` deployment type; the file passes `ct-connect validate` with zero errors.
3. `custom-application-config.mjs` exports a configuration object with `entryPointUriPath`, `cloudIdentifier`, `env.production.url`, and `oAuthScopes` referencing at minimum `manage_products`, `manage_customers`, `manage_orders`, and a platform-specific custom scope (`manage_nextgen_platform`); the config is consumed by ApplicationShell at runtime.
4. The application renders the Merchant Center top navigation bar and left-side nav with at minimum two route entries ("Dashboard" and "Component Library") when accessed at the `entryPointUriPath`; navigation between routes does not trigger full-page reloads.
5. A `Dockerfile` (or Vercel/serverless config) and CI job exist that build the custom application, run `mc-scripts build`, and produce a deployable artifact; the artifact URL is injected into `connect.yaml` as the `url` for the `merchant-center-custom-application` deployment type.
6. TypeScript strict mode (`"strict": true`) is enabled in `tsconfig.json`; `npm run typecheck` exits 0 on the initial scaffold with no suppressions.
7. A local development flow (`npm run start`) starts the app with `mc-scripts start`, proxying to a Merchant Center staging environment using `MC_API_URL`; developers can sign in with Merchant Center credentials and see the custom application routes without any additional auth step.
8. The `entryPointUriPath` is environment-specific and is validated at startup; the application throws a clear configuration error and refuses to render if `entryPointUriPath` is undefined.

**Dependencies:** None
**FRs Covered:** FR40
**Complexity:** XL

---

### Story 1.2: Multi-tenant PostgreSQL Schema with RLS

**As a** platform operator
**I want** all platform data stored in a multi-tenant PostgreSQL database with Row-Level Security enforced at the database layer
**So that** tenant data is strictly isolated even if application-layer bugs occur, and behavioral events are captured from day one

**Acceptance Criteria:**
1. A Neon PostgreSQL project is provisioned with a `main` branch; Prisma (`prisma/schema.prisma`) defines all tables with a non-nullable `tenant_id UUID NOT NULL` column; a composite index on `(tenant_id, id)` exists on every tenant-scoped table; `prisma migrate deploy` runs without errors on the Neon `main` branch.
2. A PostgreSQL Row-Level Security policy is enabled on every tenant-scoped table via `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`; a `USING (tenant_id = current_setting('app.current_tenant_id')::UUID)` policy is applied; direct `psql` queries without setting `app.current_tenant_id` return zero rows for all tenant tables.
3. A Prisma middleware (or `$extends` query extension) automatically calls `SET LOCAL app.current_tenant_id = '<tenantId>'` within every transaction before any query executes; the `tenantId` is derived from the authenticated MC session context; no application-layer query is permitted to omit the tenant context.
4. The `behavioral_events` table is defined in the Prisma schema with columns: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`, `tenant_id UUID NOT NULL`, `session_id TEXT`, `component_id TEXT`, `event_type TEXT NOT NULL`, `payload JSONB`, `occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()`; a range partition on `occurred_at` (monthly) is applied; writes to this table succeed from day 1.
5. A `tenants` table exists with `id UUID PRIMARY KEY`, `ct_project_key TEXT UNIQUE NOT NULL`, `name TEXT`, `created_at TIMESTAMPTZ DEFAULT now()`; a seeding script (`prisma/seed.ts`) inserts a default dev tenant and can be run with `npx prisma db seed`.
6. All Prisma migrations are idempotent and applied via `prisma migrate deploy` (not `migrate dev`) in production; a `prisma/migrations` directory with timestamped migration files exists; running migrations twice does not produce errors or duplicate policies.
7. A Prisma `$disconnect` call is wired to the Next.js process shutdown handler; connection pooling is configured via `DATABASE_URL` pointing to a PgBouncer-compatible Neon pooled connection string with `?pgbouncer=true&connection_limit=1` in serverless contexts.
8. A database health-check endpoint (`GET /api/health/db`) executes `SELECT 1` via Prisma and returns `{ status: "ok" }` within 500 ms.

**Dependencies:** Story 1.1
**FRs Covered:** FR40
**Complexity:** L

---

### Story 1.3: CASL RBAC & ApplicationShell Permission Integration

**As a** platform IT Admin
**I want** role-based access control enforced throughout the application using CASL 6.x permissions derived from the authenticated user's MC OAuth scopes
**So that** Storefront Developers, Operators, and IT Admins each see only the features and actions they are authorized to perform, with no client-side bypass possible

**Acceptance Criteria:**
1. A CASL `AbilityBuilder` factory (`src/permissions/ability.ts`) accepts an array of MC `oAuthScopes` (extracted from the ApplicationShell `useApplicationContext().permissions` hook) and returns a typed `AppAbility` instance; roles map: `manage_nextgen_platform` grants Admin, `manage_products` grants Developer, `view_products` grants Operator; role-to-ability mappings are unit tested with 100% branch coverage.
2. The `AppAbility` instance is provided application-wide via a React context (`AbilityContext`) using CASL's `createContextualCan`; the `<Can>` component is exported from `src/permissions/Can.tsx` and wraps every permission-gated UI element.
3. Server-side API route handlers validate the CASL ability on every mutating request; the service extracts the `mcAccessToken` from the `Authorization: Bearer` header, decodes the project key, resolves the tenant, and re-derives the `AppAbility` before executing any database write; unauthorized requests return HTTP 403 with `{ error: "Forbidden", requiredAbility: "..." }`.
4. A `useAbility()` hook is exported from `src/permissions/hooks.ts`; it memoizes the ability instance so it does not reconstruct on every render.
5. At least the following subject types are defined: `ComponentLibrary`, `ComponentSchema`, `Page`, `Workspace`, `BehavioralEvent`, `Tenant`; each subject has a corresponding Prisma model; TypeScript compilation fails if an unknown subject is referenced in `<Can>`.
6. An integration test mounts the application shell in a mocked MC context with `view_products` only scope and asserts that "Create Component" and "Publish" buttons are not present in the DOM; the same test with `manage_nextgen_platform` scope asserts both buttons are present.
7. CASL ability definitions are stored as a versioned constant in `src/permissions/roles.ts`; changing a role definition triggers a TypeScript error if any existing `<Can>` usage references a removed action/subject pair.

**Dependencies:** Story 1.1
**FRs Covered:** FR42
**Complexity:** L

---

### Story 1.4: MC Session Auth & Role Assignment

**As an** IT Admin
**I want** to assign platform roles to Merchant Center team members and have those roles enforced via the MC session auth cookie
**So that** no separate identity provider or login screen is needed, and role management is consolidated in Merchant Center

**Acceptance Criteria:**
1. The application reads the authenticated user identity exclusively from the `useApplicationContext()` hook provided by `@commercetools-frontend/application-shell`; the `mcAccessToken` HttpOnly cookie is never accessed directly from JavaScript; any attempt to read `document.cookie` for auth purposes fails a lint rule.
2. A "Role Assignment" UI page (accessible to Admin CASL ability only) lists all Merchant Center team members fetched via `useMcQuery`; each member row displays their current platform role (stored in a CT Custom Object keyed by `container: "nextgen-platform-roles"`, `key: "{userId}"`) and a dropdown to change it.
3. Role changes are persisted by a `useMcMutation` call that writes to the CT Custom Object (`value: { role: "Admin" | "Developer" | "Operator" }`); the mutation is optimistic-updated in the UI and rolls back on error with a `<Notification>` from `@commercetools-frontend/ui-kit`.
4. On application load, the `AbilityBuilder` reads the current user's role from the CT Custom Object and merges it with `oAuthScopes` from `useApplicationContext()`; a user with `manage_products` scope but an Operator Custom Object role receives only Operator abilities.
5. Session expiry is handled by ApplicationShell natively; when the MC session expires, the user is redirected to the MC login page; no custom token refresh logic exists in the application.
6. An integration test simulates a 401 from the CT API and asserts the ApplicationShell `onError` handler redirects to `/login`.

**Dependencies:** Story 1.1, Story 1.3
**FRs Covered:** FR40, FR42
**Complexity:** M

---

### Story 1.5: CI/CD Pipeline & Neon Branch-per-PR

**As a** Storefront Developer
**I want** every pull request to automatically provision an isolated database branch, run all checks, and deploy a preview environment
**So that** I can validate database migrations and application behavior in a production-like environment before merging

**Acceptance Criteria:**
1. A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every `pull_request` event and executes in order: `npm ci`, `npm run lint` (ESLint + Prettier check), `npm run typecheck` (tsc --noEmit), `npm run test:unit` (Vitest), and `npm run test:integration`; the workflow fails fast on the first failing step; all steps complete within 10 minutes.
2. A separate GitHub Actions job uses `neondatabase/create-branch-action` to create a Neon branch named `pr-{PR_NUMBER}` from the `main` database branch; the branch's `DATABASE_URL` is injected as a step output and used for all subsequent integration test and preview deploy steps.
3. `prisma migrate deploy` is executed against the PR-specific Neon branch as a workflow step before integration tests run; if migrations fail, the workflow fails with a clear error message.
4. On PR merge to `main`, a cleanup workflow deletes the `pr-{PR_NUMBER}` Neon branch within 5 minutes; failed cleanup posts a GitHub PR comment with the branch name for manual deletion.
5. A deployment workflow triggers on push to `main`, runs `mc-scripts build`, and deploys the Connect artifact to the commercetools Connect staging environment; deployment status is reported as a GitHub commit status check.
6. ESLint is configured with `@typescript-eslint/recommended`, `plugin:react-hooks/recommended`, and a custom rule disallowing direct `document.cookie` access; Prettier enforces 2-space indentation, single quotes, and trailing commas.
7. GitHub branch protection rules require: at least 1 approving review, all CI status checks passing, and no direct pushes to `main`.

**Dependencies:** Story 1.1, Story 1.2
**FRs Covered:** FR40
**Complexity:** M

---

### Story 1.6: Base Observability Stack

**As a** platform IT Admin
**I want** errors, performance metrics, and structured logs collected automatically from both the browser and service layers
**So that** I can detect and diagnose production incidents without manual log inspection

**Acceptance Criteria:**
1. Sentry is initialized using `@sentry/nextjs`; the `dsn` is read from `NEXT_PUBLIC_SENTRY_DSN`; `Sentry.init` is called before `<ApplicationShell>` renders; `tracesSampleRate` is `0.2` in production and `1.0` in development; source maps are uploaded during CI build via `@sentry/webpack-plugin`.
2. Every unhandled React error is captured via a Sentry `ErrorBoundary` wrapping the application root; the error boundary renders a user-friendly "Something went wrong" UI with a Sentry event ID displayed; the boundary resets on route change.
3. Axiom is configured for server-side structured logging; all service-layer API route handlers use a shared `logger` instance that calls `axiom.ingest()`; log entries include `{ level, message, tenantId, requestId, durationMs, statusCode }` fields; `tenantId` is never omitted from service-layer logs.
4. Vercel Analytics (`@vercel/analytics`) is initialized in the Next.js root; Web Vitals (LCP, FID/INP, CLS) are reported automatically; a custom `track()` call is made for every significant user action with `{ tenantId, componentId, action }` properties.
5. A Sentry alert rule notifies the `#platform-alerts` Slack channel when the error rate for any transaction exceeds 5% over a 5-minute rolling window.
6. A `/api/health` endpoint returns `{ status: "ok", version, timestamp }` within 500ms; the Connect health-check probe calls this endpoint every 30 seconds.
7. All observability credentials are stored as GitHub Actions secrets and never committed to the repository; a `.env.example` file documents all required variables.

**Dependencies:** Story 1.1, Story 1.5
**FRs Covered:** FR40
**Complexity:** M

---

### Story 1.7: Epic 6 Procurement Skeleton

**As an** IT Admin onboarding a new tenant
**I want** a guided procurement gate that collects SSO configuration, data residency preference, and DPA acknowledgment before activating the platform
**So that** compliance and legal requirements are captured at the point of tenant provisioning, and the SSO integration surfaces are defined even if not yet fully implemented

**Acceptance Criteria:**
1. A "Tenant Onboarding" wizard route (`/nextgen-platform/onboarding`) is accessible only to users with Admin CASL ability; it is gated by a FlopFlip feature flag `epic6-procurement-skeleton` evaluated via `useFlagVariation('epic6-procurement-skeleton')`.
2. The wizard has three named steps: (1) "SSO Configuration", (2) "Data Residency", (3) "DPA Acknowledgment"; step progression is blocked if the current step's required fields are not valid; wizard state is persisted to a CT Custom Object after each step so the admin can resume.
3. The "SSO Configuration" step renders a placeholder form with fields: `ssoProvider` (dropdown: "SAML 2.0", "OIDC", "None"), `metadataUrl` (text input, URL-validated), and a disabled "Test Connection" button labelled "Coming in Epic 6"; values are saved to the CT Custom Object on "Next".
4. The "Data Residency" step renders a `RadioGroup` from `@commercetools-frontend/ui-kit` with options for available Neon regions (`us-east-1`, `eu-central-1`, `ap-southeast-1`); the selected region is stored in the tenant's Custom Object and in the `tenants` Prisma table; changing the region after initial save displays a warning: "Data residency cannot be changed after activation".
5. The "DPA Acknowledgment" step displays a scrollable text area containing placeholder DPA text; a required checkbox "I have read and accept the Data Processing Agreement" must be checked before "Activate Tenant" is enabled; `dpa_accepted_at TIMESTAMPTZ` and `dpa_accepted_by TEXT` are written to the `tenants` table on activation.
6. On successful completion, the wizard marks the tenant as `status: "active"` in the `tenants` table and redirects to the main platform dashboard; a `behavioral_events` row is inserted with `event_type: "tenant_activated"`.
7. The entire onboarding wizard is covered by at least one Playwright E2E test that walks all three steps and asserts tenant `status` is `"active"` in the Neon PR branch database after completion.

**Dependencies:** Story 1.1, Story 1.2, Story 1.3, Story 1.4
**FRs Covered:** FR40, FR42
**Complexity:** M

---

## Epic 2: Governed Component Library

### Story 2.1: Component Library Schema & CLV-Variant Support

**As a** Storefront Developer
**I want** to define component schemas (tastics) with typed property definitions including a `clv_tier` dimension for CLV-variant fields
**So that** different content and configurations can be served to customers based on their CLV tier, with schema structure enforced at the platform layer

**Acceptance Criteria:**
1. A `ComponentSchema` TypeScript type is defined with: `id`, `name`, `version`, `zone: "green" | "red"`, `properties: ComponentProperty[]`, `clvVariants: ClvVariantConfig[]`, `createdAt`, `publishedAt | null`; this type aligns with the Prisma model shape; `properties` and `clvVariants` are stored as `Json` columns.
2. `ClvVariantConfig` is defined as `{ dimension: "clv_tier"; tiers: Array<{ tierId: string; tierLabel: string; overrides: Record<string, unknown> }> }`; tier labels support at minimum: `"bronze"`, `"silver"`, `"gold"`, `"platinum"`; the `overrides` map keys must correspond to existing `ComponentProperty.key` values — a Zod schema validates this constraint.
3. `ComponentProperty` supports `type` values: `"text"`, `"richtext"`, `"image"`, `"boolean"`, `"number"`, `"enum"`, `"reference"`, `"json"`; each property has `key`, `label`, `required`, `defaultValue?`, `editPermission: "editable" | "locked" | "hidden"` (default `"editable"`); the full schema is validated with Zod on creation and update.
4. Component schemas are persisted to CT Custom Objects (`container: "component-schemas"`, `key: "{componentId}"`) via `useMcMutation`; a `useMcQuery` hook fetches the schema by key; optimistic updates are applied in the UI on save.
5. A "New Component Schema" form allows the developer to add/remove properties via a dynamic form built with `react-hook-form` and `@commercetools-frontend/ui-kit` form components; adding a CLV variant tier automatically generates override input fields for every `"editable"` property.
6. The Zod validation schema is shared between the browser (form validation) and the service layer (API route validation) via a single import; TypeScript compilation fails if the Zod schema and the TypeScript `ComponentSchema` type diverge.
7. A Vitest unit test suite covers: valid schema creation, invalid `clv_tier` override key rejection, missing required property rejection, and schema version increment on update.

**Dependencies:** Story 1.1, Story 1.2, Story 1.3
**FRs Covered:** FR13, FR14, FR29
**Complexity:** L

---

### Story 2.2: Green Zone / Red Zone Designation UI

**As a** Storefront Developer
**I want** to designate each component in the library as either Green Zone (operator-editable) or Red Zone (platform-protected) from a Developer Console UI
**So that** I can precisely control which components operators are permitted to modify without developer intervention

**Acceptance Criteria:**
1. The Component Library list page displays each component with a zone badge: a green "Green Zone" badge or a red "Red Zone" badge rendered using `@commercetools-frontend/ui-kit` `<Tag>` components with appropriate color tokens; zone status is read from `ComponentSchema.zone` in the CT Custom Object.
2. A toggle on each component row (FlopFlip `useFlagVariation('zone-designation-enabled')` must return `true` for interactivity) allows the Developer to flip the zone between `"green"` and `"red"`; the toggle is disabled and shows a tooltip "Feature not yet enabled" when the flag is `false`.
3. Changing a component's zone triggers a `useMcMutation` that writes the updated `ComponentSchema` (with incremented `version`) to the CT Custom Object; the mutation is guarded by a CASL `<Can do="manage" on="ComponentSchema">` check.
4. A confirmation modal appears when switching a previously-published component from Green to Red Zone, warning: "This will immediately revoke operator edit access. Active operator sessions will lose edit capability within 60 seconds." The user must type the component name to confirm.
5. Zone changes are reflected in the FlopFlip flag evaluation context: when a component is designated Red Zone, `useFlagVariation('component-{componentId}-red-zone')` returns `true` via a Custom Object that the FlopFlip adapter reads within one polling cycle (default 60s).
6. The Developer Console displays a zone summary panel showing counts: "X Green Zone components, Y Red Zone components, Z Unpublished"; clicking a count filters the list to that subset; the filter state is reflected in the URL query string (`?zone=green`).
7. An integration test verifies that POSTing a zone change with an Operator role token returns HTTP 403, and with a Developer role token returns HTTP 200 with the updated schema in the response body.

**Dependencies:** Story 2.1, Story 1.3
**FRs Covered:** FR30, FR31, FR32
**Complexity:** M

---

### Story 2.3: Field-Level Edit Permission Configuration

**As a** Storefront Developer
**I want** to configure per-property edit permissions on each component schema, specifying whether each field is editable, locked, or hidden for operators
**So that** I can enforce precise content governance at the field level without preventing operators from customizing permitted fields

**Acceptance Criteria:**
1. The Component Schema detail page renders a property permission matrix table: one row per `ComponentProperty`, with columns: "Property Key", "Type", "Operator Permission" (dropdown: "Editable", "Locked", "Hidden"), "CLV Override Allowed" (checkbox); built using `@commercetools-frontend/ui-kit` `<DataTable>`.
2. Changing a property's `editPermission` updates local form state; changes are not persisted until "Save Changes" is clicked, which triggers a `useMcMutation` to update the CT Custom Object with the full updated schema (version incremented).
3. The `"locked"` state renders the field as `disabled` in the operator editor; `"hidden"` means the field does not appear in the operator editor at all; `"editable"` renders the field as fully interactive; these states are enforced in the operator-facing editor, not just the Developer Console.
4. CLV variant override inputs respect field-level permission: a field marked `"locked"` cannot have per-tier overrides (the "CLV Override Allowed" checkbox is forced unchecked and disabled); a Zod validation rule rejects schemas where `locked` or `hidden` fields have CLV overrides.
5. A bulk-action control ("Lock All" / "Unlock All") allows the developer to set all properties to `"locked"` or `"editable"` in one click; the action is logged as a `behavioral_events` entry with `event_type: "bulk_permission_change"`.
6. When a component is Red Zone, all property `editPermission` values are forced to `"locked"` or `"hidden"` at the API validation layer — a Zod refinement rejects any Red Zone schema containing an `"editable"` property; the Developer Console UI disables the dropdown for all properties when Red Zone and displays a banner: "Red Zone components cannot have editable operator fields".
7. A Vitest unit test asserts that `validateComponentSchema()` rejects a schema with `zone: "red"` and any property with `editPermission: "editable"`, and accepts a schema with `zone: "green"` and mixed permission states.

**Dependencies:** Story 2.1, Story 2.2
**FRs Covered:** FR31, FR32
**Complexity:** M

---

### Story 2.4: Component Library Publish & Versioning

**As a** Storefront Developer
**I want** to publish a versioned snapshot of the component library and roll back to a previous version if needed
**So that** changes to component schemas reach the storefront in a controlled, auditable manner without requiring code deployments

**Acceptance Criteria:**
1. A "Publish Library" button (guarded by `<Can do="publish" on="ComponentLibrary">`) triggers a publish flow that creates a CT Custom Object (`container: "component-library-versions"`, `key: "v{versionNumber}"`) containing a snapshot of all current `ComponentSchema` objects and a `publishedAt` timestamp.
2. A "Version History" drawer lists all published versions with: version number, publisher name, published timestamp, and component count; paginated at 20 items per page.
3. A "Rollback to this version" button (Admin ability only) copies the selected version snapshot's schemas back into the `component-schemas` container; the rollback creates a new version entry tagged `{ rollbackFrom: currentVersion, rollbackTo: targetVersion }`.
4. A pre-publish validation step runs automatically when "Publish Library" is clicked: checks that all component schemas pass Zod validation, all required properties have `defaultValue` set, and no two components share the same `name`; failures are displayed as a blocking error list in a modal before the mutation fires.
5. Each publish event writes a row to the `behavioral_events` table with `event_type: "library_published"`, `payload: { versionNumber, componentCount, publishedBy }`, and `tenant_id`.
6. The active published version is tracked in a `container: "component-library-meta"`, `key: "active-version"` Custom Object; an unpublished library returns a `404` with body `{ error: "No published library found" }`.
7. A Playwright E2E test verifies the full publish-then-rollback cycle: create a schema, publish v1, modify the schema, publish v2, rollback to v1, and assert the `active-version` Custom Object points to v1.

**Dependencies:** Story 2.1, Story 2.2, Story 2.3
**FRs Covered:** FR13, FR14, FR29
**Complexity:** M

---

### Story 2.5: Component Library Live Update Without Redeployment

**As a** Storefront Developer
**I want** published changes to the component library to propagate to live storefront instances without requiring a code redeployment
**So that** operators can see and work with updated component definitions within minutes of a publish event

**Acceptance Criteria:**
1. The operator-facing storefront runtime polls the `component-library-meta` CT Custom Object (`key: "active-version"`) every 60 seconds via a singleton module; when `active-version` changes, the runtime fetches the new version snapshot and updates an in-memory cache.
2. The polling interval is configurable via `LIBRARY_POLL_INTERVAL_MS` (default `60000`); the interval is cleared on server shutdown; the poller does not poll when `NODE_ENV === "test"`.
3. When the in-memory cache is updated, a server-sent event or WebSocket message is pushed to all connected operator sessions; the operator editor UI displays a `<Notification type="info">Component library updated. Reload to see changes.</Notification>` banner without forcing a full page reload.
4. A stale-while-revalidate pattern is implemented: on a cache miss, the service returns `503` with `Retry-After: 5` and immediately begins fetching; a second request within 5 seconds returns freshly loaded data.
5. A `POST /api/cache/invalidate` endpoint (authenticated, Admin role only) clears the in-memory cache and forces an immediate re-fetch; this endpoint is called by the publish flow as a post-publish step.
6. Cache hit rate and poll latency metrics are emitted via Axiom for monitoring.

**Dependencies:** Story 2.4, Story 1.6
**FRs Covered:** FR13, FR14
**Complexity:** M

---

### Story 2.6: Operator Access Simulation

**As a** Storefront Developer
**I want** to impersonate an operator role within the Developer Console to preview exactly what an operator would see and be able to edit
**So that** I can verify governance enforcement and catch misconfigured permissions before publishing to production

**Acceptance Criteria:**
1. A "Simulate Operator View" toggle in the Developer Console top bar (visible only to Developer or Admin CASL ability) activates impersonation mode; while active, a persistent yellow banner reads "Simulating Operator Access — governance enforcement active".
2. In simulation mode, the `AppAbility` instance is rebuilt via `AbilityBuilder` with only Operator role abilities regardless of the actual user's scopes; the CASL `<Can>` guards throughout the application re-evaluate against this simulated ability; the actual `mcAccessToken` is unchanged and all API calls still authenticate as the real user.
3. The component editor in simulation mode enforces field-level permissions from the current schema: `"locked"` fields render with `disabled` prop, `"hidden"` fields are absent, `"editable"` fields render normally; a "Permission Debug" panel (collapsible, simulation-mode only) lists each field with its resolved permission state.
4. Red Zone components in simulation mode render as fully read-only with a "Red Zone — Not Editable by Operators" badge; no edit controls are rendered; the API call is blocked client-side by the CASL guard before it fires.
5. Simulation mode respects the current FlopFlip flag context; a "Flag Context" panel lists all relevant flag evaluations and their current values.
6. Exiting simulation mode immediately restores the real `AppAbility` instance; all form state entered during simulation is discarded; a Vitest test asserts that no `useMcMutation` calls were made during a simulated operator session.
7. Simulation mode usage is tracked via `behavioral_events` with `event_type: "simulation_started"` and `event_type: "simulation_ended"` including `payload: { simulatedRole: "Operator", durationMs }`.

**Dependencies:** Story 2.2, Story 2.3, Story 1.3
**FRs Covered:** FR30, FR31, FR32, FR50
**Complexity:** M

---

### Story 2.7: Component Behavioral Provenance Tracking

**As a** Storefront Developer
**I want** to view CTR lift, CLV impact, and experiment win rate metrics attributed to each component in the library
**So that** I can make data-driven decisions about which components to retain, promote, or retire

**Acceptance Criteria:**
1. The Component Schema detail page includes a "Behavioral Provenance" tab displaying three metric cards: "CTR Lift" (percentage vs. baseline), "CLV Impact" (average CLV delta for users exposed to this component), and "Experiment Win Rate" (percentage of A/B tests featuring this component that reached statistical significance).
2. The analytics service endpoint queries the `behavioral_events` table filtering by `component_id` and `tenant_id` (RLS enforced); CTR lift is computed as `(component_ctr - baseline_ctr) / baseline_ctr * 100` where baseline is the 30-day rolling average CTR across all tenant components; results are cached in-memory for 5 minutes.
3. `event_type: "component_impression"` and `"component_click"` feed the CTR calculation; `event_type: "experiment_result"` with matching `payload.componentId` feeds win rate; `event_type: "clv_delta"` with matching `payload.componentId` feeds CLV impact.
4. A "Data Availability" indicator shows the event count and date range; if fewer than 100 `component_impression` events exist, the CTR metric displays "Insufficient data (< 100 impressions)" instead of a percentage.
5. A time-range selector allows the developer to view metrics for the last 7, 30, or 90 days; the selected range is preserved in the URL query string (`?range=30d`).
6. CLV impact data is broken down by `clv_tier` if CLV variants exist: a bar chart shows the CLV delta per tier (`bronze`, `silver`, `gold`, `platinum`).
7. All analytics queries are parameterized via Prisma's `$queryRaw` with typed parameters (never string-interpolated SQL); a Vitest integration test against the Neon PR branch database verifies that querying with an invalid `tenantId` returns an empty result set (RLS blocks cross-tenant access).
8. A Prisma index migration adds `CREATE INDEX behavioral_events_component_tenant_idx ON behavioral_events (component_id, tenant_id, occurred_at DESC)` to ensure query performance.

**Dependencies:** Story 2.1, Story 1.2, Story 1.6
**FRs Covered:** FR50
**Complexity:** L

---

### Story 2.8: WCAG 2.1 AA Compliance for Platform Components

**As a** Storefront Developer
**I want** all platform-provided components to meet WCAG 2.1 AA accessibility standards by default
**So that** storefronts built on the platform are accessible to users with disabilities without requiring manual remediation

**Acceptance Criteria:**
1. `axe-core` is integrated into CI via `@axe-core/playwright` (E2E tests) and `vitest-axe` (component tests); every Vitest component test for a platform component includes `expect(await axe(container)).toHaveNoViolations()`; the CI pipeline fails if any new component test lacks this assertion.
2. All color tokens are defined in `src/tokens/colors.ts`; a token validation script runs in CI and fails if any text/background color pair has a contrast ratio below 4.5:1 (normal text) or 3:1 (large text/UI components).
3. All interactive elements (buttons, inputs, toggles, links) have explicit `aria-label` or `aria-labelledby` attributes when the visible label is insufficient; all form inputs are associated with their labels via `htmlFor`/`id` pairs; enforced by `eslint-plugin-jsx-a11y`.
4. All platform component images include a `ComponentProperty` of `type: "text"` with `key: "altText"` and `required: true`; a Zod refinement rejects image-type schemas missing this property.
5. All platform UI components support full keyboard navigation following WCAG 2.1 SC 2.4.3; modal dialogs trap focus within the dialog and return focus to the trigger on close.
6. An accessibility audit report generated by `@axe-core/playwright` during the nightly CI run is uploaded as a GitHub Actions artifact; a zero-violation gate on the nightly run pages the on-call engineer.
7. `prefers-reduced-motion` media queries are respected by all animated platform components; CSS transitions are wrapped in `@media (prefers-reduced-motion: no-preference)` guards.

**Dependencies:** Story 2.1
**FRs Covered:** FR14
**Complexity:** M

---

### Story 2.9: Developer Console Navigation & Component Library Dashboard

**As a** Storefront Developer
**I want** a clear Developer Console dashboard that provides an at-a-glance overview of the component library status with intuitive navigation
**So that** I can efficiently manage the component library without needing to know the underlying CT Custom Objects structure

**Acceptance Criteria:**
1. The Developer Console is accessible via the Merchant Center left-side nav entry "Component Library" (rendered by the `<ApplicationShell>` `navBarItems` configuration); the nav entry is only visible to users with Developer or Admin CASL ability.
2. The Component Library dashboard renders a `@commercetools-frontend/ui-kit` `<DataTable>` with columns: "Component Name", "Zone" (Green/Red badge), "Status" (Draft/Published/Outdated), "Last Published" (relative timestamp), "Properties Count", and an "Actions" column.
3. Status badges use `@commercetools-frontend/ui-kit` `<StatusBadge>`: `"Draft"` renders grey, `"Published"` green, `"Outdated"` yellow; a component is `"Outdated"` when its `version` in `component-schemas` is higher than the `version` in the `active-version` library snapshot.
4. A search/filter bar supports free-text search on component name, a "Zone" filter dropdown, and a "Status" filter dropdown; active filters are reflected in URL query params and survive page reload.
5. A summary stats bar at the top displays: total component count, count by zone, count by status, and the current active library version number with a "Publish New Version" CTA button.
6. Clicking a component row navigates to the component detail page which renders the property editor, behavioral provenance tab, and zone/publish controls.
7. The dashboard fetches all component schemas in a single `useMcQuery` call (filtering by `container = "component-schemas"`); a loading skeleton displays while the query is in flight; an error state includes a retry button.

**Dependencies:** Story 2.1, Story 1.3
**FRs Covered:** FR13
**Complexity:** S

---

## Epic 3: Storefront Editor & Publishing

### Story 3.1: StorefrontCanvas Foundation

**As a** storefront operator
**I want** a canvas that renders my live storefront with Green/Red Zone component overlays and full keyboard navigation
**So that** I can visually identify editable vs. platform-managed sections and navigate the editor efficiently without relying on a mouse

**Acceptance Criteria:**
1. Canvas fetches the current page layout from CT Custom Objects via `useMcQuery` and renders each section as a `ComponentSlot`; the `mcAccessToken` HttpOnly cookie is forwarded automatically by ApplicationShell — no manual auth header.
2. Green Zone slots (where `useFlagVariation('greenZoneEnabled')` returns `true`) render a dashed border on hover with a visible section label; Red Zone slots render a muted lock icon and a "platform-managed" tooltip via a `GovernanceBadge` component.
3. `Tab` key cycles focus through all `ComponentSlot` elements in DOM order; pressing `Enter` on a focused slot opens the property sidebar and shifts focus to the first editable field inside it; pressing `Escape` returns focus to the originating slot.
4. An ARIA live region (`aria-live="polite"`) announces slot state changes (e.g., "Hero Banner selected", "AI generating content") so screen-reader users receive real-time feedback without visual inspection.
5. Canvas reflects four explicit states — `idle`, `element-selected`, `ai-generating`, and `read-only` — with `data-canvas-state` attribute updated on the root element; in `read-only` state all slot overlays are suppressed and interaction is disabled.
6. AI-modified slots display an "AI tint" badge (amber outline + sparkle icon) until the operator explicitly saves or discards the AI suggestion; badge state is stored transiently in component local state, not persisted to CT Custom Objects.
7. Canvas passes WCAG 2.1 AA audit (axe-core zero violations) for all four states; colour-contrast ratios for dashed borders and lock icons meet the 3:1 non-text contrast requirement.

**Dependencies:** FlopFlip feature flags deployed, CT Custom Objects component schema (Epic 2)
**FRs Covered:** FR1, FR2, FR15, FR16
**Complexity:** XL

---

### Story 3.2: Component Add, Reorder, and Remove

**As a** storefront operator
**I want** to add new components between existing sections, reorder them via drag-and-drop or keyboard, and remove components with a confirmation step
**So that** I can compose storefront pages freely without writing code

**Acceptance Criteria:**
1. A "+" insert button appears between every two adjacent `ComponentSlot` elements on hover and is always visible when a slot has keyboard focus; clicking or pressing `Enter` on "+" opens a component-picker drawer listing available Green Zone component types sourced from CT Custom Objects.
2. Drag handles are rendered on each Green Zone slot; dragging a slot to a new position optimistically re-orders the layout array in local state and persists the new order to CT Custom Objects via `useMcMutation` on drop; Red Zone slots have no drag handle and cannot be reordered.
3. Keyboard reorder uses `⌘↑` / `⌘↓` (Mac) and `Ctrl↑` / `Ctrl↓` (Windows/Linux) to move a focused slot one position up or down; each move announces the new position via the ARIA live region (e.g., "Hero Banner moved to position 2 of 5").
4. The delete action on a slot is accessible via a "Remove" button in the property sidebar and a keyboard shortcut (`Delete` key when slot is focused); both paths show a confirmation dialog before committing the mutation.
5. Reorder and remove mutations are wrapped in an undo stack (max 20 entries per canvas session); `⌘Z` restores the previous layout state from local undo history and re-fires the CT Custom Objects `useMcMutation` with the prior value.
6. All add/reorder/remove operations are blocked when the canvas is in `read-only` state or the operator lacks the `storefront:write` CASL permission; the UI surfaces a contextual tooltip explaining the restriction.
7. CASL guard `can('reorder', 'ComponentSlot')` is evaluated client-side before rendering drag handles; server-side CT Custom Objects mutation endpoint enforces the same CASL rule to prevent API-level bypass.

**Dependencies:** Story 3.1
**FRs Covered:** FR2, FR3
**Complexity:** L

---

### Story 3.3: Green Zone Property Sidebar

**As a** storefront operator
**I want** to edit component properties within Green Zone constraints using a structured sidebar form
**So that** I can customise content, styling, and behaviour of components without breaking platform-governed configurations

**Acceptance Criteria:**
1. Selecting a Green Zone `ComponentSlot` opens a property sidebar panel built with `react-hook-form`; it renders field definitions sourced from the component's schema in CT Custom Objects; field types supported include text, rich-text, image URL, boolean toggle, and enum select.
2. Red Zone fields within a mixed-governance component are rendered as disabled inputs with a `GovernanceBadge` lock icon inline; hovering the badge shows "Managed by platform — contact your administrator to change this value."
3. Form validation runs on `onChange`; errors are displayed inline beneath the relevant field; the "Save draft" button remains disabled while any validation error is present.
4. Saving the sidebar form writes updated field values to CT Custom Objects via `useMcMutation`; on success the canvas slot re-renders with the new values within 300 ms without a full page reload.
5. Unsaved sidebar changes are tracked via `react-hook-form`'s `isDirty` flag; navigating away while `isDirty` is `true` triggers a "Discard changes?" confirmation dialog.
6. The sidebar panel transition manages focus correctly: opening shifts focus to the first interactive field; closing returns focus to the originating `ComponentSlot` element per WCAG 2.4.3.
7. All sidebar interactions are unavailable in `read-only` canvas state; the sidebar renders in display mode showing current values without form controls.

**Dependencies:** Story 3.1, Epic 2 component schemas
**FRs Covered:** FR3
**Complexity:** L

---

### Story 3.4: ContextBar & Multi-context Canvas

**As a** storefront operator
**I want** to switch between B2X personas, locales, and customer groups via the ContextBar without losing my draft changes for any context
**So that** I can author context-specific storefront variations and review each in isolation

**Acceptance Criteria:**
1. The ContextBar renders three chip groups — B2X (B2C / B2B / dealer), locale (e.g., en-US / de-DE), and customer-group — with current selections highlighted; chip values are loaded from CT project settings via `useMcQuery`.
2. Each unique combination of (B2X, locale, customer-group) is treated as an independent context key; draft canvas state for each context is stored separately in CT Custom Objects under `storefront-draft:{pageId}:{contextKey}`.
3. Switching context triggers a cross-fade canvas transition (200 ms CSS opacity); the outgoing context's draft state is flushed to CT Custom Objects before the incoming context's draft is loaded, ensuring no data loss.
4. A draft indicator chip displays "N unpublished changes" in amber when the active context has unsaved draft changes; the count reflects the number of modified `ComponentSlot` entries compared to the last published snapshot.
5. Context switching does not discard draft changes; after switching from context A to context B and back to A, all draft edits to context A are fully restored from CT Custom Objects.
6. The ContextSwitcher dropdown shows a per-context status badge (Live / Draft) for all contexts that have been edited.
7. When the operator attempts to navigate away from the MC application, ApplicationShell's navigation guard triggers a "Save draft?" modal if the active context has unpublished changes.

**Dependencies:** Story 3.1, CT Custom Objects draft schema
**FRs Covered:** FR1, FR3, FR4, FR5
**Complexity:** L

---

### Story 3.5: Multi-Viewport Preview

**As a** storefront operator
**I want** to preview my storefront canvas at Desktop (1440 px), Tablet (768 px), and Mobile (390 px) device sizes within the editor
**So that** I can verify responsive layouts before publishing without leaving the MC application

**Acceptance Criteria:**
1. A device-switcher toolbar offers three options — Desktop (1440 px), Tablet (768 px), Mobile (390 px) — with icons; the active selection is persisted to the operator's CT Custom Objects user preferences key.
2. Selecting a device size wraps the canvas in a scaled device frame constrained to the selected viewport width; the frame is CSS-scaled to fit the available editor area without horizontal scrolling in the editor chrome.
3. In all device preview modes the canvas enters `read-only` state automatically; no `ComponentSlot` overlays, drag handles, or "+" insert buttons are rendered; the sidebar closes if open.
4. Returning to "edit mode" from preview restores the canvas to its previous state and re-opens the sidebar if a slot was selected, with focus returned to the appropriate element.
5. The preview frame renders the storefront using the current draft state from CT Custom Objects (not the live published version), labelled with a "DRAFT PREVIEW" watermark banner.
6. Keyboard shortcuts `⌘Shift+D` / `⌘Shift+T` / `⌘Shift+M` cycle through Desktop / Tablet / Mobile; the ARIA live region announces the active device.

**Dependencies:** Story 3.1, Story 3.4
**FRs Covered:** FR4
**Complexity:** M

---

### Story 3.6: B2X Context Preview

**As a** storefront operator
**I want** to view B2C and B2B (or dealer) context renders side-by-side with synchronised scrolling
**So that** I can quickly spot divergences between context-specific storefront layouts before publishing

**Acceptance Criteria:**
1. A "Split Preview" toggle renders `B2XPreviewSplit` — two side-by-side preview panes each containing a device-framed iframe; the left pane shows the current primary context and the right pane shows a selectable secondary context via dropdown.
2. Both panes render the current draft state for their respective contexts from CT Custom Objects; if no draft exists for the secondary context the published snapshot is used, with a "Live" badge.
3. Scrolling in either pane is synchronised via a shared `scrollTop` binding — when the user scrolls the left pane the right pane matches position proportionally.
4. `B2XPreviewSplit` is only available at the Desktop (1440 px) viewport size; attempting to activate it at Tablet or Mobile shows a tooltip "Split preview is available at Desktop size only."
5. Each pane displays a context chip and a Live/Draft status badge; clicking the chip changes that pane's context without affecting the other pane or the main editor context.
6. Exiting split preview via the toggle or pressing `Escape` restores the single-pane canvas view and returns the editor to its previous state.

**Dependencies:** Story 3.4, Story 3.5
**FRs Covered:** FR5
**Complexity:** M

---

### Story 3.7: Mobile Device Editor Access

**As a** storefront operator on a mobile device
**I want** a touch-optimised editor experience with responsive chrome and touch-based reorder gestures
**So that** I can make urgent storefront updates from a phone without needing a desktop browser

**Acceptance Criteria:**
1. When the MC application is accessed on a viewport narrower than 768 px, the editor chrome collapses into a bottom-sheet drawer pattern; the canvas occupies full viewport width.
2. Touch-based reorder replaces drag-and-drop: a long-press (500 ms) on a Green Zone `ComponentSlot` activates reorder mode with a lift shadow; dragging drops on release into the nearest valid slot gap.
3. The `⌘↑` / `⌘↓` keyboard shortcuts are replaced on mobile by up/down arrow buttons rendered within the reorder mode overlay.
4. The property sidebar opens as a full-viewport bottom sheet modal on mobile; `react-hook-form` fields are rendered with `font-size: 16px` minimum to prevent iOS Safari auto-zoom on input focus.
5. Touch targets for all interactive elements meet the WCAG 2.5.5 minimum 44×44 CSS pixel touch target size.
6. Performance: the mobile editor renders initial paint within 2.5 s on a Moto G Power–class device (simulated via Lighthouse throttling); no layout shift caused by bottom-sheet transitions (CLS < 0.1).

**Dependencies:** Story 3.1, Story 3.2, Story 3.3
**FRs Covered:** FR6
**Complexity:** M

---

### Story 3.8: Real-time Collaboration

**As a** storefront operator
**I want** to see which of my colleagues are currently editing which sections of a page, and receive notifications when edits conflict
**So that** I can collaborate on storefront content without accidentally overwriting a colleague's work

**Acceptance Criteria:**
1. On canvas mount, `@liveblocks/client` v3.18 enters a room identified by `storefront:{pageId}:{contextKey}`; the `mcAccessToken` is exchanged for a Liveblocks auth token via the MC application's `/api/liveblocks-auth` endpoint before room entry.
2. Each operator's presence is broadcast via `room.updatePresence({ activeSlotId, displayName })` on every `ComponentSlot` focus/selection change, throttled to at most every 200 ms.
3. `ComponentSlot` overlays display avatar chips (operator initials, max 3 visible + overflow count) for all other operators currently editing that slot, sourced from `useOthers()` Liveblocks hook.
4. Liveblocks `useStorage` maintains a shared `pendingSlotLocks` map; when an operator opens the sidebar for a slot, that `slotId` is added to the map; other operators see the slot dimmed to 50% opacity with a "Being edited by [name]" tooltip.
5. When two operators save conflicting edits to the same slot within a 5-second window (detected by comparing `updatedAt` timestamps), a conflict-resolution toast is shown to the later saver: "Conflict detected — [Name]'s changes were saved first. Review and re-apply your edits."
6. On Liveblocks connection error or websocket disconnect, the editor falls back gracefully to single-user mode with a non-blocking banner "Real-time collaboration unavailable — working offline"; all local edits remain functional.
7. The `/api/liveblocks-auth` endpoint validates the `mcAccessToken` cookie and returns HTTP 403 if the CASL `storefront:read` check fails.

**Dependencies:** Story 3.1, Liveblocks 3.18 project provisioned
**FRs Covered:** FR3
**Complexity:** L

---

### Story 3.9: Storefront Branches

**As a** storefront operator
**I want** to create named branches of a page's canvas state, switch between them, merge a branch into the main draft, and delete branches I no longer need
**So that** I can experiment with major layout changes in isolation without risking the current live content

**Acceptance Criteria:**
1. A branch-switcher dropdown lists all branches for the current page from a Prisma `StorefrontBranch` table (`id`, `pageId`, `name`, `createdAt`, `createdByHash`, `baseSnapshotId`); the dropdown shows the active branch name and a branch-count badge.
2. "Create branch" opens a modal with a required name field (max 64 chars, unique per page enforced by Prisma unique constraint); on submit, the current canvas state snapshot is deep-copied into a new `StorefrontBranch` record and the editor switches to the new branch.
3. Switching branches triggers a cross-fade canvas transition; unsaved draft changes on the departing branch are auto-saved to CT Custom Objects before the new branch state is loaded.
4. Branch status badge renders one of: "Ahead" (branch has changes not in main), "Merged" (branch content equals main snapshot), or "Conflict" (main has advanced since branch was created); status is computed by comparing `updatedAt` timestamps.
5. "Merge branch" (CASL `storefront:branch:merge` permission) triggers a three-way diff; non-conflicting slot changes are auto-merged; conflicting slots surface a side-by-side diff modal for manual resolution.
6. "Delete branch" is available only when status is "Merged"; deleting an "Ahead" branch shows a warning modal; the Prisma delete cascades via RLS-enforced tenant isolation.
7. Branch operations are recorded in the audit log Prisma table with `actionType`, `branchId`, `pageId`, and `userHash` (HMAC, never raw userId).

**Dependencies:** Story 3.1, Story 3.4, Prisma `StorefrontBranch` migration
**FRs Covered:** FR1, FR2, FR3
**Complexity:** L

---

### Story 3.10: Governance Validation before Publish

**As a** storefront operator
**I want** the system to run a pre-publish compliance check and surface specific Red Zone violations with component names before I can complete a publish
**So that** platform-governed constraints are never bypassed inadvertently during publishing

**Acceptance Criteria:**
1. Triggering the PublishAction first dispatches a `governance.validate` Inngest function (sync step, timeout 10 s) that reads the pending canvas draft from CT Custom Objects and evaluates each `ComponentSlot` against its governance schema; the publish flow is blocked until this step resolves.
2. If zero violations are found, the publish flow proceeds immediately; a transient "Governance check passed" status appears in the PublishAction button for 1 s.
3. If violations are found, a blocking "Governance Violations" modal lists each violation: component name, slot position, violated property name, and the constraint breached (e.g., "Hero Banner (slot 2) — backgroundColour — must be a brand-approved hex value").
4. The "Publish" button within the violations modal is disabled until all listed violations are resolved; each violation row has a "Fix" shortcut link that closes the modal and opens the property sidebar focused on the offending field.
5. After the operator resolves a violation, the `governance.validate` Inngest step is re-run automatically; the violations list refreshes to reflect only remaining issues.
6. Red Zone property violations (where `useFlagVariation('redZoneEnabled')` is `true` for the property) are marked with a `GovernanceBadge` in the violations list; they cannot be resolved by the operator and include a "Contact admin" CTA.
7. Governance validation results are not persisted to the audit log; only the final publish event is audited.

**Dependencies:** Story 3.3, Inngest `governance.validate` function deployed
**FRs Covered:** FR15, FR18
**Complexity:** L

---

### Story 3.11: Stage to Staging Environment

**As a** storefront operator
**I want** to deploy my draft canvas changes to a staging environment and receive a preview URL
**So that** I can share a review link with stakeholders before committing to a production publish

**Acceptance Criteria:**
1. The PublishAction dropdown includes a "Stage first" option; clicking "Stage" triggers the `storefront.stagePublish` Inngest function, passing `{ pageId, contextKey, draftSnapshotId }` as event data.
2. The `storefront.stagePublish` Inngest job performs an atomic Vercel ISR on-demand revalidation call against the staging Vercel deployment via `revalidatePath`; the job retries up to 3 times with exponential back-off on 5xx responses.
3. On Inngest job completion the staging preview URL is stored in CT Custom Objects and displayed in the editor as a clickable "View staged" link that opens in a new tab.
4. A "Staged" status indicator replaces the amber draft chip in the ContextBar for the staged context; it shows "Staged — [relative timestamp]" in blue.
5. If the staging revalidation job fails after all retries, an error toast is shown: "Staging failed — Vercel revalidation error. Try again or contact support." with a retry button.
6. Staging a draft does not alter the live production storefront; the staged URL is only accessible with a `?preview=1` query parameter gated by Vercel Edge Middleware validating a shared preview secret.
7. Staging is gated by `storefront:stage` CASL permission; operators without this permission see the option disabled.

**Dependencies:** Story 3.4, Inngest `storefront.stagePublish` function, Vercel staging project
**FRs Covered:** FR16
**Complexity:** M

---

### Story 3.12: Publish to Production

**As a** Brand Publisher
**I want** to atomically publish my approved canvas changes to production with context-specific confirmation and a first-publish celebration overlay
**So that** live storefront updates are deployed reliably and operators receive clear feedback on what was published

**Acceptance Criteria:**
1. The "Publish" action is gated by CASL `can('publish', 'Storefront')` on the client; the server-side Inngest `storefront.publish` handler independently validates the `mcAccessToken` against the same CASL rule before executing.
2. The PublishAction button reflects four states — `no-changes` (disabled), `has-changes` (active, amber dot), `publishing` (spinner), `published` (green check, 5 s auto-dismiss) — managed via a local state machine.
3. Clicking "Publish" opens a context-specific confirmation dialog: "Publish to [B2X] / [locale] / [customer-group]? This will update N components live."
4. On confirmation, the `storefront.publish` Inngest function executes `revalidatePath` for all affected page paths on the production Vercel deployment via the ISR on-demand revalidation API; all paths are submitted in a single batch request.
5. On successful completion, the ContextBar displays a confirmation toast: "Published to [context] — N changes live" for 5 s; the draft indicator clears; the CT Custom Objects draft key for the context is deleted.
6. If this is the operator's first-ever publish action (determined by absence of `firstPublishAt` in their CT Custom Objects user preferences), the `FirstPublishCelebration` full-canvas overlay is displayed for 4 s then auto-dismissed; this event is recorded to prevent repeat display.
7. If the Inngest job fails, the PublishAction returns to `has-changes` state with an error toast "Publish failed — changes have been preserved as draft"; the CT Custom Objects draft is not cleared.

**Dependencies:** Story 3.10, Story 3.11, Inngest `storefront.publish` function, Vercel production ISR token, CASL Brand Publisher role
**FRs Covered:** FR17, FR19
**Complexity:** L

---

### Story 3.13: Immutable Publish Audit Log

**As an** Admin or Auditor
**I want** an append-only log of every publish action that includes the author's HMAC user hash, timestamp, context, and a content diff
**So that** I can trace every production change for compliance and GDPR-safe accountability

**Acceptance Criteria:**
1. Every successful execution of the `storefront.publish` Inngest job writes a record to the Prisma `PublishAuditLog` table (`id UUID`, `pageId`, `contextKey`, `userHash VARCHAR(64)`, `publishedAt TIMESTAMPTZ`, `diffJson JSONB`, `changeCount INT`); RLS policy ensures records are tenant-scoped.
2. `userHash` is computed as `HMAC-SHA256(userId, AUDIT_HMAC_SECRET)` server-side within the Inngest job handler; the raw `userId` is never written to the `PublishAuditLog` table or logged in any application log output.
3. `diffJson` stores a structured diff of the published snapshot vs. the prior published snapshot: `[{ slotId, componentType, changedFields: [{ field, before, after }] }]`; field values are truncated to 500 characters.
4. The `PublishAuditLog` table has no `DELETE` privilege granted to any application role in the Prisma schema; permitted operations are `INSERT` (from the Inngest service account) and `SELECT` (from `admin` and `auditor` roles).
5. An "Audit Log" panel (visible only to operators with `auditLog:read` CASL permission) fetches paginated log entries via `useMcQuery`, displaying: Published At, Context, Changes count, and Author (displayed as `userHash[0..7]…`).
6. Each audit log row has an expandable "View diff" section that renders the `diffJson` as colour-coded diff (green additions, red removals) using a lightweight inline diff renderer.
7. Staging audit events (Story 3.11) are written to a separate `StagingAuditLog` table following the same schema and immutability constraints; displayed in separate tabs in the Audit Log panel.

**Dependencies:** Story 3.12, Prisma `PublishAuditLog` migration with RLS, `AUDIT_HMAC_SECRET` env var
**FRs Covered:** FR20
**Complexity:** M

---

### Story 3.14: Accessibility Warnings before Publish

**As a** storefront operator
**I want** the system to scan my pending canvas changes for WCAG AA violations before I publish and surface them with specific component references
**So that** I can make an informed decision about publishing content with known accessibility issues while remaining unblocked from publishing urgent updates

**Acceptance Criteria:**
1. When the publish confirmation dialog opens, an axe-core v4 scan runs client-side against the in-memory draft canvas DOM (rendered into a hidden off-screen `<div>` with `aria-hidden="true"`) for all modified `ComponentSlot` elements only.
2. The axe-core scan uses the `wcag2aa` ruleset tag; violations with `impact` of `"critical"` or `"serious"` are surfaced under an "Accessibility Warnings" collapsible section with a warning icon badge showing the violation count.
3. Each violation row displays: the component name (from `ComponentSlot` `data-component-type`), the WCAG criterion violated (e.g., "1.4.3 Contrast (Minimum)"), a brief description, and a "Review" link that closes the modal and focuses the offending slot.
4. Accessibility violations do not block publishing; if any violations are present, the "Confirm publish" button label changes to "Publish anyway" and a required acknowledgment checkbox must be checked before the button becomes active.
5. If zero violations are found, the "Accessibility Warnings" section is not rendered; the confirmation modal proceeds with its standard layout.
6. The axe-core scan completes within 3 s for a canvas with up to 20 modified slots; if exceeded, the scan is aborted and a non-blocking notice "Accessibility scan timed out — review manually" is shown; publishing is not blocked.
7. Acknowledged accessibility violations are recorded in `PublishAuditLog.diffJson` as an additional `accessibilityAcknowledged: true` flag with the violation count and WCAG criterion IDs.

**Dependencies:** Story 3.12, Story 3.13, axe-core v4 installed
**FRs Covered:** FR51
**Complexity:** M
## Epic 4: AI Core Site Builder & Migrator

### Story 4.1: CT Project Connection via API Credentials

**As a** platform operator
**I want** to connect my existing commercetools project by entering API credentials that are validated and securely stored
**So that** the AI Site Builder can access product catalogue, category, and channel data to power governed completions

**Acceptance Criteria:**
1. The MC Custom Application renders a "Connect Project" form collecting `clientId`, `clientSecret`, `projectKey`, `authUrl`, and `apiUrl`; all fields are required and validated for non-empty format before submission.
2. On submit, the frontend calls the CT Auth API (`POST {authUrl}/oauth/token` with `grant_type=client_credentials`) via a server-side proxy route; a successful `200` with a non-empty `access_token` confirms validity; any `401`/`4xx` surfaces an inline error banner with the raw CT error code.
3. Valid credentials are written to `securedConfiguration` on the CT Custom Application resource via `useMcMutation`; they are never stored in `customConfiguration` or exposed client-side after the initial form POST.
4. After storage, the application triggers behavioral collection activation by writing a CT Custom Object (`container: "site-builder-config"`, `key: "behavioral-collection-status"`) with `{ active: true, projectKey, connectedAt }`.
5. A CASL `can('manage', 'ProjectConnection')` guard is evaluated server-side before any credential write; operators lacking this permission see a disabled form with a tooltip explaining required roles.
6. A reconnect flow re-validates credentials against the CT Auth API and overwrites `securedConfiguration`; stale collection-status Custom Objects are updated atomically using the `version` field to prevent write conflicts.
7. Credential health is re-checked on every application bootstrap via a lightweight `HEAD` probe; a degraded-credential banner with a "Reconnect" CTA is shown if the probe returns `401`.

**Dependencies:** None
**FRs Covered:** FR34
**Complexity:** M

---

### Story 4.2: Commerce Intelligence Drawer — Create Mode Infrastructure

**As a** platform operator editing a page in Create mode
**I want** a Commerce Intelligence Drawer that slides in from the right without reflowing the canvas, toggled via ⌘/, with a full focus trap while open
**So that** I can access AI-powered completion tools without losing my place in the canvas layout

**Acceptance Criteria:**
1. The drawer is implemented as a fixed-position overlay panel (`position: fixed; right: 0`) that animates in via a CSS `transform: translateX` transition (300 ms ease-in-out); it does not affect the CSS grid or flex layout of the canvas or the property sidebar.
2. Pressing ⌘/ (macOS) or Ctrl+/ (Windows/Linux) toggles the drawer open/closed; a close button inside the drawer also dismisses it; the keyboard shortcut is registered globally in Create mode only.
3. When the drawer is open, a focus trap (using `focus-trap-react` or equivalent) confines keyboard navigation inside the drawer; pressing Escape closes it and returns focus to the last focused element on the canvas.
4. The drawer initialises an Inngest client connection on open; the Inngest function `site-builder/ai-completion-job` is registered in the Inngest 4.2.6 app and its event subscription established so the drawer can receive streamed events.
5. The drawer shell renders three distinct zones: a header with title "Commerce Intelligence" and the ⌘/ hint, a scrollable body (reserved for `AIReasoningCard` output), and a sticky footer with Approve/Cancel CTAs (disabled until a completion candidate is ready).
6. Opening the drawer in Create mode does not trigger any AI inference call on its own; inference is triggered only by observed canvas edit sequences (Story 4.3); the drawer shows an idle state with instructional copy until inference begins.
7. An ARIA `role="dialog"` with `aria-label="Commerce Intelligence"` and `aria-modal="true"` is applied to the drawer root; a visually hidden `aria-live="polite"` region is rendered inside for status announcements.

**Dependencies:** Story 4.1, Inngest 4.2.6 app bootstrap
**FRs Covered:** FR7, FR65
**Complexity:** XL

---

### Story 4.3: AI Intent Inference Engine

**As a** platform operator making edits on the canvas in Create mode
**I want** the system to observe my edit sequence, infer my completion intent, and propose a governed component sequence as a candidate
**So that** I do not have to manually specify what sections to add — the AI completes my intent from partial work

**Acceptance Criteria:**
1. An edit-observation hook (`useCanvasEditObserver`) subscribes to the canvas state manager's action stream; it records a timestamped edit-event log (`{ componentId, action, timestamp, sectionIndex }`) in a React ref, debounced at 800 ms to avoid noise from rapid consecutive edits.
2. After three or more distinct edit events are recorded, the hook fires the Inngest event `site-builder/intent-observed` with payload `{ editLog, pageType, existingComponentIds, projectKey }`, triggering the `site-builder/ai-completion-job` Inngest function.
3. The `site-builder/ai-completion-job` Inngest function calls OpenRouter via `@openrouter/ai-sdk-provider` using `createOpenRouter({ apiKey })` and `openrouter('anthropic/claude-3.5-sonnet')`; the system prompt enforces: "You may only suggest components from the following published library: {componentLibraryJson}".
4. The inference prompt includes the full edit log, the current page skeleton (component IDs and slot positions), and the published component library JSON fetched from CT Custom Object `container: "component-library"`, `key: "published"`; suggestions referencing components absent from this list cause the function to return a `GOVERNED_REJECTION` event.
5. Streaming begins within 2 seconds of the Inngest function receiving the event; a 30-second hard timeout is enforced via `step.sleep` abort — if the OpenRouter stream has not resolved, the function emits a `TIMEOUT` event and the drawer shows a graceful error state.
6. The inferred candidate is a structured JSON object `{ suggestedComponents: [{ componentTypeId, slotIndex, defaultProps }], confidence: number, reasoning: string }` validated against a Zod schema before passing downstream; invalid shapes are rejected and the operator shown "Could not generate a suggestion".
7. Inference results are never applied to the canvas without operator approval (Story 4.4); the raw candidate is held in React state in the drawer and discarded on drawer close or Cancel action.

**Dependencies:** Story 4.2, published component library CT Custom Object, OpenRouter API key
**FRs Covered:** FR7, FR8
**Complexity:** XL

---

### Story 4.4: AIReasoningCard / ConfidenceCard UI

**As a** platform operator reviewing an AI completion candidate
**I want** to see a clear "What I'll do" card showing the proposed components, governance scope, and my data signals — with Approve/Edit/Cancel actions — before any canvas change occurs
**So that** I retain full control and understand the basis for every AI suggestion

**Acceptance Criteria:**
1. The `ConfidenceCard` React component renders inside the Commerce Intelligence Drawer body immediately after the Inngest function emits a structured candidate; it replaces the idle instructional copy and is focused automatically.
2. The card header displays the title "What I'll do" and a confidence percentage badge (derived from `candidate.confidence`); confidence below 60% renders the badge in amber, 60–84% in blue, 85%+ in green.
3. The card body lists each `suggestedComponent` as a row showing: the component display name (resolved from the published library), the target slot label, and a Green Zone badge confirming library membership; rows are in proposed slot order.
4. A "Your data shows" section renders the `candidate.reasoning` string formatted as plain prose; this section must use the exact phrase "your data shows" at least once to maintain the product's established language convention.
5. Three action buttons are rendered in the card footer: **Approve** (primary, triggers Story 4.5 application), **Edit** (secondary, opens slot-by-slot edit mode allowing component swap via library picker before approval), and **Cancel** (tertiary, discards the candidate); no canvas mutation occurs until Approve is explicitly clicked.
6. Keyboard navigation: Approve is mapped to Enter when the card has focus, Cancel to Escape; all interactions are announced via the drawer's `aria-live="polite"` region.
7. The `AIReasoningCard` variant (used for streaming progress) and `ConfidenceCard` (used for final approval) are separate named exports from a shared `ai-cards` module; they share a base layout but differ in action surface and data shape.

**Dependencies:** Story 4.3, Inngest candidate event
**FRs Covered:** FR9
**Complexity:** L

---

### Story 4.5: Governed AI Completion Application

**As a** platform operator who has approved a ConfidenceCard
**I want** the approved component sequence to be applied to the canvas only within the Green Zone, with any non-library component causing an outright rejection
**So that** the platform's component governance is never bypassed by AI-generated output

**Acceptance Criteria:**
1. On Approve, the application dispatches `APPLY_AI_COMPLETION` to the canvas state manager; a governance middleware re-validates every `componentTypeId` in the approved candidate against the live published component library CT Custom Object fetched at apply-time (not inference-time) to guard against library changes during the session.
2. If any component in the candidate is absent from the published library at apply-time, the entire completion is rejected; no canvas mutation occurs; the ConfidenceCard is replaced by an inline error card reading "One or more suggested components are no longer in the governed library"; Inngest emits a `GOVERNED_REJECTION` event for audit logging.
3. All approved components are placed only in Green Zone slots; if the candidate includes a placement in a Red Zone slot, the governance middleware strips that placement and logs a warning; it does not fail the entire completion.
4. Each applied component is initialised with `defaultProps` from the candidate merged with component schema defaults; required fields left empty by the AI are marked with `__aiIncomplete: true` visible in the property sidebar.
5. The canvas state manager writes the applied completion as a draft (not published); a "Draft updated by AI" indicator appears in the page header.
6. The full approved candidate JSON, the governance validation result, and the final applied diff are written to a CT Custom Object (`container: "ai-completion-audit"`, `key: "{pageId}-{timestamp}"`) for compliance and debugging.
7. A CASL `can('apply', 'AICompletion')` guard is evaluated before dispatch; the guard check is enforced both client-side and in the server-side route that writes the audit Custom Object.

**Dependencies:** Story 4.4, canvas state manager, CT Custom Objects API
**FRs Covered:** FR8, FR10, FR11
**Complexity:** L

---

### Story 4.6: Accept/Modify/Reject Individual AI Placements

**As a** platform operator reviewing a multi-component AI completion draft
**I want** to accept, modify, or reject each proposed component placement individually before final application
**So that** I can take the parts of the AI suggestion that are useful while overriding specific placements without discarding the whole completion

**Acceptance Criteria:**
1. After the `ConfidenceCard` is shown and before the operator clicks global Approve, each component row in the card exposes three inline actions: a checkmark (Accept), a swap icon (Modify), and an X (Reject); visible on row hover/focus and always visible on touch viewports.
2. Clicking Modify opens a library picker modal filtered to Green Zone components only; the operator selects a replacement and the row updates to show the new component name with a "Modified" badge; the replacement is validated against the published library on selection.
3. Clicking Reject marks the row with a strikethrough style and a "Rejected" badge; rejected rows are excluded from the final `APPLY_AI_COMPLETION` payload; at least one row must remain accepted for the global Approve button to be enabled.
4. Individual row state (accepted/modified/rejected) is maintained in local React state within the `ConfidenceCard`; closing the drawer discards all per-row decisions and returns to idle.
5. The global Approve button label updates dynamically: "Approve 3 of 5 components"; the confidence badge recalculates proportionally based on accepted+modified count divided by total.
6. The final payload sent to the governance middleware contains only accepted and modified rows, with modified rows carrying the operator-selected `componentTypeId`; the audit CT Custom Object records both the original suggestion and the operator's per-row decisions.
7. All row action buttons are reachable via Tab; the library picker modal implements its own focus trap; closing the picker returns focus to the modified row's swap icon.

**Dependencies:** Story 4.4, Story 4.5
**FRs Covered:** FR10, FR11
**Complexity:** M

---

### Story 4.7: AI Completion Streaming Progress Feedback

**As a** platform operator waiting for an AI completion to generate
**I want** to see a skeleton pulse animation on the affected canvas section and hear screen-reader announcements of progress, with clear timeout handling
**So that** I have continuous feedback during the async operation and am never left wondering if the system is working

**Acceptance Criteria:**
1. Immediately after `site-builder/intent-observed` is fired, the canvas renders a skeleton pulse overlay on every slot index listed in `editLog`; the overlay uses a CSS `@keyframes` pulse animation (opacity 0.4 → 1 → 0.4, 1.2 s infinite) and does not shift or reflow surrounding components.
2. The streaming start is gated to 2 seconds after the Inngest event is sent; if the first OpenRouter streamed token arrives before 2 s, it is buffered and the skeleton continues until the 2 s mark, ensuring a consistent perceived experience.
3. The drawer's `aria-live="polite"` region announces: "Analysing your edits…" (on event fire), "Generating completion…" (on first token), "Completion ready for review" (on resolution), "Generation timed out — please try again" (on timeout), and "Generation failed" (on error).
4. A 30-second hard timeout is enforced in the Inngest function via a `Promise.race` between the OpenRouter stream resolution and a `step.sleep('30s')` abort signal; on timeout, the function emits `{ type: 'TIMEOUT' }` to the drawer, the skeleton overlays are removed, and a non-blocking toast appears with a "Try again" action.
5. A visible progress indicator (indeterminate linear bar) renders in the drawer header from event fire until candidate resolution or timeout; it is removed on both success and failure paths.
6. If the browser tab loses focus during streaming, the operation continues in the background; on tab refocus, the UI reconciles with the current Inngest event state.
7. All skeleton and progress elements have `aria-hidden="true"` to avoid polluting the accessibility tree; only the `aria-live` region conveys state to assistive technologies.

**Dependencies:** Story 4.2, Story 4.3
**FRs Covered:** FR12
**Complexity:** M

---

### Story 4.8: Historical Behavioral Data Import

**As a** platform operator onboarding to the AI Site Builder
**I want** to import historical analytics data from GA4, Hotjar, Mixpanel, or Frontastic analytics, map fields to the platform schema, and have it ingested into the `behavioral_events` table
**So that** the AI inference engine has a rich behavioral baseline from day one rather than starting cold

**Acceptance Criteria:**
1. The onboarding wizard presents a data source selector with four options: GA4, Hotjar, Mixpanel, and Frontastic Analytics; selecting a source reveals instructions for exporting a CSV or JSON file and a file upload input (max 500 MB, accepted MIME types: `text/csv`, `application/json`).
2. After upload, the application parses the first 200 rows/records client-side and presents a field-mapping UI showing detected source columns on the left and the target `behavioral_events` schema fields on the right; auto-mapping is attempted using fuzzy name matching (e.g. `event_name` → `eventType`, `client_id` → `sessionId`).
3. The field-mapping UI validates that `eventType`, `timestamp`, and `pageUrl` are mapped before allowing the operator to proceed; unmapped required fields are highlighted in red with a tooltip listing the expected format.
4. On confirmation, the client fires an Inngest event `behavioral/historical-import` with payload `{ sourceType, mappingConfig, uploadedFileRef, projectKey }`; the Inngest function `behavioral/ingest-historical-data` streams the file, transforms each record using the mapping config, validates rows against a Zod schema, and bulk-inserts into the `behavioral_events` table in batches.
5. Rows failing Zod validation are written to a `behavioral_import_errors` table with the row index and error detail; the operator sees a post-import summary: total rows, successfully ingested count, error count, and a downloadable error CSV.
6. The Inngest function processes files in 1,000-row batches using `step.run` chunking; each batch emits a progress event consumed by a polling hook that updates a progress bar (0–100%) in the onboarding wizard.
7. Imported data is tagged with `{ source: 'historical-import', importedAt, sourceType }` metadata in each `behavioral_events` row; this tag allows the inference engine to weight live behavioral data more heavily than historical imports.

**Dependencies:** Story 4.1, behavioral_events table (Epic 1), Inngest 4.2.6
**FRs Covered:** FR63
**Complexity:** L

---

### Story 4.9: Frontastic Migration Path

**As a** operator migrating an existing Frontastic site
**I want** the platform to automatically detect tastic schema compatibility, auto-map component types, and publish the reviewed mapping to CT Custom Objects
**So that** my Frontastic components migrate to the governed library with minimal manual rework

**Acceptance Criteria:**
1. The migration wizard accepts a Frontastic project export (ZIP containing tastic JSON schemas and page-folder structure); the server-side parser identifies all files matching `**/tastic-schema.json` and `**/tastics/**/*.json`, extracts `tasticType`, `schema`, and `configuration` arrays, and produces a raw tastic inventory object.
2. The auto-mapper compares each `tasticType` against the published component library using a two-pass strategy: exact `tasticType` string match first, then OpenRouter-powered semantic similarity for unmatched types; each mapping result carries a `matchConfidence` (0–1) and `matchMethod` (`"exact"` | `"semantic"` | `"unmatched"`).
3. The mapping review UI renders a table with columns: Frontastic Tastic Type, Matched Library Component, Match Confidence, Zone Assignment (Green/Red, editable dropdown), and Status; rows with `matchConfidence < 0.7` are highlighted in amber; unmatched rows default to Red Zone and require explicit operator action.
4. Schema field auto-mapping translates Frontastic `schema[].fields[]` entries to the target component's `propSchema` fields; type coercions are defined in a static mapping table; unmappable field types are flagged as Red Zone overrides requiring developer review.
5. Promoting any auto-mapped component from Red Zone to Green Zone triggers a CASL `can('promote', 'RedZoneComponent')` guard; promotion requires the operator to confirm a Green Zone acceptance criteria checklist.
6. On publishing the reviewed mapping, the application writes a CT Custom Object (`container: "migration-mapping"`, `key: "frontastic-{projectKey}-{timestamp}"`) containing the full mapping table JSON; a second CT Custom Object update merges approved Green Zone components into the published component library atomically using the `version` field.
7. A migration summary report is displayed post-publish: total tastics detected, auto-mapped (exact/semantic), operator-mapped, unmatched/skipped, Green/Red Zone counts; downloadable as PDF.

**Dependencies:** Story 4.1, published component library CT Custom Object, OpenRouter, Story 4.12
**FRs Covered:** FR34, FR35, FR36, FR37
**Complexity:** XL

---

### Story 4.10: Custom Next.js Migration Path

**As a** developer migrating a custom Next.js storefront
**I want** the platform to analyse my codebase via a GitHub App integration, extract components, scaffold a Green/Red Zone structure, and export a mapping for review
**So that** I can migrate without manually inventorying every component in a large codebase

**Acceptance Criteria:**
1. The migration wizard provides a "Connect GitHub Repository" step that initiates the GitHub App OAuth flow; after authorisation, the app lists accessible repositories; the operator selects a repo and branch, and the GitHub App token is stored in `securedConfiguration`.
2. The platform's GitHub App installation calls the GitHub Contents API to recursively list files under `components/`, `src/components/`, and `app/` directories; it fetches the content of every `.tsx` and `.jsx` file (up to 500 files; larger repos prompt the operator to narrow the scope path); fetched content is written to a temporary Neon table `migration_codebase_files`.
3. An Inngest function `migration/analyse-nextjs-codebase` processes the fetched files in batches of 20 using `step.run`; for each file it calls OpenRouter (`openrouter('anthropic/claude-3.5-sonnet')`) with a prompt instructing extraction of: exported component name, prop interface shape, inferred page/section type, and any CT SDK usage patterns.
4. Extracted components are matched against the published component library using the same two-pass strategy as Story 4.9; each match result includes `inferredZone` (`"green"` if CT SDK usage detected and maps to library, `"red"` otherwise) and a `scaffoldPriority` score.
5. The developer review UI (Story 4.12) receives the extraction results and renders them with file paths, prop diffs between the extracted interface and the library component schema, and the inferred zone; developers can override zone assignment and edit field mappings inline.
6. A mapping export action generates a `migration-manifest.json` file containing: component inventory, zone assignments, field mappings, and a scaffold plan; this file can be re-imported to resume a paused migration session.
7. All GitHub App API calls use the installation access token (not the user OAuth token); tokens are refreshed automatically before expiry; if the token cannot be refreshed, the migration session is paused with a "Reconnect GitHub" CTA.

**Dependencies:** Story 4.1, GitHub App registration, Neon branch database, OpenRouter, Inngest 4.2.6, Story 4.12
**FRs Covered:** FR34, FR35, FR36, FR37
**Complexity:** XL

---

### Story 4.11: Monolith Migration Path + Core Web Vitals Baseline

**As a** pre-sales engineer or operator planning a monolith migration
**I want** to measure Core Web Vitals for the existing monolith site and generate a before/after ROI report — available without full platform activation — and then trigger full canvas generation for the migration
**So that** I can prove the business case for migration and initiate the migration from a measurable baseline

**Acceptance Criteria:**
1. The CWV baseline tool is accessible from a standalone route (`/migrate/cwv-baseline`) that requires only a valid CT project connection (Story 4.1) and does NOT require a full platform subscription; a "Pre-sales mode" banner is shown when accessed without full activation.
2. The operator enters one or more URLs representing key monolith pages (up to 10); the platform triggers Lighthouse audits for each via the Google PageSpeed Insights API, collecting LCP, CLS, FID/INP, FCP, and TTFB for both mobile and desktop strategies.
3. Baseline metrics are persisted to a CT Custom Object (`container: "cwv-baseline"`, `key: "{projectKey}-{timestamp}"`) immediately after collection; if full platform activation occurs later, this baseline is automatically linked to the project for ongoing before/after comparison.
4. The ROI report renders a table comparing baseline CWV scores against published platform benchmark values (stored in CT Custom Object `container: "platform-benchmarks"`, `key: "cwv-targets"`); each metric shows: current value, target value, delta, and a pass/fail badge using Core Web Vitals thresholds (LCP ≤ 2.5 s = good, CLS ≤ 0.1 = good, INP ≤ 200 ms = good).
5. An estimated revenue impact section uses the formula `revenueImpact = baselineRevenue * (lcpDeltaMs / 1000) * 0.01`; `baselineRevenue` is entered by the operator; the report is exportable as PDF via `window.print()` with a print-optimised CSS stylesheet.
6. For operators with full platform activation, the monolith migration wizard accepts a sitemap XML URL; the platform fires the Inngest function `migration/generate-monolith-canvas` which uses OpenRouter to generate a complete draft canvas for each page type, respecting Green/Red Zone governance.
7. The generated canvas drafts are written as CT Custom Objects (`container: "migration-canvas-drafts"`, `key: "{pageType}-{projectKey}"`) and surfaced in the platform canvas editor as "Migration Drafts" — editable before publish; a readiness check (Story 4.13) is automatically queued for all generated drafts.

**Dependencies:** Story 4.1, Google PageSpeed Insights API key, CT Custom Objects API, OpenRouter, Inngest 4.2.6, Story 4.12, Story 4.13
**FRs Covered:** FR34, FR35, FR36, FR37, FR38, FR39
**Complexity:** XL

---

### Story 4.12: Migration Scaffolded Component Mapping Review

**As a** platform operator or developer reviewing a migration mapping from any of the three migration paths
**I want** a unified review UI where I can adjust zone assignments, permissions, and field type mappings before publishing to the component library
**So that** regardless of migration origin, I have a single consistent review surface before any mapping goes live

**Acceptance Criteria:**
1. The unified review UI at `/migrate/review/{migrationId}` accepts a `migrationId` resolving to a CT Custom Object (`container: "migration-mapping"`, `key: "{migrationId}"`); the source migration path (Frontastic / Custom Next.js / Monolith) is displayed as a badge in the page header.
2. The review table supports bulk actions: "Set all unmatched to Red Zone", "Accept all high-confidence mappings (≥ 0.85)", and "Export mapping as JSON"; row-level actions include: edit zone, edit field mappings (opens a field-mapping drawer), adjust CASL permissions, and skip/exclude component from migration.
3. The field-mapping drawer shows the source schema fields alongside the target library component's `propSchema`; field type mismatches are highlighted; the operator can select a type coercion strategy (`cast`, `transform`, `manual`) or mark the field as `__requiresManualFill`; changes are validated client-side against the Zod schema for the target component.
4. Zone assignment changes trigger a governance check: promoting to Green Zone requires completing a checklist modal (accessibility compliant, no external API dependencies not proxied through CT, no hard-coded credentials).
5. A summary sidebar shows live-updating counts: total components, Green Zone, Red Zone, excluded, field mappings complete/incomplete; the "Publish Mapping" button is enabled only when all non-excluded components have complete field mappings and explicit zone assignments.
6. On publish, the application writes the finalised mapping back to the migration CT Custom Object (with `status: "published"`) and merges all Green Zone components into the published component library Custom Object using a version-safe update; a Neon database migration is generated for any new component schema fields.
7. The published mapping triggers a webhook event `migration.mapping.published` that the Neon branch CI pipeline can consume to run automated schema validation tests.

**Dependencies:** Story 4.9 or 4.10 or 4.11 (any migration path), published component library CT Custom Object, Neon branch database
**FRs Covered:** FR36
**Complexity:** L

---

### Story 4.13: Migrated Page Validation & Readiness Report

**As a** platform operator preparing a migrated site for go-live
**I want** all migrated pages validated for required field completeness, broken reference detection, and accessibility, with a per-page pass/fail readiness report
**So that** I can confidently go live knowing no migrated page has missing data, dead references, or critical accessibility failures

**Acceptance Criteria:**
1. The readiness report is triggered manually from the migration review UI (Story 4.12) via "Run Validation", or automatically after `migration/generate-monolith-canvas` completes; it queues an Inngest function `migration/validate-pages` that processes each migrated page draft sequentially using `step.run`.
2. For each page, the validator checks required field completeness: every component is inspected for properties flagged `required: true` in the library component schema; components with any `required` field that is null, undefined, or `__aiIncomplete: true` are flagged as `INCOMPLETE` with specific field names.
3. Broken reference detection resolves all CT reference fields (product, category, content entry references) against the live CT project API; any reference returning `404` or `ResourceNotFound` is flagged as `BROKEN_REFERENCE` with the field path and unresolvable reference ID.
4. Accessibility validation runs a subset of axe-core rules server-side against a rendered HTML snapshot: `color-contrast`, `image-alt`, `label`, `link-name`, and `landmark-one-main`; violations at `critical` or `serious` severity are included as `ACCESSIBILITY_VIOLATION` items.
5. The per-page report object has shape `{ pageId, pageType, pageUrl, status: 'PASS'|'FAIL'|'WARNING', checks: { requiredFields, brokenReferences, accessibility }, checkedAt }`; a page is `PASS` only if all three categories have zero failures; `FAIL` if any critical violations exist.
6. The readiness report UI renders a filterable table of all pages with status badges; a top-level summary shows: total pages, passing, failing, warnings, and an overall go-live readiness indicator.
7. The full readiness report is written to a CT Custom Object (`container: "migration-readiness"`, `key: "{migrationId}-{timestamp}"`); each re-run creates a new versioned CT Custom Object rather than overwriting, preserving validation history.

**Dependencies:** Story 4.12, CT Custom Objects API, CT project API (reference resolution), axe-core, Inngest 4.2.6
**FRs Covered:** FR39
**Complexity:** M
## Epic 5: Behavioral Data Infrastructure

### Story 5.1: Behavioral Event Collection Pipeline

**As a** storefront operator
**I want** a lightweight JavaScript snippet to automatically collect click, scroll, and impression events from my storefront and stream them to ClickHouse
**So that** behavioral data accumulates immediately upon project connection, building a rich analytics moat before any analytics UI surface is required

**Acceptance Criteria:**
1. A `<script>` tag snippet is generated per CT project connection and available for copy/paste in the IT Admin dashboard; the snippet initializes an event listener for `click`, `scroll`, and `IntersectionObserver` impression events and attaches a `data-aci-section` attribute resolver to canvas-rendered sections.
2. Events are batched client-side (max 50 events or 2-second flush interval, whichever comes first) and POSTed to `/api/events` with payload schema `{ tenant_id, session_id, user_hash, event_type, section_id, page_path, timestamp_ms, metadata }`.
3. The `/api/events` route handler validates the payload against a Zod schema, writes to a ClickHouse `behavioral_events` table via the `@clickhouse/client` Node.js driver using `INSERT INTO behavioral_events FORMAT JSONEachRow`, and returns `202 Accepted` within 500 ms at p99 under 100K events/second load.
4. The snippet is loaded via `async` attribute and wrapped in a `requestIdleCallback` fallback so that no storefront render-blocking occurs; Lighthouse performance score regression must be less than 1 point in CI.
5. `user_hash` is computed as `HMAC-SHA256(sessionId, TENANT_SECRET)` — raw `userId` is never transmitted or stored; the hash is re-keyed per tenant secret rotation.
6. Event collection activates automatically when the CT project is first connected; the behavioral events table is activated from Epic 1 Story 1.2; no manual activation step is required.
7. A ClickHouse `MergeTree` table `behavioral_events` is partitioned by `toYYYYMM(timestamp)` and ordered by `(tenant_id, section_id, timestamp)` to support efficient per-tenant, per-section range scans.

**Dependencies:** Story 1.2 (behavioral_events table), Story 4.1 (CT project connection)
**FRs Covered:** FR25
**Complexity:** XL

---

### Story 5.2: Consent-Aware Event Collection & PCI Boundary

**As a** compliance officer
**I want** event collection to be strictly gated on consent flags and blocked entirely within PCI-scoped checkout and payment routes
**So that** the platform meets GDPR dual-track consent requirements and maintains PCI DSS compliance by preventing ACI script execution near cardholder data flows

**Acceptance Criteria:**
1. The event snippet reads an `aciConsent` boolean from the tenant's session cookie/localStorage consent store before initializing any listeners; if `aciConsent === false` no events are dispatched, no network requests are made, and the batch queue is cleared immediately.
2. A separate `clvConsent` flag gates identity-linked CLV personalization event enrichment (appending `clv_tier` to event metadata); `aciConsent` and `clvConsent` are treated as independent legal consent layers — granting one does not imply granting the other.
3. A strict Content Security Policy header is injected by the Next.js middleware for all routes matching `/checkout/**` and `/payment/**`: `script-src 'self'` with no ACI snippet domain in the allowlist, enforced via `next.config.js` `headers()` and validated with a CSP evaluator test in CI.
4. On consent withdrawal, a server-side `POST /api/consent/revoke` sets `aciConsent = false` in the tenant config store; the snippet polls a `/api/consent/status` endpoint every 30 seconds and halts all collection within one polling cycle of revocation, with no page reload required.
5. Integration tests assert that no `behavioral_events` rows are written to ClickHouse for sessions where `aciConsent` is `false`, using a ClickHouse test fixture with row count assertions.
6. A CSP violation report endpoint (`/api/csp-report`) captures and logs any ACI script execution attempts on PCI routes for audit purposes.
7. Consent state transitions are written to a `consent_audit_log` table with columns `(tenant_id, consent_type, previous_value, new_value, changed_at, changed_by_user_id)`.

**Dependencies:** Story 5.1, Story 5.10
**FRs Covered:** FR26, FR47, FR49
**Complexity:** L

---

### Story 5.3: Canvas-Anchored Heatmap Overlay

**As an** ACI Analyst
**I want** to toggle a heatmap overlay directly on the canvas that visualises click density per section
**So that** I can identify high- and low-engagement areas without leaving the canvas editor or opening a separate analytics dashboard

**Acceptance Criteria:**
1. A "Heatmap" toggle button appears in the canvas toolbar; activating it fetches a ClickHouse query result via `useMcQuery` calling `GET /api/analytics/heatmap?page_path=<path>&tenant_id=<id>&from=<iso>&to=<iso>` which executes `SELECT section_id, count() AS clicks FROM behavioral_events WHERE tenant_id = {tenantId} AND page_path = {pagePath} AND timestamp BETWEEN {from} AND {to} GROUP BY section_id`.
2. The overlay renders as a semi-transparent `<canvas>` element positioned `absolute` over the canvas iframe using a `position: absolute; pointer-events: none; z-index: 999` layer, so canvas interactions remain fully functional when the overlay is active.
3. Color gradient is mapped from cool (blue, <10th percentile click density) through warm (yellow, median) to hot (red, >90th percentile), computed client-side using `d3-scale` `scaleSequential` with a reversed `interpolateRdYlBu` palette.
4. Heatmap data is scoped strictly per tenant via the ClickHouse query's `tenant_id` predicate; cross-tenant data leakage is validated with an integration test asserting zero cross-tenant row returns.
5. The overlay updates when the canvas date-range filter changes (shared filter state via Zustand store); a loading skeleton replaces the overlay during refetch, and the refetch completes within 3 seconds per NFR.
6. Sections with fewer than 10 click events display an "Insufficient data" badge instead of a heat color to prevent misleading visualisation on sparse data.
7. The heatmap toggle state persists in the URL query string (`?overlay=heatmap`) so analysts can share a direct link to a heatmap view of a specific page.

**Dependencies:** Story 5.1 (ClickHouse data), canvas editor (Epic 2)
**FRs Covered:** FR21
**Complexity:** L

---

### Story 5.4: Section Engagement Score Badges

**As an** ACI Analyst
**I want** each canvas section to display an inline engagement score badge (0–100)
**So that** I can instantly see relative section performance without running manual queries or switching context

**Acceptance Criteria:**
1. Each canvas section renders a pill-shaped badge in its top-right corner showing a numeric engagement score (0–100); the badge is only visible when the analytics overlay mode is active.
2. The engagement score is computed server-side in `/api/analytics/engagement-score` as a weighted average: `score = (CTR * 0.4) + (scroll_depth_pct * 0.35) + (time_on_section_normalised * 0.25)`, from ClickHouse aggregations over `behavioral_events` for the given `tenant_id`, `section_id`, and date range.
3. Badge color follows threshold rules in a shared `getScoreColor(score: number)` utility: green (`#16a34a`) for score > 70, amber (`#d97706`) for 40–70 inclusive, and red (`#dc2626`) for score < 40; color thresholds are unit-tested.
4. Scores are fetched in a single bulk request `GET /api/analytics/engagement-scores?page_path=<path>` returning an array of `{ section_id, score }` objects; individual per-section requests are not made to avoid N+1 query patterns.
5. Badges display a spinner while data loads and a dash (`—`) if no data is available for a section, rather than showing a misleading 0.
6. Hovering a badge reveals a tooltip breakdown showing the three component values (CTR %, scroll depth %, time-on-section seconds) used to compute the score.
7. Engagement scores are cached in a React Query cache with a 5-minute stale time to prevent excessive ClickHouse queries during active canvas editing sessions.

**Dependencies:** Story 5.1, Story 5.3 (overlay toggle pattern)
**FRs Covered:** FR22
**Complexity:** M

---

### Story 5.5: Drop-off Rate Annotations

**As an** ACI Analyst
**I want** hover tooltips on canvas sections that show the exit/drop-off rate for each section
**So that** I can identify where users abandon a page and prioritise sections for content optimisation

**Acceptance Criteria:**
1. Each canvas section in analytics overlay mode shows a downward-arrow annotation icon; hovering it triggers a tooltip rendering the drop-off rate as a percentage (e.g., "34.2% drop-off") sourced from a ClickHouse funnel query.
2. The funnel query executed: `SELECT section_id, countIf(is_last_section = 1) / count() AS dropoff_rate FROM behavioral_events WHERE tenant_id = {tenantId} AND page_path = {pagePath} AND timestamp BETWEEN {from} AND {to} GROUP BY section_id ORDER BY section_id`, where `is_last_section` is a pre-computed boolean column set during event ingestion.
3. Tooltip data is fetched via `GET /api/analytics/dropoff` using `useMcQuery`; the request is deduped so hovering multiple sections in quick succession does not fire redundant ClickHouse queries.
4. When the canvas date-range filter changes, all cached drop-off annotations are invalidated and refetched; a subtle loading state (opacity 0.5) is applied to annotation icons during refetch.
5. Sections with a drop-off rate above 50% render the annotation icon in red to draw immediate analyst attention; this threshold is configurable via a tenant-level analytics settings record.
6. Tooltip renders within 200 ms of hover using optimistic cached data from the bulk fetch; if no cached data exists, a skeleton loader appears for the duration of the fetch.
7. Drop-off annotations are excluded from exported canvas screenshots/PDFs to avoid presenting raw analytics data in design assets.

**Dependencies:** Story 5.1 (ClickHouse data with `is_last_section` column), Story 5.3 (overlay mode)
**FRs Covered:** FR27
**Complexity:** M

---

### Story 5.6: Page-Level Performance Metrics Overlay

**As an** ACI Analyst
**I want** a toggleable overlay panel on the canvas showing page-level load time, scroll depth, and exit rate
**So that** I can assess overall page health at a glance while reviewing section-level composition

**Acceptance Criteria:**
1. A "Page Metrics" toggle in the canvas toolbar opens a fixed overlay panel anchored to the top-right of the canvas viewport, displaying three metrics: median page load time (ms), average scroll depth (%), and page exit rate (%).
2. Each metric is sourced from a dedicated ClickHouse aggregation: load time from `median(page_load_ms)`, scroll depth from `avg(max_scroll_pct)`, and exit rate from `countIf(is_exit_page = 1) / count()`, all filtered by `tenant_id`, `page_path`, and the shared date-range filter.
3. The panel data loads within 3 seconds of the analyst navigating to a new canvas page (measured from `router.pathname` change event to panel render-complete), enforced as an automated Playwright performance assertion in CI.
4. The overlay panel is built as a self-contained React component that does not rerender the canvas iframe on open/close; it is portalled to a `#analytics-overlay-root` DOM node outside the canvas tree.
5. Each metric card within the panel displays a sparkline (7-day trend using `recharts` `LineChart`) alongside the current period value, sourced from a `GROUP BY toDate(timestamp)` ClickHouse sub-query.
6. If ClickHouse returns no rows for the current page, the panel displays an empty state: "No data yet — metrics will appear once your storefront receives traffic."
7. The panel's visibility state is tracked in the URL query string (`?overlay=page-metrics`) consistent with the heatmap overlay pattern.

**Dependencies:** Story 5.1, Story 5.3 (overlay toggle pattern)
**FRs Covered:** FR27
**Complexity:** M

---

### Story 5.7: ACI Section Flagging & Operator Notifications

**As an** ACI Analyst
**I want** to flag a low-performing canvas section via a right-click context menu and automatically notify the assigned operators
**So that** content owners are immediately alerted to sections that require attention without manual out-of-band communication

**Acceptance Criteria:**
1. Right-clicking any canvas section in analytics overlay mode reveals a context menu option "Flag for review"; selecting it opens a modal with a required "Reason" text field (max 500 chars) and optional severity selector (Low / Medium / High).
2. On submission, a `POST /api/flags` call creates a `section_flags` record `{ id, tenant_id, section_id, page_path, reason, severity, flagged_by, created_at }` in the Neon Postgres database.
3. The flag creation triggers a Resend email via the Resend v6.12.2 SDK to all operators assigned to the flagged page; the email subject is `[Action Required] Section flagged: <section_id> on <page_path>` and the body includes the reason, severity, analyst name, and a deep-link URL resolving to the flagged section in the editor.
4. An in-app notification is simultaneously created in the `notifications` table and surfaced in the platform's notification bell for each assigned operator.
5. The deep-link URL navigates the operator directly to the flagged section, auto-scrolling it into view and displaying a yellow highlight border (Story 5.8 implements the receiver side).
6. Flag creation is idempotent per `(tenant_id, section_id, flagged_by, DATE(created_at))` to prevent duplicate notifications from double-clicks; a unique constraint enforces this in the schema.
7. A flag badge (triangular warning icon) persists on the canvas section until the flag is resolved; operators can mark a flag resolved from the notification panel, which updates `section_flags.resolved_at`.

**Dependencies:** Story 5.1 (section IDs), canvas editor (Epic 2), Resend configured
**FRs Covered:** FR23
**Complexity:** M

---

### Story 5.8: Navigate from ACI Flag to Editor Component

**As an** operator
**I want** to click a link in an ACI flag notification and land directly on the flagged canvas section with it highlighted
**So that** I can immediately understand the context of the flag without searching through the canvas manually

**Acceptance Criteria:**
1. The deep-link URL format `/app/<project-key>/canvas/<page-path>?section=<section_id>&flag=<flag_id>` is handled by the canvas page route; on load, the route reads `section` and `flag` query params and uses a `useEffect` to `document.querySelector('[data-aci-section="<section_id>"]').scrollIntoView({ behavior: 'smooth' })`.
2. The targeted section renders with a 2px amber animated pulse border for 5 seconds post-load, then fades to a static amber outline, implemented via a CSS `@keyframes` animation applied through a `data-flagged` attribute selector.
3. A dismissible banner at the top of the canvas editor reads: "You arrived via a flag raised by <analyst_name> on <date>: '<reason>' — View flag details | Dismiss"; clicking "View flag details" opens the `section_flags` record in a slide-over panel.
4. A breadcrumb trail appended to the existing canvas breadcrumb shows `… > Flag #<flag_id>` to provide clear navigation origin context.
5. If the `flag_id` corresponds to a resolved flag, the banner displays "This flag has already been resolved" in green and the amber highlight is suppressed.
6. If the `section_id` no longer exists on the page (section deleted after flag was raised), the route displays a non-blocking toast: "The flagged section no longer exists on this page" and loads the canvas normally.
7. The deep-link is protected by CASL role guard — unauthenticated or unauthorised users are redirected to the login page; the `flag_id` cannot be accessed cross-tenant due to a `tenant_id` predicate in the `section_flags` lookup query.

**Dependencies:** Story 5.7
**FRs Covered:** FR24
**Complexity:** S

---

### Story 5.9: GDPR Right-to-Erasure & Data Retention Configuration

**As an** IT Admin
**I want** to submit a right-to-erasure request for a specific `user_hash` and configure the platform's data retention period
**So that** the platform meets GDPR Article 17 obligations and I have control over how long behavioral data is stored

**Acceptance Criteria:**
1. The IT Admin dashboard exposes an "Erasure Request" form with a single `user_hash` input field; on submission, `POST /api/gdpr/erasure` enqueues an Inngest function `gdpr/erasure.requested` with payload `{ tenant_id, user_hash, requested_at, requested_by }`.
2. The Inngest job `handleErasureRequest` executes `ALTER TABLE behavioral_events DELETE WHERE tenant_id = {tenantId} AND user_hash = {userHash}` against the ClickHouse Cloud instance via the `@clickhouse/client` lightweight mutations API; job completion is confirmed via a ClickHouse `system.mutations` poll until `is_done = 1`.
3. The erasure completes and a confirmation email is sent via Resend to the requesting IT Admin within 30 calendar days; the Inngest job has `retryLimit: 5` and `timeoutMs: 2592000000` (30 days) to guarantee SLA compliance.
4. Upon job completion, a `gdpr_erasure_log` record is written: `{ tenant_id, user_hash, requested_at, completed_at, status: 'completed' | 'failed', rows_deleted }`; this log is queryable by the IT Admin for audit purposes.
5. A "Data Retention" settings panel allows the IT Admin to configure a retention period between 1 and 24 months (integer selector, default 13 months); the value is stored in the tenant's `analytics_settings` record.
6. An Inngest scheduled cron function `gdpr/retention.purge` runs daily and executes `ALTER TABLE behavioral_events DELETE WHERE tenant_id = {tenantId} AND timestamp < now() - INTERVAL {retentionMonths} MONTH` for each tenant; purge runs are logged to `gdpr_purge_log`.
7. The IT Admin dashboard displays the current retention setting, date of the last automated purge, rows purged, and a list of pending/completed erasure requests with their status.

**Dependencies:** Story 5.1 (ClickHouse `behavioral_events` table), Inngest service
**FRs Covered:** FR28, FR48
**Complexity:** M

---

### Story 5.10: Dual-Track Consent Management UI

**As an** IT Admin
**I want** separate, independently togglable consent controls for aggregate behavioral analytics and identity-linked CLV personalization
**So that** the platform's two distinct legal consent tracks are clearly separated, versioned, and auditable for GDPR accountability

**Acceptance Criteria:**
1. The IT Admin dashboard "Consent Management" panel presents two labelled toggle switches in separate cards: "Aggregate Behavioral Analytics (ACI)" and "Identity-Linked Personalization (CLV)"; toggling either has no effect on the other.
2. Each toggle change calls `PATCH /api/consent` with `{ tenant_id, consent_type: 'aci' | 'clv', enabled: boolean }`; the handler updates the `tenant_consent` table, writes a `consent_audit_log` entry, and returns the new consent state with a `version` integer that increments on each change.
3. The `consent_audit_log` table captures `{ id, tenant_id, consent_type, previous_value, new_value, changed_at, changed_by_user_id, version }` for every toggle event; this log is the source of truth for Story 6.8's audit visibility surface.
4. Consent configuration is displayed with the current version number and the timestamp/user who last modified each consent type; version history (last 10 changes per consent type) is visible in an expandable "History" accordion beneath each toggle card.
5. A warning modal appears when disabling either consent type, explaining the downstream impact and requiring the admin to type "CONFIRM" before the change is saved.
6. The consent state is consumed by the event snippet (Story 5.2) via `GET /api/consent/status?tenant_id=<id>` with a 30-second cache TTL; the response schema is `{ aci: boolean, clv: boolean, version: number }`.
7. CASL role guard restricts consent toggle operations to users with the `admin:consent:write` permission; read access permitted for `admin:consent:read`; enforced via `useMcMutation` policy assertions on the API route.

**Dependencies:** Story 5.2 (consent enforcement in event pipeline)
**FRs Covered:** FR26, FR47
**Complexity:** M

---

## Epic 6: Enterprise Administration & Compliance

### Story 6.1: SAML 2.0 / OIDC Enterprise SSO Configuration

**As an** IT Admin
**I want** to configure my organisation's SSO provider (SAML 2.0 or OIDC) within the platform settings
**So that** enterprise users can authenticate via our corporate identity provider while the platform's `ApplicationShell` session remains the canonical runtime auth context

**Acceptance Criteria:**
1. The IT Admin settings page contains an "SSO Configuration" section with a protocol selector (SAML 2.0 / OIDC); selecting SAML reveals inputs for: Metadata URL (auto-parses entity ID, ACS URL, certificate on fetch), Entity ID override, and SLO URL; selecting OIDC reveals inputs for: Client ID, Client Secret (masked), and Well-Known Configuration URL.
2. A "Test Connection" button triggers `POST /api/sso/test` which, for SAML, issues an SP-initiated `AuthnRequest` to the configured IdP; for OIDC, fetches the well-known endpoint and validates `authorization_endpoint`, `token_endpoint`, and `jwks_uri` are reachable; the button is disabled until all required fields are populated.
3. On successful test, "Save Configuration" persists the SSO config to the `tenant_sso_config` table; the `config_json` is encrypted using AES-256-GCM via the platform's KMS-backed secret store before write.
4. The `ApplicationShell` session auth remains the canonical runtime session — SSO controls Merchant Center IdP-initiated access; a SAML assertion or OIDC token is exchanged for a platform JWT at `POST /api/sso/callback` which sets the `mc_session` cookie.
5. SAML SLO is implemented at `GET /api/sso/slo`; receiving a valid IdP-initiated `LogoutRequest` invalidates the platform session and redirects to the configured post-logout URL.
6. The platform's SP SAML metadata is auto-generated and accessible at `GET /api/sso/metadata` as a downloadable XML document containing the ACS URL, entity ID, certificate, and SLO URL.
7. If SSO configuration is saved but the "Test Connection" step was never completed successfully, a persistent banner warns: "SSO is configured but untested — users may be locked out if the configuration is incorrect."

**Dependencies:** Story 1.7 (Epic 6 skeleton / tenant provisioning)
**FRs Covered:** FR40
**Complexity:** XL

---

### Story 6.2: SCIM 2.0 Automated User Provisioning & Deprovisioning

**As an** IT Admin
**I want** my Identity Provider to automatically provision, update, and deprovision platform users via SCIM 2.0
**So that** user lifecycle management is fully automated and deprovisioned users lose all platform access within 60 seconds

**Acceptance Criteria:**
1. The platform exposes a SCIM 2.0 endpoint base URL at `/scim/v2` implementing RFC 7644 operations: `POST /scim/v2/Users` (Create), `GET /scim/v2/Users/{id}` (Read), `PUT /scim/v2/Users/{id}` (Replace), `PATCH /scim/v2/Users/{id}` (Update via `Operations` array), and `DELETE /scim/v2/Users/{id}` (Deprovision).
2. The `POST /scim/v2/Users` handler maps SCIM core attributes to platform user records; the `roles` extension attribute (`urn:ietf:params:scim:schemas:extension:enterprise:2.0:User:roles`) is mapped to CASL platform roles via a configurable `scim_role_mapping` table.
3. `DELETE /scim/v2/Users/{id}` or a `PATCH` with `"active": false` triggers the Inngest function `scim/user.deprovisioned` which: invalidates all active JWT sessions, removes CASL role assignments, and sets `users.deprovisioned_at = NOW()`; the Inngest job must complete within 60 seconds.
4. All SCIM endpoints require a Bearer token authentication via `Authorization: Bearer <scim_token>` header; the SCIM token is a 256-bit random secret generated at setup and displayed once in the IT Admin settings panel with a "Regenerate Token" option.
5. `GET /scim/v2/Users` supports RFC 7644 filtering via `?filter=userName eq "user@example.com"` and pagination via `startIndex` and `count` query parameters, returning a `ListResponse` with `totalResults`, `startIndex`, `itemsPerPage`, and `Resources` array.
6. SCIM operations are idempotent: `PUT` to an existing user with identical attributes returns `200 OK` with no database write; duplicate `POST` for an existing `userName` returns `409 Conflict`.
7. All SCIM API calls are logged to a `scim_audit_log` table for security audit purposes.

**Dependencies:** Story 1.7 (tenant provisioning), Story 6.3 (role management)
**FRs Covered:** FR41
**Complexity:** L

---

### Story 6.3: Full Role Management UI

**As an** IT Admin
**I want** a comprehensive role assignment matrix UI where I can view, assign, and audit user roles across the platform
**So that** I have complete visibility and control over who has access to what, with a full history of changes for compliance

**Acceptance Criteria:**
1. The "Role Management" page renders a paginated data table listing all tenant users with columns: Display Name, Email, Current Roles (as chips), Last Login, and an "Edit Roles" action button; the table supports search by name/email and filter by role.
2. Clicking "Edit Roles" opens a slide-over panel showing a checklist of all available CASL platform roles; saving calls `PATCH /api/users/{id}/roles` with `{ roles: string[] }` which updates the CASL role assignments via `useMcMutation`.
3. A "Permission Matrix" tab renders a read-only grid with roles as columns and permission actions as rows; checkmarks indicate which roles grant each permission; this matrix is generated from the CASL `defineAbility` rule set at build time.
4. Bulk role changes are supported: selecting multiple users and clicking "Bulk Assign Role" opens a modal to add or remove a single role from all selected users; bulk operations are limited to 100 users per request.
5. A "Role Assignment History" tab displays an audit log sourced from the `role_assignment_log` table; entries are paginated and filterable by date range and target user.
6. Role changes are written to `role_assignment_log` on every `PATCH /api/users/{id}/roles` call, capturing `previous_roles` and `new_roles` as JSON arrays alongside `changed_by_user_id` and `changed_at`.
7. The "Edit Roles" action is guarded by CASL `admin:roles:write` permission; the API route enforces the same CASL policy server-side.

**Dependencies:** Story 1.7, Story 6.2 (SCIM provisioning creates users)
**FRs Covered:** FR42
**Complexity:** L

---

### Story 6.4: Multi-Brand Access Boundaries

**As a** Cross-Brand Admin
**I want** per-brand data access strictly isolated so that users scoped to one brand cannot access data from another brand, even under shared credentials
**So that** brand data sovereignty is guaranteed and no accidental cross-brand data exposure is possible

**Acceptance Criteria:**
1. Each brand maps to a distinct CT project scope; a `brand_id` UUID column is present on all multi-tenant data tables and is set at record creation time from the authenticated user's brand scope claim in the platform JWT.
2. All Neon Postgres queries against brand-scoped tables are wrapped in a Row-Level Security policy: `CREATE POLICY brand_isolation ON <table> USING (brand_id = current_setting('app.brand_id')::uuid)`; the `app.brand_id` session variable is set at the start of every database connection from the authenticated user's JWT brand claim.
3. The `Cross-Brand Admin` CASL role bypasses the RLS `brand_id` filter via a superuser-equivalent Neon role used exclusively for cross-brand queries; this elevated DB role is only assigned when the CASL ability check confirms `cross_brand_admin` permission.
4. ClickHouse queries include an explicit `AND tenant_id = {tenantId} AND brand_id = {brandId}` predicate on every analytical query; the `brand_id` is injected from the authenticated session and never accepted from client-supplied query parameters.
5. An integration test suite asserts that a user with `brand_id = 'brand-A'` JWT receives zero rows when querying tables containing only `brand-B` data, with the RLS policy active.
6. The IT Admin settings "Brands" tab lists all brand scopes within the tenant; Cross-Brand Admins see all brands, per-brand users see only their own brand.
7. Attempting a cross-brand API call returns `403 Forbidden` with error body `{ code: 'BRAND_ACCESS_DENIED', message: 'You do not have access to this brand' }`; enforced at the API route middleware layer before any DB query.

**Dependencies:** Story 1.7, Story 6.3 (role management for `cross_brand_admin` role)
**FRs Covered:** FR43
**Complexity:** L

---

### Story 6.5: EU/US Data Residency Region Selection

**As an** IT Admin
**I want** all platform data reads and writes routed to the region-specific database instance matching my selected data residency region
**So that** data sovereignty requirements are met and data never transits outside the chosen jurisdiction after activation

**Acceptance Criteria:**
1. The region selected during tenant provisioning (Story 1.7 skeleton) is fully honoured: the `tenant_settings.data_residency_region` field (`'eu' | 'us'`) determines which Neon Postgres connection string is used via `NEON_EU_DATABASE_URL` or `NEON_US_DATABASE_URL` environment variables.
2. A database connection pool factory `getDbForTenant(tenantId: string): Pool` reads the tenant's region from a lightweight in-memory cache (refreshed every 5 minutes) and returns the appropriate regional Neon connection pool; all API route handlers call this factory.
3. The IT Admin settings "Data & Compliance" tab displays the current data residency region with a lock icon and the label "Region cannot be changed after activation"; the region value is read-only once `tenant_settings.activated_at` is set.
4. Region change without explicit data migration is blocked at the API level with `400 Bad Request` and error `{ code: 'REGION_LOCKED' }`; the UI displays a "Contact Support to request a region migration" link.
5. ClickHouse Cloud behavioral data is stored in a region-matched cluster: EU tenants write to the `eu-central` ClickHouse cluster endpoint and US tenants write to the `us-east` endpoint, using the same `getClickhouseForTenant` factory pattern.
6. An integration test verifies that a write made via a EU-region tenant connection string lands in the EU Neon instance (asserted via `current_database()` and server location metadata) and not the US instance.
7. The admin settings panel displays the region as a human-readable label alongside the activation date and a tooltip explaining the data residency guarantee.

**Dependencies:** Story 1.7 (region selection at provisioning)
**FRs Covered:** FR44
**Complexity:** M

---

### Story 6.6: Data Processing Agreement Generation & Download

**As an** IT Admin
**I want** to generate, sign, and download a Data Processing Agreement PDF directly from the platform, with version history and re-sign prompts when the DPA is updated
**So that** the organisation maintains a current, legally valid DPA with the platform at all times without manual legal team coordination

**Acceptance Criteria:**
1. The IT Admin settings "Legal & Compliance" tab displays a "Data Processing Agreement" card showing: current DPA version, status (`Signed` / `Unsigned` / `Signature Required — New Version Available`), date signed, and the legal entity name on record.
2. Clicking "Generate & Sign DPA" opens a modal confirming the tenant's legal entity name (editable), the selected data residency region (read-only), and the current DPA version; submitting calls `POST /api/legal/dpa/sign` which records `{ tenant_id, legal_entity_name, region, dpa_version, signed_at, signed_by_user_id }` in the `dpa_signatures` table.
3. DPA PDF generation is performed server-side using `@react-pdf/renderer`; the PDF includes platform name, tenant legal entity name, data residency region, DPA version, effective date, signature date, and the signing user's name and email; streamed as `application/pdf` from `GET /api/legal/dpa/download?signature_id=<id>`.
4. A "Signature History" section lists all historical DPA signatures for the tenant with: DPA Version, Legal Entity Name, Region, Signed By, Signed At, and a "Download" link per entry; non-deletable.
5. When the platform's DPA version is incremented, a banner appears: "A new DPA version is available — please review and re-sign"; a Resend email is dispatched to the tenant's IT Admin.
6. Re-signing generates a new `dpa_signatures` record and PDF; the previous signature record is retained in history with `superseded_at` set to the re-sign timestamp.
7. DPA download links are protected by CASL `admin:legal:read` permission and are tenant-scoped.

**Dependencies:** Story 1.7 (tenant legal entity name), Story 6.5 (region locked)
**FRs Covered:** FR45
**Complexity:** M

---

### Story 6.7: Usage Dashboard

**As an** IT Admin
**I want** a real-time usage dashboard showing my consumption of each platform metric against my subscription tier limits
**So that** I can proactively manage usage, anticipate overages, and make informed decisions about tier upgrades before limits are hit

**Acceptance Criteria:**
1. The "Usage" tab renders a grid of gauge chart cards, one per metered resource: Sessions Consumed, AI Completions Used, Experiments Run, Recommendations Applied, PRs Generated, and Connected Storefronts; each gauge shows current period consumption vs subscription tier limit.
2. Gauge charts are implemented with `recharts` `RadialBarChart`; fill color transitions from green (0–79% of limit) to amber (80–99%) to red (100%+); the 80% threshold triggers a one-time per-billing-period Resend email warning to the IT Admin.
3. Each metric is sourced from the `usage_events` table aggregated by `billing_period_start` and `billing_period_end`; the query is `SELECT metric_type, SUM(quantity) FROM usage_events WHERE tenant_id = {tenantId} AND billing_period_id = {currentPeriodId} GROUP BY metric_type`.
4. The dashboard displays the current billing period start and end dates, and a "Resets in X days" label for each metric.
5. Clicking any gauge card opens a time-series drawer showing daily usage for that metric over the current billing period, rendered as a `recharts` `AreaChart`.
6. Subscription tier limits are stored in a `subscription_tiers` reference table; the dashboard joins this table to derive the gauge maximum, so limit changes are reflected immediately without a code deploy.
7. The Usage tab is accessible to users with CASL `admin:usage:read` permission; all `usage_events` queries include a `WHERE tenant_id = {tenantId}` predicate enforced in the API route.

**Dependencies:** Story 1.7 (subscription tier set at provisioning), Resend configured
**FRs Covered:** FR46
**Complexity:** L

---

### Story 6.8: Tenant Dual-Consent Audit Visibility

**As an** IT Admin
**I want** a queryable audit log of all consent configuration changes with CSV export capability
**So that** I can demonstrate GDPR accountability to regulators by producing a complete, timestamped record of consent state changes for any point in time

**Acceptance Criteria:**
1. The "Consent Audit Log" tab displays a paginated table sourced from the `consent_audit_log` table (written by Story 5.10) with columns: Timestamp, Consent Type (ACI / CLV), Changed By, Previous Value (Enabled/Disabled), New Value (Enabled/Disabled), and Version Number.
2. A date-range filter allows querying consent state at any historical point; the query applies immediately on change without requiring a "Search" button click.
3. A "Point-in-Time Consent State" lookup widget accepts a datetime input and returns the effective consent state at that exact moment by querying the most recent `consent_audit_log` entry before the specified timestamp; surfaced as two labelled badges (Enabled/Disabled).
4. An "Export CSV" button triggers `GET /api/admin/consent-audit/export?from=<iso>&to=<iso>` which streams a CSV file with headers `timestamp,consent_type,changed_by_email,previous_value,new_value,version`; named `consent-audit-<tenant_id>-<from>-<to>.csv`.
5. For large exports (>10,000 rows), the response is streamed using Node.js `Readable` stream piped to the response to avoid memory exhaustion.
6. Audit log entries are immutable — no `DELETE` or `UPDATE` operations are permitted on `consent_audit_log` rows; a `CHECK` constraint and revoked `DELETE`/`UPDATE` privileges on the Neon Postgres role enforce this.
7. Access to the consent audit log is restricted to CASL `admin:consent:audit` permission; the tab is hidden in the UI for users lacking this permission.

**Dependencies:** Story 5.10 (consent audit log population), Story 6.3 (role management)
**FRs Covered:** FR46, FR47
**Complexity:** M

---

### Story 6.9: IT Admin Guided Onboarding & Platform Activation Flow

**As an** IT Admin
**I want** a step-by-step guided onboarding flow that walks me through SSO setup, data residency confirmation, DPA signing, storefront connection, and component library import
**So that** the platform is fully activated and production-ready in a single guided session, with clear progress tracking and no steps that can block other steps

**Acceptance Criteria:**
1. The onboarding flow presents a vertical stepper with five steps: (1) SSO Configuration, (2) Data Residency Confirmation, (3) DPA Signing, (4) First Storefront Connection, (5) Component Library Import; each step shows a status indicator: Not Started / In Progress / Completed / Skipped.
2. Steps are independently completable in any order — clicking any step's "Start" button navigates to that step's dedicated panel without requiring prior steps to be complete; progress is persisted via `onboarding_progress` records in Neon Postgres.
3. Step 1 (SSO Configuration) deep-links to the SSO config panel from Story 6.1; completion is detected when `tenant_sso_config.enabled = true`; Step 3 (DPA Signing) marks complete when `dpa_signatures` contains a current-version record.
4. Step 2 (Data Residency Confirmation) displays the region selected at provisioning with a required confirmation checkbox; ticking this sets `tenant_settings.residency_confirmed_at`.
5. On completion of all five steps, `tenant_settings.activated_at` is set via `PATCH /api/admin/activate`; a Resend welcome email is dispatched to the IT Admin with subject "Your platform is now active — here's what to do next" including quick-start links.
6. A persistent progress banner on the IT Admin home page shows "X of 5 onboarding steps complete" with a link back to the stepper until `activated_at` is set; once activated, the banner is replaced with a "Platform Active" status chip.
7. Each onboarding step emits an `onboarding/step.completed` Inngest event with `{ tenant_id, step_name, completed_at, completed_by_user_id }` for downstream automation.

**Dependencies:** Story 1.7, Story 6.1, Story 6.5, Story 6.6, Resend configured, Inngest configured
**FRs Covered:** FR40, FR41, FR42, FR43, FR44, FR45, FR46
**Complexity:** M
## Epic 8: AI Experience Engine

### Story 8.1: Tenant Intelligence Score & Data Ramp Onboarding

**As a** commerce operator
**I want** to see a composite Intelligence Score (0–100) in the Merchant Center nav rail and a guided onboarding ramp when my store is new
**So that** I know how ready my store is for AI-driven recommendations and what actions will accelerate that readiness

**Acceptance Criteria:**
1. A `TenantIntelligenceScore` record is maintained in Postgres with four sub-scores: `sessions_score` (30%), `experiments_score` (25%), `clv_cohort_score` (25%), `prediction_accuracy_score` (20%); composite is recalculated via an Inngest function `intelligence/score.recalculate` triggered on every new ClickHouse event batch ingested (Inngest event `behavioral/batch.ingested`).
2. The MC nav rail renders a `<IntelligenceScoreBadge>` component (0–100 with colour ramp: 0–30 red, 31–60 amber, 61–100 green) protected by a CASL `read:intelligenceScore` ability guard; score tooltip shows sub-score breakdown.
3. When `sessions_score` corresponds to < 2000 qualified sessions, the UX-DR31 Day 1 empty state is shown in the Optimize drawer: a progress bar (`qualifiedSessions / 2000 * 100`) with label "Collecting behavioural data — X sessions of 2,000 needed to generate your first hypothesis".
4. The progress bar is updated in real-time via a Postgres `LISTEN/NOTIFY` channel (`tenant_session_count_updated`) proxied through a Next.js Server-Sent Event route (`/api/intelligence/stream`).
5. When `qualifiedSessions >= 2000` and no hypothesis exists, a "Create your first hypothesis manually" CTA is rendered (routes to Story 8.2 hypothesis form), satisfying UX-DR31 manual hypothesis CTA requirement.
6. `intelligence/score.recalculate` writes a score history row to `intelligence_score_history` (`tenant_id`, `composite_score`, sub-scores, `calculated_at`) so score trends can be charted over time.
7. CASL `manage:intelligenceScore` ability (admin only) allows resetting the score history for testing; all score reads are row-level-security scoped to `tenant_id`.

**Dependencies:** Epic 5 ClickHouse behavioral data pipeline live; Inngest 4.2.6
**FRs Covered:** FR61
**Complexity:** L

---

### Story 8.2: Manual Experiment Hypothesis Creation

**As a** commerce operator
**I want** to right-click any section or component on the canvas and create a hypothesis directly from that surface
**So that** I can record my own testing ideas even before automated hypothesis generation is available

**Acceptance Criteria:**
1. Canvas context menu gains a "Create Hypothesis" item when the operator right-clicks any section or component in Optimize mode; the item is hidden in Create mode; CASL `create:hypothesis` ability guard enforced server-side on the POST handler.
2. A hypothesis form modal collects: `name` (required, max 120 chars), `target_type` (`page` | `section` | `component`), `target_id` (pre-filled from canvas context), `expected_change` (free text, max 500 chars), `success_metric` (enum: `ctr` | `conversion_rate` | `add_to_cart` | `revenue_per_session` | `clv_delta`).
3. On submit, a `POST /api/hypotheses` route validates the payload with Zod `HypothesisCreateSchema` and inserts a row into the `hypotheses` table (`id`, `tenant_id`, `name`, `target_type`, `target_id`, `expected_change`, `success_metric`, `source` (`manual` | `automated`), `status` (`draft` | `running` | `retired`), `created_at`).
4. Saved hypothesis appears immediately in the Recommendation Panel (UX-DR26) under a "Pending Setup" section with an "Add to Experiment" CTA that routes to the experiment configuration flow (Story 8.4).
5. Form validation prevents submission if an identical `(tenant_id, target_id, success_metric)` tuple exists with `status = 'draft'` to avoid duplicate hypotheses; a warning banner is shown instead.
6. Hypothesis creation fires an Inngest event `hypothesis/manual.created` with payload `{ tenantId, hypothesisId, targetId }` so the Intelligence Score is recalculated (Story 8.1).

**Dependencies:** Story 8.1, Story 8.8 (Optimize mode canvas)
**FRs Covered:** FR52
**Complexity:** M

---

### Story 8.3: Automated Hypothesis Generation

**As a** commerce operator
**I want** the platform to automatically surface testable hypotheses derived from my store's behavioural patterns
**So that** I receive expert-level optimisation ideas without needing data analysis skills

**Acceptance Criteria:**
1. An Inngest cron function `hypothesis/auto.generate` runs every 24 hours (`cron: "0 3 * * *"`); it queries ClickHouse to identify pages with ≥ 2000 qualified sessions in the last 30 days filtered by `session_quality_score >= 0.6` and grouped by `(page_id, section_id)`.
2. For each eligible surface, the function calls OpenRouter via `@openrouter/ai-sdk-provider` (`model: 'anthropic/claude-3.5-sonnet'`) with top 5 behavioural metrics aggregated from ClickHouse; the prompt instructs the model to return a JSON array of hypothesis candidates conforming to `AutoHypothesisSchema`.
3. Each returned candidate is scored: `confidence_score = (sessions_factor * 0.4) + (metric_deviation_factor * 0.4) + (model_confidence * 0.2)` where `sessions_factor = min(qualified_sessions / 10000, 1)`; candidates with `confidence_score < 0.4` are discarded.
4. Accepted candidates are upserted into the `hypotheses` table with `source = 'automated'`, `status = 'draft'`, and `confidence_score`; duplicate detection uses `(tenant_id, target_id, success_metric, source)` unique index.
5. When the first automated hypothesis is generated for a tenant, an Inngest event `hypothesis/first.generated` fires, triggering a Resend transactional email and an in-app notification in the MC nav rail notification bell.
6. The `hypothesis/auto.generate` function uses Inngest's `step.run` for ClickHouse query, `step.ai.wrap` for OpenRouter call, and `step.run` for DB upsert; total function timeout is 300 seconds with a concurrency limit of 1 per tenant.
7. Operators can view all auto-generated hypotheses in the Recommendation Panel grouped by confidence tier (High ≥ 0.7, Medium 0.4–0.69); each shows the behavioural signal summary that triggered it.

**Dependencies:** Story 8.1 (ClickHouse ≥ 2000 sessions gate); Epic 5 behavioral data pipeline; OpenRouter API key
**FRs Covered:** FR53
**Complexity:** XL

---

### Story 8.4: A/B Experiment Runner — Horizon 1 Measurement

**As a** commerce operator
**I want** to run statistically rigorous A/B experiments on my storefront with automatic significance detection
**So that** I can make confident, data-backed decisions about which experience variants to roll out

**Acceptance Criteria:**
1. An experiment record is created in the `experiments` table (`id`, `tenant_id`, `hypothesis_id`, `variant_a_config` JSONB, `variant_b_config` JSONB, `traffic_split_pct` (10–90, default 50), `status`, `started_at`, `ended_at`, `max_duration_days` (default 30), `h1_significance_reached_at`, `h2_window_closes_at`) on operator confirmation.
2. An Inngest function `experiment/runner.start` is triggered on `experiment/created` event; it writes an edge flag record to the `edge_flags` table; the Next.js middleware reads this flag and deterministically assigns visitors to variant A or B using `murmurhash3(session_id + experiment_id) % 100 < traffic_split_pct`.
3. A scheduled Inngest function `experiment/h1.evaluate` runs every 6 hours and calculates Z-test: `z = (p_b - p_a) / sqrt(p_pooled * (1 - p_pooled) * (1/n_a + 1/n_b))`; experiment marked significant when `|z| > 1.96` (p < 0.05, two-tailed).
4. Confidence intervals for conversion rate delta are calculated as `delta ± 1.96 * sqrt(p_a*(1-p_a)/n_a + p_b*(1-p_b)/n_b)` and stored in `experiments.h1_confidence_interval` JSONB; displayed in the Experiment Status Surface as "+X.X% (CI: +Y.Y% to +Z.Z%)".
5. Experiment auto-stops when significance is reached OR `now() > started_at + max_duration_days * interval '1 day'`; on stop, Inngest function `experiment/runner.stop` removes the edge flag and emits `experiment/h1.complete`.
6. Traffic split is configurable between 10% and 90%; the UI warns when `n < 100` per variant (insufficient for Z-test) by computing minimum detectable effect at current sample size.
7. CASL `create:experiment` and `manage:experiment` ability guards applied to all API routes; maximum 5 simultaneously running experiments per tenant enforced by DB constraint check.

**Dependencies:** Story 8.2 or 8.3 (hypothesis must exist); Epic 5 ClickHouse pipeline; Story 8.1 (≥ 2000 session gate)
**FRs Covered:** FR54
**Complexity:** XL

---

### Story 8.5: Horizon 2 CLV Measurement

**As a** commerce operator
**I want** CLV delta, repeat purchase rate, and AOV tracked for 90 days after each experiment concludes
**So that** I understand the long-term revenue impact of my optimisation decisions, not just immediate conversion lifts

**Acceptance Criteria:**
1. When an experiment reaches H1 significance or max duration, an Inngest function `experiment/h2.start` sets `experiments.h2_window_closes_at = now() + interval '90 days'` and records each variant cohort's visitor `session_id` list in `experiment_cohorts` table.
2. A daily Inngest cron function `experiment/h2.evaluate` queries ClickHouse for each active H2 window, joining `behavioral_events` with `experiment_cohorts` to track purchases and CLV signals over the 90-day window.
3. CLV delta is calculated as `clv_delta = avg_clv_b - avg_clv_a`; AOV as `aov_delta = (total_revenue_b / order_count_b) - (total_revenue_a / order_count_a)`; repeat purchase rate as `rpr_delta = (returning_sessions_b / cohort_size_b) - (returning_sessions_a / cohort_size_a)`; all three stored in `experiments.h2_metrics` JSONB.
4. When `now() >= h2_window_closes_at`, Inngest function `experiment/h2.close` fires; H2 significance is tested using the Z-test applied to `repeat_purchase_rate` as the primary H2 metric; if significant, `experiments.h2_significance_reached_at` is set.
5. The Horizon badge in the Recommendation Panel updates from ⚡ (H1 only) to 📈 (H2 significant) when `h2_significance_reached_at` is populated; badge tooltip shows the full H2 metric breakdown.
6. H2 results are appended to the experiment record's ConfidenceCard with a secondary "90-day outcome" section showing CLV delta and repeat purchase rate delta with confidence intervals.
7. Operators receive an in-app notification and Resend email when their first H2 result closes, explaining the difference between H1 and H2 horizons.

**Dependencies:** Story 8.4 (H1 experiment runner); Epic 5 ClickHouse CLV tier signals
**FRs Covered:** FR55
**Complexity:** L

---

### Story 8.6: Canvas-Anchored Recommendation Panel

**As a** commerce operator
**I want** a ranked list of AI recommendations for the current canvas page to appear in a right-side drawer when I'm in Optimize mode
**So that** I can quickly evaluate and act on the most impactful improvements without leaving the visual editing context

**Acceptance Criteria:**
1. The Recommendation Panel (UX-DR26) renders as a right drawer (`width: 380px`, `position: fixed`, `right: 0`) within the canvas layout; it auto-opens when the drawer transitions to Optimize mode (Story 8.8); panel state is persisted in `sessionStorage`.
2. Recommendations are fetched from `GET /api/recommendations?pageId={id}&tenantId={id}` which queries the `hypotheses` table filtered by `target_id = pageId AND status = 'draft' AND tenant_id = ?`; results ranked by `confidence_score DESC`; results matching `tried_and_retired` table rows are excluded.
3. Each recommendation card shows: behavioural signal summary, expected outcome with confidence interval, Horizon badge (⚡ for H1 only, 📈 for H2 confirmed), and three action buttons: "Apply" (Story 8.9), "Generate PR" (Story 8.11), "Skip" (marks `hypotheses.skipped_at`, removes from panel).
4. The panel header displays "X recommendations for [Page Name]" with a sort control (Confidence / Expected Impact / Newest); a "Tried & Retired" section is collapsible at the bottom showing all retired recommendations with taxonomy tags.
5. An empty state is shown when no recommendations exist and `qualifiedSessions < 2000`: renders UX-DR31 data ramp progress; when sessions ≥ 2000 but no hypotheses yet, shows "Generating your first recommendations…" with estimated time.
6. Panel updates in real-time via `EventSource` subscription to `/api/recommendations/stream?pageId={id}` which emits on Postgres `NOTIFY recommendation_updated` events; new cards animate in without full panel re-render.
7. CASL `read:recommendations` ability guard on the API route; panel is not rendered for users without this ability.

**Dependencies:** Story 8.3 (automated hypotheses); Story 8.8 (Optimize mode); Story 8.13 (Tried-and-Retired)
**FRs Covered:** FR56
**Complexity:** L

---

### Story 8.7: ConfidenceCard for Recommendations

**As a** commerce operator
**I want** to expand any recommendation and see a full, transparent breakdown of the data and logic behind it
**So that** I can make informed decisions about whether to act on a recommendation without blindly trusting "AI"

**Acceptance Criteria:**
1. Clicking any recommendation card in the panel expands an inline `<ConfidenceCard>` component (no modal, expands within the panel with `max-height` animation); the card is divided into four labelled sections: "What I observed", "What I predict", "How I'd test it", "What I can't be sure of".
2. "What I observed" section displays: behavioural signal in plain language using "your data shows" phrasing, session count ("Based on X sessions in the last 30 days"), and confidence percentage rendered as a filled arc gauge; the strings are generated at hypothesis creation time by the OpenRouter call and stored in `hypotheses.confidence_card_observed`.
3. "What I predict" section displays expected outcome plus the confidence interval in brackets; if H2 data is available, a secondary "90-day view" sub-section shows CLV delta and repeat purchase rate delta with their own CI.
4. "How I'd test it" section displays the experiment setup summary auto-generated at hypothesis creation: recommended traffic split %, estimated days to significance, primary success metric label, and secondary metrics tracked.
5. "What I can't be sure of" section lists known limitations stored in `hypotheses.confidence_card_caveats` JSONB array; at least two caveats are required — the OpenRouter prompt enforces this minimum.
6. The strings "AI recommends", "the AI thinks", "model believes", and semantic equivalents are blocked at the API layer: a Zod `.refine()` validator on `HypothesisCreateSchema.confidence_card_observed` rejects any string matching `/(AI recommends|AI thinks|model believes|algorithm suggests)/i` with error message "Use 'your data shows' language only".
7. ConfidenceCard component is fully keyboard-navigable (Enter to expand, Escape to collapse) and passes WCAG 2.1 AA contrast checks for all text/background combinations.

**Dependencies:** Story 8.3 (OpenRouter-generated card content); Story 8.6 (Recommendation Panel)
**FRs Covered:** FR56, FR65
**Complexity:** M

---

### Story 8.8: Commerce Intelligence Drawer — Optimize Mode

**As a** commerce operator
**I want** the Commerce Intelligence Drawer to automatically switch to Optimize mode when I navigate to a canvas page with sufficient behavioural data
**So that** I always see the most relevant capabilities for the page I am editing without manually switching modes

**Acceptance Criteria:**
1. On canvas page load, a `GET /api/intelligence/mode?pageId={id}` call returns `{ mode: 'optimize' | 'create', qualifiedSessions: number, threshold: 2000 }` by querying ClickHouse for qualified sessions in the last 30 days; the drawer `mode` state is set to the returned value (FR65 auto-switch logic).
2. The drawer header renders a mode indicator pill ("Optimize" in green / "Create" in blue) with a manual override toggle; toggling from Optimize to Create emits `drawer/mode.override` Inngest event for audit logging; the override is stored in `sessionStorage` and expires at end of session.
3. When auto-switching to Optimize mode, the drawer preserves its current scroll position and any in-progress Create-mode form state in a `pendingCreateState` ref; a toast notification "Switched to Optimize mode — your draft is saved" is shown.
4. If `qualifiedSessions` drops below 2000 mid-session (detected by re-polling the mode API every 5 minutes), the drawer stays in Optimize mode but shows a yellow staleness banner: "Data may be insufficient — X sessions in the last 30 days" — it does not auto-revert to Create mode per UX-DR8.
5. Optimize mode renders the Recommendation Panel (Story 8.6), Campaign Workspace entry point (Story 8.14), and Experiment Status Surface (Story 8.15) in the drawer body.
6. CASL `read:optimizeMode` ability guard: users without this ability always see Create mode regardless of session count; the mode API returns `{ mode: 'create', reason: 'insufficient_permissions' }` for these users.

**Dependencies:** Epic 5 ClickHouse pipeline; Story 8.6 (Recommendation Panel)
**FRs Covered:** FR65
**Complexity:** M

---

### Story 8.9: Single-Shot Recommendation Apply with Progressive Rollout

**As a** commerce operator
**I want** to apply a recommendation as a live canvas change with a controlled progressive rollout so I can monitor real-world impact at each traffic gate before full deployment
**So that** I can confidently ship optimisations while protecting the majority of my traffic if a change underperforms

**Acceptance Criteria:**
1. Clicking "Apply" on a recommendation opens an "Apply Recommendation" confirmation sheet showing the canvas diff (before/after component config), the 4-gate rollout schedule (5% → 25% → 50% → 100%), and a "Start Rollout" button; the sheet shows the primary success metric and the metric degradation threshold that will trigger a Rollback Alert (Story 8.10).
2. On confirm, an Inngest function `rollout/progressive.start` is triggered; it uses `step.run` to write a `rollouts` DB record (`id`, `tenant_id`, `recommendation_id`, `canvas_change` JSONB, `current_gate_pct`, `gate_history` JSONB array, `status`) and sets `current_gate_pct = 5`.
3. Edge flag `rollout_{rolloutId}_pct` is written to the `edge_flags` table with `rollout_pct = 5`; the Next.js middleware applies the canvas change JSON patch only for the assigned traffic percentage, using `murmurhash3` deterministic visitor assignment.
4. The Experiment Status Surface badge shows the current gate percentage and live metric vs baseline; advancing to the next gate requires the operator to click "Advance to X%" — no automatic advancement occurs; Inngest function `rollout/gate.advance` updates `edge_flags.rollout_pct` and appends to `gate_history`.
5. The 100% gate applies the canvas change permanently to `pages.config` (full JSON patch merge) and removes the edge flag; `rollouts.status` is set to `complete`.
6. Gate advancement is blocked if a Rollback Alert (Story 8.10) is currently active for this rollout; the CASL `manage:rollout` ability guard is validated on each gate advance call.
7. Full canvas change is only visible in the visual editor at 100% gate; at gates < 100%, the canvas shows the original config with a "X% of live traffic seeing this variant" overlay badge on the affected section.

**Dependencies:** Story 8.6 (Apply action); Story 8.10 (Rollback Alert integration); Story 8.15 (Experiment Status Surface)
**FRs Covered:** FR57
**Complexity:** XL

---

### Story 8.10: Rollback Alert & Atomic Revert

**As a** commerce operator
**I want** to be proactively alerted when a live rollout is degrading key metrics and be able to revert it atomically with a single action
**So that** I can protect my customers' experience and revenue without requiring engineering intervention during an incident

**Acceptance Criteria:**
1. An Inngest function `rollout/monitor.tick` is scheduled every 15 minutes for each rollout with `status = 'running'`; it queries ClickHouse for the rollout variant's metric vs the pre-rollout baseline; alert triggered when `(current_rate - baseline_metric) / baseline_metric < -rollouts.degradation_threshold_pct / 100`.
2. When the alert condition is met, Inngest function `rollout/alert.send` fires: an in-app notification is pushed to all tenant `manage:rollout` users via Postgres `NOTIFY rollback_alert_{tenantId}`; the Rollback Alert UI (UX-DR29) is rendered as a fixed-position overlay showing metric vs baseline and a "Roll Back Now" primary button; a Resend email is also dispatched.
3. Clicking "Roll Back Now" calls `POST /api/rollouts/{id}/rollback` (CASL `manage:rollout` guard); this triggers Inngest function `rollout/atomic.revert` which uses a database transaction to: (a) delete the `edge_flags` record, (b) revert `pages.config` JSON patch if gate was at 100%, (c) set `rollouts.status = 'rolled_back'` — all three writes in a single Postgres transaction; no partial state is possible.
4. After atomic revert completes, the Inngest function verifies completion by re-reading the `edge_flags` table; if the flag still exists (write failure), the function retries up to 3 times with exponential backoff before emitting `rollout/revert.failed`.
5. A reason-capture UI is shown after rollback confirmation: a textarea with a 10-second auto-skip countdown; entered reason is stored in `rollouts.rollback_reason`; auto-skip stores `rollback_reason = null`; reason is used by Story 8.13 failure taxonomy classifier.
6. `rollout/monitor.tick` uses Inngest's `step.run` with a concurrency key of `rollout_{rolloutId}` to prevent duplicate concurrent monitors; the function is cancelled automatically when `rollouts.status` transitions to `complete` or `rolled_back`.
7. Rollback alerts are suppressed during operator-acknowledged maintenance windows; a `maintenance_windows` table records `(tenant_id, starts_at, ends_at)`; `rollout/monitor.tick` checks for active windows before firing alerts.

**Dependencies:** Story 8.9 (progressive rollout); Epic 5 ClickHouse pipeline
**FRs Covered:** FR59
**Complexity:** L

---

### Story 8.11: GitHub PR Generation for Beyond-Green-Zone Changes

**As a** commerce operator
**I want** the platform to automatically create a GitHub pull request when a recommendation requires code changes beyond what the visual canvas can apply
**So that** my development team can review and ship deeper technical changes with full context and a working preview environment

**Acceptance Criteria:**
1. When an operator clicks "Generate PR" on a recommendation, the API checks whether the required change exceeds Green Zone constraints; if beyond constraints, the GitHub App PR generation flow is invoked.
2. The GitHub App (configured via `GITHUB_APP_ID`, `GITHUB_APP_PRIVATE_KEY`, `GITHUB_INSTALLATION_ID` env vars) uses `@octokit/app` to authenticate; `octokit.rest.git.createRef` creates a new branch `ai-recommendation/{recommendationId}` from the tenant's configured `base_branch`.
3. The PR body is assembled from four sections: (a) code diff generated by an OpenRouter call diffing current component source against the AI-modified version, (b) tastic schema update as a JSON diff block, (c) behavioural evidence brief (session count, signal description, confidence score), (d) expected outcome with CI; PR is created via `octokit.rest.pulls.create`.
4. A Neon branch is auto-provisioned for the PR via `POST https://console.neon.tech/api/v2/projects/{projectId}/branches`; the connection string is injected into the Vercel preview deployment as `DATABASE_URL` via the Vercel API; preview deployment URL is posted as a PR comment by the GitHub App.
5. PR creation triggers Inngest function `pr/monitor.start` which subscribes to GitHub webhook events `pull_request` (`closed`, `merged`) via `POST /api/webhooks/github`; on merge, Inngest emits `pr/merged`; on close-without-merge, emits `pr/closed`; both update `pull_requests.status` accordingly.
6. The recommendation card transitions to "Awaiting Developer" state (UX-DR30) immediately after PR creation, showing the PR URL, PR number, and `created_at` timestamp; the `pull_requests` table records: `id`, `tenant_id`, `recommendation_id`, `pr_number`, `pr_url`, `branch_name`, `neon_branch_id`, `status`, `created_at`, `nudge_sent_at`.
7. If Neon branch provisioning fails (API timeout or quota exceeded), PR creation proceeds without the preview DB; the PR body includes a warning "⚠ Preview database unavailable — manual DB setup required"; failure is logged to `pr_creation_errors` table.

**Dependencies:** Story 8.6 (Generate PR action); GitHub App configured in tenant settings; Neon project ID; Vercel API token
**FRs Covered:** FR58
**Complexity:** XL

---

### Story 8.12: PR Status Tracker

**As a** commerce operator
**I want** to see the status of pending GitHub PRs for my recommendations and send a single developer reminder from within the platform
**So that** I can track development progress and nudge my team without switching to GitHub or requiring a GitHub account

**Acceptance Criteria:**
1. Any recommendation with `pull_requests.status = 'open'` renders in "Awaiting Developer" state (UX-DR30) in the Recommendation Panel: a "🔗 View PR #N" link, the assigned developer's GitHub username (or "Unassigned"), and a human-readable elapsed time since `pull_requests.created_at`.
2. A "Remind" button is shown when `pull_requests.nudge_sent_at IS NULL`; clicking "Remind" calls `POST /api/pull-requests/{id}/nudge` (CASL `manage:pullRequest` guard); the API verifies `nudge_sent_at IS NULL` before proceeding — enforcing the single-nudge limit at the database layer.
3. The nudge action sends two notifications in parallel via Inngest function `pr/nudge.send`: (a) a Resend email to the developer with `template: pr_reminder` including PR URL and expected outcome summary; (b) a GitHub PR comment posted via `octokit.rest.issues.createComment`.
4. After nudge is sent, `pull_requests.nudge_sent_at = now()` is written and the "Remind" button is replaced with "Reminded [relative time]" label (non-interactive); no second nudge is possible for this PR.
5. No GitHub account is required for the operator: the GitHub App authenticates all GitHub API calls using the installation token; the operator only sees PR metadata surfaced through the platform's own `pull_requests` table.
6. When `pull_requests.status` transitions to `merged` (via GitHub webhook), the recommendation card transitions to "Shipped — monitoring rollout" state and the progressive rollout flow (Story 8.9) is triggered with the merged change as the `canvasChange` source.

**Dependencies:** Story 8.11 (PR creation and GitHub webhook); Resend email configured
**FRs Covered:** FR58
**Complexity:** S

---

### Story 8.13: Failure Taxonomy & Tried-and-Retired Library

**As a** commerce operator
**I want** rolled-back experiments to be automatically classified by failure reason and to see a Tried-and-Retired library that prevents duplicate recommendations
**So that** the system learns from failures and does not waste my time re-suggesting changes that have already been proven not to work in my context

**Acceptance Criteria:**
1. When a rollout or experiment reaches `status = 'rolled_back'` or `status = 'retired'`, an Inngest function `taxonomy/classify.experiment` calls OpenRouter with the experiment's `rollback_reason` text, metric delta at rollback, session count, and a system prompt listing the four taxonomy classes: `metric_degradation`, `context_mismatch`, `operator_override`, `data_immaturity`.
2. The classification result is stored in `experiments.failure_taxonomy` (enum column) and `experiments.taxonomy_confidence` (float); if `taxonomy_confidence < 0.5`, the experiment is classified `operator_override` as the safe default; all four taxonomy labels are available for manual override by users with `manage:experiment` CASL ability.
3. A row is inserted into `tried_and_retired` table (`tenant_id`, `target_id`, `success_metric`, `taxonomy`, `experiment_id`, `retired_at`); the Recommendation Panel query excludes any hypothesis whose `(target_id, success_metric)` matches a `tried_and_retired` row where `retired_at > now() - interval '30 days'` for taxonomy classes `metric_degradation` and `context_mismatch`; `operator_override` and `data_immaturity` are not suppressed.
4. The "Tried & Retired" collapsible section at the bottom of the Recommendation Panel lists all retired recommendations for the current page; each card shows: recommendation name, retirement date, taxonomy tag (colour-coded pill), and a "Re-evaluate" CTA that fires `hypothesis/auto.generate` for that specific `targetId`.
5. Campaign-level taxonomy aggregates are shown in the Campaign Workspace (Story 8.14): a donut chart showing breakdown of retired experiments by taxonomy type.
6. Taxonomy classification is idempotent: `taxonomy/classify.experiment` uses an upsert on `(experiment_id)` unique constraint in `tried_and_retired`; re-running the function updates the taxonomy rather than creating a duplicate.

**Dependencies:** Story 8.9 / 8.10 (rollback mechanism); Story 8.6 (Recommendation Panel)
**FRs Covered:** FR60
**Complexity:** L

---

### Story 8.14: Campaign Workspace

**As a** commerce operator
**I want** to group related experiments under a named campaign with a goal metric, timeline, and success threshold so I can think in terms of business outcomes rather than individual tests
**So that** I can report on a coherent optimisation programme to stakeholders and understand whether a collection of changes achieved a meaningful goal

**Acceptance Criteria:**
1. A campaign creation form (UX-DR27) collects: `name` (required, max 80 chars), `goal_metric` (enum: `conversion_rate` | `revenue_per_session` | `add_to_cart_rate` | `clv_delta`), `start_date`, `end_date` (must be ≥ 14 days after start), `success_threshold_pct`; submitted via `POST /api/campaigns` (CASL `create:campaign` guard).
2. Experiments and rollouts can be associated with a campaign via a `campaign_id` foreign key; the association UI is a searchable dropdown on the experiment setup form and in the Recommendation Panel "Apply" sheet; one experiment can belong to at most one campaign.
3. The campaign dashboard shows: count of active vs completed experiments, aggregate metric progress vs goal rendered as a progress bar, days remaining until `end_date`, and a "Campaign on track" / "At risk" status indicator.
4. Aggregate metric progress is computed by `GET /api/campaigns/{id}/metrics` which queries ClickHouse: `SELECT AVG(metric_delta) AS aggregate_delta FROM experiment_results WHERE campaign_id = ? AND metric_name = ?` weighted by `n_sessions` per experiment; results cached in Postgres `campaign_metrics_cache` with a 1-hour TTL refreshed by Inngest function `campaign/metrics.refresh`.
5. Campaign results are reported as campaign-level outcomes: the campaign completion report states "This campaign achieved a X% improvement in [goal_metric] across Y experiments, [exceeding/missing] the X% target" — individual experiment metric changes are in an expandable appendix.
6. Completed campaigns are archived (read-only) with a "Download Report" button that generates a PDF via `@react-pdf/renderer`; the PDF includes the campaign outcome headline, experiment list, and failure taxonomy breakdown.

**Dependencies:** Story 8.4 (experiments); Story 8.9 (rollouts); Story 8.13 (failure taxonomy)
**FRs Covered:** FR64
**Complexity:** L

---

### Story 8.15: Experiment Status Surface

**As a** commerce operator
**I want** to see a live experiment status badge directly on the canvas section that is being tested and drill into a full status panel with metric details and control actions
**So that** I always have situational awareness of running experiments without leaving the canvas editing context

**Acceptance Criteria:**
1. When a section or component has an associated experiment with `status = 'running'`, the canvas renders an inline overlay badge (UX-DR28): a pill showing experiment name (truncated to 24 chars), current variant label (A/B), current traffic split percentage, and a colour-coded metric delta indicator (green if delta ≥ 0, red if delta < 0).
2. Clicking the badge opens a full status panel as a popover; the panel displays: traffic allocation bar chart (A: X% / B: Y% / holdout: Z%), H1 metrics table (CTR, conversion rate, add-to-cart per variant vs baseline), ETA to statistical significance, H2 status, and last-refreshed timestamp.
3. The status panel provides three action buttons: "Pause" (sets `experiments.status = 'paused'`, removes edge flag traffic allocation without reverting canvas change, CASL `manage:experiment` guard), "Accelerate" (calls `rollout/gate.advance` to move to the next gate), "Roll Back" (triggers Story 8.10 rollback flow with confirmation dialog).
4. Metric data in the panel is refreshed every 60 seconds via `setInterval` polling of `GET /api/experiments/{id}/metrics` which queries a ClickHouse materialised view `experiment_metrics_mv` for low-latency reads.
5. When an experiment is paused via the Pause action, the canvas badge changes to a "⏸ Paused" state; all visitor assignments from the edge flag are removed; existing conversion data is preserved and the experiment can be resumed.
6. The ETA to significance label shows "< 1 day", "~X days", or "Insufficient data" (when `daily_traffic_rate < 50`) and is never shown as a precise timestamp.
7. CASL `read:experimentStatus` guard applied to the overlay badge and panel API route; users without `manage:experiment` see the badge in read-only mode with action buttons disabled.

**Dependencies:** Story 8.4 (experiment runner); Story 8.9 (progressive rollout); Story 8.10 (rollback)
**FRs Covered:** FR54, FR57
**Complexity:** M

---

### Story 8.16: Historical Behavioral Data Import Pre-warm

**As a** commerce operator onboarding a new store
**I want** to import existing behavioural data from GA4, Hotjar, Mixpanel, or Frontastic into the platform
**So that** I can reach the 2,000-session threshold for AI hypothesis generation faster rather than waiting months for native data to accumulate

**Acceptance Criteria:**
1. An import wizard (UX-DR31 pre-warm variant) is accessible from the Data Ramp Onboarding empty state (Story 8.1); step 1 selects source (`ga4` | `hotjar` | `mixpanel` | `frontastic`); step 2 uploads a CSV/JSON export file (max 500 MB); step 3 is the field mapping UI.
2. The field mapping UI renders a two-column table: left column lists `behavioral_events` schema fields; right column has a dropdown for each row populated with the uploaded file's detected column headers; default mappings are pre-filled per source (e.g. GA4 `sessionId` → `session_id`); unmapped required fields block import progression.
3. On "Start Import", the wizard calls `POST /api/import/behavioral` which validates the field mapping with Zod, writes an `import_jobs` record, and triggers Inngest function `import/behavioral.process` with the job ID.
4. `import/behavioral.process` uses `step.run` in a loop with batches of 10,000 rows; each batch transforms source fields, appends `source: "import"` tag, and bulk-inserts into ClickHouse via HTTP API `INSERT INTO behavioral_events FORMAT JSONEachRow`; `rows_imported` is updated after each batch so the UI progress bar reflects real-time progress.
5. After import completes, the pre-warm indicator shows: imported session count, native session count, total qualified sessions, and "Estimated days to first hypothesis: X"; if `total_qualified >= 2000`, hypothesis generation is triggered immediately.
6. Imported data tagged `source: "import"` is included in hypothesis generation queries but weighted at 0.7x relative to native data in the `confidence_score` calculation; this weighting is documented in the ConfidenceCard "What I can't be sure of" caveat when imported data contributes > 30% of the evidence base.
7. Import errors are written to `import_errors` table and surfaced as a downloadable error report in the wizard completion screen; import succeeds if ≥ 80% of rows pass validation (partial import allowed).

**Dependencies:** Story 8.1 (Data Ramp Onboarding UI); Epic 5 ClickHouse schema
**FRs Covered:** FR63
**Complexity:** M

---

### Story 8.17: First 10 Experiments Free Activation

**As a** commerce operator
**I want** to run my first 10 experiments at no consumption charge and receive a clear upgrade prompt when I exhaust my free allocation
**So that** I can validate the AI Experience Engine's value before committing to paid consumption billing

**Acceptance Criteria:**
1. A `tenant_billing` table stores `free_experiments_used` (int, default 0) and `free_experiments_limit` (int, default 10, per FR62); every time `experiments.status` transitions to `running`, an Inngest function `billing/experiment.started` increments `free_experiments_used` within a serialisable transaction to prevent race conditions.
2. The `POST /api/experiments/{id}/start` route checks `free_experiments_used < free_experiments_limit OR tenant_billing.active_subscription = true` before allowing the transition; if neither condition is met, the API returns `HTTP 402 Payment Required` with `{ error: "free_experiment_limit_reached", upgradeUrl: "/settings/billing" }`.
3. The Tenant Intelligence Score panel (Story 8.1) displays a billing counter: "X of 10 free experiments used" rendered as a segmented bar with 10 segments; when `free_experiments_used >= 8`, segments 9 and 10 are coloured amber with a tooltip "Running low on free experiments".
4. When the 10th experiment starts (`free_experiments_used` transitions to 10), an Inngest event `billing/free_quota.exhausted` fires, triggering an in-app notification and a Resend email with upgrade CTA; the notification persists until dismissed.
5. For experiments 11+ on an active paid subscription, `billing/experiment.started` additionally writes a consumption billing event to `billing_events` table with `billable: true`; free-tier experiments are written with `billable: false`.
6. The free experiment counter is visible in the "Apply Recommendation" confirmation sheet (Story 8.9) as "X free experiments remaining" so operators know their quota before starting a rollout.

**Dependencies:** Story 8.4 (experiment runner); Story 8.1 (Intelligence Score panel)
**FRs Covered:** FR62
**Complexity:** S

---

### Story 8.18: Confidence Decay & Recommendation Freshness

**As a** commerce operator
**I want** recommendations to show a visible freshness indicator that decays over time and to be re-validated automatically when new matching behavioral data arrives
**So that** I never act on stale AI recommendations without knowing they are based on outdated evidence

**Acceptance Criteria:**
1. A computed column `current_confidence_score` is maintained on the `hypotheses` table via a Postgres generated column expression implementing the decay curve: 100% at day 0, ~50% at day 45, ~10% at day 90, 0.1 floor at day 90+; `age_days = EXTRACT(DAY FROM now() - created_at)`.
2. Recommendations with `current_confidence_score < (confidence_score * 0.5)` (confidence has decayed by ≥ 50% of original) are shown in the Recommendation Panel with a grey "faded" visual treatment and a Confidence Decay indicator: a downward-trending spark icon with label "Based on data from X days ago".
3. The ConfidenceCard confidence arc gauge renders `current_confidence_score * 100`% (not the original score) with a secondary label "Original confidence: Y%" when the two values differ by > 5 percentage points; the "What I can't be sure of" section automatically appends "This recommendation is based on data from X days ago — confidence has decayed to Y%" when `age_days > 45`.
4. An Inngest function `hypothesis/freshness.check` runs daily; for each hypothesis with `age_days > 45`, it queries ClickHouse for new matching behavioral data since `last_validated_at`; if `new_sessions >= 500`, it fires `hypothesis/revalidate` event.
5. The `hypothesis/revalidate` Inngest function re-runs the OpenRouter confidence scoring call with fresh behavioral data; if the new `confidence_score` is within 10% of the original, `hypotheses.created_at` is updated to `now()` (resetting the decay clock); if the new score diverges by > 10%, the hypothesis is updated with the new score and a `revalidation_note` is appended to `confidence_card_caveats`.
6. Recommendations where `current_confidence_score <= 0.1` (fully decayed, day ≥ 90) are hidden from the active recommendation panel and moved to a "Needs Re-evaluation" section; operators can manually trigger re-evaluation via `POST /api/hypotheses/{id}/revalidate` (CASL `manage:hypothesis` guard).

**Dependencies:** Story 8.3 (automated hypotheses with OpenRouter confidence scores); Story 8.6 (Recommendation Panel); Story 8.7 (ConfidenceCard)
**FRs Covered:** FR56, FR60
**Complexity:** S
