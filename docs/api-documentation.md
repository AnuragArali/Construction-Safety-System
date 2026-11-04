# REST API Documentation
## Edge Construction Safety Management System

Base URL: `http://localhost:8000/api`

---

### 1. System Status & Telemetry

#### `GET /api/status`
Returns general system status, edge hardware identification, monitoring state, and privacy audit metrics.

**Response:**
```json
{
  "system_name": "Edge-Enabled Construction Safety Management System",
  "version": "1.0.0",
  "is_edge_device": false,
  "monitoring": {
    "monitoring_active": true,
    "camera_connected": true,
    "source": "0",
    "language": "en",
    "latest_stats": {
      "fps": 15.2,
      "inference_time_ms": 28.4
    }
  },
  "privacy": {
    "status": "COMPLIANT",
    "continuous_video_upload_blocked": true,
    "raw_video_storage_disabled": true,
    "compliance_score": 100
  },
  "supported_languages": ["en", "hi", "kn", "es"],
  "current_language": "en"
}
```

---

### 2. Edge Monitoring Control

#### `POST /api/monitoring/start`
Starts camera ingestion, edge AI pipeline, and safety evaluation.

**Request Body:**
```json
{
  "source": "0",
  "language": "en"
}
```

**Response:**
```json
{
  "status": "started",
  "source": "0",
  "language": "en"
}
```

#### `POST /api/monitoring/stop`
Stops the video processing thread and releases camera hardware.

**Response:**
```json
{
  "status": "stopped"
}
```

#### `GET /api/monitoring/stream`
Returns an `multipart/x-mixed-replace; boundary=frame` MJPEG stream with real-time safety bounding boxes, hazard zones, and facial privacy blurring.

#### `GET /api/monitoring/detections`
Returns raw telemetry from the latest processed frame:
- Worker bounding boxes & PPE detection status
- Active violations
- Inference duration (ms)
- Measured FPS

---

### 3. Safety Alerts & Events

#### `GET /api/alerts/latest?limit=8`
Retrieves recent safety violations dispatched by the alert manager.

#### `GET /api/events`
Query parameters:
- `limit` (default: 50)
- `offset` (default: 0)
- `violation_type` (optional filter)
- `severity` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`)
- `category` (`PPE`, `ZONE_BOUNDARY`)

#### `GET /api/events/statistics`
Returns aggregated analytics:
- `total_events`
- `today_violations`
- `compliance_rate`
- `by_type` (violation counts)
- `by_severity` (severity counts)
- `daily_trends` (7-day daily count array)

---

### 4. Safety Rules & Guidelines

#### `GET /api/rules`
Returns registered safety rules.

#### `POST /api/rules/toggle`
**Request Body:**
```json
{
  "rule_code": "RULE_HELMET",
  "is_enabled": true
}
```

#### `GET /api/recommendations?language=en`
Returns OSHA/ANSI PPE specifications and native-language corrective recommendations (`en`, `hi`, `kn`, `es`).

---

### 5. Privacy & Administration

#### `GET /api/privacy/compliance`
Returns comprehensive edge privacy audit verification.

#### `POST /api/privacy/purge?days=14`
Manually triggers privacy retention purge for records older than the specified days.

#### `GET /api/settings` and `POST /api/settings`
Updates voice alert configuration, language, target FPS, and cooldown timers.
