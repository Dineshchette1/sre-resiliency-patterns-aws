# Part 1: Understanding and Documenting Resiliency Patterns

## Section 1: Resiliency Patterns

### 1. Circuit Breaker Pattern

**What problem it solves:** Stops us from repeatedly calling a service that is failing, which could crash the whole system or use up too many resources.

**How it works:** It watches for failed requests. If enough of them fail (for example 3 out of 5), the breaker "opens" and stops more requests from going through. After a short wait, it allows a few test calls in a "half-open" state. If those succeed, it "closes" again.

**Things to consider:**
- How many failures should trigger it (for example a 50% failure rate)
- How long to wait before trying again
- Logging and monitoring each state (open, half-open, closed)

**When to use it:**
- Calling unstable external services
- Services with high failure rates or API limits

**When not to use it:**
- When errors are rare or retrying is enough

**Real-world use:** Netflix uses it to stop one slow service from taking down everything else.

### 2. Retry with Exponential Backoff

**What problem it solves:** Handles temporary errors like timeouts by retrying requests with increasing delays.

**How it works:** If a request fails, we wait a bit and try again. Each retry waits longer (1s, then 2s, then 4s), often with some randomness (jitter) added so many clients don't retry at the same time.

**Things to consider:**
- How many times to retry
- The delay pattern (backoff)
- Adding jitter to reduce traffic spikes
- Combining it with timeouts and circuit breakers

**When to use it:**
- Services that usually recover quickly
- APIs with temporary rate limits

**When not to use it:**
- Permanent errors like wrong credentials

**Real-world use:** AWS SDKs use this to handle network glitches and throttling.

### 3. Fallback Pattern

**What problem it solves:** Keeps the app working by giving an alternate response when the real service fails.

**How it works:** If the main service fails (like fetching reviews), we show cached or default content instead, so users don't see a blank screen.

**Things to consider:**
- Make sure the fallback data is still useful
- Handle stale cache data
- Design fallback content that makes sense (not just "try again later")

**When to use it:**
- Less critical features like recommendations or reviews

**When not to use it:**
- Sensitive operations like payments or banking

**Real-world use:** Travel websites show cached flight prices when live data is down.

### 4. Cache-aside Pattern

**What problem it solves:** Reduces repeated database calls, improves performance, and keeps things running if the database is slow or down.

**How it works:** We check the cache first. If the data isn't there, we read it from the database and save it in the cache for next time.

**Things to consider:**
- When to refresh or remove old data (TTL)
- Which eviction method to use (LRU, LFU)
- What to do when data is missing or outdated

**When to use it:**
- Data that is read often and rarely changes

**When not to use it:**
- When we always need the most up-to-date data

**Real-world use:** Amazon caches product pages to reduce load and speed up responses.

## Section 2: Failure Mode Analysis

### 1. Infrastructure Failures
- **Causes:** Server crashes, disk issues, or a whole availability zone going down
- **Warning signs:** Spikes in 5xx errors, CloudWatch alarms, EC2 instance unreachable
- **Impact:** Services stop working, possible downtime and data loss
- **What helps:** Auto Scaling, backups, multiple availability zones, load balancers

### 2. Network Failures
- **Causes:** Internet or DNS issues, high latency, dropped packets
- **Warning signs:** Timeouts, failed health checks, slow responses
- **Impact:** Broken user sessions, services can't talk to each other
- **What helps:** Retry with backoff, circuit breakers, load balancer failover, proper timeouts

### 3. Dependency Failures
- **Causes:** Third-party APIs failing, hitting rate limits, DNS failures
- **Warning signs:** HTTP 429 or 503 errors, long delays, slower app performance
- **Impact:** Errors shown to users, chained failures across services
- **What helps:** Circuit breaker, fallback, caching, and the bulkhead pattern to isolate problems

## Section 3: Resiliency Strategy for an E-Commerce Application

| Tier | Patterns | Why |
|---|---|---|
| **Web tier** (frontend and API gateway) | Retry with backoff for API calls, cache-aside for product images and descriptions | Keeps pages responsive even if the backend is slow |
| **Application tier** (cart, orders, users microservices) | Circuit breaker to stop calling failing services, bulkhead to isolate each service (if cart breaks, login still works) | Stops one service from taking everything else down |
| **Database tier** | Cache-aside for popular data like products, fallback to slightly older data if the DB is slow or down | Reduces pressure on the database and avoids delays |
| **External payment processor** (Stripe, PayPal) | Circuit breaker to stop flooding a failing payment API, retry with backoff for temporary errors, fallback to queue the payment and retry later | Payments are critical, and this reduces cart abandonment |
