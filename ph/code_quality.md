# Code Quality & Security Checklist (253 Items)
> Clean code prevents security bugs. Security hardening protects clean code.
> 
> **Priority Legend:** 🔴 CRITICAL | 🟡 HIGH | 🟢 MEDIUM

---

## 🧩 Functions & Logic (1–10)

- [ ] **1.** 🔴 Functions do ONE thing — if you can't name it with a single verb-noun, split it
- [ ] **2.** 🟡 Max 20 lines per function — longer means too many responsibilities
- [ ] **3.** 🟡 Max 3 arguments — pass objects/configs if you need more
- [ ] **4.** 🟡 One level of abstraction per function — no mixing business logic with SQL/API calls
- [ ] **5.** 🔴 No side effects on inputs — return new values, never mutate arguments
- [ ] **6.** 🟡 Guard clauses over deep nesting — return early, flatten the pyramid
- [ ] **7.** 🟢 Avoid boolean arguments — `render(item, true)` tells nothing; use named options
- [ ] **8.** 🟡 Prefer composition over inheritance — small composable functions beat deep class trees
- [ ] **9.** 🟢 No output arguments — don't pass a variable just to mutate it; return the result
- [ ] **10.** 🟡 No god objects/functions — if it knows about everything, it shouldn't exist

---

## 📝 Naming & Readability (11–17)

- [ ] **11.** 🟢 Booleans read as questions — `isActive`, `hasPermission`, `canEdit`
- [ ] **12.** 🟢 No abbreviations — `user` not `usr`, `request` not `req`
- [ ] **13.** 🟢 Functions are verbs, data is nouns — `calculateTotal()` not `total()`
- [ ] **14.** 🟢 Collections are plural — `users`, `orderItems`, not `userList`
- [ ] **15.** 🟡 Named constants, never magic numbers — `MAX_RETRIES = 3` not `if retries > 3`
- [ ] **16.** 🟢 Self-documenting code > comments — rename if you need a comment to explain WHAT
- [ ] **17.** 🟢 Variable names must be searchable — `d`, `x`, `tmp` are ungoogleable; use `daysSinceLastLogin`

---

## 🔄 Data & State (18–23)

- [ ] **18.** 🔴 Immutability by default — spread/clone for updates, never mutate in place
- [ ] **19.** 🔴 Single source of truth — derive computed values, don't duplicate state
- [ ] **20.** 🟡 Explicit state transitions — no implicit status changes; state machines for complex flows
- [ ] **21.** 🔴 Initialize before use — no "maybe undefined" variables that crash later
- [ ] **22.** 🔴 Avoid global mutable state — pass what you need, inject dependencies
- [ ] **23.** 🔴 Transactions for multi-step mutations — partial writes = data corruption

---

## ⚠️ Error Handling (24–29)

- [ ] **24.** 🔴 Never swallow errors silently — empty `catch` blocks are crime scenes
- [ ] **25.** 🟡 Catch specific exceptions — broad `catch Exception` hides unrelated bugs
- [ ] **26.** 🔴 Preserve stack traces when re-throwing — don't murder the evidence
```
# BAD: catch (e) { throw e }           # stack trace nuked
# GOOD: catch (e) { throw }            # stack trace preserved
```

- [ ] **27.** 🟡 Error messages explain what AND what to do — not just "Invalid input"
- [ ] **28.** 🔴 Never expose internals to clients — no stack traces, query strings, file paths
- [ ] **29.** 🟡 Distinguish recoverable vs fatal — retry the first, alert on the second

---

## 🧪 Testing (30–40)

- [ ] **30.** 🟢 Test names describe the scenario — `returnsEmptyWhenNoOrders` not `testOrders`
- [ ] **31.** 🟡 One assertion concept per test — testing 5 things = 5 tests
- [ ] **32.** 🔴 Test edge cases explicitly — null, empty, max, negative, unicode, timezone
- [ ] **33.** 🔴 Mock external dependencies — tests shouldn't hit real APIs/databases
- [ ] **34.** 🟡 Dependency injection — pass collaborators, don't hardcode singletons
- [ ] **35.** 🟡 Fast test suite — slow tests don't run; aim for sub-second units
- [ ] **36.** 🟡 Test behavior, not implementation — users don't care about internal methods
- [ ] **37.** 🔴 No logic in tests — no `if/for` in tests. If the test has bugs, who tests the test?
- [ ] **38.** 🔴 No flaky tests tolerated — if it flakes once, fix/skip with a ticket (don't normalize it)
- [ ] **39.** 🔴 Avoid sleeps/timeouts in tests — use fakes, clocks, signals; sleeps create slow + flaky suites
- [ ] **40.** 🔴 Each test owns its data — no shared mutable fixtures that leak state across tests

---

## 🌐 API Design (41–47)

- [ ] **41.** 🟡 Version from day one — `/v1/resource` not `/resource`
- [ ] **42.** 🔴 Correct HTTP methods and status codes — 200/201/400/401/403/404/500 matter
- [ ] **43.** 🔴 Sensitive data never in GET params or URLs — use body or headers
- [ ] **44.** 🔴 Paginate all list endpoints — no unbounded queries, always limit
- [ ] **45.** 🔴 Rate limit every endpoint — sliding window, stricter on auth/expensive ops
- [ ] **46.** 🔴 Idempotency keys on mutations — retries must not cause double-charges
- [ ] **47.** 🟡 Consistent response structure — `{ success, data?, error?, meta? }` everywhere

---

## ⚡ Concurrency (48–55)

- [ ] **48.** 🔴 No TOCTOU bugs — check-and-act must be atomic
- [ ] **49.** 🔴 Locks for shared mutable state — concurrent writes without sync = corruption
- [ ] **50.** 🔴 Never fire-and-forget async — always handle or await; silent failures are bugs
- [ ] **51.** 🔴 Missing await is deadly — async calls without await produce the funniest bugs
```
# BAD: sendEmail(user)         # forgot await, error vanishes
# GOOD: await sendEmail(user)  # error propagates
```

- [ ] **52.** 🔴 Timeouts on all external calls — no request hangs forever
- [ ] **53.** 🔴 Unhandled promise rejections — orphaned promises that crash the process or vanish silently
- [ ] **54.** 🔴 Sequential awaits that should be parallel — `await a(); await b()` when independent is wasteful
```
# BAD: 2 seconds total
const users = await fetchUsers();     # 1s
const orders = await fetchOrders();   # 1s

# GOOD: 1 second total
const [users, orders] = await Promise.all([
    fetchUsers(),
    fetchOrders()
]);
```

- [ ] **55.** 🟡 `async void` functions — no way to catch errors from them; always return the promise

---

## 🏗️ Architecture (56–62)

- [ ] **56.** 🔴 Separate concerns — data layer ≠ business logic ≠ presentation
- [ ] **57.** 🔴 No circular dependencies — if A needs B and B needs A, refactor
- [ ] **58.** 🟡 Interface over implementation — depend on abstractions, not concrete classes
- [ ] **59.** 🔴 Config via environment — no hardcoded values that change between deployments
- [ ] **60.** 🟡 Feature flags for risky changes — deploy dark, enable gradually
- [ ] **61.** 🟡 Stateless services when possible — scale horizontally without sticky sessions
- [ ] **62.** 🟡 No service locator pattern — hidden dependencies retrieved at runtime; prefer explicit injection

---

## ⚡ Performance & Scalability (63–69)

- [ ] **63.** 🔴 N+1 query detection — never fetch users then loop to fetch their orders one-by-one
```
# BAD: users.forEach(u => fetchOrders(u.id))    # 1 + N queries
# GOOD: fetchUsersWithOrders()                  # 1 query with join
```

- [ ] **64.** 🔴 Index your foreign keys and query columns — unindexed joins on big tables destroy you
- [ ] **65.** 🟡 Cache invalidation strategy defined — not just "we cache it," but when does it expire/bust?
- [ ] **66.** 🔴 No synchronous heavy ops on request thread — offload image processing, emails, reports to queues
- [ ] **67.** 🔴 String concatenation in loops is evil — `result += str` creates a new object every iteration
```
# BAD: result = ""; items.forEach(i => result += i)
# GOOD: result = items.join("")
```

- [ ] **68.** 🟡 Regex compiled inside a loop — compiling the same pattern 10,000 times is embarrassingly bad
- [ ] **69.** 🔴 Unbounded in-memory collection building — loading 500k rows to filter 3 of them

---

## 🎭 Sneaky Bad Practices (70–78)

- [ ] **70.** 🟢 `else` after a `return` — it's just noise and signals the dev wasn't thinking
```
# BAD
if (valid) {
    return process()
} else {
    return error()
}

# GOOD
if (valid) return process()
return error()
```

- [ ] **71.** 🔴 Comparing floats with `==` — `0.1 + 0.2 == 0.3` is FALSE, always use epsilon
```
# BAD: if (a == b)
# GOOD: if (abs(a - b) < EPSILON)
```

- [ ] **72.** 🟡 Swallowing null by defaulting silently — `user.name ?? "Unknown"` sounds nice until "Unknown" ends up in production
- [ ] **73.** 🔴 Date math without timezone awareness — `new Date()` has ruined more careers than job interviews
- [ ] **74.** 🔴 Mutable default arguments — `def func(data=[])` is an infamous trap; the list persists across calls
```
# BAD: def add(item, items=[])  # same list object every call
# GOOD: def add(item, items=None):
           items = items or []
```

- [ ] **75.** 🟡 No "fix it later" comments — TODOs with no ticket are lies you tell yourself
- [ ] **76.** 🟡 Don't catch exceptions you can't handle — logging and re-raising is just noise
- [ ] **77.** 🟢 Avoid double negatives — `if (!notValid)` makes everyone's brain hurt
- [ ] **78.** 🟢 Negative named booleans — `isNotEnabled`, `disableSsl`; double negatives destroy brain cells. Name positively: `isEnabled`, `useSsl`

---

## 🛡️ Authentication (79–83)

- [ ] **79.** 🔴 Never roll your own auth — use OAuth2, OIDC, or battle-tested libraries
- [ ] **80.** 🔴 Tokens in `httpOnly; Secure; SameSite` cookies — never localStorage (XSS risk)
- [ ] **81.** 🔴 Bcrypt/Argon2 for passwords — never MD5/SHA1/SHA256 (too fast = crackable)
- [ ] **82.** 🔴 Destroy session on logout — invalidate ALL sessions on password reset
- [ ] **83.** 🔴 Rate-limit auth endpoints — exponential backoff + lockout after N failures

---

## 🔐 Authorization (84–87)

- [ ] **84.** 🔴 Verify resource ownership every request — `/me/orders` not `/user/123/orders`
- [ ] **85.** 🔴 Server-side RBAC checks — frontend hiding buttons ≠ security
- [ ] **86.** 🟡 UUIDs over sequential IDs — prevents enumeration attacks
- [ ] **87.** 🟡 Row-level security at DB layer — defense in depth, not just app layer

---

## 🧹 Input Validation (88–92)

- [ ] **88.** 🔴 Schema-validate ALL input — whitelist approach, reject unknown fields
- [ ] **89.** 🔴 Parameterized queries only — zero concatenated SQL, ever
- [ ] **90.** 🔴 Sanitize HTML output — never trust user content as markup
- [ ] **91.** 🔴 File uploads: validate size + MIME + extension + strip EXIF + validate content
- [ ] **92.** 🔴 URL allowlists for SSRF prevention — never fetch user-provided URLs blindly

---

## 🔒 Secrets & Crypto (93–96)

- [ ] **93.** 🔴 Zero hardcoded secrets — env vars only, verify at startup
- [ ] **94.** 🔴 `.env` in `.gitignore` + audit git history for leaks
- [ ] **95.** 🔴 CSPRNG for tokens/IDs — never `Math.random()` or `random.random()`
- [ ] **96.** 🔴 Modern algorithms only — AES-256-GCM, ChaCha20, Ed25519; never DES/RC4/ECB

---

## 🌐 Headers & Transport (97–99)

- [ ] **97.** 🔴 Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- [ ] **98.** 🔴 HTTPS everywhere — redirect HTTP, no mixed content
- [ ] **99.** 🔴 CORS explicit allowlist — never `Access-Control-Allow-Origin: *` on auth endpoints

---

## 📊 Observability (100–104)

- [ ] **100.** 🔴 Never log sensitive data — passwords, tokens, cards, PII stay out
- [ ] **101.** 🟡 Structured logging (JSON) — machine-parseable, not grep-dependent
- [ ] **102.** 🟡 Request correlation IDs — trace requests across services
- [ ] **103.** 🔴 Alerts on anomalies — spike in errors, unusual access patterns
- [ ] **104.** 🔴 Audit log for sensitive ops — who did what to which resource, when, immutable

---

## 📦 Supply Chain (105–108)

- [ ] **105.** 🔴 Pin + lock dependencies — reproducible builds, no `^` version ranges
- [ ] **106.** 🔴 Vulnerability scanning in CI — block deploys on critical CVEs
- [ ] **107.** 🟡 No self-approvals — at least one real review before merge
- [ ] **108.** 🔴 Rollback plan before deploy — know how to undo before you ship

---

## 🖥️ Frontend Security (109–110)

- [ ] **109.** 🟡 Subresource Integrity (SRI) on CDN assets — don't trust CDNs blindly
```
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-abc123..."
        crossorigin="anonymous"></script>
```

- [ ] **110.** 🔴 No sensitive data in browser history/URL state — tokens, passwords, PII in URL = leaked in logs, history, referrers

---

## 🧹 Dead Code & Cruft (111–117)

- [ ] **111.** 🟡 Unreachable code after returns/throws — compilers may not warn, humans definitely won't read it
```
# BAD
function process() {
    return result;
    logger.info("done");  # never executes, just confuses
}
```

- [ ] **112.** 🟡 Unused variables, imports, and parameters — every one is a lie about what the code needs
- [ ] **113.** 🟡 Commented-out code blocks — that's what git history is for; delete it or restore it
- [ ] **114.** 🟡 Unused feature flags / dead branches — if the flag has been `true` for 6 months, remove the `if`
- [ ] **115.** 🟡 Orphaned functions/methods — no callers anywhere = dead weight; search before assuming it's needed
- [ ] **116.** 🟢 Vestigial interfaces / abstract classes with one implementation and no plans for more — abstraction without purpose
- [ ] **117.** 🟡 Zombie dependencies in your manifest — packages imported but never used, still downloading and scanning

---

## 🔁 Duplication & Copy-Paste (118–122)

- [ ] **118.** 🟡 Near-identical functions differing by one line — extract the common part, parameterize the difference
- [ ] **119.** 🔴 Same validation logic in multiple places — one change, three places to forget
- [ ] **120.** 🟡 Repeated error-handling boilerplate — wrap in a middleware/decorator/higher-order function
- [ ] **121.** 🔴 Copy-pasted SQL/queries across files — one schema change, N bugs
- [ ] **122.** 🟡 Duplicated constants / config values — `TIMEOUT = 30` defined in 4 files, now they disagree

---

## 🧠 Complexity Smells (123–133)

- [ ] **123.** 🟡 Nested ternaries — one ternary is fine; nested ternaries are a war crime
```
# BAD
const label = a ? (b ? "X" : "Y") : (c ? "Z" : "W");

# GOOD
if (a && b) return "X";
if (a) return "Y";
if (c) return "Z";
return "W";
```

- [ ] **124.** 🟡 `switch` / `if-else` chains longer than 5 branches — use a lookup map/dictionary
```
# BAD
if (type === "A") return handleA();
else if (type === "B") return handleB();
// ... 12 more

# GOOD
const handlers = { A: handleA, B: handleB, ... };
return handlers[type]();
```

- [ ] **125.** 🟡 Deeply nested callbacks — flatten with async/await or extract named functions
- [ ] **126.** 🟡 Overly clever one-liners — if it needs a comment to explain, it's not clever, it's hostile
- [ ] **127.** 🔴 Multiple return types from one function — returns `string | null | number | false` is a type nightmare
```
# BAD: returns User | null | false | undefined depending on mood
# GOOD: returns User | null — that's it
```

- [ ] **128.** 🔴 Functions that return *and* throw *and* mutate — pick ONE communication channel
- [ ] **129.** 🔴 Long parameter lists with same-type args — `createUser("John", "Smith", "John", "Active")` which "John" is what?
```
# BAD: createUser("John", "Smith", "john@x.com", "admin", true, true)
# GOOD: createUser({ firstName: "John", lastName: "Smith", ... })
```

- [ ] **130.** 🔴 Overuse of `any` / `Object` / `dynamic` — you opted into a type system then turned it off
- [ ] **131.** 🟡 Negated conditionals as the primary branch — put the positive/common path first
```
# BAD
if (!user.isDisabled) { ... long block ... }
else { return; }

# GOOD
if (user.isDisabled) return;
// ... long block ...
```

- [ ] **132.** 🟡 Cyclomatic complexity cap — if a function has too many branches, extract helpers (e.g., complexity <= 10)
- [ ] **133.** 🟡 File/class size > 300 lines — it's doing too much. Split by feature, not by type

---

## 🔢 Primitive Obsession (134–140)

- [ ] **134.** 🔴 Strings doing the job of enums — `status = "actve"` (typo) compiles fine, an enum wouldn't
- [ ] **135.** 🟡 Parallel arrays instead of object arrays — `names[i]` + `ages[i]` + `emails[i]` is fragile; use `users[i].name`
- [ ] **136.** 🟡 Stringly-typed everything — passing `"USD"`, `"EUR"` as raw strings instead of a `Currency` type
- [ ] **137.** 🟡 Raw tuples for structured data — `[200, "OK", user]` — what's index 2 again? Use an object
- [ ] **138.** 🟡 Booleans that should be enums — `isActive, isVerified, isPending` → just use a `Status` enum
- [ ] **139.** 🟡 Encoding meaning in string formats — `"user:admin:readonly"` parsed with `.split(":")` — make a real data structure
- [ ] **140.** 🟢 Units in names — `timeout` → `timeoutMs`, `retry` → `retryCount`, `size` → `sizeBytes`

---

## 🏋️ Class & Module Smells (141–150)

- [ ] **141.** 🟢 Data classes with no behavior — if it's just getters/setters, it's a struct pretending to be a class
- [ ] **142.** 🟡 Feature envy — method uses 10 fields from another class and 0 from its own; it belongs over there
- [ ] **143.** 🔴 Shotgun surgery — one change requires touching 15 files; your abstractions are wrong
- [ ] **144.** 🟡 Divergent change — one class changes for 5 unrelated reasons; it's doing 5 jobs
- [ ] **145.** 🟢 Middle-man classes that just delegate — `this.service.doThing()` adds zero value; call service directly
- [ ] **146.** 🟢 Lazy classes that do almost nothing — justify every class's existence; merge or delete
- [ ] **147.** 🟡 Inappropriate intimacy — classes accessing each other's private/internal details; respect boundaries
- [ ] **148.** 🟡 Excessive method chaining where intermediate state is unclear — `obj.load().parse().validate().transform().save()` — where did the error happen?
- [ ] **149.** 🟡 Static method abuse — untestable, unhookable, essentially global functions wearing a class costume
- [ ] **150.** 🟡 Constructor doing real work — constructors that call APIs, read files, or do heavy computation; use factory methods

---

## 📐 Literals, Defaults & Config (151–155)

- [ ] **151.** 🟡 Hardcoded timeouts/limits buried in logic — `setTimeout(fn, 86400000)` — what is that number?
```
# BAD: setTimeout(fn, 86400000)
# GOOD:
const ONE_DAY_MS = 24 * 60 * 60 * 1000;
setTimeout(fn, ONE_DAY_MS);
```

- [ ] **152.** 🟡 Format strings / templates duplicated — date formats, URL patterns, error templates defined inline everywhere
- [ ] **153.** 🟡 Implicit defaults that differ across call sites — one place defaults `pageSize` to 10, another to 50
- [ ] **154.** 🟡 Environment-specific logic via `if (env === "prod")` scattered everywhere — use config objects
- [ ] **155.** 🟡 Logging format/level inconsistency — `console.log`, `logger.warn`, `print()` mixed in the same codebase

---

## 🛡️ Defensive Coding Gaps (156–164)

- [ ] **156.** 🔴 No null/undefined check before property access — `user.address.city` when address can be null
```
# BAD: user.address.city          # TypeError if address is null
# GOOD: user.address?.city ?? ""  # safe navigation
```

- [ ] **157.** 🔴 Assumes array is non-empty — `items[0].id` without checking length first
- [ ] **158.** 🔴 parseInt / type coercion without radix or validation — `parseInt("08")` has bitten people for decades
```
# BAD: parseInt(input)
# GOOD: parseInt(input, 10)   # or Number(input) with validation
```

- [ ] **159.** 🔴 Division without zero check — `total / count` when count could be 0
- [ ] **160.** 🔴 `.map()` / `.filter()` on possibly-null collections — `data.items.map(...)` when `items` may not exist
- [ ] **161.** 🔴 Enum/union not exhaustively handled — new status added, 4 switch statements silently skip it
```
# In TypeScript:
function handle(s: Status): string {
    switch (s) {
        case "active": return "...";
        case "inactive": return "...";
        default: const _exhaustive: never = s;  # compile error if case missed
    }
}
```

- [ ] **162.** 🔴 Regex without anchoring — `/admin/` matches `"not-admin-really"`, use `/^admin$/`
- [ ] **163.** 🔴 Object spread overwrites in wrong order — `{ ...defaults, ...input }` vs `{ ...input, ...defaults }` is a silent bug
- [ ] **164.** 🔴 Accidental reference mutation — `const items = state.items; items.push(x)` mutates state! Spread it: `[...items, x]`

---

## 📜 Comment & Documentation Smells (165–169)

- [ ] **165.** 🟢 Comments that restate the code — `i++ // increment i` wastes everyone's time
- [ ] **166.** 🔴 Outdated comments that contradict the code — worse than no comment; they actively mislead
- [ ] **167.** 🟢 Commented-out alternate implementations — "we might need this" — no you won't; delete it
- [ ] **168.** 🟢 Journal comments at top of file — changelogs belong in git, not in source files
- [ ] **169.** 🟢 Javadoc / docstrings on every trivial method — `/** Gets the name. */ getName()` is noise; document WHY, not WHAT

---

## 🔧 Resource & Cleanup (170–174)

- [ ] **170.** 🔴 Opened resources without guaranteed close — DB connections, file handles, streams need `finally` / `using` / `with`
```
# BAD
const conn = await db.connect();
const result = await conn.query(sql);  # if this throws, conn leaks
conn.release();

# GOOD
const conn = await db.connect();
try {
    return await conn.query(sql);
} finally {
    conn.release();
}
```

- [ ] **171.** 🔴 Event listeners never removed — memory leak that grows quietly until OOM
- [ ] **172.** 🔴 Timers/intervals never cleared — `setInterval` without corresponding `clearInterval` on teardown
- [ ] **173.** 🟡 Temp files / artifacts never cleaned up — disk fills up slowly, then suddenly
- [ ] **174.** 🟡 Connection pools never configured — defaults are almost never right for your load

---

## 🔀 Control Flow Smells (175–182)

- [ ] **175.** 🟡 Using exceptions for control flow — `try { parse(x) } catch { handleNotParseable() }` — check first, don't throw for expected cases
- [ ] **176.** 🟢 `for` loop that always runs exactly once — it's not a loop, it's a confusing `if`
- [ ] **177.** 🟢 Loop with `break` on first iteration — you wanted `.find()`, not `.forEach()`
- [ ] **178.** 🟢 Re-checking a condition inside a loop that was the loop's condition — redundant and confusing
- [ ] **179.** 🟡 Flag variables controlling flow — `let found = false; for (...) { if (...) found = true; }` — use early return or `.some()`
- [ ] **180.** 🟡 Multiple loops over the same collection for related tasks — combine into one pass
- [ ] **181.** 🔴 Recursion without base-case guarantees — stack overflow is not a theoretical concern
- [ ] **182.** 🟡 Temporal coupling — don't require callers to remember "call A before B" without enforcing it

---

## 🪵 Logging & Debug Leftovers (183–189)

- [ ] **183.** 🔴 `console.log` / `print` / `System.out` left in production code — use proper logger with levels
- [ ] **184.** 🔴 Debug-only code behind no flag — `if (true) { dumpState() }` committed accidentally
- [ ] **185.** 🔴 Logging inside tight loops — 1M log lines per second is not observability, it's a DDoS on your log infra
- [ ] **186.** 🔴 Log messages with no context — `logger.error("Failed")` — failed WHAT? For WHICH user/request?
- [ ] **187.** 🟡 Inconsistent log levels — `logger.error("User logged in")` — that's info, not an error
- [ ] **188.** 🔴 Log injection — user input in logs (`log('User ' + name)`) lets attackers forge log entries via `\n`
- [ ] **189.** 🟡 Don't log-and-throw blindly — either add context or let it bubble; double-logging destroys signal

---

## 👃 Code Smell Classics (190–197)

- [ ] **190.** 🟡 Law of Demeter violations (train wrecks) — `user.getProfile().getAddress().getZipCode()` violates encapsulation
- [ ] **191.** 🟡 Data clumps — same 3-4 arguments passed together in multiple functions → make them an object
- [ ] **192.** 🔴 Variable shadowing — reusing a variable name in a nested scope confuses humans and compilers
```
# BAD
let user = getUser();
if (active) {
  let user = getAdmin();  # WTF is 'user' now?
}
```

- [ ] **193.** 🟢 Scope minimization — declare variables as close to their usage as possible, not at the top
- [ ] **194.** 🟡 YAGNI violations — delete "just in case" code. If it's not called, it's a bug waiting to happen
- [ ] **195.** 🟡 Re-assigning function arguments — treat inputs as `const`. Create a new variable if you need to change it
- [ ] **196.** 🟢 Boolean blindness — `setFlag(true)` is meaningless. `enableFeature()` or `disableValidation()` is self-documenting
- [ ] **197.** 🟡 Comments are deodorant — if the code stinks, rewrite it. Don't explain the smell away

---

## 📦 Contract & Boundary Smells (198–203)

- [ ] **198.** 🔴 Validate at boundaries once — don't re-validate the same input 5 layers deep
- [ ] **199.** 🔴 No hidden I/O in "utility" functions — helpers shouldn't secretly read env, disk, network, globals
- [ ] **200.** 🟡 No time-dependent logic without injection — wrap `now()`/clock so code is testable and deterministic
- [ ] **201.** 🟡 Don't mix sync and async styles — e.g., callbacks + promises together; pick one per module
- [ ] **202.** 🟡 DTOs vs Entities — never return DB entities directly. Map to a DTO to hide internal schema changes
- [ ] **203.** 🟡 Custom error types over generic Error — `throw new NotFoundError()` > `throw new Error("404")`

---

## 🔐 Additional Security Smells (204–208)

- [ ] **204.** 🔴 Timing attacks — `if (inputToken === storedToken)` leaks length. Use constant-time compare libs
- [ ] **205.** 🟡 Avoid convenience imports that pull the world — importing a huge module for one helper is a smell
- [ ] **206.** 🟡 No cyclic re-exports/barrel abuse — barrel files that create sneaky cycles are maintainability debt
- [ ] **207.** 🔴 Constant-time comparison for secrets — use `crypto.timingSafeEqual()` or equivalent, never `===`
- [ ] **208.** 🟡 Error context must be structured — include key fields (ids, operation, state) not prose-only strings

---

## 📝 Encoding & Serialization (209–212)

- [ ] **209.** 🔴 Implicit encoding assumptions — always specify UTF-8 explicitly for file/network I/O
```
# BAD: data = file.read()              # what encoding?
# GOOD: data = file.read(encoding="utf-8")
```

- [ ] **210.** 🔴 JSON serialization of dates/decimals — `JSON.stringify(new Date())` gives different results across runtimes
- [ ] **211.** 🟡 Binary vs text mode confusion — reading a binary file as text silently corrupts data
- [ ] **212.** 🟡 Locale-dependent formatting in logic — `toString()` on numbers gives `"1,000"` in Germany, breaking parsers

---

## 🗂️ Collection & Iteration Traps (213–217)

- [ ] **213.** 🔴 Mutating a collection while iterating — `ConcurrentModificationException` in every language
```
# BAD
for item in items:
    if item.expired:
        items.remove(item)    # skips elements or crashes

# GOOD
items = [i for i in items if not i.expired]
```

- [ ] **214.** 🔴 Off-by-one errors in manual indexing — use iterators/range-based loops; manual `i < len` is a trap
- [ ] **215.** 🟡 HashMap/dict key mutation — mutating an object used as a key makes it unfindable
- [ ] **216.** 🟡 Sorting with inconsistent comparators — `compare(a,b)` must be transitive or sort is undefined behavior
- [ ] **217.** 🟡 Relying on iteration order of unordered collections — dict/set order is implementation-defined in many languages

---

## ⚖️ Equality & Comparison Gotchas (218–221)

- [ ] **218.** 🔴 Identity vs equality confusion — `==` vs `===` vs `.equals()` — know which your language uses by default
- [ ] **219.** 🔴 Broken custom equality — if you override `equals`, override `hashCode`; collections break otherwise
- [ ] **220.** 🟡 Null comparison traps — `null == undefined` is `true` in JS; `None == 0` behavior varies by language
- [ ] **221.** 🟡 String comparison for non-ASCII — `"café" == "café"` can be `false` due to Unicode normalization (NFC vs NFD)

---

## 🧠 Memory & Lifecycle Smells (222–225)

- [ ] **222.** 🔴 Closure capturing more than intended — lambdas holding references to entire scopes, preventing GC
```
# BAD
function setup() {
    const hugeData = loadGigabytes();
    return () => console.log(hugeData.length);
    # entire hugeData kept alive just for .length
}

# GOOD
function setup() {
    const len = loadGigabytes().length;
    return () => console.log(len);
}
```

- [ ] **223.** 🟡 Unbounded caches without eviction — `cache[key] = value` growing forever is a slow memory leak
- [ ] **224.** 🟡 Retaining references in error objects — stack traces capturing large local variables in some runtimes
- [ ] **225.** 🟡 Circular references preventing cleanup — two objects referencing each other in non-GC or weak-ref contexts

---

## 🔢 Type Coercion & Conversion (226–229)

- [ ] **226.** 🔴 Silent type coercion in comparisons — `"5" > "10"` is `true` (string comparison); convert first
- [ ] **227.** 🔴 Lossy numeric conversions — `int(3.9)` gives `3`, not `4`; be explicit about truncation vs rounding
- [ ] **228.** 🟡 Integer overflow/underflow — unbounded arithmetic wrapping silently in fixed-width integer languages
- [ ] **229.** 🟡 Truthy/falsy misuse — `if (count)` fails when `count = 0` is a valid value, not an absence

---

## 🧠 Cognitive Load Smells (230–235)

- [ ] **230.** 🟡 Explaining variables over complex booleans — Don't make readers parse logic in their head
```
# BAD
if (auth.user && auth.user.role === 'admin' && (order.status === 'paid' || order.status === 'shipped')) { ... }

# GOOD
const isAdmin = auth.user?.role === 'admin';
const isOrderActive = ['paid', 'shipped'].includes(order.status);
if (isAdmin && isOrderActive) { ... }
```

- [ ] **231.** 🟡 Tramp data (drilling) — passing a variable through 4 layers just because the 5th layer needs it
- [ ] **232.** 🔴 Getters with side effects — `user.isActive` should return a boolean, not trigger a DB call or mutate state
- [ ] **233.** 🟢 Yoda conditions — `if (5 === count)` was for C compilers. Modern linters save you. Just write `if (count === 5)`
- [ ] **234.** 🔴 Assignments inside conditions — `if (user = getUser())` looks like a typo and is hard to read
- [ ] **235.** 🟡 Speculative generality — "I'll add this extra parameter just in case" — delete it; it confuses code now for a future that may never happen

---

## 🔧 Build & Environment Hygiene (236–239)

- [ ] **236.** 🔴 No `.editorconfig` or formatter config committed — tabs vs spaces wars solved by automation, not arguments
- [ ] **237.** 🔴 Linter warnings ignored or disabled project-wide — `// eslint-disable` at the top of every file is a surrender flag
- [ ] **238.** 🟡 No pre-commit hooks for formatting/linting — reviews shouldn't waste time on style
- [ ] **239.** 🟡 Build artifacts committed to repo — `node_modules/`, `__pycache__/`, `.class` files don't belong in git

---

## 🧪 Additional Test Smells (240–243)

- [ ] **240.** 🟡 Hardcoded test fixtures — `const user = { id: 1, name: "Test" }` in 50 tests. Use a factory function
- [ ] **241.** 🟢 Assertions without messages — `assert(a === b)` fails. *Why*? `assert(a === b, "User age should match DB")`
- [ ] **242.** 🔴 Testing private methods — if it's private, it's an implementation detail. Test via public method
- [ ] **243.** 🟡 Over-mocking — mocking 5 layers deep means your code is too coupled. Refactor to test the integration

---

## 🔢 Advanced Primitive Smells (244–247)

- [ ] **244.** 🔴 Bitwise flags for booleans — `if (permissions & 4)` is unreadable. Use `hasPermission('WRITE')`
- [ ] **245.** 🟡 Stringly typed IDs — passing `"user_123"` everywhere. Wrap it: `new UserId("123")`
- [ ] **246.** 🟡 Switch statements on type — if you switch on `class.type`, use polymorphism. The class should have a `handle()` method
- [ ] **247.** 🟢 Loop-switch sequence — a loop containing a large switch often means you're iterating over a mixed collection that should be normalized first

---

## ⚡ Additional Async Smells (248–250)

- [ ] **248.** 🔴 `Promise.all` fail-fast ignorance — if one promise rejects, others are silently cancelled. Is that what you want?
- [ ] **249.** 🟡 `.then()` pyramid of doom — if you have 3+ `.then()`, use `async/await`
```
# BAD
getUser().then(u => getOrders(u).then(o => getItems(o)))

# GOOD
const u = await getUser();
const o = await getOrders(u);
const i = await getItems(o);
```

- [ ] **250.** 🟢 Mixed async styles in same file — don't mix callbacks, `.then()`, and `async/await`. Pick one per module

---

## 🏗️ OOP Structural Smells (251–253)

- [ ] **251.** 🟡 Anemic domain model — classes with only getters/setters and no logic are just expensive Maps. Move behavior into the class
- [ ] **252.** 🟡 Inheritance for code reuse — "I need a `User` class, I'll inherit from `DatabaseRecord`." **No.** Use composition. Inheritance is for polymorphism
- [ ] **253.** 🟢 Public fields everywhere — if every field is public, you have a struct, not a class. Hide the data

---

## 🔴 Critical Items Summary (Must-Fix Before Ship)

These cause production bugs, security vulnerabilities, or data corruption:

**Core Security (All 🔴):**
- #79-96 — Authentication, authorization, input validation, secrets, crypto

**Data Integrity:**
- #5, #18, #21, #23 — Side effects, immutability, global state, transactions
- #222 — Closure memory leaks

**Crash-Prone:**
- #24, #26 — Swallowing errors, stack trace murder
- #48-55 — Concurrency bugs (TOCTOU, missing await, unhandled promises)
- #156-164 — Defensive coding gaps (null access, zero division)
- #170-172 — Resource leaks
- #181 — Infinite recursion

**Performance Killers:**
- #63, #66-67, #69 — N+1 queries, sync heavy ops, unbounded collections

**Sneaky Bugs:**
- #71 — Float comparison
- #73 — Timezone bugs
- #74 — Mutable default args
- #127-128 — Multiple return types, mixed communication channels
- #192 — Variable shadowing

**Serialization/Encoding:**
- #209-210 — Implicit encoding, JSON date serialization

**Collections:**
- #213-214 — Mutate-while-iterate, off-by-one

**Memory:**
- #222 — Closure capturing too much
- #226-228 — Silent type coercion, lossy conversions

---

## 🟡 High Priority Items (Fix Soon)

Maintainability debt that slows development:
- Complexity smells (#123-133)
- Duplication (#118-122)
- Primitive obsession (#134-140)
- Shotgun surgery patterns (#143)
- Defensive coding gaps (#156-164)
- Encoding & serialization (#209-212)
- Collection traps (#213-217)
- Equality gotchas (#218-221)

---

## 🟢 Medium Priority (Nice to Have)

Code pleasantness improvements that rarely cause bugs:
- Naming conventions (#11-17)
- Comment style (#165-169)
- Boolean blindness (#196)
- Lazy classes (#146)
- Scope minimization (#193)
- Yoda conditions (#233)
