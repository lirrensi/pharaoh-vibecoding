# Code Security Checklist

> Security is not a feature. It's a requirement.
>
> **Priority Legend:** 🔴 CRITICAL | 🟡 HIGH | 🟢 MEDIUM
>
> **Format:** Every item follows: **IF [condition found] THEN [required action]**

---

## 🛡️ Authentication

- [ ] **1.** 🔴 IF implementing authentication → THEN use OAuth2/OIDC or battle-tested libraries — never roll your own
- [ ] **2.** 🔴 IF storing auth tokens client-side → THEN use `httpOnly; Secure; SameSite` cookies — never localStorage (XSS exfiltration)
- [ ] **3.** 🔴 IF storing passwords → THEN use Bcrypt (cost≥12) or Argon2id — never MD5/SHA1/SHA256 (too fast = crackable)
- [ ] **4.** 🔴 IF user logs out or resets password → THEN destroy/invalidate ALL active sessions server-side
- [ ] **5.** 🔴 IF endpoint accepts credentials → THEN rate-limit with exponential backoff + account lockout after N failures
- [ ] **6.** 🟡 IF supporting password-based auth → THEN enforce MFA on sensitive accounts/operations (admin, financial, PII access)
- [ ] **7.** 🟡 IF issuing tokens → THEN set short expiry + implement refresh token rotation (revoke family on reuse detection)
- [ ] **8.** 🔴 IF implementing password recovery/reset → THEN use unpredictable, single-use, short-lived tokens sent out-of-band — never reveal if email exists (prevents enumeration)
- [ ] **9.** 🟡 IF using OAuth → THEN enforce `state` parameter + PKCE on all flows (including mobile/native) — prevents CSRF and authorization code interception

---

## 🔐 Authorization

- [ ] **10.** 🔴 IF accessing user-owned resources → THEN verify resource ownership every request — `/me/orders` not `/user/123/orders`
- [ ] **11.** 🔴 IF endpoint has role restrictions → THEN enforce RBAC/ABAC server-side — frontend hiding buttons ≠ security
- [ ] **12.** 🟡 IF using database IDs in URLs/APIs → THEN use UUIDs over sequential IDs — prevents enumeration attacks
- [ ] **13.** 🟡 IF multi-tenant system → THEN enforce row-level security at DB layer — defense in depth, not just app layer
- [ ] **14.** 🔴 IF API has admin/elevated endpoints → THEN verify privilege escalation is impossible (horizontal AND vertical)
- [ ] **15.** 🟡 IF using JWTs for authorization → THEN validate issuer, audience, expiry, and algorithm (reject `alg: none`)

---

## 🧹 Input Validation & Injection

- [ ] **16.** 🔴 IF accepting any external input → THEN schema-validate with whitelist approach, reject unknown fields
- [ ] **17.** 🔴 IF building database queries → THEN use parameterized queries only — zero concatenated SQL, ever
- [ ] **18.** 🔴 IF using NoSQL databases (MongoDB, CouchDB) or ORMs → THEN strictly cast data types and never pass raw user JSON/objects into queries — prevents NoSQL/Object Injection
- [ ] **19.** 🔴 IF rendering user content in HTML → THEN sanitize/escape output — context-aware (HTML body vs attribute vs JS vs CSS)
- [ ] **20.** 🔴 IF accepting file uploads → THEN validate size + MIME (magic bytes, not just header) + extension + strip metadata + scan content
- [ ] **21.** 🔴 IF server fetches user-provided URLs → THEN enforce URL allowlists for SSRF prevention — block internal IPs/metadata endpoints
- [ ] **22.** 🔴 IF accepting XML input → THEN disable external entity processing (XXE) — no DTD loading
- [ ] **23.** 🔴 IF deserializing data (pickle, Java serialization, YAML.load, unserialize) → THEN never deserialize untrusted input — use safe loaders/formats
- [ ] **24.** 🔴 IF building OS commands with user input → THEN never use shell interpolation — use parameterized exec / library APIs
- [ ] **25.** 🔴 IF interpolating user input into server-side templates (Jinja2, Twig, Freemarker, ERB, Pug) → THEN use sandboxed rendering + never pass raw user strings as template source — prevents SSTI (Server-Side Template Injection → RCE)
- [ ] **26.** 🟡 IF querying LDAP/Active Directory with user input → THEN escape/parameterize LDAP filter values — prevents LDAP injection auth bypass

---

## 🔒 Secrets & Crypto

- [ ] **27.** 🔴 IF code references API keys, passwords, or credentials → THEN load from env/vault only, verify presence at startup, never hardcode
- [ ] **28.** 🔴 IF `.env` files exist → THEN confirm in `.gitignore` + audit git history for prior leaks (use tools like truffleHog/gitleaks)
- [ ] **29.** 🔴 IF generating tokens, session IDs, nonces, or random identifiers → THEN use CSPRNG — never `Math.random()` or `random.random()`
- [ ] **30.** 🔴 IF encrypting or signing data → THEN use modern algorithms only — AES-256-GCM, ChaCha20-Poly1305, Ed25519; never DES/RC4/ECB/RSA-PKCS1v1.5
- [ ] **31.** 🔴 IF comparing secrets (tokens, hashes, API keys) → THEN use constant-time comparison (`crypto.timingSafeEqual()`, `hmac.compare_digest()`) — never `===` or `==`
- [ ] **32.** 🟡 IF secrets have no rotation policy → THEN implement automated rotation + expiry — assume every secret eventually leaks

---

## 🌐 Headers & Transport

- [ ] **33.** 🔴 IF serving HTTP responses → THEN set security headers: Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options: nosniff
- [ ] **34.** 🔴 IF application is web-accessible → THEN HTTPS everywhere — redirect HTTP, no mixed content, HSTS preload
- [ ] **35.** 🔴 IF API uses CORS → THEN explicit origin allowlist — never `Access-Control-Allow-Origin: *` on authenticated endpoints
- [ ] **36.** 🟡 IF serving user-uploaded files → THEN serve from a separate domain/CDN with `Content-Disposition: attachment` — prevents stored XSS
- [ ] **37.** 🟡 IF using cookies → THEN set appropriate Path, Domain, and `__Host-`/`__Secure-` prefixes where possible
- [ ] **38.** 🟡 IF app sits behind a reverse proxy, load balancer, or CDN → THEN explicitly configure "trusted proxies" before evaluating `X-Forwarded-For` or `X-Real-IP` — prevents IP spoofing and rate-limit bypass
- [ ] **39.** 🟡 IF serving web app → THEN set `Permissions-Policy` header to restrict camera, mic, location, etc. — prevents opportunistic access via embedded content
- [ ] **40.** 🟡 IF cross-origin requests allowed → THEN set `Cross-Origin-Opener-Policy: same-origin` — prevents tab-napping via opener window
- [ ] **41.** 🟡 IF hosting sensitive resources → THEN set `Cross-Origin-Resource-Policy: same-origin` — prevents your resources from being embedded by malicious sites

---

## 🔄 State & Session

- [ ] **42.** 🔴 IF forms/mutations change state → THEN implement CSRF protection — anti-CSRF tokens or SameSite cookies
- [ ] **43.** 🔴 IF actions have side effects (payments, deletes, config changes) → THEN require idempotency keys — prevent replay/double-submit
- [ ] **44.** 🔴 IF using WebSockets or long-lived connections → THEN authenticate on connect AND validate messages — don't trust the pipe
- [ ] **45.** 🟡 IF handling concurrent requests on shared state → THEN implement proper locking / optimistic concurrency — race conditions are security bugs (TOCTOU)
- [ ] **46.** 🟡 IF caching responses → THEN ensure `Cache-Control: no-store` on authenticated/sensitive responses — prevent cache poisoning and data leakage
- [ ] **47.** 🟡 IF using Server-Sent Events (SSE) or EventSource → THEN validate Origin header + set proper CORS + no open redirect in URL params

---

## 📊 Observability & Audit

- [ ] **48.** 🔴 IF logging anything → THEN never log passwords, tokens, card numbers, PII, or secrets
- [ ] **49.** 🔴 IF sensitive operations occur (login, permission change, data export, admin action) → THEN write immutable audit log: who, what, which resource, when, from where
- [ ] **50.** 🟡 IF application has logging → THEN use structured format (JSON) — machine-parseable, not grep-dependent
- [ ] **51.** 🟡 IF distributed system → THEN propagate request correlation IDs across all services for tracing
- [ ] **52.** 🔴 IF system is in production → THEN alert on anomalies — auth failure spikes, unusual access patterns, error rate changes
- [ ] **53.** 🟡 IF user input can appear in log output → THEN sanitize for log injection — attackers forge entries via `\n`, ANSI escape codes, or format strings
- [ ] **54.** 🔴 IF error occurs → THEN return generic message to client, log full detail server-side — never expose stack traces, DB errors, or internal paths to users

---

## 📦 Supply Chain & CI/CD

- [ ] **55.** 🔴 IF project has dependencies → THEN pin exact versions + use lockfile — reproducible builds, no `^` ranges in production
- [ ] **56.** 🔴 IF CI pipeline exists → THEN run vulnerability scanning (SCA) — block deploys on critical/high CVEs
- [ ] **57.** 🟡 IF merging code → THEN require at least one independent review — no self-approvals
- [ ] **58.** 🔴 IF deploying to production → THEN have tested rollback plan — know how to undo before you ship
- [ ] **59.** 🟡 IF using containers → THEN minimal base images, run as non-root, no secrets baked into image layers
- [ ] **60.** 🟡 IF CI/CD pipeline has secrets → THEN use ephemeral credentials, scope to minimum access, audit access logs
- [ ] **61.** 🟡 IF distributing software → THEN generate & publish SBOM (Software Bill of Materials) + sign images (Sigstore/Notary) — track transitive dependencies for CVE response, prevent tampered images
- [ ] **62.** 🔴 IF running CI/CD pipelines → THEN integrate SAST + DAST + IaC scanning + fuzz testing on every PR/merge (in addition to SCA) — auto-block deploys on critical/high findings
- [ ] **63.** 🔴 IF building/deploying containerized or cloud-native workloads → THEN adopt SLSA Level 2+ provenance, verify image signatures, and enforce Pod Security Standards / NetworkPolicies / seccomp profiles

---

## 🖥️ Frontend Security

- [ ] **64.** 🟡 IF loading scripts from CDNs → THEN use Subresource Integrity (SRI) — don't trust third-party CDNs blindly
```html
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-abc123..."
        crossorigin="anonymous"></script>
```

- [ ] **65.** 🔴 IF sensitive data exists (tokens, passwords, PII) → THEN never put in URLs/query strings — leaked via browser history, referrer headers, server logs
- [ ] **66.** 🔴 IF rendering dynamic content → THEN never use `innerHTML`, `dangerouslySetInnerHTML`, `eval()`, `document.write()`, or `v-html` with untrusted data
- [ ] **67.** 🟡 IF client-side storage used (localStorage, sessionStorage, IndexedDB) → THEN never store secrets or sensitive PII — all are accessible to XSS
- [ ] **68.** 🟡 IF using `window.postMessage` or listening for message events → THEN always validate `event.origin` against an allowlist + schema-validate `event.data` — cross-origin message forgery leads to XSS and data exfiltration
- [ ] **69.** 🟡 IF application handles mobile deep links or custom URI schemes (`myapp://`) → THEN treat the entire URI payload as untrusted external input — prevents client-side execution and phishing

---

## 🏗️ Infrastructure & Runtime

- [ ] **70.** 🔴 IF handling file paths with user input → THEN canonicalize + validate against base directory — prevent path traversal (`../../../etc/passwd`)
- [ ] **71.** 🔴 IF application processes data in loops/buffers → THEN enforce size limits + timeouts — prevent DoS via resource exhaustion (zip bombs, regex DoS, billion laughs)
- [ ] **72.** 🟡 IF running services → THEN apply principle of least privilege — minimum permissions for files, network, database, cloud IAM
- [ ] **73.** 🟡 IF application accepts regex from users → THEN sanitize or use RE2/safe regex — prevent ReDoS (catastrophic backtracking)
- [ ] **74.** 🔴 IF running in production → THEN disable debug modes, development endpoints, verbose errors, default credentials
- [ ] **75.** 🟡 IF using cloud services → THEN audit IAM policies, ensure no `*:*` permissions, enable CloudTrail/audit logging
- [ ] **76.** 🟡 IF database is accessible → THEN encrypt at rest + in transit, restrict network access, separate read/write credentials
- [ ] **77.** 🟡 IF writing in unmanaged languages (C, C++) or using FFI/Native modules → THEN enforce strict bounds checking + compile with OS-level memory protections (ASLR, DEP, PIE) — prevents buffer overflows

---

## 🧬 API-Specific Security

- [ ] **78.** 🔴 IF API returns data → THEN filter response fields server-side — never return full DB objects (mass assignment / over-exposure)
- [ ] **79.** 🔴 IF API accepts nested/complex objects → THEN limit depth + size — prevent resource exhaustion via deeply nested JSON/GraphQL queries
- [ ] **80.** 🟡 IF API is public → THEN enforce rate limiting per-client — not just auth endpoints, ALL endpoints
- [ ] **81.** 🟡 IF API versioning exists → THEN deprecate and remove old versions — stale APIs are unpatched attack surface
- [ ] **82.** 🔴 IF GraphQL → THEN disable introspection in production, enforce query depth/cost limits, whitelist allowed queries
- [ ] **83.** 🔴 IF API receives webhooks from external services (Stripe, GitHub, Twilio, etc.) → THEN verify webhook signatures using the provider's signing secret — never trust payload authenticity based on source IP alone
- [ ] **84.** 🟡 IF API supports batch/bulk endpoints (`POST /users/bulk`, GraphQL batching, array of IDs) → THEN enforce per-request item limits + apply auth/rate-limits per sub-operation — prevents amplification attacks

---

## 🧯 Error Handling & Failure Modes

- [ ] **85.** 🔴 IF security check fails → THEN fail closed (deny access) — never fail open
- [ ] **86.** 🔴 IF auth/lookup fails → THEN return identical responses for "user not found" vs "wrong password" — prevent user enumeration
- [ ] **87.** 🟡 IF external dependency fails → THEN implement circuit breaker + graceful degradation — don't cascade failures into security bypasses

---

## 📱 Mobile & Native Clients

- [ ] **88.** 🔴 IF building mobile apps → THEN store nothing sensitive in SharedPreferences/Keychain without OS-level encryption (Android Keystore / iOS Secure Enclave) + biometric gating for high-risk actions
- [ ] **89.** 🔴 IF mobile app → THEN implement root/jailbreak detection + terminate if detected (or at minimum disable sensitive functionality)
- [ ] **90.** 🔴 IF using deep links/custom URL schemes → THEN validate + whitelist allowed domains/paths — prevent deep link hijacking
- [ ] **91.** 🟡 IF mobile app uses WebViews → THEN disable JavaScript Interface unless absolutely needed + use `file://` domain separation + CSP
- [ ] **92.** 🔴 IF distributing mobile app → THEN code-sign + verify signature at runtime (anti-tampering)
- [ ] **93.** 🟡 IF using WebRTC → THEN disable STUN/TURN IP leakage (RTCPeerConnection ICE candidate filtering) — prevents local IP exposure

---

## 🌐 Zero-Trust & Network Security

- [ ] **94.** 🔴 IF internal services talk to each other → THEN require mTLS everywhere — no "internal = trusted"
- [ ] **95.** 🔴 IF user auth → THEN implement continuous session risk scoring (impossible travel, device fingerprint changes, TOR exit nodes) + re-auth on high risk
- [ ] **96.** 🟡 IF remote access (SSH, RDP, bastion) → THEN require hardware security keys (YubiKey/WebAuthn) — no passwords/phishable MFA
- [ ] **97.** 🔴 IF any service account / machine identity exists → THEN use short-lived certs (SPIFFE/SPIRE, AWS IAM Roles Anywhere, GCP Workload Identity) — no long-lived service account keys
- [ ] **98.** 🟡 IF API keys exist → THEN scope them to exact IP + exact endpoint + exact permission + auto-expire after 90 days max
- [ ] **99.** 🟡 IF using caching layers (Redis, Memcached, etc.) → THEN disable public access + require auth + run in private VPC + encrypt sensitive data before caching
- [ ] **100.** 🟡 IF behind Cloudflare/AWS → THEN disable "I'm under attack mode" bypass techniques (direct IP access, old TLS versions)

---

## 💰 Business Logic & Abuse Prevention

- [ ] **101.** 🔴 IF processing payments, e-commerce, or quota limits → THEN calculate all prices, discounts, and totals securely on the backend — never trust or rely on pricing submitted by the frontend
- [ ] **102.** 🔴 IF coupons/gift cards/promos → THEN single-use + rate-limit redemption + atomic check-then-act — prevent race condition abuse
- [ ] **103.** 🟡 IF email/SMS verification codes → THEN rate-limit per user + per IP + expire in ≤10 min + one-time-use only
- [ ] **104.** 🔴 IF password reset / email change → THEN send delayed notification to old email ("email changed in 7 days unless canceled")
- [ ] **105.** 🟡 IF account recovery → THEN require multiple proofs + human review for high-value accounts
- [ ] **106.** 🔴 IF pricing/subscription logic → THEN use signed price IDs (Stripe style) — never trust client-sent price/amount
- [ ] **107.** 🟡 IF allowing bulk operations → THEN quota + cost analysis before execution — prevent "delete all my projects" abuse
- [ ] **108.** 🔴 IF accepting emails (contact forms, etc.) → THEN strip `\r\n` from user input — prevents SMTP header injection
- [ ] **109.** 🟡 IF using HTTP/2 or HTTP/3 → THEN test for request smuggling (TE/CL mismatches) — still possible

---

## 🔐 Data Protection & Privacy

- [ ] **110.** 🔴 IF application handles PII (names, emails, addresses, phone numbers, government IDs) → THEN classify data by sensitivity tiers, encrypt at rest, and enforce access controls per tier — not all data is equal, treat PII as toxic
- [ ] **111.** 🔴 IF application operates under GDPR/CCPA/HIPAA or similar → THEN implement data subject rights: export, deletion, consent withdrawal — "we can't delete it" is a legal vulnerability
- [ ] **112.** 🔴 IF user requests account deletion → THEN hard-delete or cryptographically erase PII within regulatory timeframe — soft-delete that keeps PII indefinitely violates retention laws
- [ ] **113.** 🟡 IF sharing data with third parties (analytics, payment processors, marketing tools) → THEN minimize fields sent + ensure DPA (Data Processing Agreement) is in place — you're liable for your vendors' breaches
- [ ] **114.** 🟡 IF storing data long-term → THEN define and enforce retention policies — auto-purge data you no longer need. Stored data you don't need is liability, not asset
- [ ] **115.** 🟡 IF backups contain PII or secrets → THEN encrypt backups, restrict access, test restoration, and include in retention/deletion policies — backups are the most overlooked breach vector
- [ ] **116.** 🔴 IF backup encryption → THEN use separate keys from production + offline storage — prevents single point of compromise

---

## 🤖 AI/LLM Security

- [ ] **117.** 🔴 IF using LLM APIs → THEN implement prompt injection detection & output sanitization — attacker manipulates prompts to bypass restrictions or extract data
- [ ] **118.** 🔴 IF accepting user input as LLM context → THEN separate untrusted content from system prompts — prevents prompt injection via context injection
- [ ] **119.** 🔴 IF LLM generates code/commands → THEN sandbox execution + validate output — prevents RCE via model-generated shell commands
- [ ] **120.** 🟡 IF storing LLM training data → THEN verify no PII/secrets in training corpus — prevents privacy violations and credential leakage
- [ ] **121.** 🔴 IF using agentic AI (autonomous code gen, auto-PR, deployment agents) → THEN sandbox every AI-executed action, implement goal-hijacking detection, and log/audit all agent decisions for replay attacks
- [ ] **122.** 🟡 IF AI-generated code is in production → THEN maintain an AI code inventory (what % of each repo is AI-generated) + run weekly automated security scans against OWASP LLM Top 10 + Agentic AI Top 10
- [ ] **123.** 🔴 IF non-deterministic systems (ML/AI) touch and mutate data → THEN maintain automated, tested backups with point-in-time recovery — AI data corruption is harder to detect and reverse than traditional bugs

---

## 🔮 Post-Quantum & Future-Proofing

- [ ] **124.** 🟡 IF long-term secrets (≥10 years) → THEN migrate to hybrid post-quantum KEM (Kyber + X25519) — prepares for quantum computing threats
- [ ] **125.** 🟡 IF using TLS → THEN monitor for TLS 1.2 deprecation + enable TLS 1.3 only + post-quantum in flight (Cloudflare does this already)
- [ ] **126.** 🟡 IF multi-region → THEN ensure data residency compliance (GDPR, data localization laws) — legal exposure

---

## 🛡️ Operational Security

- [ ] **127.** 🟡 IF team uses 2FA → THEN require hardware keys (FIDO2/WebAuthn) for high-privilege accounts — SMS/Authenticator apps vulnerable to SIM-swapping
- [ ] **128.** 🟡 IF has incident response plan → THEN test it regularly via tabletop exercises — untested plans fail when needed most
- [ ] **129.** 🟡 IF using open source → THEN audit for abandoned/unmaintained dependencies — "零日" (zero-day) in unpatched libs
- [ ] **130.** 🟡 IF CI runs tests → THEN ensure test suites can't be bypassed via CI config tampering — attackers could disable security tests

---

## 🔴 Critical Items Summary (Must-Fix Before Ship)

| Category | Critical Items |
|----------|----------------|
| Authentication | #1–5, #8 |
| Authorization | #10, #11, #14 |
| Injection Prevention | #16–25 |
| Secrets & Crypto | #27–31 |
| Transport & Headers | #33–35 |
| State & Session | #42–44 |
| Logging & Audit | #48, #49, #52, #54 |
| Supply Chain | #55, #56, #58, #62, #63 |
| Frontend | #65, #66 |
| Infrastructure | #70, #71, #74 |
| API | #78, #79, #82, #83 |
| Error Handling | #85, #86 |
| Mobile | #88–90, #92 |
| Zero-Trust | #94, #95, #97 |
| Business Logic | #101, #102, #104, #106, #108 |
| Data Protection | #110–112, #116 |
| AI/LLM | #117–119, #121, #123 |

---

## 🟡 High Priority (Fix Soon)

| Category | Items |
|----------|-------|
| Auth hardening | #6, #7, #9, #15 |
| Authorization depth | #12, #13 |
| Headers | #36–41 |
| State safety | #45–47 |
| Observability | #50, #51, #53 |
| Supply chain | #57, #59–61 |
| Frontend | #64, #67–69 |
| Infrastructure | #72, #73, #75–77 |
| API | #80, #81, #84 |
| Resilience | #87 |
| Mobile | #91, #93 |
| Zero-Trust | #96, #98–100 |
| Business Logic | #103, #105, #107, #109 |
| Data Protection | #113–115 |
| AI/LLM | #120, #122 |
| Post-Quantum | #124–126 |
| Operational | #127–130 |

---

## Quick Reference by Category

| Category | Item Range |
|----------|------------|
| Authentication | #1–9 |
| Authorization | #10–15 |
| Input Validation & Injection | #16–26 |
| Secrets & Crypto | #27–32 |
| Headers & Transport | #33–41 |
| State & Session | #42–47 |
| Observability & Audit | #48–54 |
| Supply Chain & CI/CD | #55–63 |
| Frontend Security | #64–69 |
| Infrastructure & Runtime | #70–77 |
| API-Specific Security | #78–84 |
| Error Handling & Failure Modes | #85–87 |
| Mobile & Native Clients | #88–93 |
| Zero-Trust & Network Security | #94–100 |
| Business Logic & Abuse Prevention | #101–109 |
| Data Protection & Privacy | #110–116 |
| AI/LLM Security | #117–123 |
| Post-Quantum & Future-Proofing | #124–126 |
| Operational Security | #127–130 |

**Total: 130 Items**
