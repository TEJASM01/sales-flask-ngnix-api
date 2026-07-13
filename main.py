from flask import Flask, jsonify, Response, abort, render_template
from pathlib import Path
import json

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "mock_sales_data.json", "r", encoding="utf-8") as f:
    sales_data = json.load(f)


def build_dashboard_context() -> dict:
    total_sales = sum(item["Sales"] for item in sales_data)
    total_profit = sum(item["Profit"] for item in sales_data)
    total_orders = sum(item["Orders"] for item in sales_data)
    avg_satisfaction = round(sum(item["CustomerSatisfaction"] for item in sales_data) / len(sales_data), 2)
    profit_margin_pct = round((total_profit / total_sales) * 100, 2) if total_sales else 0

    sales_by_region = {}
    sales_by_channel = {}
    category_counts = {}

    for item in sales_data:
        region = item["Region"]
        channel = item["SalesChannel"]
        category = item["ProductCategory"]

        sales_by_region[region] = sales_by_region.get(region, 0) + item["Sales"]
        sales_by_channel[channel] = sales_by_channel.get(channel, 0) + item["Sales"]
        category_counts[category] = category_counts.get(category, 0) + 1

    top_product = max(sales_data, key=lambda item: item["Sales"])
    top_region, top_region_sales = max(sales_by_region.items(), key=lambda pair: pair[1])
    top_channel, top_channel_sales = max(sales_by_channel.items(), key=lambda pair: pair[1])
    avg_order_value = round(total_sales / total_orders, 2) if total_orders else 0

    return {
        "kpis": {
            "total_sales": total_sales,
            "total_profit": total_profit,
            "total_orders": total_orders,
            "avg_satisfaction": avg_satisfaction,
            "profit_margin_pct": profit_margin_pct,
        },
        "top_product": top_product,
        "record_count": len(sales_data),
        "avg_order_value": avg_order_value,
        "top_region": {
            "name": top_region,
            "sales": top_region_sales,
        },
        "top_channel": {
            "name": top_channel,
            "sales": top_channel_sales,
        },
        "category_coverage": len(category_counts),
        "channel_chart": {
            "labels": list(sales_by_channel.keys()),
            "values": list(sales_by_channel.values()),
        },
        "region_summary": [
            {"region": region, "sales": sales}
            for region, sales in sorted(sales_by_region.items(), key=lambda pair: pair[1], reverse=True)
        ],
    }


def read_markdown_file(file_name: str) -> str:
    file_path = BASE_DIR / file_name
    if not file_path.exists():
        abort(404, description=f"{file_name} not found at {file_path}")
    content = file_path.read_text(encoding="utf-8")
    if not content.strip():
        abort(500, description=f"{file_name} exists but is empty")
    return content


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Sales API is running behind Nginx",
        "total_records": len(sales_data),
        "dashboard": "/dashboard",
        "context_files": {
            "context": "/context.md",
            "api_documentation": "/api_documentation.md",
            "guard_rails": "/guard_rails.md",
            "skills": "/skills.md",
            "available_api": "/available_api.md"
        },
        "discovery": "/ai-plugin-context"
    })


@app.route("/sales", methods=["GET"])
def get_sales():
    return jsonify(sales_data)


@app.route("/sales-table", methods=["GET"])
def get_sales_table():
    return jsonify({
        "columns": [
            "Month", "Region", "ProductCategory", "Product", "Sales",
            "Profit", "Orders", "CustomerSatisfaction", "SalesChannel"
        ],
        "rows": sales_data,
        "total_rows": len(sales_data)
    })


@app.route("/dashboard", methods=["GET"])
def dashboard():
    dashboard_data = build_dashboard_context()
    return render_template("dashboard.html", dashboard_data=dashboard_data)


# These routes still exist in Flask, but Nginx serves the md files directly first.
@app.route("/guard_rails.md", methods=["GET"])
def get_guard_rails():
    return Response(read_markdown_file("guard_rails.md"), mimetype="text/plain; charset=utf-8")


@app.route("/skills.md", methods=["GET"])
def get_skills():
    return Response(read_markdown_file("skills.md"), mimetype="text/plain; charset=utf-8")


@app.route("/available_api.md", methods=["GET"])
def get_available_api():
    return Response(read_markdown_file("available_api.md"), mimetype="text/plain; charset=utf-8")


@app.route("/ai-plugin-context", methods=["GET"])
def get_ai_plugin_context():
    return jsonify({
        "name": "Sales Data API",
        "description": "AI context discovery document for a sales-data-only assistant.",
        "version": "1.0.0",
        "domain": "sales_data_analysis",
        "primary_rule": "Answer only questions related to sales data available from this API.",
        "source_of_truth": "Use only approved Sales Data API endpoints. Do not use external data.",
        "hallucination_policy": "Do not invent records, fields, values, trends, causes, or explanations.",
        "out_of_scope_policy": "Refuse questions that are not related to the Sales Data API.",
        "prohibited_endpoint_policy": "Do not call prohibited or unlisted endpoints, even if they exist.",
        "context_files": {
            "context": "/context.md",
            "api_documentation": "/api_documentation.md",
            "guard_rails": "/guard_rails.md",
            "skills": "/skills.md",
            "available_api": "/available_api.md"
        },
        "allowed_data_apis": {
            "home": {"method": "GET", "path": "/", "purpose": "Check API status and record count"},
            "sales": {"method": "GET", "path": "/sales", "purpose": "Retrieve approved sales records for analysis"},
            "sales_table": {"method": "GET", "path": "/sales-table", "purpose": "Retrieve approved sales records in table format"}
        },
        "allowed_context_apis": {
            "guard_rails": {"method": "GET", "path": "/guard_rails.md", "purpose": "Retrieve site guard rails"},
            "skills": {"method": "GET", "path": "/skills.md", "purpose": "Retrieve allowed assistant skills"},
            "available_api": {"method": "GET", "path": "/available_api.md", "purpose": "Retrieve API usage policy"},
            "context": {"method": "GET", "path": "/context.md", "purpose": "Retrieve AI context information"},
            "api_documentation": {"method": "GET", "path": "/api_documentation.md", "purpose": "Retrieve API documentation"}
        },
        "allowed_fields": [
            "Month", "Region", "ProductCategory", "Product", "Sales",
            "Profit", "Orders", "CustomerSatisfaction", "SalesChannel"
        ],
        "prohibited_apis": [
            {"method": "GET", "path": "/available_data", "reason": "This endpoint exists but is intentionally not approved for AI assistant access."}
        ],
        "allowed_http_methods": ["GET"],
        "prohibited_http_methods": ["POST", "PUT", "PATCH", "DELETE"],
        "default_refusal_message": "I can only help with sales-data questions supported by this API. Please ask about sales, profit, orders, regions, products, customer satisfaction, or sales channels.",
        "endpoint_refusal_message": "I cannot call that endpoint because it is not approved. I can only use the approved Sales Data API endpoints.",
        "insufficient_data_message": "The available sales data does not contain enough information to answer that."
    })


@app.route("/available_data", methods=["GET"])
def get_available_data():
    return jsonify({
        "message": "This endpoint exists but is not approved for AI assistant access.",
        "warning": "AI assistants should not call this endpoint.",
        "data": sales_data
    })


@app.route("/context.md", methods=["GET"])
def get_context():
    content = read_markdown_file("context.md")
    return Response(content, mimetype="text/plain; charset=utf-8")


@app.route("/api_documentation.md", methods=["GET"])
def get_api_documentation():
    content = read_markdown_file("api_documentation.md")
    return Response(content, mimetype="text/plain; charset=utf-8")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
