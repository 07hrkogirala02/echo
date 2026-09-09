from google.cloud import bigquery


PROJECT_ID = "echo-505604"
DATASET_ID = "echo_dataset"

client = bigquery.Client(project=PROJECT_ID)


def detect_competing_events(
    deployment_id,
    window_minutes=120,
):
    """
    Finds events occurring around a deployment.

    Events are considered potential competing events
    when they occur within the investigation window.

    This function does NOT decide whether an event
    caused the impact. That decision happens later
    through event relevance scoring.
    """

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
                TIMESTAMP_SUB(
                    d.deployment_time,
                    INTERVAL @window_minutes MINUTE
                )

                AND

                TIMESTAMP_ADD(
                    d.deployment_time,
                    INTERVAL @window_minutes MINUTE
                )

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
            bigquery.ScalarQueryParameter(
                "deployment_id",
                "STRING",
                deployment_id,
            ),
            bigquery.ScalarQueryParameter(
                "window_minutes",
                "INT64",
                window_minutes,
            ),
        ]
    )

    results = client.query(
        query,
        job_config=job_config,
    ).result()

    events = []

    for row in results:

        events.append(
            {
                "timestamp": (
                    row.timestamp.isoformat()
                    if row.timestamp
                    else None
                ),

                "event_type": row.event_type,

                "service": row.service,

                "description": row.description,

                "minutes_from_deployment": (
                    row.minutes_from_deployment
                ),
            }
        )

    return events