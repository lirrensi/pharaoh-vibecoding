# Code Quality Checklist (249 Items)
> Logical errors, structural issues, maintainability traps, and sneaky bugs.
>
> **Note:** Security-specific items in `code_security.md`
> **Note:** Performance-specific items in `code_perf.md`
>
> **Priority Legend:** 🔴 CRITICAL | 🟡 HIGH | 🟢 MEDIUM | 🔪 SIMPLIFY

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

- [ ] **123.** 🟡 Nested ternaries — one ternary is fine; nested ternaries are a war crime. Prefer switch statements or if/else chains for multiple conditions.
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
- [ ] **126.** 🟡 Overly clever one-liners — if it needs a comment to explain, it's not clever, it's hostile. Prioritize readability over brevity. `arr.filter(x => x.active).map(x => x.id)[0]` is fine. `arr.reduce((a, b) => a || b.id, null)` is showing off.
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
- [ ] **194.** 🔪 YAGNI violations — delete "just in case" code. If it's not called now, it's a bug waiting to happen. **The Rule:** "If I delete this, will anything break?" Yes → keep it. No → DELETE IMMEDIATELY. "Maybe in the future?" → DELETE. Git remembers.
- [ ] **195.** 🟡 Re-assigning function arguments — treat inputs as `const`. Create a new variable if you need to change it
- [ ] **196.** 🟢 Boolean blindness — `setFlag(true)` is meaningless. `enableFeature()` or `disableValidation()` is self-documenting
- [ ] **197.** 🟡 Comments are deodorant — if the code stinks, rewrite it. Don't explain the smell away. **If you write a comment, you failed to make the code clear.** Rename the variable. Extract the function. Kill the comment.

---

## 📦 Contract & Boundary Smells (198–203)

- [ ] **198.** 🔴 Validate at boundaries once — don't re-validate the same input 5 layers deep
- [ ] **199.** 🔴 No hidden I/O in "utility" functions — helpers shouldn't secretly read env, disk, network, globals
- [ ] **200.** 🟡 No time-dependent logic without injection — wrap `now()`/clock so code is testable and deterministic
- [ ] **201.** 🟡 Don't mix sync and async styles — e.g., callbacks + promises together; pick one per module
- [ ] **202.** 🟡 DTOs vs Entities — never return DB entities directly. Map to a DTO to hide internal schema changes
- [ ] **203.** 🟡 Custom error types over generic Error — `throw new NotFoundError()` > `throw new Error("404")`

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

## 🔪 Over-Engineering & Bloat (254–268)

*Focus: Ruthless deletion. If it's not pulling its weight, kill it.*

- [ ] **254.** 🔪 **Unnecessary abstraction layers** — Controller → Service → Manager → Repository → DAO where each just delegates to the next. If a layer adds no decisions, collapse it.
```
# BAD: 5 files to save a user
UserController → UserService → UserManager → UserRepository → UserDAO

# GOOD: 2-3 files
UserController → UserService → UserRepository
```

- [ ] **255.** 🔪 **Premature abstraction (Rule of Three)** — Interfaces/base classes created with only ONE implementation. Wait until you have 2+ real cases that need them. Abstractions must earn their complexity.
- [ ] **256.** 🔪 **Forced DRY — coupling unrelated code** — Two functions that share 80% code but serve different domains. Merging them creates a fragile frankenstein that breaks when either domain changes independently. Duplication is cheaper than wrong abstraction.
```
# BAD: Forced together because they "look the same"
function processEntity(entity, type) {
    if (type === "user") { /* 20 user-specific lines */ }
    if (type === "order") { /* 20 order-specific lines */ }
    // 10 shared lines
}

# GOOD: Duplication is cheaper than coupling
function processUser(user) { ... }
function processOrder(order) { ... }
```

- [ ] **257.** 🔪 **Over-fragmented code (Ravioli)** — 50-line feature spread across 12 files with 3-line functions. Locality of behavior matters. If understanding a flow requires opening 8 tabs, you over-split.
- [ ] **258.** 🟢 **Nano-functions that obscure flow** — Extracting every 2 lines into a named function when inline is clearer. The reader now has to jump around to follow logic.
```
# BAD: Extraction that hurts readability
function processOrder(order) {
    validateExists(order);
    checkStatus(order);
    applyDiscount(order);
    updateTotal(order);
    saveOrder(order);
}
// ...where each function is 1-2 lines and only called here

# GOOD: Inline when it's clearer
function processOrder(order) {
    if (!order) throw new NotFoundError();
    if (order.status !== 'pending') throw new InvalidStateError();
    order.total = order.subtotal * (1 - order.discountRate);
    await db.orders.save(order);
}
```

- [ ] **259.** 🟢 **Comment-delimited sections in functions** — Block comments like `// --- Validate ---` separating "phases" are extract-method signals. The comment should become the function name.
```
# BAD
function processOrder(order) {
    // --- Validate order ---
    if (!order.items.length) throw ...
    // --- Calculate totals ---
    let subtotal = 0;
    // --- Apply discounts ---
    if (order.coupon) { ... }
    // --- Save to database ---
    await db.save(order);
}

# GOOD: The comments became function names
function processOrder(order) {
    validateOrder(order);
    const total = calculateTotal(order.items, order.coupon);
    await saveOrder({ ...order, total });
}
```

- [ ] **260.** 🔪 **Over-configurable code** — 12 options/params where only 2 are ever used. Every option doubles the testing surface. Hard-code until you genuinely need flexibility.
```
# BAD: 12 options, 3 ever used
createServer({
    port: 3000,
    host: 'localhost',
    protocol: 'http',
    encoding: 'utf-8',
    maxHeaderSize: 8192,
    keepAliveTimeout: 5000,
    // ... 6 more that are always defaults
})

# GOOD: Sensible defaults, expose only what varies
createServer({ port: 3000 })
```

- [ ] **261.** 🟢 **Unnecessary async wrappers** — Synchronous logic wrapped in `async`/`Promise` for no reason. Adds stack trace noise and cognitive overhead.
```
# BAD
async function getFullName(user) {
    return `${user.first} ${user.last}`;  // nothing async here
}

# GOOD
function getFullName(user) {
    return `${user.first} ${user.last}`;
}
```

- [ ] **262.** 🔪 **Polymorphism for ≤2 cases** — Interface + 2 implementations + factory + registry... for "free" vs "premium." An if/else is 3 lines. Patterns are solutions to recurring problems. No problem = no pattern needed.
- [ ] **263.** 🟢 **Storing easily derived values** — Caching computed state (`itemCount`, `totalPrice`, `isEmpty`) that then requires manual synchronization instead of computing on access via getters.
```
# BAD
class Cart {
    items = [];
    itemCount = 0;      // redundant — items.length
    totalPrice = 0;     // redundant — sum of items
    isEmpty = true;     // redundant — items.length === 0
}

# GOOD
class Cart {
    items = [];
    get itemCount() { return this.items.length; }
    get totalPrice() { return this.items.reduce((s, i) => s + i.price, 0); }
    get isEmpty() { return this.items.length === 0; }
}
```

- [ ] **264.** 🔪 **Helper/Utility class sprawl** — `StringUtils`, `DateHelper`, `MathEx` with static methods. If it's a pure function, put it in the module that uses it. Don't create grab-bag classes.
- [ ] **265.** 🔪 **Unnecessary design patterns** — Observer with 1 subscriber, Strategy with 1 strategy, Factory that returns the same class. The pattern IS the complexity if you don't have the problem.
- [ ] **266.** 🔪 **Config hell** — `if (config.features.isNewThingEnabled)` scattered through business logic. Pass a context object or use strategy pattern. Don't hunt for flags in the logic.
- [ ] **267.** 🔪 **Ceremony layers** — Request → Controller → Service → Manager → Provider → Helper where each just passes data along. Each layer should justify itself with a decision or transformation.
- [ ] **268.** 🔪 **Over-generalized solutions** — A function handling 15 cases via config/switches when you only ever use 2. The config complexity exceeds the problem complexity.

---

## 🔧 Refactoring & Simplification Safety (269–278)

*Focus: How to safely simplify without breaking behavior.*

- [ ] **269.** 🔴 **Separate refactor commits from behavior changes** — If a PR both "cleans up" AND "changes logic", reviewing is guesswork. One or the other.
- [ ] **270.** 🔴 **Characterization tests before refactor** — Lock current behavior (especially legacy/buggy behavior) before cleanup. No tests = no refactor safety net. If you don't have a test, you aren't refactoring; you're just changing code and hoping.
- [ ] **271.** 🟡 **Refactor in reversible steps** — Small mechanical transformations. Keep diffs reviewable. Big-bang rewrites are risky.
- [ ] **272.** 🟡 **Don't refactor without observability** — If it runs in prod, ensure logs/metrics/traces exist to validate no regressions.
- [ ] **273.** 🔪 **Delete code aggressively (with proof)** — Prefer removing unused paths over "simplifying" them. "If I delete this, will anything break?" No = DELETE. Yes = keep but simplify.
- [ ] **274.** 🟢 **Inline needless indirection** — If a function is a 1-line pass-through with no semantic value, remove it. Call the target directly.
- [ ] **275.** 🟡 **Reduce public API surface** — Make modules/classes expose the minimum. Fewer exports/public methods = easier refactors later.
- [ ] **276.** 🟡 **One obvious way** — Within a codebase, pick ONE pattern for the same thing (errors, results, async style, DI). Consistency simplifies more than cleverness.
- [ ] **277.** 🟢 **Normalize data to kill branching** — Convert inputs to canonical shape early so downstream code is simpler. Shape divergence = branching explosion.
- [ ] **278.** 🟡 **Keep refactors tool-friendly** — Use formatter + linter + "rename symbol" refactors; avoid manual risky edits that tools can't verify.

---

## 🧠 Cognitive Load & Hidden Coupling (279–286)

*Focus: "Don't make me think." Hidden dependencies and cognitive overhead.*

- [ ] **279.** 🟡 **Hidden coupling — temporal APIs** — `init()` must be called before `run()`. The API should enforce this (constructor, state machine) or do it internally. Don't make callers guess.
- [ ] **280.** 🟡 **Destructuring abuse** — Deeply nested object destructuring in function signatures saves lines but destroys readability and makes null-reference bugs harder to spot.
```
# BAD
function printCity({ user: { profile: { address: { city } } } }) { ... }

# GOOD
function printCity(data) {
    const city = data?.user?.profile?.address?.city;
}
```

- [ ] **281.** 🟡 **Deeply nested object access (Law of Demeter)** — `user.profile.address.city` violates encapsulation. Ask for what you need, don't navigate the object graph. Pass `city` directly. (See also #190)
- [ ] **282.** 🟢 **Over-defensive checks** — Re-validating what the type system or upstream validation already guarantees. Redundant guards add noise and suggest code is less safe than it is. (See also #198)
- [ ] **283.** 🟡 **Unnecessary generic type parameters** — `class Repository<T extends BaseEntity<T>>` when you only ever use `Repository<User>`. Add generics at the second use case, not the first.
- [ ] **284.** 🟢 **Type gymnastics** — If the type definition is harder to read than the code it types, simplify. Types should clarify, not obscure.
- [ ] **285.** 🔪 **"WTF/min" density** — Clever one-liners, heavy chaining, missing intermediate variables. `arr.reduce((a, b) => a || b.id, null)` is showing off, not engineering. (See also #126, #230)
- [ ] **286.** 🟢 **Preserve helpful intermediate variables** — Don't inline everything. A well-named `const` for a complex boolean is self-documenting code. (Pairs with #230)

---

## 🔴 Critical Items Summary (Must-Fix Before Ship)

These cause production bugs or data corruption:

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

**API & Security (see code_security.md for full security checklist):**
- #43 — Sensitive data in GET params/URLs
- #45 — Rate limiting (also see code_security.md #5)

**Refactor Safety (CRITICAL):**
- #269 — Separate refactor commits from behavior changes
- #270 — Characterization tests before refactor (no tests = no refactor)

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
- Refactor safety (#271-272, #275-276, #278)
- Cognitive load (#279-281, #283)
- Hidden coupling (#279)

---

## 🟢 Medium Priority (Nice to Have)

Code pleasantness improvements that rarely cause bugs:
- Naming conventions (#11-17)
- Comment style (#165-169)
- Boolean blindness (#196)
- Lazy classes (#146)
- Scope minimization (#193)
- Yoda conditions (#233)
- Nano-functions (#258)
- Intermediate variables (#286)
- Type gymnastics (#284)
- Over-defensive checks (#282)

---

## 🔪 SIMPLIFY Priority (De-Bloat & Ruthless Deletion)

*Focus: Over-engineering, unnecessary complexity, and "just in case" code. Use for self-review after writing sessions.*

**Abstraction Bloat:**
- #254 — Unnecessary abstraction layers
- #255 — Premature abstraction (Rule of Three)
- #262 — Polymorphism for ≤2 cases
- #265 — Unnecessary design patterns
- #267 — Ceremony layers

**Wrong DRY / False Duplication:**
- #256 — Forced DRY — coupling unrelated code
- #268 — Over-generalized solutions

**Over-Fragmentation:**
- #257 — Over-fragmented code (Ravioli)
- #258 — Nano-functions that obscure flow

**Config & Utility Bloat:**
- #260 — Over-configurable code
- #264 — Helper/Utility class sprawl
- #266 — Config hell

**YAGNI & Dead Weight:**
- #194 — YAGNI violations (delete aggressively)
- #273 — Delete code aggressively (with proof)

**Cognitive Overhead:**
- #285 — "WTF/min" density (clever code syndrome)
