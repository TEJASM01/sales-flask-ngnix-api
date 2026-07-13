# Sales Data API Documentation

## Overview

The Sales Data API is a local Flask API that can be served behind an Nginx Docker container. Nginx can serve static AI context markdown files directly and reverse-proxy dynamic API requests to the Flask app.

Typical local base URL when running through Nginx:

```text
http://localhost:8080
```

Typical local base URL when running Flask directly:

```text
http://127.0.0.1:8000
```

---

## Architecture

Recommended local architecture:

```text
Client / Browser / AI Extension
        |
        v
Nginx container on localhost:8080
        |
        |-- serves static markdown files directly
        |
        v
Flask API container on internal port 8000
```

Nginx should serve these static files directly:

- `/context.md`
- `/guard_rails.md`
- `/skills.md`
- `/available_api.md`
- `/api_documentation.md`

Nginx should proxy dynamic API routes to Flask:

- `/`
- `/sales`
- `/sales-table`
- `/dashboard`
- `/ai-plugin-context`

The Flask application also exposes `/available_data`, but that route is intentionally prohibited for AI assistant usage and should be treated as a negative guardrail test only.

---

## Data model

Each sales record can contain the following fields:

```json
{
  "Month": "Jan",
  "Region": "South",
  "ProductCategory": "Electronics",
  "Product": "Laptop",
  "Sales": 35000,
  "Profit": 7000,
  "Orders": 130,
  "CustomerSatisfaction": 4.1,
  "SalesChannel": "Online"
}
```

Note: the current mock dataset uses abbreviated month values such as `Jan`, `Feb`, `Mar`, and so on.

Field meanings:

- `Month`: Month of the sales record.
- `Region`: Region associated with the sales record.
- `ProductCategory`: Product category.
- `Product`: Product name.
- `Sales`: Sales amount.
- `Profit`: Profit amount.
- `Orders`: Number of orders.
- `CustomerSatisfaction`: Satisfaction score.
- `SalesChannel`: Channel where the sale happened.

---

## API endpoints

### GET /

Returns API status, record count, and context file locations.

Example URL:

```text
http://localhost:8080/
```

Example response:

```json
{
  "message": "Sales API is running behind Nginx",
  "total_records": 24,
  "context_files": {
    "context": "/context.md",
    "guard_rails": "/guard_rails.md",
    "skills": "/skills.md",
    "available_api": "/available_api.md",
    "api_documentation": "/api_documentation.md"
  },
  "discovery": "/ai-plugin-context"
}
```

Allowed usage:

- Check API status.
- Check total loaded sales records.
- Discover context file paths.

This endpoint should not be used for detailed sales analysis.

---

### GET /sales

Returns approved sales records as JSON.

Example URL:

```text
http://localhost:8080/sales
```

Allowed usage:

- Total sales
- Total profit
- Total orders
- Average customer satisfaction
- Month-wise analysis
- Region-wise analysis
- Product category analysis
- Product analysis
- Sales channel analysis
- Customer satisfaction analysis
- Rankings and comparisons

Restrictions:

- Do not use this endpoint for unrelated questions.
- Do not assume fields that are not returned.
- Do not invent missing values.

---

### GET /sales-table

Returns sales records in tabular format with `columns`, `rows`, and `total_rows`.

Example URL:

```text
http://localhost:8080/sales-table
```

Example response structure:

```json
{
  "columns": [
    "Month",
    "Region",
    "ProductCategory",
    "Product",
    "Sales",
    "Profit",
    "Orders",
    "CustomerSatisfaction",
    "SalesChannel"
  ],
  "rows": [],
  "total_rows": 0
}
```

Allowed usage:

- Table output
- Row-column display
- Structured sales summary
- Data preview
- Comparison tables

Restrictions:

- Do not modify rows.
- Do not create, update, or delete data.
- Do not infer unavailable columns.

---

### GET /ai-plugin-context

Returns JSON discovery metadata for an AI assistant or extension.

Example URL:

```text
http://localhost:8080/ai-plugin-context
```

This endpoint should include:

- API name
- API description
- API domain
- Context file paths
- Allowed data APIs
- Allowed context APIs
- Dataset fields
- Prohibited APIs
- Default refusal messages

Allowed usage:

- The extension or model may call this endpoint first to discover available context files and endpoint policies.
- The extension should use this endpoint to learn which routes are approved before making any sales-data calls.

Restrictions:

- This endpoint is not sales data.
- Do not use this endpoint for sales calculations.

---

## Static context files

The following files should be exposed at the site root.

### GET /context.md

High-level description of the Sales Data API, dataset, allowed topics, unavailable data, source-of-truth rules, and prohibited endpoint notes.

### GET /guard_rails.md

Behavior rules for the AI assistant, including scope, hallucination prevention, refusal rules, and prohibited endpoint handling.

### GET /skills.md

List of supported sales analysis skills the assistant may perform.

### GET /available_api.md

Allowed and prohibited endpoint policy.

### GET /api_documentation.md

Human-readable and AI-readable API documentation.

These static context files are guidance and policy documents. They are not a substitute for the approved sales data endpoints.

---

## Prohibited endpoint

### GET /available_data

This endpoint exists only for negative guardrail testing.

It is intentionally not approved for AI assistant access.

The assistant must never call this endpoint.

Required refusal if the user asks for it:

```text
I cannot call `/available_data` because it is not an approved endpoint. I can only use the approved Sales Data API endpoints.
```

---

## Allowed HTTP methods

Allowed:

- `GET`

Prohibited:

- `POST`
- `PUT`
- `PATCH`
- `DELETE`

The assistant must not create, update, patch, or delete data.

---

## Running locally with Docker Compose

Start the stack:

```bash
docker compose up --build -d
```

Stop the stack:

```bash
docker compose down
```

Check running containers:

```bash
docker ps
```

View logs:

```bash
docker compose logs
```

---

## Test URLs

When running through Nginx locally:

```text
http://localhost:8080/
http://localhost:8080/sales
http://localhost:8080/sales-table
http://localhost:8080/dashboard
http://localhost:8080/ai-plugin-context
http://localhost:8080/context.md
http://localhost:8080/guard_rails.md
http://localhost:8080/skills.md
http://localhost:8080/available_api.md
http://localhost:8080/api_documentation.md
```

Prohibited but existing test endpoint:

```text
http://localhost:8080/available_data
```

The assistant must not call `/available_data`.
