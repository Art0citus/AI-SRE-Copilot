# AI SRE Copilot

An observability and incident-monitoring project built with **FastAPI, Prometheus, and Docker Compose**. It collects application metrics, tracks HTTP request latency, and detects elevated server-error rates using Prometheus alerting rules.

> **Current status:** V1 — Application Monitoring & Alerting. AI-powered root-cause analysis and automated incident response are planned enhancements.

## Features

- **Health Checks:** Endpoint to verify application availability.
- **Structured Request Logging:** Logs HTTP methods, paths, response status codes, and request durations.
- **Prometheus Metrics:** Tracks HTTP request counts and latency distributions.
- **Error Simulation:** Dedicated endpoint for testing HTTP 500 responses.
- **Latency Testing:** Slow endpoint for experimenting with request-duration monitoring.
- **Alert Rules:** Detects sustained HTTP 5xx error rates.
- **Docker Compose:** Runs Prometheus locally and scrapes application metrics.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Prometheus
- Prometheus Client
- Docker Compose
- Pytest

## Architecture

```text
                  ┌─────────────────────┐
                  │   Client / Tester   │
                  └──────────┬──────────┘
                             │ HTTP
                             ▼
                  ┌─────────────────────┐
                  │   FastAPI App       │
                  │                     │
                  │ Health Checks       │
                  │ Request Logging     │
                  │ Error Simulation    │
                  │ Metrics Endpoint    │
                  └──────────┬──────────┘
                             │ /metrics
                             ▼
                  ┌─────────────────────┐
                  │     Prometheus      │
                  │ Metrics Collection  │
                  │ PromQL Queries      │
                  │ Alert Rule Evaluation│
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ HighServerErrorRate │
                  │ Alert State         │
                  └─────────────────────┘
```

## Project Structure

```text
ai-sre-copilot/
├── app/
│   ├── main.py
│   └── logging_config.py
├── tests/
│   └── test_main.py
├── alerts.yml
├── prometheus.yml
├── docker-compose.yml
├── requirements.txt
├── .env
└── .gitignore
```

The exact files may vary as the project evolves. Do not commit secrets from `.env`.

## Getting Started

### Prerequisites

Install the following:

- Python 3.11 or newer
- Docker Desktop with Docker Compose
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-sre-copilot.git
cd ai-sre-copilot
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the FastAPI application

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`.

Keep this terminal running.

### 5. Start Prometheus

Open a second terminal in the project root and run:

```bash
docker compose up -d
```

Prometheus should be available at `http://localhost:9090`.

The configuration scrapes the FastAPI metrics endpoint at:

```text
http://host.docker.internal:8000/metrics
```

This target is configured for a local Docker Desktop setup on Windows.

## Application Endpoints

| Endpoint | Description |
|---|---|
| `GET /health` | Application health check |
| `GET /metrics` | Prometheus metrics |
| `GET /slow` | Simulates a slow request |
| `GET /error` | Generates an HTTP 500 response |
| `GET /docs` | Interactive API documentation |

## Prometheus Metrics

### HTTP Request Counter

```promql
http_requests_total
```

Tracks HTTP requests by method, endpoint, and status code.

### HTTP Request Duration

```promql
http_request_duration_seconds
```

A histogram of request durations in seconds.

### Server Error Rate

```promql
sum(rate(http_requests_total{status=~"5.."}[1m]))
```

Calculates the rate of HTTP 5xx responses over a one-minute window.

## Alerting

The project includes a Prometheus alert named `HighServerErrorRate`.

Its expression is:

```promql
sum(rate(http_requests_total{status=~"5.."}[1m])) > 0.1
```

The rule uses a `30s` pending duration before firing and labels the alert with `severity="critical"`.

To inspect the rule and its state, visit:

- [Prometheus Alerts](http://localhost:9090/alerts)
- [Prometheus Rules](http://localhost:9090/rules)
- [Prometheus Targets](http://localhost:9090/targets)

### Test the alert

With FastAPI and Prometheus running, open a separate PowerShell terminal:

```powershell
1..30 | ForEach-Object {
    try {
        Invoke-WebRequest "http://localhost:8000/error"
    } catch {
        Write-Host "HTTP error generated"
    }
}
```

Then inspect the server-error-rate query in Prometheus Graph. The alert fires when the expression remains true for the configured pending duration. A short burst alone may not be sufficient.

## Run Tests

Activate the virtual environment, then execute:

```bash
python -m pytest
```

## Roadmap

- [x] FastAPI health and diagnostic endpoints
- [x] Request logging and latency instrumentation
- [x] Prometheus metrics collection
- [x] Prometheus alert-rule evaluation
- [ ] Alertmanager notification integration
- [ ] AI-assisted incident analysis
- [ ] Log and metric correlation
- [ ] Incident dashboard
- [ ] Root-cause analysis using an LLM
- [ ] CI/CD pipeline and deployment automation

## Learning Objectives

This project explores practical Site Reliability Engineering concepts:

- Application observability
- Metrics instrumentation
- Time-series monitoring
- PromQL queries
- Alert thresholds and pending durations
- Containerized monitoring infrastructure
- Incident simulation and debugging

## Contributing

Contributions, suggestions, and improvements are welcome. Feel free to open an issue or submit a pull request.

## License

This project is currently unlicensed unless a license file is added. Consider adding an MIT License if you want others to reuse and modify the code under those terms.
