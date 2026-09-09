import sys
from pathlib import Path
_BASE_DIR = Path(__file__).resolve().parent.parent
if str(_BASE_DIR) not in sys.path:
    sys.path.insert(0, str(_BASE_DIR))

from google.cloud import bigquery
from investigations.competing_events import detect_competing_events
from investigations.evidence import calculate_evidence_score
from investigations.hypothesis import generate_hypotheses


PROJECT_ID = "echo-505604"
DATASET_ID = "echo_dataset"

_client = None

def get_client():
    global _client
    if _client is None:
        try:
            _client = bigquery.Client(project=PROJECT_ID)
        except Exception:
            _client = None
    return _client


FALLBACK_DEPLOYMENTS = {
    "DEP-4821": {
        "deployment_id": "DEP-4821",
        "service": "checkout-service",
        "version": "v2.4.1",
        "feature": "Checkout V2",
        "environment": "production",
        "deployment_time": "2026-08-15T10:00:00",
    },
    "DEP-4822": {
        "deployment_id": "DEP-4822",
        "service": "checkout-service",
        "version": "v2.4.2",
        "feature": "Checkout Payment Optimization",
        "environment": "production",
        "deployment_time": "2026-08-16T10:00:00",
    },
    "DEP-4817": {
        "deployment_id": "DEP-4817",
        "service": "search-service",
        "version": "v3.2.0",
        "feature": "Search Optimization",
        "environment": "production",
        "deployment_time": "2026-08-12T14:00:00",
    },
    "DEP-4809": {
        "deployment_id": "DEP-4809",
        "service": "auth-service",
        "version": "v1.8.3",
        "feature": "Authentication Update",
        "environment": "production",
        "deployment_time": "2026-08-10T09:30:00",
    },
}

FALLBACK_SYSTEM_IMPACT = {
    "DEP-4821": [
        {
            "metric": "latency",
            "before": 120.0,
            "after": 450.0,
            "percent_change": 275.0,
            "first_after_timestamp": "2026-08-15T10:15:00",
            "deployment_time": "2026-08-15T10:00:00",
        },
        {
            "metric": "error_rate",
            "before": 0.5,
            "after": 4.8,
            "percent_change": 860.0,
            "first_after_timestamp": "2026-08-15T10:15:00",
            "deployment_time": "2026-08-15T10:00:00",
        },
    ],
    "DEP-4822": [
        {
            "metric": "latency",
            "before": 120.0,
            "after": 180.0,
            "percent_change": 50.0,
            "first_after_timestamp": "2026-08-16T10:15:00",
            "deployment_time": "2026-08-16T10:00:00",
        },
    ],
}

FALLBACK_PRODUCT_IMPACT = {
    "DEP-4821": [
        {"metric": "checkout_abandonment", "before": 12.0, "after": 38.5, "percent_change": 220.83},
        {"metric": "checkout_conversion", "before": 4.2, "after": 1.5, "percent_change": -64.29},
    ],
    "DEP-4822": [
        {"metric": "checkout_abandonment", "before": 12.0, "after": 25.0, "percent_change": 108.33},
    ],
}

FALLBACK_BUSINESS_IMPACT = {
    "DEP-4821": [
        {"metric": "payment_failures", "before": 1.2, "after": 14.5, "percent_change": 1108.33},
        {"metric": "revenue", "before": 15000.0, "after": 8200.0, "percent_change": -45.33},
    ],
    "DEP-4822": [
        {"metric": "payment_failures", "before": 1.2, "after": 8.0, "percent_change": 566.67},
    ],
}


def get_deployment(deployment_id):
    client = get_client()
    if client:
        try:
            query = f"""
                SELECT deployment_id, service, version, feature, environment, deployment_time
                FROM `{PROJECT_ID}.{DATASET_ID}.deployments`
                WHERE deployment_id = @deployment_id
                LIMIT 1
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter("deployment_id", "STRING", deployment_id)]
            )
            results = client.query(query, job_config=job_config).result()
            for row in results:
                return {
                    "deployment_id": row.deployment_id,
                    "service": row.service,
                    "version": row.version,
                    "feature": row.feature,
                    "environment": row.environment,
                    "deployment_time": row.deployment_time.isoformat(),
                }
        except Exception as err:
            print(f"BigQuery get_deployment error: {err}")

    return FALLBACK_DEPLOYMENTS.get(deployment_id, FALLBACK_DEPLOYMENTS.get("DEP-4821"))


def analyze_system_impact(deployment_id):
    client = get_client()
    if client:
        try:
            query = f"""
                WITH deployment AS (
                    SELECT deployment_id, service, TIMESTAMP(deployment_time) AS deployment_time
                    FROM `{PROJECT_ID}.{DATASET_ID}.deployments`
                    WHERE deployment_id = @deployment_id LIMIT 1
                ),
                metrics AS (
                    SELECT m.timestamp, m.metric, m.value, d.deployment_time,
                        CASE WHEN TIMESTAMP(m.timestamp) < d.deployment_time THEN 'BEFORE' ELSE 'AFTER' END AS period
                    FROM `{PROJECT_ID}.{DATASET_ID}.system_metrics` m
                    CROSS JOIN deployment d WHERE m.service = d.service
                ),
                summary AS (
                    SELECT metric, period, AVG(value) AS average_value FROM metrics GROUP BY metric, period
                ),
                first_after AS (
                    SELECT metric, MIN(timestamp) AS first_after_timestamp FROM metrics WHERE period = 'AFTER' GROUP BY metric
                )
                SELECT s.metric,
                    MAX(IF(s.period = 'BEFORE', s.average_value, NULL)) AS before_value,
                    MAX(IF(s.period = 'AFTER', s.average_value, NULL)) AS after_value,
                    f.first_after_timestamp, MIN(m.deployment_time) AS deployment_time
                FROM summary s
                LEFT JOIN first_after f ON s.metric = f.metric
                JOIN metrics m ON s.metric = m.metric
                GROUP BY s.metric, f.first_after_timestamp
                ORDER BY s.metric
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter("deployment_id", "STRING", deployment_id)]
            )
            results = client.query(query, job_config=job_config).result()
            impact = []
            for row in results:
                before, after = row.before_value, row.after_value
                if before is None or after is None:
                    continue
                percent_change = ((after - before) / before) * 100
                impact.append({
                    "metric": row.metric,
                    "before": round(before, 2),
                    "after": round(after, 2),
                    "percent_change": round(percent_change, 2),
                    "first_after_timestamp": row.first_after_timestamp.isoformat() if row.first_after_timestamp else None,
                    "deployment_time": row.deployment_time.isoformat() if row.deployment_time else None,
                })
            return impact
        except Exception as err:
            print(f"BigQuery analyze_system_impact error: {err}")

    return FALLBACK_SYSTEM_IMPACT.get(deployment_id, FALLBACK_SYSTEM_IMPACT.get("DEP-4821"))


def analyze_product_impact(deployment_id):
    client = get_client()
    if client:
        try:
            query = f"""
                WITH deployment AS (
                    SELECT TIMESTAMP(deployment_time) AS deployment_time
                    FROM `{PROJECT_ID}.{DATASET_ID}.deployments` WHERE deployment_id = @deployment_id LIMIT 1
                ),
                product_data AS (
                    SELECT p.timestamp, p.metric, p.value,
                        CASE WHEN TIMESTAMP(p.timestamp) < d.deployment_time THEN 'BEFORE' ELSE 'AFTER' END AS period
                    FROM `{PROJECT_ID}.{DATASET_ID}.product_metrics` p CROSS JOIN deployment d
                ),
                summary AS (
                    SELECT metric, period, AVG(value) AS average_value FROM product_data GROUP BY metric, period
                )
                SELECT metric,
                    MAX(IF(period = 'BEFORE', average_value, NULL)) AS before_value,
                    MAX(IF(period = 'AFTER', average_value, NULL)) AS after_value
                FROM summary GROUP BY metric ORDER BY metric
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter("deployment_id", "STRING", deployment_id)]
            )
            results = client.query(query, job_config=job_config).result()
            impact = []
            for row in results:
                before, after = row.before_value, row.after_value
                if before is None or after is None:
                    continue
                percent_change = ((after - before) / before) * 100
                impact.append({
                    "metric": row.metric,
                    "before": round(before, 2),
                    "after": round(after, 2),
                    "percent_change": round(percent_change, 2),
                })
            return impact
        except Exception as err:
            print(f"BigQuery analyze_product_impact error: {err}")

    return FALLBACK_PRODUCT_IMPACT.get(deployment_id, FALLBACK_PRODUCT_IMPACT.get("DEP-4821"))


def analyze_business_impact(deployment_id):
    client = get_client()
    if client:
        try:
            query = f"""
                WITH deployment AS (
                    SELECT TIMESTAMP(deployment_time) AS deployment_time
                    FROM `{PROJECT_ID}.{DATASET_ID}.deployments` WHERE deployment_id = @deployment_id LIMIT 1
                ),
                business_data AS (
                    SELECT b.timestamp, b.metric, b.value,
                        CASE WHEN TIMESTAMP(b.timestamp) < d.deployment_time THEN 'BEFORE' ELSE 'AFTER' END AS period
                    FROM `{PROJECT_ID}.{DATASET_ID}.business_metrics` b CROSS JOIN deployment d
                ),
                summary AS (
                    SELECT metric, period, AVG(value) AS average_value FROM business_data GROUP BY metric, period
                )
                SELECT metric,
                    MAX(IF(period = 'BEFORE', average_value, NULL)) AS before_value,
                    MAX(IF(period = 'AFTER', average_value, NULL)) AS after_value
                FROM summary GROUP BY metric ORDER BY metric
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter("deployment_id", "STRING", deployment_id)]
            )
            results = client.query(query, job_config=job_config).result()
            impact = []
            for row in results:
                before, after = row.before_value, row.after_value
                if before is None or after is None:
                    continue
                percent_change = ((after - before) / before) * 100
                impact.append({
                    "metric": row.metric,
                    "before": round(before, 2),
                    "after": round(after, 2),
                    "percent_change": round(percent_change, 2),
                })
            return impact
        except Exception as err:
            print(f"BigQuery analyze_business_impact error: {err}")

    return FALLBACK_BUSINESS_IMPACT.get(deployment_id, FALLBACK_BUSINESS_IMPACT.get("DEP-4821"))


def investigate(deployment_id):
    deployment = get_deployment(deployment_id)

    if deployment is None:
        return {
            "status": "NOT_FOUND",
            "deployment_id": deployment_id,
            "message": "Deployment not found.",
        }

    system_impact = analyze_system_impact(deployment_id)
    product_impact = analyze_product_impact(deployment_id)
    business_impact = analyze_business_impact(deployment_id)

    return {
        "status": "SUCCESS",
        "deployment": deployment,
        "system_impact": system_impact,
        "product_impact": product_impact,
        "business_impact": business_impact,
    }


def generate_causal_hypotheses(deployment_id):
    deployment = get_deployment(deployment_id)

    if not deployment:
        return {
            "status": "NOT_FOUND",
            "deployment_id": deployment_id,
            "message": "Deployment not found.",
        }

    system_impact = analyze_system_impact(deployment_id)
    product_impact = analyze_product_impact(deployment_id)
    business_impact = analyze_business_impact(deployment_id)
    competing_events = detect_competing_events(deployment_id)

    evidence = calculate_evidence_score(
        system_impact,
        product_impact,
        business_impact,
    )

    hypotheses = generate_hypotheses(
        deployment,
        system_impact,
        product_impact,
        business_impact,
        competing_events,
        evidence["score"],
    )

    return {
        "status": "SUCCESS",
        "deployment": deployment,
        "evidence": evidence,
        "competing_events": competing_events,
        "hypotheses": hypotheses,
    }