# Code Security Checklist (48 Items)

> Security is not a feature. It's a requirement.
> 
> **Priority Legend:** 🔴 CRITICAL | 🟡 HIGH | 🟢 MEDIUM

---

## 🛡️ Authentication (1–5)

- [ ] **1.** 🔴 Never roll your own auth — use OAuth2, OIDC, or battle-tested libraries
- [ ] **2.** 🔴 Tokens in `httpOnly; Secure; SameSite` cookies — never localStorage (XSS risk)
- [ ] **3.** 🔴 Bcrypt/Argon2 for passwords — never MD5/SHA1/SHA256 (too fast = crackable)
- [ ] **4.** 🔴 Destroy session on logout — invalidate ALL sessions on password reset
- [ ] **5.** 🔴 Rate-limit auth endpoints — exponential backoff + lockout after N failures

---

## 🔐 Authorization (6–9)

- [ ] **6.** 🔴 Verify resource ownership every request — `/me/orders` not `/user/123/orders`
- [ ] **7.** 🔴 Server-side RBAC checks — frontend hiding buttons ≠ security
- [ ] **8.** 🟡 UUIDs over sequential IDs — prevents enumeration attacks
- [ ] **9.** 🟡 Row-level security at DB layer — defense in depth, not just app layer

---

## 🧹 Input Validation (10–14)

- [ ] **10.** 🔴 Schema-validate ALL input — whitelist approach, reject unknown fields
- [ ] **11.** 🔴 Parameterized queries only — zero concatenated SQL, ever
- [ ] **12.** 🔴 Sanitize HTML output — never trust user content as markup
- [ ] **13.** 🔴 File uploads: validate size + MIME + extension + strip EXIF + validate content
- [ ] **14.** 🔴 URL allowlists for SSRF prevention — never fetch user-provided URLs blindly

---

## 🔒 Secrets & Crypto (15–18)

- [ ] **15.** 🔴 Zero hardcoded secrets — env vars only, verify at startup
- [ ] **16.** 🔴 `.env` in `.gitignore` + audit git history for leaks
- [ ] **17.** 🔴 CSPRNG for tokens/IDs — never `Math.random()` or `random.random()`
- [ ] **18.** 🔴 Modern algorithms only — AES-256-GCM, ChaCha20, Ed25519; never DES/RC4/ECB

---

## 🌐 Headers & Transport (19–21)

- [ ] **19.** 🔴 Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- [ ] **20.** 🔴 HTTPS everywhere — redirect HTTP, no mixed content
- [ ] **21.** 🔴 CORS explicit allowlist — never `Access-Control-Allow-Origin: *` on auth endpoints

---

## 📊 Observability Security (22–26)

- [ ] **22.** 🔴 Never log sensitive data — passwords, tokens, cards, PII stay out
- [ ] **23.** 🟡 Structured logging (JSON) — machine-parseable, not grep-dependent
- [ ] **24.** 🟡 Request correlation IDs — trace requests across services
- [ ] **25.** 🔴 Alerts on anomalies — spike in errors, unusual access patterns
- [ ] **26.** 🔴 Audit log for sensitive ops — who did what to which resource, when, immutable

---

## 📦 Supply Chain (27–30)

- [ ] **27.** 🔴 Pin + lock dependencies — reproducible builds, no `^` version ranges
- [ ] **28.** 🔴 Vulnerability scanning in CI — block deploys on critical CVEs
- [ ] **29.** 🟡 No self-approvals — at least one real review before merge
- [ ] **30.** 🔴 Rollback plan before deploy — know how to undo before you ship

---

## 🖥️ Frontend Security (31–32)

- [ ] **31.** 🟡 Subresource Integrity (SRI) on CDN assets — don't trust CDNs blindly
```html
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-abc123..."
        crossorigin="anonymous"></script>
```

- [ ] **32.** 🔴 No sensitive data in browser history/URL state — tokens, passwords, PII in URL = leaked in logs, history, referrers

---

## 🔐 Additional Security Smells (33–38)

- [ ] **33.** 🔴 Timing attacks — `if (inputToken === storedToken)` leaks length. Use constant-time compare libs
- [ ] **34.** 🔴 Constant-time comparison for secrets — use `crypto.timingSafeEqual()` or equivalent, never `===`
- [ ] **35.** 🟡 Avoid convenience imports that pull the world — importing a huge module for one helper is a smell
- [ ] **36.** 🟡 No cyclic re-exports/barrel abuse — barrel files that create sneaky cycles are maintainability debt
- [ ] **37.** 🟡 Error context must be structured — include key fields (ids, operation, state) not prose-only strings
- [ ] **38.** 🟡 Log injection prevention — user input in logs (`log('User ' + name)`) lets attackers forge log entries via `\n`

---

## 🔴 Critical Items Summary (Must-Fix Before Ship)

These cause production security vulnerabilities or data breaches:

**Authentication & Session:**
- #1–5 — Never roll own auth, proper token storage, password hashing, session management, rate limiting

**Authorization:**
- #6–7 — Resource ownership, server-side RBAC

**Injection Prevention:**
- #10–14 — Input validation, SQL injection, XSS, file upload security, SSRF

**Secrets Management:**
- #15–18 — No hardcoded secrets, CSPRNG, modern crypto

**Transport Security:**
- #19–21 — Security headers, HTTPS, CORS

**Logging & Audit:**
- #22, #26 — Never log secrets, audit trail for sensitive ops

**Supply Chain:**
- #27–28, #30 — Dependency security, rollback planning

---

## 🟡 High Priority Items (Fix Soon)

Defense-in-depth and operational security:
- #8–9 — UUIDs, row-level security
- #23–25 — Structured logging, correlation, anomaly alerts
- #29 — Code review requirement
- #31 — SRI for CDN assets
- #34, #38 — Timing attacks, log injection

---

## 🟢 Medium Priority (Nice to Have)

Security hygiene improvements:
- #35–37 — Import hygiene, error structure

---

## Quick Reference: Security by Category

| Category | Items |
|----------|-------|
| Authentication | #1–5 |
| Authorization | #6–9 |
| Input Validation | #10–14 |
| Secrets & Crypto | #15–18 |
| Headers & Transport | #19–21 |
| Observability | #22–26 |
| Supply Chain | #27–30 |
| Frontend Security | #31–32 |
| Additional Smells | #33–38 |
