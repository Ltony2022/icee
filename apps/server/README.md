# Icee Utils Backend API

Django backend serving the Icee Utils application. All endpoints return JSON unless noted otherwise.

**Base URL:** `http://127.0.0.1:8765`

---

## DNS Proxy

Manage the DNS proxy that intercepts DNS queries to block domains and log traffic.

### Proxy Control

#### `GET /api/dns-proxy/status/`

Check if the DNS proxy subprocess is running.

**Response:**

```json
{ "running": true, "pid": 12345 }
```

#### `POST /api/dns-proxy/start/`

Start the DNS proxy subprocess. Requires admin privileges (modifies system DNS).

**Request body (all fields optional):**

```json
{
  "listen_host": "127.0.0.1",
  "listen_port": 5353,
  "upstream_host": "1.1.1.1",
  "upstream_port": 53,
  "timeout": 2.0,
  "log_level": "INFO"
}
```

**Response:**

```json
{
  "status": "started",
  "pid": 12345,
  "config": {
    "listen_host": "127.0.0.1",
    "listen_port": 5353,
    "upstream_host": "1.1.1.1",
    "upstream_port": 53,
    "timeout": 2.0,
    "log_level": "INFO"
  }
}
```

**Error (409):** `{ "error": "proxy is already running", "pid": 12345 }`

#### `POST /api/dns-proxy/stop/`

Stop the running DNS proxy subprocess. This restores original DNS settings.

**Response:**

```json
{ "status": "stopped", "pid": 12345 }
```

**Error (409):** `{ "error": "proxy is not running" }`

---

### Blocked Domains

#### `GET /api/dns-proxy/blocked-domains/`

List all currently blocked domains.

**Response:**

```json
{ "blocked_domains": ["doubleclick.net", "facebook.com"] }
```

#### `POST /api/dns-proxy/blocked-domains/add/`

Add a domain to the block list. Subdomains are automatically blocked.

**Request body:**

```json
{ "domain": "example.com" }
```

**Response:**

```json
{
  "status": "success",
  "blocked_domains": ["doubleclick.net", "example.com", "facebook.com"]
}
```

**Error (400):** `{ "error": "domain is required" }`
**Error (409):** `{ "error": "domain already blocked", "blocked_domains": [...] }`

#### `DELETE /api/dns-proxy/blocked-domains/remove/`

Remove a domain from the block list.

**Request body:**

```json
{ "domain": "facebook.com" }
```

**Response:**

```json
{ "status": "success", "blocked_domains": ["doubleclick.net"] }
```

**Error (404):** `{ "error": "domain not found", "blocked_domains": [...] }`

---

### DNS Logs

#### `GET /api/dns-proxy/logs/`

Return recent DNS proxy log entries.

**Query params:**
| Param | Type | Default | Description |
|---------|------|---------|------------------------------------|
| `lines` | int | 100 | Number of recent lines (max 1000) |

**Example:** `GET /api/dns-proxy/logs/?lines=50`

**Response:**

```json
{
  "logs": [
    "2025-01-01 12:00:00 INFO IN 127.0.0.1:5353 -> example.com (A)",
    "..."
  ],
  "total_lines": 542,
  "returned_lines": 50
}
```

#### `DELETE /api/dns-proxy/logs/clear/`

Clear all DNS proxy log entries.

**Response:**

```json
{ "status": "cleared" }
```

---

## Flashcards

Spaced repetition flashcard system using the SM-2 algorithm.

### Sets

#### `GET /flashcards/set`

List all flashcard sets with card counts.

**Response:**

```json
[
  {
    "set_id": 1,
    "set_name": "Japanese N5",
    "nearest_practice": "2025-01-15",
    "totalCards": 50,
    "reviewCards": 12
  }
]
```

#### `GET /flashcards/set/<set_id>/info`

Get metadata for a single set.

#### `POST /flashcards/set/new`

Create a new flashcard set.

**Request body:**

```json
{ "set_name": "Japanese N5" }
```

#### `PUT /flashcards/set/update`

Update a set's name or nearest practice date.

**Request body:**

```json
{ "set_id": 1, "set_name": "Updated Name" }
```

#### `DELETE /flashcards/set/delete`

Delete a set and all its flashcards.

**Request body:**

```json
{ "set_id": 1 }
```

---

### Flashcard CRUD

#### `GET /flashcards/set/<set_id>/`

Get all flashcards in a set.

**Response:**

```json
[
  {
    "flashcard_id": 1,
    "question": "What is ...",
    "answer": "It is ...",
    "nextPractice": "2025-01-15"
  }
]
```

#### `POST /flashcards/set/<set_id>/create`

Add a new flashcard (initialized with SM-2 defaults: EFactor=2.5, interval=1, repetition=1).

**Request body:**

```json
{ "question": "What is ...", "answer": "It is ..." }
```

#### `PUT /flashcards/set/<set_id>/update`

Update a flashcard's question and answer.

**Request body:**

```json
{ "flashcard_id": 1, "question": "Updated Q", "answer": "Updated A" }
```

#### `DELETE /flashcards/set/<set_id>/delete`

Delete a flashcard.

**Request body:**

```json
{ "flashcard_id": 1 }
```

---

### Spaced Repetition

#### `GET /flashcards/set/<set_id>/getPracticeFlashcard`

Get flashcards due for practice (nextPractice <= now or never practiced).

#### `PUT /flashcards/set/<set_id>/updateUserFlashcard`

Submit a practice grade and update the card using the SM-2 algorithm.

**Request body:**

```json
{ "flashcard_id": 1, "user_grade": 4 }
```

`user_grade` ranges from 0-5: grades 0-2 reset the card, grades 3-5 advance the interval.

#### `PUT /flashcards/set/<set_id>/updateDate`

Manually set a flashcard's next practice date.

**Request body:**

```json
{ "flashcard_id": 1, "nextPractice": "2025-02-01" }
```

---

## Pomodoro

#### `GET /api/pomodoro/`

Get pomodoro timer configuration (stub - returns placeholder).

---

## Blocker (Legacy)

> These endpoints are stubs from an earlier hosts-file-based blocking approach. The DNS Proxy endpoints above are the replacement.

#### `GET /api/blockingList/`

Placeholder endpoint.

#### `GET /api/blocksite/`

Placeholder endpoint.
