# Sales Flask API behind local Nginx Docker

This setup runs two local Docker containers:

1. `flask-api` - runs the Flask API using Gunicorn on internal port 8000.
2. `nginx` - runs Nginx on host port 8080, serves markdown files directly, and reverse-proxies API calls to Flask.

## Run

```bash
docker compose up --build
```

Run in background:

```bash
docker compose up --build -d
```

Stop:

```bash
docker compose down
```

## Test URLs

```text
http://localhost:8080/
http://localhost:8080/sales
http://localhost:8080/sales-table
http://localhost:8080/dashboard
http://localhost:8080/context.md
http://localhost:8080/guard_rails.md
http://localhost:8080/skills.md
http://localhost:8080/available_api.md
http://localhost:8080/api_documentation.md
http://localhost:8080/ai-plugin-context
http://localhost:8080/available_data
```

`/available_data` exists but is intentionally prohibited for AI assistant usage.
