# ⚡ CODE PERFORMANCE REVIEW CHECKLIST

> *Make it fast. Make it thick. Ship it right.*

**Priority Legend:** 🔴 CRITICAL | 🟡 HIGH | 🟢 MEDIUM

---

# 🧭 QUICK REFERENCE: "USER SAYS X → CHECK Y"

| User Says | First Places to Look |
|-----------|----------------------|
| *"App is slow"* | Profile first → DB queries (N+1, missing index) → Caching |
| *"Slow under load"* | Connection pools → Async bottlenecks → Scaling config → Lock contention |
| *"Page loads slowly"* | Bundle size → Render waterfall → Image optimization → CDN |
| *"API times out"* | External I/O timeouts → N+1 queries → Missing pagination |
| *"Uses too much memory"* | Unbounded collections → Cache eviction → Object allocation in loops |
| *"Database is slow"* | EXPLAIN ANALYZE → Missing indexes → N+1 → Connection pool exhaustion |
| *"Works fine locally, slow in prod"* | Cold starts → Resource limits → Geographic latency → Missing env config |
| *"Gets slow over time"* | Memory leak → Cache without eviction → DB table bloat → Log accumulation |
| *"High variance / bad P99"* | Queues/locks/GC/downstream → Trace waterfall → GC metrics |
| *"Slow only on first request after deploy"* | Cold start/cache → Warmup metrics → Lazy initialization |

---

# 🔍 SYMPTOM → LIKELY AREA → FIRST TOOL

| Symptom | Likely Area | First Tool |
|---------|-------------|------------|
| Slow only on certain endpoints | Backend/DB | Trace + DB query timings |
| Slow only on first request after deploy | Cold start/cache | Trace + warmup metrics |
| Gets worse with concurrency | Contention/pools | Saturation metrics + load test |
| UI feels janky (scroll/input lag) | Frontend main thread | DevTools Performance + INP |
| High variance / bad P99 | Queues/locks/GC/downstream | Trace waterfall + GC metrics |
| Memory grows unbounded | Leaks / unbounded cache | Memory profiler + heap dump |
| Spikes in error rate | Downstream failures / timeouts | Distributed trace + error logs |

---

# 📈 SCALING DECISION TREE — OPTIMIZE OR SCALE?

Ask these questions:

| Signal | Action |
|--------|--------|
| ✅ CPU consistently >80%? | Optimize code or scale vertically |
| ✅ RAM usage growing unbounded? | Fix leaks or add memory |
| ✅ Disk I/O saturated? | Optimize queries, add SSD, or read replicas |
| ✅ Network bandwidth maxed? | Compress payloads, CDN, paginate |
| ✅ Hitting connection limits? | Tune pools, add replicas, async I/O |

**Key insight:**
- 🛑 If P99 latency is high but CPU/RAM are low → You have an I/O or algorithmic bottleneck → **OPTIMIZE FIRST**
- 🚀 If optimizing yields <10% gain and cost of eng time > cost of infra → **Just scale it** (for now)

---

# ⚖️ LATENCY vs THROUGHPUT — OPTIMIZE FOR WHAT?

| Metric | What It Means | How to Improve |
|--------|---------------|----------------|
| **Latency** | Time for one operation to complete (e.g., API response time) | Reduce round trips, cache, optimize algorithms, edge compute |
| **Throughput** | Operations per second the system can handle (e.g., req/sec) | Parallelize, batch, scale horizontally, optimize resource usage |

**Examples:**
- User says "page loads slow" → optimize **latency** (LCP, TTFB, reduce render blocking)
- Ops says "we're dropping requests at peak" → optimize **throughput** (scale workers, tune pools, queue backpressure)

---

# 🛠️ PERFORMANCE TOOLBOX — BY STACK

## Python
| Category | Tools |
|----------|-------|
| CPU Profiler | `python -m cProfile`, `py-spy`, `scalene` |
| Memory | `tracemalloc`, `memory_profiler`, `memray` |
| Async | `aiomonitor`, `yappi` |
| DB | `django-debug-toolbar`, `sqlalchemy echo=True`, `pg_stat_statements` |

## Node.js
| Category | Tools |
|----------|-------|
| CPU Profiler | `node --prof`, `clinic.js`, `0x` |
| Heap | `node --inspect`, Chrome DevTools Memory tab |
| APM | `dd-trace`, `OpenTelemetry` |
| Load Test | `autocannon`, `k6` |

## React / Frontend
| Category | Tools |
|----------|-------|
| Bundle | `webpack-bundle-analyzer`, `source-map-explorer` |
| Render | React DevTools Profiler, `why-did-you-render` |
| Metrics | `web-vitals`, Lighthouse CI, CrUX dashboard |
| Virtualize | `react-window`, `react-virtualized` |

## Go
| Category | Tools |
|----------|-------|
| CPU/Heap | `pprof` |
| Trace | `go tool trace` |
| Race Detector | `go run -race` |

## JVM (Java/Scala/Kotlin)
| Category | Tools |
|----------|-------|
| CPU Profiler | `async-profiler` |
| Memory | Eclipse MAT, `jmap` |
| Production | JFR (Java Flight Recorder), Pyroscope |

## PostgreSQL
| Category | Tools |
|----------|-------|
| Slow queries | `log_min_duration_statement = 200ms` |
| Index advice | `pg_qualstats`, `hypopg` |
| Bloat | `pg_bloat_check`, `pg_repack` |
| Explain | `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` |

---

# 🚩 QUICK SCAN: TOP PERFORMANCE RED FLAGS

*Fast visual cues during code review — see [full Hall of Shame](#-performance-anti-patterns-hall-of-shame) for complete list.*

| Red Flag | Quick Fix |
|----------|-----------|
| `SELECT *` in production | Select only needed columns |
| No timeout on external HTTP call | Always set `timeout=(connect, read)` |
| `requests.get()` / ORM query inside a loop | Classic N+1 — use batch/join |
| `result += string` inside a loop | Use `"".join(items)` |
| `new Connection()` per request | Use connection pooling |
| Rendering 1000+ DOM nodes | Use virtualization |
| `fs.readFileSync()` in async handler | Use async/streams |

---

# 📋 THE CHECKLIST

---

## 🧮 Algorithmic Complexity

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Big-O audit every hot path** | Profile before assuming. Then check: is this O(n²) hiding in a loop? Could it be O(n log n) or O(n)? |
| 🔴 CRITICAL | **Choose the right sort algorithm** | Built-in sorts (Timsort, introsort) are usually best. Hand-rolled bubble sort for 100k items = crime. |
| 🟡 HIGH | **Avoid sorting the same data repeatedly** | Sort once and maintain order, or use a sorted data structure (heap, sorted list). Sorting inside a loop is a red flag. |
| 🟡 HIGH | **Use binary search on sorted data** | Linear scan on sorted data is wasteful. If data is sorted, binary search gives O(log n) for free. |
| 🟡 HIGH | **Short-circuit and early exit** | Break out of loops as soon as the answer is found. Evaluating the full collection when you only need the first match is wasteful. |
| 🟡 HIGH | **Audit space complexity alongside time complexity** | Sometimes you trade time for space intentionally — make it explicit. O(n) memory for O(1) lookup? Worth it? |
| 🟢 MEDIUM | **Understand amortized complexity** | `list.append()` is amortized O(1), not pure O(1). Important for pre-allocation decisions in hot loops. |
| 🟢 MEDIUM | **Reduce recursion depth with iteration or tail-call** | Deep recursion is both slower (stack frames) and risky (stack overflow). Prefer iterative solutions for linear traversal. |
| 🟢 MEDIUM | **Use lazy evaluation / generators** | Don't compute the entire result if only the first N items are needed. Generators avoid building giant collections in memory. |

```python
# Algorithmic Complexity Examples

# BAD: nested loop searching → O(n²)
# GOOD: hashmap lookup → O(1)

# BAD: bubble_sort(items)     # O(n²) always
# GOOD: sorted(items)         # Timsort O(n log n), O(n) if nearly sorted

# BAD: for query in queries: results.sort()
# GOOD: results.sort()  # once before the loop

import bisect
# GOOD: bisect.bisect_left(sorted_list, target)  # O(log n)

# BAD: found = any_match(items); return found
# GOOD: for item in items: if match(item): return True

# Pre-allocate when size is known (amortized complexity)
result = [None] * n  # avoids repeated resizing
for i in range(n):
    result[i] = compute(i)

# BAD: results = [expensive(x) for x in huge_list]
# GOOD: results = (expensive(x) for x in huge_list)  # lazy
```

---

## 🗂️ Data Structure Choices

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Use a set/hashmap for membership tests** | Checking "is X in this list?" in a loop is O(n) per check. Convert to a set first for O(1) lookups. |
| 🔴 CRITICAL | **Use a min/max heap for top-K problems** | Sorting everything to get the top 10 is O(n log n). A heap gives you top-K in O(n log k), much better for large n. |
| 🟡 HIGH | **Use deque for queue operations** | `list.pop(0)` on a Python list is O(n) because it shifts everything. `collections.deque.popleft()` is O(1). |
| 🟡 HIGH | **Prefer arrays over linked lists for cache locality** | Linked list nodes scatter across memory — cache misses hurt. Arrays are contiguous in memory; iteration is ~10x faster in practice. |
| 🟡 HIGH | **Use memoization / dynamic programming for repeated subproblems** | If the same inputs produce the same output and you call it many times, cache the result. Don't recompute. |
| 🟢 MEDIUM | **Counter/defaultdict instead of manual frequency maps** | Manual frequency counting with `dict.get()` and conditional assignments is verbose and slower than Counter. |

```python
# Data Structure Examples

# BAD: if user_id in list_of_ids    # O(n)
# GOOD: if user_id in set_of_ids    # O(1)

import heapq
# GOOD: top10 = heapq.nlargest(10, items, key=lambda x: x.score)

from collections import deque
# BAD: queue.pop(0)     # O(n)
# GOOD: dq.popleft()    # O(1)

# Sequential array access = CPU prefetcher happy
# Linked list traversal = pointer chase = cache thrash

from functools import lru_cache
@lru_cache(maxsize=1024)
def expensive(n): ...

from collections import Counter
# GOOD: freq = Counter(items)  # clean and fast
```

---

## 🗄️ Database & Query Performance

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Eliminate N+1 query problems** | Fetching users then looping to fetch each user's orders one-by-one is catastrophic. Use JOINs or batch fetches. |
| 🔴 CRITICAL | **Index foreign keys and WHERE clause columns** | Without indexes, every query is a full table scan. An unindexed join on a 10M row table will make you famous for the wrong reason. |
| 🔴 CRITICAL | **SELECT only what you need — never SELECT \*** | Fetching 50 columns when you need 3 wastes network, memory, and parse time. Especially painful on wide tables or with ORMs. |
| 🔴 CRITICAL | **Paginate — never load unbounded result sets** | SELECT without LIMIT is a time bomb. One table growing to millions of rows will eventually OOM your app server. |
| 🔴 CRITICAL | **EXPLAIN ANALYZE every new query before shipping** | Make this a habit. Look for: Seq Scan on large tables, high row estimates vs actual, missing indexes. |
| 🔴 CRITICAL | **Avoid long transactions** | They block vacuum/cleanup and increase lock contention. Keep transactions as short as possible. |
| 🟡 HIGH | **Use batch inserts / upserts instead of row-by-row** | Inserting 10,000 rows one at a time is 10,000 round trips. Batch them into a single statement. |
| 🟡 HIGH | **Use covering indexes to avoid table lookups** | A covering index contains all columns the query needs, so the DB never touches the actual table rows — fastest possible read. |
| 🟡 HIGH | **Avoid functions on indexed columns in WHERE clauses** | Wrapping a column in a function prevents index usage. The DB has to compute the function for every row. |
| 🟡 HIGH | **Use connection pooling — don't open a new connection per request** | Opening a DB connection takes 20–100ms. Without pooling, every request pays this cost. Use pgBouncer, HikariCP, or built-in pool. |
| 🟡 HIGH | **Prefer keyset/seek pagination over OFFSET for large offsets** | `OFFSET 100000` still scans 100k rows. Keyset pagination (`WHERE id > last_id`) is O(1). |
| 🟡 HIGH | **Partition large tables** | Range/hash partitioning on time-series data — queries skip irrelevant partitions entirely. |
| 🟡 HIGH | **Use prepared statements for high-QPS repeated queries** | Parameterized queries reuse query plans; string-concatenated queries don't. |
| 🟡 HIGH | **Tune/verify DB stats maintenance** | `ANALYZE`/`VACUUM`/auto stats must run. Bloated tables from deletes slow everything; autovacuum tuning matters. |
| 🟡 HIGH | **Avoid soft deletes on hot tables** | `is_deleted=true` rows bloat indexes and slow queries. Consider hard deletes + archive table instead. |
| 🟢 MEDIUM | **Use read replicas for read-heavy workloads** | Write to primary, read from replicas. Doubles (or more) your read capacity with zero schema changes. |
| 🟢 MEDIUM | **Beware ORM "helpfulness"** | Implicit joins, eager loads, and hidden extra queries can reintroduce N+1 problems silently. |

```sql
-- Database Examples

-- BAD: users.forEach(u => fetchOrders(u.id))  -- 1 + N queries
-- GOOD: fetchUsersWithOrders()                -- 1 query with join

-- GOOD habit before shipping any new query:
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) 
SELECT ...;
-- Look for: Seq Scan on large tables, high row estimates vs actual

-- Fix: CREATE INDEX idx_orders_user_id ON orders(user_id)

-- BAD: SELECT * FROM users
-- GOOD: SELECT id, name, email FROM users

-- BAD: SELECT * FROM orders WHERE status = 'pending'
-- GOOD: SELECT * FROM orders WHERE status = 'pending' LIMIT 100 OFFSET :cursor

-- EVEN BETTER (keyset pagination):
-- SELECT * FROM orders WHERE id > :last_id AND status = 'pending' LIMIT 100

-- BAD: for row in data: db.execute("INSERT ...", row)
-- GOOD: db.bulk_insert(data)  -- single round trip

-- If query always selects (user_id, email, created_at)
-- CREATE INDEX idx_cov ON users(user_id) INCLUDE (email, created_at)

-- BAD: WHERE YEAR(created_at) = 2024     -- no index used
-- GOOD: WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'

-- Configure pool: min_connections=5, max_connections=20
-- Never: new Connection() on every request handler

-- Route reads: db.execute(query, use_replica=True)
-- Route writes: db.execute(query, use_primary=True)

-- Partition example (PostgreSQL):
-- CREATE TABLE orders (id bigint, created_at timestamp, ...)
-- PARTITION BY RANGE (created_at);
```

---

## 🧠 Memory & Allocation

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **String concatenation in loops — use join()** | Strings are immutable. Concatenating in a loop creates a new string object every iteration. O(n²) total allocations. |
| 🔴 CRITICAL | **Don't build unbounded in-memory collections** | Loading 1M rows into a list to filter 3 is both slow and memory-explosive. Stream or filter at the source. |
| 🔴 CRITICAL | **Avoid object allocation inside tight loops** | Creating new objects in a hot loop stresses the garbage collector. Reuse objects or use primitives where possible. |
| 🟡 HIGH | **Use streaming/chunked processing for large data** | Process large files or query results in chunks rather than loading everything at once. Memory stays flat regardless of input size. |
| 🟡 HIGH | **Unbounded caches need eviction policies** | An in-memory cache that only grows is a memory leak with good PR. Add TTL, LRU eviction, or max size limits. |
| 🟡 HIGH | **Close closures that capture large objects** | A lambda or callback holding a reference to a huge data structure keeps it alive in memory indefinitely. |
| 🟡 HIGH | **Use \_\_slots\_\_ for small, numerous objects (Python)** | `__slots__` eliminates the per-instance `__dict__`, reducing memory by ~40-60% for classes with many instances. |
| 🟢 MEDIUM | **Prefer typed arrays (numpy, typed arrays in JS)** | Native lists/arrays store boxed objects. NumPy/typed arrays store raw values — 10-100x less memory, much faster iteration. |

```python
# Memory Examples

# BAD: result = ""; for s in items: result += s
# GOOD: result = "".join(items)

# BAD: all_orders = db.query("SELECT * FROM orders")  # 500k rows
# GOOD: db.query("SELECT * FROM orders WHERE status='pending' LIMIT 100")

# BAD: for i in range(1_000_000): result.append({"id": i, "val": i*2})
# Consider: pre-allocate, use numpy arrays, or yield instead

# BAD: data = file.read()            # entire file in RAM
# GOOD: for chunk in file.chunks(8192): process(chunk)

# BAD: cache = {}; cache[key] = value  # grows forever
# GOOD: cache = LRUCache(maxsize=1000, ttl=300)

# BAD: fn = lambda: print(len(huge_df))  # holds entire df
# GOOD: n = len(huge_df); fn = lambda: print(n)  # only captures int

# GOOD for data classes with 1M+ instances:
class Point:
    __slots__ = ["x", "y"]

# BAD: data = [1.0, 2.0, 3.0]  # list of Python float objects
# GOOD: data = np.array([1.0, 2.0, 3.0], dtype=np.float64)
```

---

## 💾 Caching Strategy

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Identify and cache hot, expensive reads** | Profile first. Then cache the reads that are: expensive to compute, called frequently, and return stable data. |
| 🔴 CRITICAL | **Define cache invalidation explicitly** | "We cache it" is not a strategy. Define: what triggers invalidation? TTL? Write-through? Cache-bust on update? |
| 🔴 CRITICAL | **Design cache keys carefully** | Bad key design causes collisions or unbounded key spaces. Include version, tenant, and all distinguishing attributes. |
| 🟡 HIGH | **Pre-warm caches for predictable hot keys** | Cold start after a deploy means your first N requests hit the DB hard. Pre-warm for known hot keys at startup. |
| 🟡 HIGH | **Use local in-process cache before distributed cache** | Redis is fast but still involves a network hop. An in-process LRU cache for extremely hot data is 10-100x faster. |
| 🟡 HIGH | **Avoid cache stampede (dogpile effect)** | When a cached key expires and 1000 requests simultaneously try to recompute it, you get a thundering herd. Use locks or probabilistic early expiry. |
| 🟡 HIGH | **Implement negative caching** | Cache "this user doesn't exist" to avoid repeated DB misses on non-existent keys. |
| 🟡 HIGH | **Use stale-while-revalidate pattern** | Serve stale data instantly, refresh in background — zero latency penalty for users. |
| 🟢 MEDIUM | **HTTP cache headers for static/semi-static responses** | Set Cache-Control, ETag, and Last-Modified appropriately. Free caching at CDN and browser layer with zero infrastructure. |

```python
# Caching Examples

# Pattern: cache-aside
def get_product(id):
    cached = cache.get(f"product:{id}")
    return cached if cached else cache.set(f"product:{id}", db.fetch(id))

# Bad: "we cache user profiles for... some time?"
# Good: TTL=300s + explicit invalidation on profile update

# On deploy: pre_warm_cache(top_1000_products)

# L1: in-process LRU (0.01ms)
# L2: Redis (0.5ms)
# L3: Database (5-50ms)

# Pattern: mutex/lock on cache miss
# Or: jitter TTL = base_ttl + random(0, 30)

# Negative cache example:
result = cache.get(key)
if result is CACHE_MISS:
    result = db.fetch(key)
    # Cache even None results to avoid repeated DB hits
    cache.set(key, result or SENTINEL_NOT_FOUND, ttl=60)

# HTTP Headers:
# Cache-Control: public, max-age=3600, stale-while-revalidate=86400
# ETag: "abc123xyz"
```

---

## ⚡ Concurrency & Async

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Parallelize independent async operations** | Sequential awaits for independent operations means you pay the latency of each one, in series. Use `Promise.all()` or `asyncio.gather()`. |
| 🔴 CRITICAL | **Offload CPU-heavy work to worker threads / processes** | Image processing, PDF generation, ML inference on the main event loop blocks all other requests. Use a worker pool. |
| 🔴 CRITICAL | **Set timeouts on all external I/O** | Without timeouts, a slow external service holds your thread/connection forever. Set connect + read timeouts on every HTTP/DB call. |
| 🟡 HIGH | **Batch and debounce high-frequency operations** | Writing a DB row or sending a metric on every single event is expensive. Batch them up and flush periodically. |
| 🟡 HIGH | **Use async I/O — don't block threads on I/O waits** | Synchronous file or network I/O blocks the whole thread. Async I/O lets one thread handle thousands of concurrent I/O waits. |
| 🟡 HIGH | **Tune thread pool and connection pool sizes together** | Threadpool of 100 with a DB connection pool of 5 means 95 threads are always waiting. Match sizes to actual bottleneck. |
| 🟡 HIGH | **Profile lock contention under load** | Locks that look fine at low concurrency can serialize at scale. Measure, don't guess. |
| 🟡 HIGH | **Avoid global locks — prefer per-key locks** | Global mutex = single-threaded under contention. Use fine-grained locks keyed by resource ID. |
| 🟡 HIGH | **Propagate async context (trace IDs, user IDs)** | Async code loses request context without explicit propagation. Use contextvars or AsyncLocalStorage. |

> 💡 **See also:** [Contention, Locking & Saturation](#-contention-locking--saturation) for backpressure, pool exhaustion, and queue management.

```python
# Concurrency Examples

# BAD: 2s total
const users = await fetchUsers();   // 1s
const orders = await fetchOrders(); // 1s

# GOOD: 1s total
const [users, orders] = await Promise.all([fetchUsers(), fetchOrders()])

# BAD: app.post("/resize", (req, res) => resizeImage(req))  // blocks event loop
# GOOD: queue.add("resize-job", req.data)  // worker picks it up async

# BAD: response = requests.get(url)  # hangs forever
# GOOD: response = requests.get(url, timeout=(3.05, 10))  # connect, read

# BAD: on_event(e): db.insert(e)         // 10k inserts/sec
# GOOD: on_event(e): buffer.add(e)       // flush every 100ms

# BAD (Flask sync): return requests.get(url).json()
# GOOD (FastAPI async): return await httpx.get(url).json()

# Rule of thumb: pool_size ≈ (cpu_cores * 2) + effective_spindle_count
# Always load-test and measure before tuning

# Per-key locking pattern:
from contextlib import contextmanager
import threading
_locks = {}
_global_lock = threading.Lock()

@contextmanager
def key_lock(key):
    with _global_lock:
        if key not in _locks:
            _locks[key] = threading.Lock()
        lock = _locks[key]
    with lock:
        yield
```

---

## 🌐 Network & I/O Efficiency

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Enable HTTP/2 and connection keep-alive** | HTTP/1.1 opens a new TCP connection per request. HTTP/2 multiplexes dozens of requests over a single connection. |
| 🔴 CRITICAL | **Compress responses — enable gzip/brotli** | A 500KB JSON response becomes 50KB with gzip. Almost free CPU cost for 10x bandwidth savings. |
| 🟡 HIGH | **Use a CDN for static assets and cacheable content** | Serve assets from edge locations close to the user. Cuts latency from 200ms to 5ms. Take static load off your origin entirely. |
| 🟡 HIGH | **Minimize payload size — send only what's needed** | REST APIs often return entire objects when clients need 2 fields. Use sparse fieldsets, projections, or GraphQL. |
| 🟡 HIGH | **Use binary protocols for internal services (gRPC, MessagePack)** | JSON is human-readable but slow to parse and bloated. For internal service-to-service calls, use gRPC or MessagePack. |
| 🟡 HIGH | **Reduce DNS lookups — reuse HTTP sessions/clients** | Creating a new HTTP client per request re-does DNS resolution, TCP handshake, and TLS handshake every time. |
| 🟢 MEDIUM | **Use ETags and conditional requests** | If data hasn't changed, don't transmit it. ETags let clients ask "give me this only if it changed" — returns 304 Not Modified otherwise. |

> 💡 **See also:** [Storage & File I/O](#-storage--file-io) for streaming large files, disk I/O optimization, and object storage.

```
# Network Examples

# Nginx: http2 on;
# Requests: session = requests.Session()  # reuses connection

# Nginx: gzip on; gzip_types application/json text/html;
# Express: app.use(compression())

# Route: /static/* → CDN (CloudFront, Cloudflare, Fastly)
# Route: /api/* → origin server

# BAD: GET /user/123 → { id, name, bio, avatar, history, preferences, ... }
# GOOD: GET /user/123?fields=id,name → { id, name }

# JSON: 200 bytes, ~2ms parse for complex objects
# Protobuf: 50 bytes, 0.2ms parse

# BAD: axios.get(url)  // new client every call
# GOOD: const client = axios.create(); client.get(url)  // reused

# Server: ETag: "abc123"
# Client: If-None-Match: "abc123"  → 304 Not Modified (zero body)
```

---

## 🖥️ CPU & Compute Optimization

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Profile before optimizing — measure, don't guess** | Gut feel is almost always wrong. Use a profiler (cProfile, async-profiler, Chrome DevTools) to find actual hotspots before touching code. |
| 🔴 CRITICAL | **Compile regex patterns outside of loops** | Compiling the same regex 100,000 times per second is embarrassing. Compile once at module level. |
| 🟡 HIGH | **Use vectorized operations instead of Python loops** | Python loops are slow. NumPy / pandas vectorized ops run in compiled C — orders of magnitude faster for numerical work. |
| 🟡 HIGH | **Avoid repeated attribute lookups in tight loops** | Python attribute lookup (`obj.method`) traverses the MRO every time. Cache the method reference outside the loop. |
| 🟡 HIGH | **Use appropriate number types — avoid float where int suffices** | Float arithmetic is slower than integer arithmetic, especially in tight loops. Use integers for counts, IDs, and integer math. |
| 🟢 MEDIUM | **Short-circuit boolean evaluation aggressively** | Put the cheapest and most likely to fail condition first in AND chains. Python/JS will skip the rest. |
| 🟢 MEDIUM | **Consider JIT-compiled alternatives for hot Python code** | PyPy, Numba, or Cython can give 10-100x speedup for numerical hot paths without rewriting in C. |

> 💡 **See also:** [Serialization & Parsing](#-serialization--parsing) for JSON performance, faster serializers, and response sizing.

```python
# CPU & Compute Examples

# Python: python -m cProfile -s cumtime script.py
# Node: node --prof app.js && node --prof-process isolate-*.log
# Go: go test -cpuprofile cpu.prof && go tool pprof cpu.prof

# BAD: for line in lines: re.search(r'\d{4}', line)
# GOOD: YEAR = re.compile(r'\d{4}')
#        for line in lines: YEAR.search(line)

# BAD: result = [x * 2 for x in data]  # Python loop
# GOOD: result = np_array * 2           # NumPy vectorized, C speed

# BAD: for x in data: results.append(transform(x))
# GOOD: app = results.append  # cache reference
#        for x in data: app(transform(x))

# BAD: total = 0.0; for x in items: total += x.count  # float
# GOOD: total = 0; for x in items: total += x.count   # int

# BAD: if expensive_check() and cheap_check():
# GOOD: if cheap_check() and expensive_check():  // cheap first

# Numba JIT for numeric hot loops:
from numba import jit
@jit(nopython=True)
def hot_function(arr): ...
```

---

## 🌟 Frontend Performance

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Code-split and lazy-load — don't ship everything upfront** | A 5MB JavaScript bundle on initial load blocks rendering. Code-split by route and lazy-load components that aren't immediately visible. |
| 🔴 CRITICAL | **Avoid render waterfalls — parallelize data fetching** | Parent component fetches, renders child, child fetches — sequential. Move to parallel fetches at the route level. |
| 🔴 CRITICAL | **Virtualize long lists — never render 10k DOM nodes** | Rendering 10,000 list items is an instant jank machine. Virtualization renders only visible items. |
| 🟡 HIGH | **Preload / prefetch critical resources** | `<link rel="preload">` for fonts, critical CSS, key API calls. `<link rel="preconnect">` for critical origins. |
| 🟡 HIGH | **Avoid render-blocking scripts** | Use `async`/`defer` on non-critical scripts. Put critical CSS in `<head>`, non-critical at end of body. |
| 🟡 HIGH | **Memoize expensive React renders** | Components re-render on every parent render, even if their props didn't change. Memoize pure components and callbacks. |
| 🟡 HIGH | **Debounce and throttle event handlers** | A scroll or resize handler firing 60 times/second on every pixel change is unnecessary. Debounce and throttle aggressive events. |
| 🟡 HIGH | **Optimize images — correct format, size, and lazy loading** | Use WebP/AVIF over JPEG. Serve appropriately sized images. Lazy-load offscreen images. Use srcset for responsive images. |
| 🟡 HIGH | **Audit third-party scripts** | Analytics, chat widgets, A/B tools — often 40% of page weight. Lazy-load, defer, or remove unused. |
| 🟡 HIGH | **Measure Core Web Vitals — LCP, FID/INP, CLS** | LCP (largest contentful paint), INP (interaction to next paint), CLS (cumulative layout shift). These directly impact SEO and UX. |
| 🟡 HIGH | **Optimize font loading** | Use `font-display: swap`, subset fonts, WOFF2 format. Preload critical fonts. |
| 🟢 MEDIUM | **Avoid layout thrashing — batch DOM reads and writes** | Interleaving DOM reads and writes forces the browser to recalculate layout repeatedly. Batch reads together, then writes. |
| 🟢 MEDIUM | **Use Service Worker for offline + cache** | Cache static assets aggressively at edge of browser. Enables offline access and faster repeat visits. |

```jsx
// Frontend Examples

// BAD: import HugeModal from "./HugeModal"  // always bundled
// GOOD: const HugeModal = lazy(() => import("./HugeModal"))

// BAD: Component renders, triggers fetch, child renders, triggers fetch
// GOOD: Route loader fetches all data in parallel before render

// BAD: data.map(item => <Row key={item.id} />)  // 10k DOM nodes
// GOOD: <VirtualList items={data} rowHeight={40} />  // ~20 DOM nodes

<!-- Preload critical path -->
<link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
<link rel="preconnect" href="https://api.example.com">

<!-- Non-critical JS -->
<script src="analytics.js" defer></script>

// React.memo: skips re-render if props unchanged
// useMemo: memoizes expensive computed values
// useCallback: memoizes function references

// BAD: window.addEventListener("scroll", fetchData)
// GOOD: window.addEventListener("scroll", debounce(fetchData, 200))

<img src="img.webp" loading="lazy" width="400" height="300"
     srcset="img-sm.webp 400w, img-lg.webp 800w"
     sizes="(max-width: 600px) 400px, 800px" />

// Tools: Lighthouse, PageSpeed Insights, web-vitals npm package
// Targets: LCP < 2.5s, INP < 200ms, CLS < 0.1

// BAD (thrashing): el.style.width = x + "px"; h = el.clientHeight; ...
// GOOD: const h = el.clientHeight; requestAnimationFrame(() => el.style.width = x)

/* Font optimization */
@font-face {
  font-family: 'Main';
  src: url('/fonts/main.woff2') format('woff2');
  font-display: swap;
}
```

---

## 📊 Performance Observability

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Instrument latency at every service boundary** | You can't optimize what you can't measure. Add timing spans around every DB call, external API, and cache operation. |
| 🔴 CRITICAL | **Track P50/P95/P99 latency — not just average** | Average latency hides slow outliers. A P99 of 5 seconds means 1% of users wait 5 seconds. That's catastrophic at scale. |
| 🔴 CRITICAL | **Use distributed tracing — not just metrics** | Metrics tell you *something* is slow; traces tell you *where*. Trace across all services. |
| 🟡 HIGH | **Add performance budgets to CI/CD** | Set hard limits: bundle size < 200KB, LCP < 2.5s, API latency P99 < 500ms. Fail the build if budgets are exceeded. |
| 🟡 HIGH | **Benchmark before and after every optimization** | Without before/after benchmarks, you don't know if your optimization actually helped, regressed, or made no difference. |
| 🟡 HIGH | **Track error rate as a performance signal** | Errors are infinite latency from the user's perspective. High error rate = performance problem. |
| 🟡 HIGH | **Use synthetic monitoring** | Monitor from outside your infra — catches what internal metrics miss. Run periodic checks from multiple regions. |
| 🟡 HIGH | **Profile in production** | Continuous profiling (Pyroscope, Datadog profiler) catches things load tests don't. Real traffic reveals real hotspots. |
| 🟢 MEDIUM | **Use flame graphs to find actual hotspots** | Flame graphs visualize where CPU time is spent across the call stack. They're the fastest way to find non-obvious bottlenecks. |

```python
# Observability Examples

# OpenTelemetry / Datadog / Jaeger traces
# with tracer.start_span("db.query"): result = db.execute(sql)

# Use histograms, not averages
# Alert on P99 > threshold, not avg > threshold

# Lighthouse CI: assert: [{ metric: lcp, maxValue: 2500 }]
# Bundlesize: { "src/main.js": "< 200 kB" }

# Python: timeit, pytest-benchmark
# Node: autocannon, k6
# Always run in conditions matching production

# Python: py-spy top --pid <PID>
# Node: clinic flame -- node app.js
# JVM: async-profiler
```

---

## 🏗️ Infrastructure & Deployment

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Set container resource limits (CPU/memory)** | Under-provisioned containers throttle and OOM. Always set requests AND limits. |
| 🔴 CRITICAL | **Optimize cold starts (Lambda/serverless)** | Serverless cold starts can add 2-5s latency. Minimize bundle size, avoid heavy imports at module level, use provisioned concurrency. |
| 🔴 CRITICAL | **Implement graceful shutdown** | Dropped connections during deploys = invisible errors. Drain connections before killing pods. |
| 🟡 HIGH | **Horizontal vs vertical scaling decision** | Know when to add instances vs add resources. CPU-bound → vertical. I/O-bound → horizontal. |
| 🟡 HIGH | **Configure auto-scaling thresholds correctly** | Scale too late = degraded service. Scale too early = wasted money. Base on P95 latency + CPU, not just CPU. |
| 🟡 HIGH | **Geographic distribution / multi-region** | Speed of light is real. Put compute near users. Use edge locations for latency-sensitive paths. |
| 🟡 HIGH | **Increase file descriptor limits** | Default Linux `ulimit -n` is often 1024. High-concurrency servers need 65k+ for open sockets. |
| 🟢 MEDIUM | **Use immutable infrastructure** | Pets vs cattle. Immutable infrastructure means consistent performance across deploys. |

```yaml
# Container: always set resource requests AND limits
resources:
  requests: { cpu: "250m", memory: "256Mi" }
  limits:   { cpu: "1000m", memory: "512Mi" }

# Lambda cold start optimization:
# - Minimize deployment package size
# - Use provisioned concurrency for latency-sensitive paths
# - Lazy-load heavy dependencies

# Graceful shutdown (Kubernetes):
# lifecycle:
#   preStop:
#     exec:
#       command: ["/bin/sh", "-c", "sleep 10"]

# Increase file descriptors:
# ulimit -n 65535
# Or in systemd: LimitNOFILE=65535
```

---

## 📦 Queue & Background Job Performance

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Make jobs idempotent** | Retried jobs that duplicate work = silent bugs + wasted load. Design for at-least-once delivery. |
| 🔴 CRITICAL | **Use dead letter queues** | Failed jobs that retry forever starve the queue. Move them to DLQ after N retries for investigation. |
| 🟡 HIGH | **Implement priority queues** | All jobs equal means urgent work waits behind bulk exports. Separate queues by priority. |
| 🟡 HIGH | **Batch job fetching at worker level** | Worker fetching 1 job at a time = queue overhead dominates. Fetch multiple jobs per network round trip. |
| 🟡 HIGH | **Use fan-out patterns for parallel processing** | One event triggers 50 workers efficiently vs sequentially. Publish to multiple consumers. |
| 🟡 HIGH | **Measure queue lag and processing rate** | Queue depth growing = consumers can't keep up. Alert before it becomes critical. |
| 🟢 MEDIUM | **Choose the right queue backend** | Redis for simple, RabbitMQ for complex routing, Kafka for high-throughput streaming. |

```python
# Queue Examples

# Idempotent job design:
@job
def process_order(order_id):
    # Check if already processed
    if Order.get(order_id).status == 'processed':
        return  # skip, already done
    # ... process ...

# Dead letter queue pattern:
@job(retries=3, retry_backoff=True, retry_jitter=True)
def risky_job(data):
    ...
# After 3 retries → DLQ for investigation

# Priority queues:
# HIGH: queue.process('email:urgent', handler)
# LOW:  queue.process('email:digest', handler)

# Batch job fetching (BullMQ example):
worker = Worker('my-queue', {
  limiter: {
    max: 1000,    # max jobs per duration
    duration: 1000  # per millisecond
  }
})

# Fan-out (Redis pub/sub or Kafka):
# Publisher sends to "orders.created" topic
# Multiple consumers: email-service, inventory-service, analytics-service
```

---

## 🛡️ Rate Limiting & Overload Protection

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Implement circuit breakers on external dependencies** | Slow downstream drags everything — fail fast instead. Open circuit after N failures, retry with backoff. |
| 🔴 CRITICAL | **Rate limit inbound traffic** | Runaway client hammering your API kills everyone else. Per-user, per-IP, per-API-key limits. |
| 🔴 CRITICAL | **Shed load gracefully (429 > 504)** | Rejecting excess load fast is better than queuing forever. Return 429 early, don't let requests pile up. |
| 🟡 HIGH | **Implement request coalescing / deduplication** | 1000 requests for same uncached resource = 1000 DB hits. Coalesce into one DB call, serve result to all waiters. |
| 🟡 HIGH | **Use the bulkhead pattern** | Isolate slow consumers so they don't starve fast paths. Separate thread pools / connections per downstream. |
| 🟡 HIGH | **Set concurrency limits per route** | Not all endpoints are equal. Limit expensive endpoints separately from cheap ones. |
| 🟢 MEDIUM | **Implement graceful degradation** | When overloaded, serve cached/stale data or simplified responses rather than errors. |

```python
# Rate Limiting Examples

# Circuit breaker (pybreaker, resilience4j, etc.)
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30)
def call_external_api():
    return requests.get(url, timeout=5)

# OPEN state: fail immediately instead of waiting 30s to time out
# HALF-OPEN: try one request, close if success, open if fail
# CLOSED: normal operation

# Request coalescing (asyncio):
from asyncio import Lock
_cache_locks = {}

async def get_with_coalescing(key):
    if key not in _cache_locks:
        _cache_locks[key] = Lock()
    
    async with _cache_locks[key]:
        # Double-check after acquiring lock
        cached = cache.get(key)
        if cached:
            return cached
        result = await fetch_from_db(key)
        cache.set(key, result)
        return result

# Bulkhead pattern (separate pools):
# api_pool = ConnectionPool(size=10)  # for API calls
# db_pool = ConnectionPool(size=20)   # for DB calls
# Slow DB won't starve API calls

# Rate limiting (Redis token bucket):
# RATE_LIMIT = 100 requests per minute per user
# redis.incr(f"ratelimit:{user_id}")
# redis.expire(f"ratelimit:{user_id}", 60)
```

---

## 🌍 System Architecture & Distributed Systems

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Reduce chattiness between services** | Making 50 internal HTTP calls to Service B to build one response is a latency death spiral. Consolidate into 1 batch call. |
| 🔴 CRITICAL | **Apply data locality — move compute to data** | Don't pull 10GB of data over the network to process it. Push the processing logic (stored proc, Spark job) to where the data lives. |
| 🟡 HIGH | **Use async/event-driven for non-critical paths** | Sending an email, updating analytics, or generating a PDF should never block the user's HTTP response. Push to a queue. |
| 🟡 HIGH | **Use content negotiation for media** | Don't send a high-res PNG to a mobile phone. Support Accept headers for requesting specific sizes/formats. |
| 🟡 HIGH | **Design for partial failure** | Distributed systems fail. Use timeouts, retries with backoff, and fallbacks. Assume any call can fail. |
| 🟢 MEDIUM | **Use service mesh for observability** | Istio, Linkerd provide automatic tracing, metrics, and traffic management without code changes. |
| 🟢 MEDIUM | **Implement health checks at every layer** | Load balancer health checks, container health probes, service health endpoints. Enable automatic recovery. |

```python
# Architecture Examples

# BAD: 50 HTTP calls to build one response
for user_id in user_ids:
    user = user_service.get(user_id)       # 50 calls
    
# GOOD: Batch API
users = user_service.get_batch(user_ids)   # 1 call

# Data locality:
# BAD: Pull 10GB to app server, process, push 10GB back
# GOOD: Run Spark job where data lives (S3/Databricks)
# BETTER: Stored procedure for simple aggregations

# Async non-critical path:
def create_order(order):
    order = db.save(order)
    # Don't block on these!
    queue.enqueue(send_confirmation_email, order.id)
    queue.enqueue(update_analytics, order.id)
    queue.enqueue(inventory.update, order.items)
    return order  # Return immediately

# Content negotiation:
@app.route("/images/<id>")
def get_image(id):
    accept = request.headers.get("Accept", "")
    if "image/webp" in accept:
        return send_file(f"{id}.webp", mimetype="image/webp")
    return send_file(f"{id}.jpg", mimetype="image/jpeg")

# Partial failure handling:
async def get_user_with_fallback(user_id):
    try:
        return await user_service.get(user_id, timeout=2)
    except TimeoutError:
        return await cache.get(f"user:{user_id}")  # fallback
```

---

## 💾 Storage & File I/O

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Stream large file uploads/downloads** | Buffering a 1GB upload in memory before processing = OOM. Stream directly to disk or object storage. |
| 🟡 HIGH | **Avoid disk I/O on hot paths** | Disk is ~1000x slower than RAM. Log writes, temp files, and config reads should not be in hot paths. |
| 🟡 HIGH | **Use object storage (S3) for blobs** | Don't serve large files through your app server. Use CDN-backed object storage. |
| 🟡 HIGH | **Compress stored data** | Parquet vs CSV for analytics, gzip stored JSON. Storage is cheap but I/O isn't. |
| 🟡 HIGH | **Use connection pooling for object storage** | Reuse HTTP connections to S3/GCS. Don't open a new connection per file. |
| 🟢 MEDIUM | **Choose the right storage class** | Hot data on SSD, cold data on HDD/archive. S3 Standard vs S3 Glacier for access patterns. |

```python
# Storage Examples

# Stream file upload (don't buffer in memory):
@app.post("/upload")
async def upload(file: UploadFile):
    async with aiofiles.open(f"/tmp/{file.filename}", "wb") as f:
        while chunk := await file.read(65536):  # 64KB chunks
            await f.write(chunk)
    return {"status": "ok"}

# Stream to S3 (don't load into memory):
import boto3
s3 = boto3.client('s3')

def upload_stream(file_obj, bucket, key):
    s3.upload_fileobj(file_obj, bucket, key)

# Compress stored data:
import pandas as pd
df.to_parquet("data.parquet")  # vs df.to_csv("data.csv")
# Parquet: 10x smaller, columnar, faster queries

# Storage class decision:
# Hot data: S3 Standard (ms latency)
# Infrequent access: S3 IA (cheaper, retrieval fee)
# Archive: S3 Glacier (hours to retrieve)
```

---

## 🔄 Serialization & Parsing

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Measure JSON serialization cost** | JSON encode/decode is often a top CPU consumer in API servers. Profile it. |
| 🟡 HIGH | **Avoid double-encoding / repeated parsing** | Parse once, reuse structured form. Don't JSON.parse → JSON.stringify in a loop. |
| 🟡 HIGH | **Use faster serializers when warranted** | `orjson`/`ujson` for Python (5-10x faster), `simdjson` for C++, Protocol Buffers for internal services. |
| 🟡 HIGH | **Cap response size + enforce projections** | Don't let a single API call return 100MB of JSON. Enforce max response size and field projections. |
| 🟢 MEDIUM | **Avoid expensive logging of whole payloads** | Logging entire JSON payloads on every request is a performance killer. Log IDs, not bodies. |

```python
# Serialization Examples

# Profile JSON cost:
import cProfile
cProfile.run("json.dumps(huge_dict)")

# Faster JSON serializers:
import orjson  # 5-10x faster than stdlib
data = orjson.dumps(payload)  # returns bytes
parsed = orjson.loads(data)

# Or ujson:
import ujson
data = ujson.dumps(payload)

# Avoid double-parsing:
# BAD:
for item in items:
    parsed = json.loads(item.json_blob)  # parse every iteration
    
# GOOD:
cached_parses = {item.id: json.loads(item.json_blob) for item in items}

# Cap response size:
@app.get("/users")
def get_users():
    users = db.query("SELECT * FROM users LIMIT 1000")  # hard limit
    if len(users) > 500:
        users = users[:500]  # enforce cap
        response.headers["X-Truncated"] = "true"
    return users

# Better: field projections
@app.get("/users")
def get_users(fields: str = "id,name"):
    allowed = {"id", "name", "email"}
    selected = set(fields.split(",")) & allowed
    return db.query(f"SELECT {','.join(selected)} FROM users LIMIT 100")
```

---

## 🔧 Runtime & GC Tuning

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Tune garbage collection parameters** | In Java/Go/Node, frequent "Stop-the-World" pauses kill latency. Tune heap size and generation sizing to minimize full GCs. |
| 🔴 CRITICAL | **Avoid GC thrashing** | Creating short-lived objects in a tight loop forces the GC to run constantly. Reuse buffers/objects to keep memory pressure stable. |
| 🟡 HIGH | **Warm up the JIT / runtime before routing traffic** | Java/C# need warmup time to JIT compile hot paths. Node.js needs time to optimize V8 paths. Don't route 100% traffic to a cold instance immediately. |
| 🟡 HIGH | **Disable unused runtime features in production** | Turn off debug logging, disable assertion checks, run Python with `-O` to strip assert statements. |
| 🟡 HIGH | **Monitor GC pause times** | If GC pauses exceed your latency budget, you have a problem. Track pause duration and frequency. |
| 🟢 MEDIUM | **Use object pools for hot paths** | Pool and reuse expensive-to-create objects (database connections, thread pools, buffers) instead of creating new ones. |

```bash
# Runtime Tuning Examples

# JVM GC tuning:
java -Xms4g -Xmx4g \           # Fixed heap size (no resize overhead)
     -XX:+UseG1GC \            # G1 garbage collector (low pause)
     -XX:MaxGCPauseMillis=200 \ # Target max pause time
     -XX:+AlwaysPreTouch \     # Touch heap pages at startup
     -jar app.jar

# Node.js --max-old-space-size:
node --max-old-space-size=4096 app.js  # 4GB heap

# Python optimization:
python -O app.py  # Strip assert statements
python -OO app.py # Strip assert AND docstrings

# Go GOGC:
GOGC=100 ./app  # Default, trigger GC when heap doubles
GOGC=off ./app  # Disable GC (only for short-lived CLI tools)

# Warm up before routing traffic:
# Kubernetes: readinessProbe initialDelaySeconds
# Load balancer: gradual traffic shift (10% → 50% → 100%)
```

---

## 📱 Mobile & Battery Performance

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Batch network requests** | Waking up the cellular radio costs battery. Batching uploads/syncs instead of firing every 30 seconds is battery-friendly. |
| 🔴 CRITICAL | **Offload heavy processing to server** | Don't process large datasets or heavy ML models on a mid-range Android phone. Send data up, process, send result down. |
| 🟡 HIGH | **Respect "Low Power Mode"** | Check if the OS is in battery saver mode. If so, disable auto-play videos, reduce fetch frequency, disable animations. |
| 🟡 HIGH | **Optimize overdraw** | Rendering layers on top of invisible layers wastes GPU cycles. Flatten view hierarchies. |
| 🟡 HIGH | **Minimize wake locks** | Holding a wake lock prevents the device from sleeping. Release as soon as possible. |
| 🟢 MEDIUM | **Use efficient image formats** | WebP is 25-35% smaller than JPEG. Smaller downloads = less radio time = less battery. |

```kotlin
// Mobile Examples (Android/Kotlin)

// Batch network requests
// BAD: Upload immediately on every user action
fun onUserAction(event: Event) {
    api.upload(event)  // Wakes radio every time
}

// GOOD: Batch and upload every 5 minutes
val eventBuffer = mutableListOf<Event>()
fun onUserAction(event: Event) {
    eventBuffer.add(event)
    if (eventBuffer.size >= 100) flush()
}

fun flush() {
    api.uploadBatch(eventBuffer)
    eventBuffer.clear()
}

// Check power save mode
val powerManager = getSystemService(Context.POWER_SERVICE) as PowerManager
if (powerManager.isPowerSaveMode) {
    // Reduce polling frequency, disable animations
    fetchInterval = 60_000L  // 1 minute instead of 10 seconds
}

// Reduce overdraw (Android)
// Use Layout Inspector to find overlapping backgrounds
// Remove unnecessary backgrounds from containers
```

```swift
// iOS Examples

// Batch network requests
// Use BGAppRefreshTask for periodic background fetch
// Batch multiple items into single API call

// Check low power mode
if ProcessInfo.processInfo.isLowPowerModeEnabled {
    // Reduce refresh frequency
    refreshInterval = 300  // 5 minutes instead of 30 seconds
}

// Minimize wake locks
// Use URLSessionConfiguration.background for uploads
// Let system decide when to execute
```

---

## ⚠️ Code Anti-Patterns (Hidden Performance Killers)

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Never use exceptions for control flow** | Throwing/catching an exception is incredibly expensive (stack unwinding). Never use try/catch for logic you expect to happen (e.g., "UserNotFound"). Use return values or Result types. |
| 🔴 CRITICAL | **Avoid reflection at runtime in hot paths** | Reflection (Java/C#) or heavy metaprogramming (Python getattr) defeats compiler optimizations. Cache the result of reflection, don't do it every request. |
| 🟡 HIGH | **Fix incorrect locking / lock contention** | Using a broad lock (locking the whole object) when you only need to protect one field serializes all threads. Use fine-grained locks or atomics. |
| 🟡 HIGH | **Don't re-create heavy objects in loops** | Date formatters, regex patterns, JSON serializers — create once, reuse. Re-creating them in a loop is a classic CPU hog. |
| 🟡 HIGH | **Avoid premature optimization** | Profile first. Optimizing the wrong thing is worse than no optimization. |
| 🟢 MEDIUM | **Don't use regex for simple string operations** | `string.contains()` is faster than `regex.match()` for literal strings. Use the right tool. |
| 🟢 MEDIUM | **Be careful with string operations in loops** | String splitting, trimming, and formatting in tight loops add up. Cache results when possible. |

```python
# Code Anti-Pattern Examples

# BAD: Exceptions as control flow
try:
    user = db.get_user(user_id)
except UserNotFoundError:
    user = None

# GOOD: Return value / Optional
user = db.get_user(user_id)  # Returns None if not found
if user is None:
    ...

# BAD: Reflection in hot path
for obj in objects:
    method = getattr(obj, 'process')  # Reflection every iteration
    method()

# GOOD: Cache reflection result
PROCESS_METHOD = operator.methodcaller('process')
for obj in objects:
    PROCESS_METHOD(obj)

# Or even better: use a protocol/interface
# BAD: Broad lock
lock = threading.Lock()

def increment_a():
    with lock:
        global_a += 1

def increment_b():
    with lock:  # Blocks if increment_a is running!
        global_b += 1

# GOOD: Per-field locks
lock_a = threading.Lock()
lock_b = threading.Lock()

# BAD: Re-create date formatter in loop
for log in logs:
    formatter = SimpleDateFormat("yyyy-MM-dd")  # Expensive!
    date = formatter.parse(log.date)

# GOOD: Create once
FORMATTER = SimpleDateFormat("yyyy-MM-dd")
for log in logs:
    date = FORMATTER.parse(log.date)

# BAD: Regex for simple string check
import re
if re.match(r"error", message):  # Overhead of regex engine
    ...

# GOOD: Simple string method
if message.startswith("error"):  # Much faster
    ...
```

---

## 🔒 Contention, Locking & Saturation

| Priority | Item | Description |
|----------|------|-------------|
| 🔴 CRITICAL | **Monitor pool exhaustion** | DB pool, thread pool, HTTP client pool — when exhausted, requests queue indefinitely. Alert before saturation. |
| 🔴 CRITICAL | **Profile database lock contention** | Long transactions, `SELECT ... FOR UPDATE`, hot rows, missing indexes causing lock amplification. |
| 🟡 HIGH | **Measure queue buildup** | Background jobs piling up? Measure lag and processing rate. Alert before backlog becomes critical. |
| 🟡 HIGH | **Fix tail latency amplifiers** | Retries without jitter, synchronized cache expiry — these cause thundering herds that spike P99. |
| 🟡 HIGH | **Implement internal backpressure** | When internal queues fill up, slow down producers. Use bounded queues and propagate pressure upstream. |
| 🟢 MEDIUM | **Use lock-free data structures when appropriate** | For extremely high-contention scenarios, consider lock-free queues, atomic operations, or concurrent collections. |

> 💡 **See also:** [Rate Limiting & Overload Protection](#-rate-limiting--overload-protection) for circuit breakers, load shedding, and external traffic control.

```python
# Contention Examples

# Monitor pool exhaustion:
# Prometheus metric: db_pool_active_connections / db_pool_max_connections
# Alert when > 80%

# Database lock contention:
# PostgreSQL: SELECT * FROM pg_locks WHERE NOT granted;
# Find blocked queries and what's blocking them

# Internal backpressure with bounded queues:
import asyncio

async def producer(queue, data):
    if queue.full():
        # Apply backpressure: slow down or drop
        await asyncio.sleep(0.1)  # rate limit self
    await queue.put(data)

async def consumer(queue):
    while True:
        item = await queue.get()
        process(item)

queue = asyncio.Queue(maxsize=1000)  # bounded!

# Fix tail latency with jitter:
import random

def get_with_jitter(key):
    # Add jitter to TTL to prevent synchronized expiry
    base_ttl = 300
    jitter = random.randint(0, 30)
    cache.set(key, value, ttl=base_ttl + jitter)

# Retry with jitter to prevent thundering herd:
def retry_with_jitter(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception:
            if attempt < max_retries - 1:
                sleep((2 ** attempt) + random.random())  # exponential + jitter
```

---

## 🔨 Build & Startup Performance

| Priority | Item | Description |
|----------|------|-------------|
| 🟡 HIGH | **Lazy imports / deferred initialization** | Import time adds to cold start and test suite time. Lazy-load heavy modules when possible. |
| 🟡 HIGH | **Enable tree-shaking and dead code elimination** | Ships less JS = parses faster. Configure bundler to remove unused code. |
| 🟡 HIGH | **Audit dependencies** | Are you importing lodash for `_.get()`? That's 70KB for one function. Use lighter alternatives. |
| 🟡 HIGH | **Use build caching** | Rebuilding unchanged layers wastes minutes per deploy. Enable CI/CD layer caching. |
| 🟢 MEDIUM | **Parallelize test execution** | Tests running serially? Use parallel test runners to speed up feedback loop. |
| 🟢 MEDIUM | **Measure import time** | Use tools to profile which modules slow down startup. Optimize the slowest ones. |

```python
# Build & Startup Examples

# Lazy imports (Python):
def expensive_function():
    import heavy_module  # Only imported when function is called
    return heavy_module.process()

# Lazy imports (JavaScript):
// Static import at top = always loaded
import { heavy } from 'heavy-module'

// Dynamic import = loaded on demand
async function doHeavy() {
    const { heavy } = await import('heavy-module')
    return heavy()
}

# Tree-shaking (JavaScript):
// BAD: Imports entire library
import _ from 'lodash'
_.get(obj, 'path')

// GOOD: Imports only what you need
import get from 'lodash/get'
get(obj, 'path')

// EVEN BETTER: Use native or lighter alternative
obj?.path  // Native optional chaining

# Build caching (Docker):
# BAD: Copy everything first
COPY . .
RUN pip install -r requirements.txt

# GOOD: Copy requirements first, cache that layer
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .  # Source changes don't invalidate pip install layer

# Measure import time (Python):
python -X importtime your_script.py 2>&1 | grep "import time"
# Or use: pip install tuna && python -X importtime script.py 2> tuna.log && tuna tuna.log
```

---

# 🚫 PERFORMANCE ANTI-PATTERNS HALL OF SHAME

*Complete list — see [Quick Scan](#-quick-scan-top-performance-red-flags) for a condensed version.*

| ❌ Anti-Pattern | Why It's Bad |
|-----------------|--------------|
| `SELECT *` in production | Wastes bandwidth, memory, blocks schema evolution |
| ORM query inside a for loop | Classic N+1 — fires 1000 queries instead of 1 |
| `requests.get()` with no timeout | Can hang thread forever, cascade failures |
| `new Connection()` per request | 20-100ms overhead per request, exhausts DB |
| `re.compile()` inside a loop | Compiles same regex 1000s of times |
| `cache[key] = value` with no eviction | Memory leak disguised as optimization |
| `result += string` inside a loop | O(n²) allocations, kills GC |
| `.sort()` inside a `.map()`/.forEach() | Sorting same data N times |
| `console.log()` in hot path | Yes, it's slow — I/O blocks event loop |
| `JSON.parse(JSON.stringify(obj))` for deep clone | Extremely expensive, loses types |
| `setInterval()` never cleared | Memory leak, keeps running after component unmount |
| Promise chains instead of `Promise.all()` | Serial execution when parallel possible |
| `fs.readFileSync()` in async handler | Blocks event loop, kills throughput |
| Unbounded retry with no backoff | Thundering herd when service recovers |
| `try/catch` for expected conditions | Exceptions are expensive, use return values |
| Logging entire request/response bodies | Disk I/O, memory, sometimes security issue |
| Using regex for simple string contains | Overhead of regex engine for literal match |
| Creating date formatter in loop | Date parsing is expensive, reuse formatters |

---

# 🚀 CRITICAL PERFORMANCE RULES — NEVER VIOLATE

| # | Rule |
|---|------|
| 1 | Profile before optimizing — measure first, then act |
| 2 | N+1 queries will destroy you — use joins/batch fetches |
| 3 | Paginate everything — unbounded queries are time bombs |
| 4 | String concat in loops = O(n²) allocations — use join() |
| 5 | Index your WHERE/JOIN columns — unindexed = full table scan |
| 6 | Parallelize independent async calls — don't await in series |
| 7 | Never render 10k DOM nodes — virtualize |
| 8 | Compile regex outside loops — not inside |
| 9 | Cache hot reads — define invalidation strategy upfront |
| 10 | Offload CPU/IO-heavy work to queues — don't block the event loop |
| 11 | Set timeouts on ALL external I/O — no hanging forever |
| 12 | Use connection pooling — never open a connection per request |
| 13 | Circuit breakers on external dependencies — fail fast |
| 14 | Rate limit inbound traffic — protect yourself from clients |
| 15 | Stream large files — never buffer in memory |

---

> ⚡ *Code Quality & Performance — Make it fast. Make it right. Ship it.*
