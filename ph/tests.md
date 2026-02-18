# Software Testing Checklist (250+ Patterns by Type)
> Load only the sections relevant to your stack. Skip what doesn't apply.
>
> Priority Legend: 🔴 CRITICAL | 🟡 HIGH | 🟢 MEDIUM
>
> Stack Flags — include a section only if true:
> - `HAS_FRONTEND` → include: Component Tests, E2E, Accessibility, Snapshot, Visual Regression
> - `HAS_DATABASE` → include: Integration, Database Tests, Backup/Restore Tests
> - `HAS_API` → include: API Tests, Contract Tests
> - `HAS_EXTERNAL_SERVICES` → include: Integration (external), Contract Tests, Timeout/Retry Tests
> - `HAS_ASYNC_QUEUES` → include: Integration (queue), Async/Event Tests
> - `HAS_AUTH` → include: Security Tests (auth sections)
> - `HAS_DATA_PIPELINE` → include: Data Pipeline Tests
> - `HAS_INFRA_AS_CODE` → include: Infrastructure Tests
> - `IS_MICROSERVICES` → include: Contract Tests, Chaos Tests
> - `NEEDS_HIGH_AVAILABILITY` → include: Performance, Chaos Tests
> - `HAS_FEATURE_FLAGS` → include: Configuration & Feature Flag Tests
> - `HAS_LOCALIZATION` → include: Localization / i18n Tests
> - `HAS_COMPLEX_STATE` → include: State Management items (under Component Tests)
> - `SENDS_NOTIFICATIONS` → include: Notification / Communication Tests
> - `HANDLES_PII` → include: Data Privacy / Compliance Tests
> - `HAS_CACHING` → include: Caching Tests
> - `HAS_TIME_LOGIC` → include: Time-Dependent Logic Tests
> - `HAS_MOBILE_APP` → include: Mobile Specific Tests
> - `HAS_COMPLEX_OUTPUTS` → include: Approval / Golden Master Tests

---

## 🧩 1. Unit Tests
> Always include. No exceptions. Every project has unit-testable logic.

- [ ] 1. 🔴 Each test covers ONE behavior — not "test the whole function," test one case
- [ ] 2. 🔴 Tests are fully isolated — no shared state, no file I/O, no network, no DB
- [ ] 3. 🔴 All external dependencies are mocked/stubbed — pure logic only
- [ ] 4. 🟡 Test names describe the scenario in plain English — `returns_null_when_user_not_found` not `test_user`
- [ ] 5. 🟡 Use AAA structure — Arrange, Act, Assert — one clear block each
- [ ] 6. 🔴 Test the happy path AND all failure paths explicitly
- [ ] 7. 🔴 Cover boundary values — zero, one, max, min, empty string, null, undefined
- [ ] 8. 🟡 Parameterize repeated similar tests — don't copy-paste 10 near-identical tests
- [ ] 9. 🔴 No logic inside tests — no `if`, no `for`, no `try/catch` — tests must be dumb
- [ ] 10. 🟡 One assertion concept per test — testing 5 unrelated things = 5 tests
- [ ] 11. 🔴 No sleeps or timers — inject a fake clock if time-dependent logic exists
- [ ] 12. 🟢 Assertion messages explain WHY it failed — `expected 3 got 5 (tax calc off by 2)` not just `false`
- [ ] 13. 🟡 Test pure functions first — functions with no side effects are the easiest wins
- [ ] 14. 🔴 Each test is independent — running them in ANY order must produce same results
- [ ] 15. 🟡 Avoid testing language built-ins or framework internals — test YOUR code, not theirs

---

## 🔗 2. Integration Tests
> Include if: `HAS_DATABASE` OR `HAS_EXTERNAL_SERVICES` OR `HAS_ASYNC_QUEUES`

- [ ] 16. 🔴 Use a dedicated test database — never run integration tests against production or shared dev DB
- [ ] 17. 🔴 Reset DB state between tests — teardown/truncate after each test, never assume clean state
- [ ] 18. 🟡 Use transactions for test isolation — wrap test in a transaction, roll back after
- [ ] 19. 🔴 Test the real query, not a mock — integration tests exist to catch ORM/query bugs
- [ ] 20. 🔴 Validate DB state after write operations — don't just assert the return value
- [ ] 21. 🟡 Test cascade behaviors — deletes, updates that ripple through foreign keys
- [ ] 22. 🔴 Test constraint violations explicitly — duplicate keys, null violations, FK violations
- [ ] 23. 🟡 Test with realistic data volumes — 1 row tests miss pagination/index bugs
- [ ] 24. 🔴 External service calls use sandbox/test environments — never call real payment APIs
- [ ] 25. 🟡 Verify actual HTTP request shape to external services — not just that your code ran
- [ ] 26. 🔴 Test timeout and retry behavior for external calls — simulate slow/failed responses
- [ ] 27. 🟡 Queue integration: verify message was actually enqueued with correct payload
- [ ] 28. 🔴 Queue integration: test consumer processes message correctly end-to-end
- [ ] 29. 🟢 Test connection pool exhaustion behavior — what happens under high concurrency?
- [ ] 30. 🟡 Integration tests should be slower but fewer — cover seams between modules, not every branch
- [ ] 31. 🟡 Test timezone handling — DB stores UTC, app handles conversion to local time correctly

---

## 🌐 3. API Tests
> Include if: `HAS_API`

- [ ] 32. 🔴 Test every endpoint for correct HTTP status codes — 200, 201, 400, 401, 403, 404, 422, 500
- [ ] 33. 🔴 Test response body shape — field names, types, nesting — not just status code
- [ ] 34. 🔴 Test authentication enforcement — unauthenticated request must get 401
- [ ] 35. 🔴 Test authorization enforcement — authenticated but unauthorized must get 403
- [ ] 36. 🔴 Test input validation — malformed body, missing required fields, wrong types
- [ ] 37. 🟡 Test pagination — first page, last page, out-of-bounds page, empty results
- [ ] 38. 🟡 Test filtering and sorting — valid params, invalid params, combined params
- [ ] 39. 🔴 Test error response shape is consistent — same `{ error, message, code }` structure everywhere
- [ ] 40. 🟡 Test content-type headers — request and response both correct
- [ ] 41. 🔴 Test large payloads — what happens at/above the size limit?
- [ ] 42. 🟡 Test idempotency on mutations — sending same POST twice should behave correctly
- [ ] 43. 🟡 GraphQL: test query, mutation, subscription separately
- [ ] 44. 🔴 GraphQL: test that private fields are not exposed via introspection in production
- [ ] 45. 🟢 Test versioned endpoints — v1 and v2 both work, old versions still respond correctly
- [ ] 46. 🟡 Test rate limiting — verify 429 is returned after limit exceeded
- [ ] 47. 🔴 Test CORS policy — only allowed origins/headers/methods, preflight behaves correctly
- [ ] 48. 🟡 Test cache headers — `Cache-Control`, `Vary`, `Expires` match expectations
- [ ] 49. 🟡 Test conditional requests — `ETag` / `If-None-Match` returns 304 correctly

---

## 🖥️ 4. Component Tests
> Include if: `HAS_FRONTEND`

- [ ] 50. 🔴 Test renders without crashing with default/required props
- [ ] 51. 🔴 Test all conditional rendering branches — `if (isLoggedIn)`, `if (hasError)`, etc.
- [ ] 52. 🟡 Test user interactions — click, type, submit, hover where behavior changes
- [ ] 53. 🔴 Test prop validation — wrong prop types should fail loudly, not silently render wrong
- [ ] 54. 🟡 Test state transitions — component goes from loading → loaded → error correctly
- [ ] 55. 🔴 Mock API calls — component tests shouldn't hit real network
- [ ] 56. 🟡 Test that the right events/callbacks are called — `onSubmit` called with correct args
- [ ] 57. 🟢 Test accessibility attributes — `aria-label`, `role`, `aria-expanded` update correctly
- [ ] 58. 🟡 Test keyboard interactions — tab order, enter/space on interactive elements
- [ ] 59. 🟢 Test responsive behavior if layout changes at breakpoints
- [ ] 60. 🔴 Test error boundaries — component handles thrown errors gracefully
- [ ] 61. 🟡 Test list rendering — empty list, single item, many items, key uniqueness
- [ ] 62. 🟡 Test loading states — spinner shows during async operations
- [ ] 63. 🟡 Test empty states — "No items" state is designed and renders correctly

### State Management Tests
> Include if: `HAS_COMPLEX_STATE` (Redux, Zustand, Vuex, NgRx, etc.)

- [ ] 64. 🔴 Test reducers/stores as pure functions — given state + action → expected new state
- [ ] 65. 🔴 Test selectors with edge-case state shapes — empty arrays, null nested objects
- [ ] 66. 🟡 Test side effects / sagas / thunks — async flows dispatch correct sequence of actions
- [ ] 67. 🟡 Test state rehydration — persisted state loads correctly after page refresh
- [ ] 68. 🟢 Test state shape migrations — v1 persisted state upgrades to v2 schema cleanly

---

## 🎭 5. End-to-End (E2E) Tests
> Include if: `HAS_FRONTEND`
> Caution: Keep E2E tests small and critical-path only. They are slow and flaky by nature.

- [ ] 69. 🔴 Cover critical user journeys only — signup, login, core purchase/action flow
- [ ] 70. 🔴 Never use fixed sleeps — use `waitFor`, `waitUntilVisible`, event-driven waits
- [ ] 71. 🔴 Use stable selectors — `data-testid` attributes, not CSS classes or XPath
- [ ] 72. 🟡 Reset application state before each test — fresh user, clean DB, cleared cookies
- [ ] 73. 🟡 Test the unhappy path too — what does the user see when payment fails?
- [ ] 74. 🔴 No E2E test should depend on another E2E test's output — full independence
- [ ] 75. 🟡 Run against a production-like environment — not localhost with mocked everything
- [ ] 76. 🟢 Cross-browser testing for critical flows — at minimum Chrome + Firefox + Safari
- [ ] 77. 🟡 Mobile viewport tests for responsive apps — test at 375px and 768px breakpoints
- [ ] 78. 🔴 Flaky E2E tests must be fixed or deleted — never tolerate intermittent failures
- [ ] 79. 🟢 Screenshot on failure — saves time debugging CI failures
- [ ] 80. 🟡 Test navigation and routing — deep links, browser back button, redirects

---

## 📸 6. Snapshot Tests
> Include if: `HAS_FRONTEND` OR outputs need regression detection (CLI, serialization)
> Caution: Overused snapshots become rubber stamps. Use sparingly.

- [ ] 81. 🟡 Snapshot tests for stable, pure UI components only — not ones that change often
- [ ] 82. 🔴 Always review snapshot diffs before committing — never blindly update snapshots
- [ ] 83. 🟡 Keep snapshots small and focused — snapshot one component, not an entire page
- [ ] 84. 🟢 Use inline snapshots for small outputs — easier to review than separate `.snap` files
- [ ] 85. 🟢 Snapshot API responses for regression detection — catches unintended schema changes
- [ ] 86. 🟢 Snapshot CLI output — useful for catching unintended output changes in tools

---

## 📋 7. Contract Tests
> Include if: `HAS_API` AND (`IS_MICROSERVICES` OR `HAS_EXTERNAL_SERVICES`)

- [ ] 87. 🔴 Consumer defines the contract — not the provider. Consumer says what it needs.
- [ ] 88. 🔴 Provider must verify against all consumer contracts before deploying
- [ ] 89. 🔴 Test schema compatibility — field additions OK, field removals or type changes are breaking
- [ ] 90. 🟡 Use Pact or equivalent — don't handroll contract testing
- [ ] 91. 🔴 Contract tests run in CI on BOTH consumer and provider repos
- [ ] 92. 🟡 Test backward compatibility explicitly — old consumer + new provider must still work
- [ ] 93. 🟢 Version your contracts — breaking change = new contract version, not a silent update
- [ ] 94. 🔴 Test old client + new server — existing consumers don't break on upgrade
- [ ] 95. 🔴 Test new client + old server — during rolling deploy, new client hits old instance gracefully
- [ ] 96. 🟡 Test deserialization of old persisted data — serialized v1 objects load in v2 code
- [ ] 97. 🟢 Keep a compatibility test suite of "golden" request/response pairs across versions

---

## 🔐 8. Security Tests
> Include if: `HAS_API` OR `HAS_AUTH` OR `HAS_FRONTEND`

- [ ] 98. 🔴 Test authentication cannot be bypassed — remove/forge token, expect 401
- [ ] 99. 🔴 Test horizontal privilege escalation — user A cannot access user B's resources
- [ ] 100. 🔴 Test vertical privilege escalation — regular user cannot access admin endpoints
- [ ] 101. 🔴 Test SQL injection on all user-input fields — use SQLMap or manual payloads
- [ ] 102. 🔴 Test XSS — inject `<script>alert(1)</script>` in every text input field
- [ ] 103. 🔴 Test CSRF — state-changing requests must fail without valid CSRF token
- [ ] 104. 🔴 Test that stack traces are NOT returned in error responses
- [ ] 105. 🔴 Test rate limiting on auth endpoints — brute force must be blocked
- [ ] 106. 🟡 Test that sensitive data is absent from GET params and logs
- [ ] 107. 🔴 Test file upload validation — wrong MIME type, oversized file, malicious filename
- [ ] 108. 🟡 Test SSRF prevention — user-provided URLs must be validated against an allowlist
- [ ] 109. 🟡 Dependency vulnerability scan in CI — block on critical CVEs (Snyk, Dependabot)
- [ ] 110. 🟡 Dependency license check — FOSSA/Snyk scan, detect forbidden licenses early

---

## ♿ 9. Accessibility Tests (a11y)
> Include if: `HAS_FRONTEND`

- [ ] 111. 🔴 Run automated axe/Lighthouse scan on every page — catch the easy 30% automatically
- [ ] 112. 🔴 All interactive elements reachable by keyboard — no mouse-only interactions
- [ ] 113. 🔴 Focus is visible and logical — focus ring must be visible, tab order makes sense
- [ ] 114. 🔴 All images have meaningful `alt` text — decorative images have `alt=""`
- [ ] 115. 🟡 Color contrast ratio meets WCAG AA — 4.5:1 for text, 3:1 for large text
- [ ] 116. 🟡 Forms have associated labels — `<label for>` or `aria-label` on every input
- [ ] 117. 🟡 Error messages are announced to screen readers — use `aria-live` or `role="alert"`
- [ ] 118. 🟢 Modal dialogs trap focus correctly — focus stays inside, Escape closes
- [ ] 119. 🟢 Test with an actual screen reader — VoiceOver (Mac), NVDA (Windows) at least once

---

## ⚡ 10. Performance Tests
> Include if: `NEEDS_HIGH_AVAILABILITY` OR `HAS_API` with scale requirements

- [ ] 120. 🔴 Define pass/fail thresholds BEFORE running — p95 < 200ms, error rate < 1%
- [ ] 121. 🔴 Load test against production-like environment — not localhost
- [ ] 122. 🟡 Load test: simulate expected peak concurrent users
- [ ] 123. 🟡 Stress test: find the breaking point — keep increasing until it fails
- [ ] 124. 🟡 Soak test: run normal load for hours — catches memory leaks and slow degradation
- [ ] 125. 🔴 Spike test: sudden 10x traffic burst — does it recover gracefully?
- [ ] 126. 🔴 Measure p50, p95, p99 — averages hide tail latency problems
- [ ] 127. 🟡 Test DB query performance under load — N+1 queries invisible at small scale appear here
- [ ] 128. 🟢 Benchmark critical functions — track regressions over time with baseline comparisons
- [ ] 129. 🟡 Profile memory usage under load — flat line expected, growing line = leak

---

## 🎲 11. Property-Based Tests
> Include if: complex domain logic, parsing, serialization, or algorithms exist

- [ ] 130. 🟡 Define invariants — properties that must ALWAYS be true regardless of input
- [ ] 131. 🟡 Roundtrip tests — `parse(serialize(x)) === x` for any valid `x`
- [ ] 132. 🟡 Test commutativity where it applies — `sort(sort(x)) === sort(x)` (idempotent)
- [ ] 133. 🟡 Use a framework — fast-check (JS), Hypothesis (Python), QuickCheck (Haskell/others)
- [ ] 134. 🟢 Shrinking matters — good frameworks reduce failing inputs to minimal reproducible case
- [ ] 135. 🟢 Seed your random generator in CI — reproducible failures across runs
- [ ] 136. 🟢 Stateful model testing — test sequences of random actions don't crash the system

---

## 💨 12. Smoke Tests
> Always include for any deployed service.

- [ ] 137. 🔴 App starts without crashing — basic boot test
- [ ] 138. 🔴 Health check endpoint returns 200 — `/health` or `/ping`
- [ ] 139. 🔴 DB connection succeeds on startup
- [ ] 140. 🔴 Required environment variables present — fail fast with clear error if missing
- [ ] 141. 🟡 Critical config loaded correctly — feature flags, third-party keys present
- [ ] 142. 🟡 Run smoke tests immediately post-deploy — before marking deploy successful
- [ ] 143. 🟢 Smoke tests must run in under 60 seconds — if they're slow, they won't be run

---

## 🐛 13. Regression Tests
> Always include. Written after bugs are found.

- [ ] 144. 🔴 Every bug fix MUST include a test that reproduces the bug first — red, then fix, then green
- [ ] 145. 🔴 Regression test must fail on the buggy code — verify it actually catches the issue
- [ ] 146. 🟡 Reference the bug ticket in the test name or comment — `// Bug #1234: null user crashes checkout`
- [ ] 147. 🟢 Group regression tests by feature area — easier to find related regressions later
- [ ] 148. 🟢 Use git bisect to find which commit introduced the bug — before writing the test

---

## 🗄️ 14. Database Tests
> Include if: `HAS_DATABASE`

- [ ] 149. 🔴 Test migrations apply cleanly on a fresh schema — CI must run migrations from scratch
- [ ] 150. 🔴 Test migrations are reversible — rollback must work without data loss
- [ ] 151. 🔴 Test DB constraints are enforced — FK, unique, not-null, check constraints
- [ ] 152. 🟡 Test seed data validity — seeds must apply after every migration cleanly
- [ ] 153. 🟡 Test indexes exist on columns used in WHERE/JOIN — query plan analysis
- [ ] 154. 🟡 Test transaction atomicity — partial failure must roll back completely
- [ ] 155. 🔴 Test concurrent write conflicts — optimistic locking, row versioning behavior
- [ ] 156. 🟢 Test soft-delete behavior — deleted records excluded from queries by default

---

## 🔀 15. Async / Event-Driven Tests
> Include if: `HAS_ASYNC_QUEUES` OR event-driven architecture

- [ ] 157. 🔴 Test event is published with correct schema after action
- [ ] 158. 🔴 Test consumer handles event correctly and produces expected side effect
- [ ] 159. 🔴 Test consumer is idempotent — processing same event twice must be safe
- [ ] 160. 🟡 Test dead letter queue behavior — what happens to malformed/unprocessable events
- [ ] 161. 🟡 Test consumer retry behavior — transient failures retry, permanent failures DLQ
- [ ] 162. 🔴 Test event ordering assumptions — if order matters, test out-of-order delivery
- [ ] 163. 🟢 Test event schema evolution — old consumers handle new event versions gracefully

---

## 🌪️ 16. Chaos / Resilience Tests
> Include if: `IS_MICROSERVICES` OR `NEEDS_HIGH_AVAILABILITY`

- [ ] 164. 🔴 Test behavior when dependency is down — circuit breaker opens, fallback activates
- [ ] 165. 🔴 Test behavior when dependency is slow — timeout fires, not infinite hang
- [ ] 166. 🟡 Test graceful degradation — partial failure returns degraded response, not total failure
- [ ] 167. 🟡 Test pod/process restart recovery — state is not lost, connections re-established
- [ ] 168. 🟡 Test network partition scenarios — split-brain behavior is defined and tested
- [ ] 169. 🟢 Use a chaos engineering tool — Chaos Monkey, Gremlin, Litmus for systematic injection

### Timeout, Retry & Circuit Breaker Tests
> Include if: `HAS_EXTERNAL_SERVICES` OR `IS_MICROSERVICES`

- [ ] 170. 🔴 Test that every outbound call has an explicit timeout — no infinite waits
- [ ] 171. 🔴 Test retry with exponential backoff — not hammering a failing service
- [ ] 172. 🔴 Test circuit breaker opens after N failures — subsequent calls fail fast
- [ ] 173. 🟡 Test circuit breaker half-open state — lets one probe request through to check recovery
- [ ] 174. 🟡 Test retry budget — total retries across all callers don't DDoS the dependency
- [ ] 175. 🟢 Test fallback responses when circuit is open — cached/default/degraded response returned
- [ ] 176. 🔴 Run Game Days — chaos tests in production (during off-hours) with real humans watching

---

## 🏗️ 17. Infrastructure / IaC Tests
> Include if: `HAS_INFRA_AS_CODE`

- [ ] 177. 🔴 Validate Terraform/Pulumi plans before apply — `terraform validate` + plan review in CI
- [ ] 178. 🔴 Policy-as-code checks — OPA, Checkov, tfsec scan for security misconfigs
- [ ] 179. 🟡 Test container image structure — correct base image, no root user, no leaked secrets
- [ ] 180. 🟡 Kubernetes manifest validation — `kubeval` or `kube-score` in CI pipeline
- [ ] 181. 🟢 Drift detection — alert when deployed infra diverges from IaC definition

---

## 📊 18. Data Pipeline Tests
> Include if: `HAS_DATA_PIPELINE`

- [ ] 182. 🔴 Test transformation correctness — known input → verify exact output
- [ ] 183. 🔴 Test schema validation on input — reject malformed records at ingestion
- [ ] 184. 🔴 Test idempotency — running pipeline twice on same data produces same result
- [ ] 185. 🟡 Test backfill/replay — reprocessing historical data produces correct results
- [ ] 186. 🟡 Test data quality rules — nulls, value ranges, referential integrity checked
- [ ] 187. 🟡 Test pipeline with empty input — no crashes, no output, clean exit
- [ ] 188. 🟢 Test large batch performance — acceptable runtime at expected data volumes
- [ ] 189. 🟢 Test schema evolution — pipeline handles new optional fields without breaking

---

## 🧪 19. Test Architecture & Hygiene
> Always include. These apply across ALL test types.

- [ ] 190. 🔴 No flaky tests tolerated — a test that sometimes fails is worse than no test
- [ ] 191. 🔴 Each test owns its data — no shared mutable fixtures between tests
- [ ] 192. 🔴 Tests must run in any order — never depend on execution sequence
- [ ] 193. 🟡 Use factory functions for test data — not hardcoded `{ id: 1, name: "Test" }` in 50 files
- [ ] 194. 🟡 Separate test types by folder AND by CI stage — unit runs first (fast), E2E runs last (slow)
- [ ] 195. 🔴 Test coverage measures behavior, not lines — 100% line coverage with bad tests is worthless
- [ ] 196. 🟡 Aim for meaningful coverage thresholds — 80% unit coverage on business logic is reasonable
- [ ] 197. 🔴 Don't test private methods — only public interface. Refactor if private logic needs testing
- [ ] 198. 🟡 Over-mocking is a code smell — if you mock 5 layers, your code is too coupled
- [ ] 199. 🟡 Test doubles: use the right type — stub (returns value), mock (verifies call), fake (working impl)
- [ ] 200. 🔴 CI must fail on ANY test failure — never merge with red tests
- [ ] 201. 🟡 Fast feedback loop — unit tests must run in under 30 seconds locally
- [ ] 202. 🟡 Test names are documentation — a new dev should understand the system by reading test names
- [ ] 203. 🟢 Delete obsolete tests — dead tests for deleted features are maintenance debt
- [ ] 204. 🟢 Mutation testing periodically — verify your test suite catches real bugs (Stryker, Mutmut)
- [ ] 205. 🟢 Review mutation testing reports — "survived mutants" are your false positives
- [ ] 206. 🔴 No production code changes to make tests pass — if you add `if (testing)`, your design is wrong

---

## 🧱 20. Static Analysis / Build Quality Gates
> Always include (even though not "tests", they prevent whole classes of bugs)

- [ ] 207. 🔴 Typecheck in CI (TS/myPy/etc.) — fail build on any type error
- [ ] 208. 🔴 Lint in CI — fail on new lint violations (don't rely on dev machines)
- [ ] 209. 🟡 Formatting is enforced (prettier/black) — no style-only diffs in PRs
- [ ] 210. 🔴 Secrets scanning in CI — block commits with keys/tokens (gitleaks/trufflehog)
- [ ] 211. 🟡 SAST in CI for critical repos — Semgrep rules for your stack
- [ ] 212. 🟡 SBOM + license policy check — detect forbidden licenses early

---

## 🔭 21. Observability / Operability Tests
> Include for anything deployed (APIs, workers, pipelines)

- [ ] 213. 🔴 Distinguish liveness vs readiness checks — readiness fails when DB/queue deps are down
- [ ] 214. 🔴 Structured logging contract — logs are JSON and include `request_id/trace_id`, user/tenant id where applicable
- [ ] 215. 🔴 PII redaction test — ensure sensitive fields never appear in logs/errors
- [ ] 216. 🟡 Metrics exist for golden signals — RPS, error rate, latency, saturation (and are tagged correctly)
- [ ] 217. 🟡 Trace propagation test — inbound `traceparent` (or equivalent) is forwarded to downstream calls
- [ ] 218. 🟡 Alert "smoke test" in staging — trigger a known error and verify alert fires (and routes correctly)

---

## 🚀 22. Release / Upgrade / Rollback Tests
> Especially important for DB-backed services and microservices

- [ ] 219. 🔴 Backward-compatible deploy test — **old app + new DB schema** works during rolling deploy
- [ ] 220. 🔴 Forward-compatible deploy test — **new app + old DB schema** works (or fails fast with clear error)
- [ ] 221. 🔴 Rollback test — after deploying, rollback to previous version without data corruption
- [ ] 222. 🟡 Feature-flag safety test — flags default to safe values and "off" truly disables codepaths
- [ ] 223. 🟡 Canary verification script — post-deploy runs a small critical-path suite before full rollout

---

## 💾 23. Backup / Restore / Disaster Recovery Tests
> Include if: `HAS_DATABASE` or you have any state you can't recreate

- [ ] 224. 🔴 Automated restore test in non-prod — restore latest backup and run validation queries
- [ ] 225. 🔴 RPO/RTO verification — measure restore time and data loss window against requirements
- [ ] 226. 🟡 Point-in-time recovery test (if supported) — restore to a specific timestamp
- [ ] 227. 🟡 Backup encryption + access control test — only intended roles can read backups

---

## 🖼️ 24. Visual Regression Tests
> Different from snapshots: catches CSS/layout regressions
> Include if: `HAS_FRONTEND`

- [ ] 228. 🔴 Screenshot diffs for key pages/components (Chromatic/Playwright visual)
- [ ] 229. 🟡 Run at multiple viewports + dark/light mode if supported
- [ ] 230. 🟡 Hide/normalize nondeterminism — timestamps, random images, animations disabled

---

## 🧨 25. Fuzz / Robustness Tests
> Great for parsers, validators, file upload, APIs

- [ ] 231. 🟡 Fuzz critical parsers/validators — ensure no crashes, hangs, or pathological CPU/memory
- [ ] 232. 🟡 Abuse-case payload tests — deeply nested JSON, long strings, weird unicode, invalid encodings
- [ ] 233. 🟢 Corpus-based fuzzing — keep past failing inputs as a regression suite

---

## 🔧 26. Configuration & Feature Flag Tests
> Include if: `HAS_FEATURE_FLAGS` OR complex environment-specific configuration

- [ ] 234. 🔴 Test all feature flag states — every flag ON and OFF produces correct behavior
- [ ] 235. 🔴 Test flag combinations that interact — flag A ON + flag B OFF doesn't create impossible state
- [ ] 236. 🟡 Test default flag values — what happens when flag service is unreachable?
- [ ] 237. 🟡 Test config validation at startup — typos in env vars caught immediately, not at 3am
- [ ] 238. 🟢 Test gradual rollout percentages — 10% rollout actually affects ~10% of users
- [ ] 239. 🟡 Test that removed flags are cleaned up — no dead code paths referencing stale flags

---

## 🌍 27. Localization / i18n Tests
> Include if: `HAS_LOCALIZATION` OR multi-language support

- [ ] 240. 🔴 Every user-facing string is externalized — no hardcoded English in components
- [ ] 241. 🟡 Test with longest translation — German/Finnish strings don't break layouts
- [ ] 242. 🟡 Test RTL rendering — Arabic/Hebrew layouts mirror correctly
- [ ] 243. 🔴 Test date/number/currency formatting per locale — `1,000.50` vs `1.000,50`
- [ ] 244. 🟢 Test pluralization rules — languages have 1, 2, or 6 plural forms
- [ ] 245. 🟢 Test fallback behavior — missing translation shows fallback language, not a key like `btn.submit`

---

## 📧 28. Notification / Communication Tests
> Include if: sends emails, SMS, push notifications, webhooks

- [ ] 246. 🔴 Test email/SMS content rendering — correct variables substituted, not `Hello {{name}}`
- [ ] 247. 🔴 Test that notifications are sent exactly once — no duplicates on retry
- [ ] 248. 🟡 Test unsubscribe/opt-out is respected — unsubscribed users receive nothing
- [ ] 249. 🟡 Test webhook delivery and retry — failed delivery retries with backoff
- [ ] 250. 🟡 Test webhook signature validation — consumers verify authenticity
- [ ] 251. 🟢 Test email rendering across clients — HTML emails in Gmail, Outlook, Apple Mail

---

## 🔐 29. Data Privacy / Compliance Tests
> Include if: handles PII, subject to GDPR/CCPA/HIPAA

- [ ] 252. 🔴 Test data deletion — "delete my account" actually removes PII from ALL stores
- [ ] 253. 🔴 Test data export — user data export contains all required fields, correct format
- [ ] 254. 🔴 Test PII is encrypted at rest — database fields storing SSN, email, etc. are encrypted
- [ ] 255. 🔴 Test PII is not logged — search logs for email/phone patterns, must find nothing
- [ ] 256. 🟡 Test consent enforcement — features requiring consent are blocked without it
- [ ] 257. 🟡 Test data retention — records older than retention period are actually purged
- [ ] 258. 🟡 Test anonymization — anonymized datasets cannot be re-identified

---

## 🧮 30. Caching Tests
> Include if: uses Redis, Memcached, CDN, or in-memory caching

- [ ] 259. 🔴 Test cache hit returns same data as cache miss — cached data isn't stale or wrong
- [ ] 260. 🔴 Test cache invalidation — after update, stale cache entry is purged/updated
- [ ] 261. 🟡 Test cache stampede / thundering herd — 1000 concurrent misses don't all hit DB
- [ ] 262. 🟡 Test TTL expiration behavior — data served correctly before/after expiry
- [ ] 263. 🟡 Test cache key collisions — different entities don't share cache keys accidentally
- [ ] 264. 🟢 Test graceful degradation when cache is down — falls back to source, doesn't error

---

## ⏱️ 31. Time-Dependent Logic Tests
> Include if: scheduling, TTLs, date-based business rules, timezones

- [ ] 265. 🔴 Inject a fake clock — never rely on `Date.now()` or `time.time()` directly
- [ ] 266. 🔴 Test timezone edge cases — UTC vs local, DST transitions, midnight boundary
- [ ] 267. 🟡 Test leap year / leap second behavior — Feb 29 logic, if applicable
- [ ] 268. 🟡 Test scheduled job execution — job fires at correct time, not twice, handles overlap
- [ ] 269. 🟡 Test expiration logic — tokens/sessions/trials expire at exactly the right moment
- [ ] 270. 🟢 Test date range queries — inclusive vs exclusive boundaries, start == end

---

## 📱 32. Mobile Specific Tests
> Include if: `HAS_MOBILE_APP` (Native/React Native/Flutter)

- [ ] 271. 🔴 Offline Mode — core features work without internet; sync queue works when reconnected
- [ ] 272. 🔴 App Lifecycle — backgrounding/foregrounding doesn't crash app or wipe state
- [ ] 273. 🔴 Permissions — graceful handling of "Don't Allow" (first prompt) vs "Denied" (settings) vs "Authorized"
- [ ] 274. 🟡 Deep Linking — `myapp://product/123` opens the correct screen with correct data pre-loaded
- [ ] 275. 🟡 Push Notifications — tapping notification opens correct screen; background notification updates badge/state
- [ ] 276. 🟢 Keyboard Handling — UI doesn't break when keyboard opens; `ScrollView` works; accessory bar (Done/Next) works
- [ ] 277. 🟢 Gestures — swipe-to-delete, pull-to-refresh, long-press all trigger correct actions
- [ ] 278. 🟡 OS Version Fragmentation — test on min-supported OS version, not just the latest
- [ ] 279. 🟢 Interruptions — incoming phone call, low battery warning, SMS notification—app resumes correctly

---

## 📂 33. Approval / Golden Master Tests
> Better than Snapshots for non-UI logic (PDFs, Emails, SQL, CSVs)
> Include if: `HAS_COMPLEX_OUTPUTS` (Reports, Emails, Parsers) OR `IS_LEGACY_CODEBASE`

- [ ] 280. 🟢 Golden Files — for complex text output (emails, SQL dumps), commit the "correct" version. Test fails if diff > 0.
- [ ] 281. 🟢 Approval Tests — record the output of a function once, then future runs must match exactly. Great for legacy refactoring.
- [ ] 282. 🟡 Round-trip Testing — `Input -> Parse -> Serialize -> Output` must match `Input`

---

## 🎣 34. Test Data Management
> Strategy for test data, not just the mechanics

- [ ] 283. 🟡 Anonymized Prod Data — seed script that pulls sanitized prod data for integration tests (better than fakes)
- [ ] 284. 🟢 Synthetic Data Generators — use Faker/Chance for *valid* complex objects (e.g., `generateValidUser()` ensures email is unique format)
- [ ] 285. 🔴 Data Tear-down — if a test fails halfway, data is cleaned up so the next run doesn't fail (try/finally blocks)

---

## 🔴 Critical Items by Stack — Quick Reference

### Every Project Must Have:
`#1-15` Unit | `#137-143` Smoke | `#144-148` Regression | `#190-206` Test Hygiene | `#207-212` Static Analysis

### Add if HAS_DATABASE:
`#16-31` Integration | `#149-156` Database Tests | `#224-227` Backup/Restore Tests

### Add if HAS_API:
`#32-49` API Tests | `#98-110` Security Tests

### Add if HAS_FRONTEND:
`#50-68` Component | `#69-80` E2E | `#81-86` Snapshot | `#111-119` Accessibility | `#228-230` Visual Regression

### Add if HAS_EXTERNAL_SERVICES or IS_MICROSERVICES:
`#87-97` Contract Tests | `#164-176` Chaos Tests

### Add if NEEDS_HIGH_AVAILABILITY:
`#120-129` Performance Tests | `#164-176` Chaos Tests

### Add if HAS_ASYNC_QUEUES:
`#157-163` Async/Event Tests

### Add if HAS_DATA_PIPELINE:
`#182-189` Data Pipeline Tests

### Add if HAS_INFRA_AS_CODE:
`#177-181` Infrastructure Tests

### Add if complex domain logic:
`#130-136` Property-Based Tests

### Add if HAS_FEATURE_FLAGS:
`#234-239` Feature Flag Tests

### Add if HAS_LOCALIZATION:
`#240-245` Localization Tests

### Add if HAS_FRONTEND with complex state:
`#64-68` State Management Tests

### Add if SENDS_NOTIFICATIONS:
`#246-251` Notification Tests

### Add if HANDLES_PII:
`#252-258` Data Privacy Tests

### Add if HAS_CACHING:
`#259-264` Caching Tests

### Add if HAS_TIME_LOGIC:
`#265-270` Time-Dependent Tests

### Add if HAS_MOBILE_APP:
`#271-279` Mobile Specific Tests

### Add if HAS_COMPLEX_OUTPUTS:
`#280-282` Approval/Golden Master Tests

### Every production service:
`#213-218` Observability Tests | `#219-223` Release/Rollback Tests

---