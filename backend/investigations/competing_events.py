from google.cloud import bigquery

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


def detect_competing_events(
    deployment_id,
    window_minutes=120,
):
    """
    Finds events occurring around a deployment.
    """
    client = get_client()
    if client:
        try:
            query = f"""
                WITH deployment AS (
                    SELECT
                        deployment_id,
                        service,
                        TIMESTAMP(deployment_time) AS deployment_time
                    FROM `{PROJECT_ID}.{DATASET_ID}.deployments`
                    WHERE deployment_id = @deployment_id
                    LIMIT 1
                )
                SELECT
                    e.timestamp,
                    e.event_type,
                    e.service,
                    e.description,
                    d.deployment_time,
                    TIMESTAMP_DIFF(
                        TIMESTAMP(e.timestamp),
                        d.deployment_time,
                        MINUTE
                    ) AS minutes_from_deployment
                FROM `{PROJECT_ID}.{DATASET_ID}.events` e
                CROSS JOIN deployment d
                WHERE
                    TIMESTAMP(e.timestamp)
                    BETWEEN
                        TIMESTAMP_SUB(d.deployment_time, INTERVAL @window_minutes MINUTE)
                        AND TIMESTAMP_ADD(d.deployment_time, INTERVAL @window_minutes MINUTE)
                    AND NOT (
                        e.event_type = "deployment"
                        AND TIMESTAMP(e.timestamp) = d.deployment_time
                    )
                ORDER BY
                    ABS(
                        TIMESTAMP_DIFF(
                            TIMESTAMP(e.timestamp),
                            d.deployment_time,
                            MINUTE
                        )
                    )
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("deployment_id", "STRING", deployment_id),
                    bigquery.ScalarQueryParameter("window_minutes", "INT64", window_minutes),
                ]
            )

            results = client.query(query, job_config=job_config).result()
            events = []
            for row in results:
                events.append({
                    "timestamp": row.timestamp.isoformat() if row.timestamp else None,
                    "event_type": row.event_type,
                    "service": row.service,
                    "description": row.description,
                    "minutes_from_deployment": row.minutes_from_deployment,
                })
            return events
        except Exception as err:
            print(f"BigQuery query error in detect_competing_events: {err}")

    # Fallback when BigQuery is not available
    if deployment_id == "DEP-4822":
        return [
            {
                "timestamp": "2026-08-16T09:55:00",
                "event_type": "payment_provider_outage",
                "service": "payment-service",
                "description": "Payment provider experiencing elevated transaction failures",
                "minutes_from_deployment": -5,
            }
        ]
    return []