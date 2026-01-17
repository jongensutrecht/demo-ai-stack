# Performance Invariant Discovery Questions

Gebruik deze vragen om performance invarianten te ontdekken.

---

## Response Time

### API Endpoints
- Wat is de acceptable response time voor API calls?
- Welke endpoints zijn kritiek voor user experience?
- Zijn er SLA requirements?

### Page Load
- Wat is de acceptable page load time?
- Zijn er kritieke pages (checkout, dashboard)?

### Background Jobs
- Wat is de maximum runtime voor background jobs?
- Mogen jobs OOIT oneindig lang duren?

**Typische invarianten:**
- `INV-PERF-001`: API responses NEVER exceed 500ms p99
- `INV-PERF-002`: Page load NEVER exceeds 3 seconds
- `INV-PERF-003`: Background jobs NEVER run longer than 5 minutes

---

## Resource Usage

### Memory
- Wat is de maximum memory per request?
- Mogen memory leaks OOIT voorkomen?
- Is er een memory budget per service?

### CPU
- Wat is de maximum CPU time per request?
- Mogen CPU-intensive operations OOIT blocking zijn?

### Connections
- Hoeveel database connections zijn er maximaal?
- Mogen connection pools OOIT uitgeput raken?

**Typische invarianten:**
- `INV-PERF-010`: Memory usage NEVER exceeds 512MB per request
- `INV-PERF-011`: CPU time NEVER exceeds 10 seconds per request
- `INV-PERF-012`: Connection pool is NEVER exhausted

---

## Database Performance

### Query Count
- Hoeveel queries zijn acceptabel per request?
- Mogen N+1 queries OOIT voorkomen?

### Query Duration
- Wat is de maximum query duration?
- Mogen full table scans OOIT voorkomen op grote tabellen?

### Indexes
- Welke queries moeten altijd indexed zijn?
- Mogen index-less queries OOIT op productie draaien?

**Typische invarianten:**
- `INV-PERF-020`: Database queries NEVER exceed 100 per request
- `INV-PERF-021`: Individual query NEVER takes more than 100ms
- `INV-PERF-022`: N+1 queries are NEVER introduced
- `INV-PERF-023`: Full table scans NEVER happen on tables > 10K rows

---

## Concurrency

### Race Conditions
- Welke operaties zijn concurrency-sensitive?
- Mogen race conditions OOIT data corrumperen?

### Deadlocks
- Zijn er multi-resource transactions?
- Mogen deadlocks OOIT voorkomen?

### Locking
- Welke resources vereisen locking?
- Mogen locks OOIT te lang gehouden worden?

**Typische invarianten:**
- `INV-PERF-030`: Race conditions NEVER cause data corruption
- `INV-PERF-031`: Deadlocks NEVER occur in transaction code
- `INV-PERF-032`: Locks are NEVER held longer than 5 seconds

---

## Scalability

### Throughput
- Hoeveel requests per seconde moet het systeem aan?
- Mogen bottlenecks OOIT ontstaan bij piekbelasting?

### Data Volume
- Hoe groot kunnen datasets worden?
- Mogen grote datasets OOIT performance problemen veroorzaken?

**Typische invarianten:**
- `INV-PERF-040`: Throughput NEVER drops below 100 req/s under load
- `INV-PERF-041`: Response time NEVER degrades with data size

---

## Questions to Ask User

```markdown
1. **Response Time**
   - Wat zijn de SLA requirements voor response times?
   - Welke endpoints zijn het meest kritiek?
   - Wat is "te langzaam" voor de gebruiker?

2. **Resource Usage**
   - Hoeveel geheugen mag een request maximaal gebruiken?
   - Zijn er bekende memory-intensive operaties?

3. **Database**
   - Hoeveel queries is acceptabel per request?
   - Zijn er grote tabellen die performance-kritiek zijn?
   - Worden er indexes gebruikt voor alle kritieke queries?

4. **Concurrency**
   - Zijn er operaties waar meerdere users tegelijk aan werken?
   - Zijn er bekende race conditions of deadlock risico's?

5. **Scale**
   - Hoeveel users/requests moet het systeem aankunnen?
   - Hoe groot kunnen datasets groeien?
```

---

## Discovery Commands

```bash
# Find potentially slow operations
rg "sleep|time\.sleep|await.*sleep" --type py
rg "for.*in.*for.*in" --type py  # Nested loops

# Find database queries
rg "\.all\(\)|\.filter\(|select.*from|SELECT.*FROM" --type py

# Find N+1 patterns
rg "for.*in.*:.*\n.*\.get\(|for.*in.*:.*\n.*\.filter\(" --multiline --type py

# Find memory-intensive operations
rg "\.read\(\)|load.*file|pandas|numpy" --type py

# Find concurrency primitives
rg "Lock|Semaphore|asyncio|threading|multiprocessing" --type py

# Find transaction code
rg "transaction|commit|rollback|BEGIN|COMMIT" --type py
```

---

## Measurement Tools

### Python
```python
# Response time
import time
start = time.perf_counter()
# ... operation ...
elapsed = time.perf_counter() - start

# Memory
import tracemalloc
tracemalloc.start()
# ... operation ...
current, peak = tracemalloc.get_traced_memory()

# Query count (Django)
from django.db import connection
query_count = len(connection.queries)
```

### Node.js
```javascript
// Response time
const start = performance.now();
// ... operation ...
const elapsed = performance.now() - start;

// Memory
const used = process.memoryUsage();
```
