from google.cloud import bigquery
from investigations.competing_events import detect_competing_events
from investigations.evidence import calculate_evidence_score
from investigations.hypothesis import generate_hypotheses


PROJECT_ID = "echo-505604"
DATASET_ID = "echo_dataset"


client = bigquery.Client(project=PROJECT_ID)


def get_deployment(deployment_id):
    query = f"""
        SELECT
            deployment_id,
            service,
            version,
            feature,
            environment,
            deployment_time
        FROM `{PROJECT_ID}.{DATASET_ID}.deployments`
        WHERE deployment_id = @deployment_id
        LIMIT 1
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "deployment_id",
                "STRING",
                deployment_id,
            )
        ]
    )

    results = client.query(
        query,
        job_config=job_config,
    ).result()

    for row in results:
        return {
            "deployment_id": row.deployment_id,
            "service": row.service,
            "version": row.version,
            "feature": row.feature,
            "environment": row.environment,
            "deployment_time": row.deployment_time.isoformat(),
        }

    return None


def analyze_system_impact(deployment_id):
    query = f"""
        WITH deployment AS (
            SELECT
                deployment_id,
                service,
                TIMESTAMP(deployment_time) AS deployment_time
            FROM `{PROJECT_ID}.{DATASET_ID}.deployments`
            WHERE deployment_id = @deployment_id
            LIMIT 1
        ),

        metrics AS (
            SELECT
                m.timestamp,
                m.metric,
                m.value,
                d.deployment_time,

                CASE
                    WHEN TIMESTAMP(m.timestamp) < d.deployment_time
                        THEN "BEFORE"
                    ELSE "AFTER"
                END AS period

            FROM `{PROJECT_ID}.{DATASET_ID}.system_metrics` m
            CROSS JOIN deployment d

            WHERE m.service = d.service
        ),

        summary AS (
            SELECT
                metric,
                period,
                AVG(value) AS average_value
            FROM metrics
            GROUP BY metric, period
        ),

        first_after AS (
            SELECT
                metric,
                MIN(timestamp) AS first_after_timestamp
            FROM metrics
            WHERE period = "AFTER"
            GROUP BY metric
        )

        SELECT
            s.metric,

            MAX(
                IF(s.period = "BEFORE", s.average_value, NULL)
            ) AS before_value,

            MAX(
                IF(s.period = "AFTER", s.average_value, NULL)
            ) AS after_value,

            f.first_after_timestamp,

            MIN(
                m.deployment_time
            ) AS deployment_time

        FROM summary s

        LEFT JOIN first_after f
            ON s.metric = f.metric

        JOIN metrics m
            ON s.metric = m.metric

        GROUP BY
            s.metric,
            f.first_after_timestamp

        ORDER BY s.metric
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "deployment_id",
                "STRING",
                deployment_id,
            )
        ]
    )

    results = client.query(
        query,
        job_config=job_config,
    ).result()

    impact = []

    for row in results:

        before = row.before_value
        after = row.after_value

        if before is None or after is None:
            continue

        percent_change = ((after - before) / before) * 100

        impact.append(
            {
                "metric": row.metric,
                "before": round(before, 2),
                "after": round(after, 2),
                "percent_change": round(percent_change, 2),
                "first_after_timestamp": (
                    row.first_after_timestamp.isoformat()
                    if row.first_after_timestamp
                    else None
                ),
                "deployment_time": (
                    row.deployment_time.isoformat()
                    if row.deployment_time
                    else None
                ),
            }
        )

    return impact


def analyze_product_impact(deployment_id):
    query = f"""
        WITH deployment AS (
            SELECT
                TIMESTAMP(deployment_time) AS deployment_time
            FROM `{PROJECT_ID}.{DATASET_ID}.deployments`
            WHERE deployment_id = @deployment_id
            LIMIT 1
        ),

        product_data AS (
            SELECT
                p.timestamp,
                p.metric,
                p.value,

                CASE
                    WHEN TIMESTAMP(p.timestamp) < d.deployment_time
                        THEN "BEFORE"
                    ELSE "AFTER"
                END AS period

            FROM `{PROJECT_ID}.{DATASET_ID}.product_metrics` p
            CROSS JOIN deployment d
        ),

        summary AS (
            SELECT
                metric,
                period,
                AVG(value) AS average_value
            FROM product_data
            GROUP BY metric, period
        )

        SELECT
            metric,

            MAX(
                IF(period = "BEFORE", average_value, NULL)
            ) AS before_value,

            MAX(
                IF(period = "AFTER", average_value, NULL)
            ) AS after_value

        FROM summary
        GROUP BY metric
        ORDER BY metric
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "deployment_id",
                "STRING",
                deployment_id,
            )
        ]
    )

    results = client.query(
        query,
        job_config=job_config,
    ).result()

    impact = []

    for row in results:

        before = row.before_value
        after = row.after_value

        if before is None or after is None:
            continue

        percent_change = ((after - before) / before) * 100

        impact.append(
            {
                "metric": row.metric,
                "before": round(before, 2),
                "after": round(after, 2),
                "percent_change": round(percent_change, 2),
            }
        )

    return impact


def analyze_business_impact(deployment_id):
    query = f"""
        WITH deployment AS (
            SELECT
                TIMESTAMP(deployment_time) AS deployment_time
            FROM `{PROJECT_ID}.{DATASET_ID}.deployments`
            WHERE deployment_id = @deployment_id
            LIMIT 1
        ),

        business_data AS (
            SELECT
                b.timestamp,
                b.metric,
                b.value,

                CASE
                    WHEN TIMESTAMP(b.timestamp) < d.deployment_time
                        THEN "BEFORE"
                    ELSE "AFTER"
                END AS period

            FROM `{PROJECT_ID}.{DATASET_ID}.business_metrics` b
            CROSS JOIN deployment d
        ),

        summary AS (
            SELECT
                metric,
                period,
                AVG(value) AS average_value
            FROM business_data
            GROUP BY metric, period
        )

        SELECT
            metric,

            MAX(
                IF(period = "BEFORE", average_value, NULL)
            ) AS before_value,

            MAX(
                IF(period = "AFTER", average_value, NULL)
            ) AS after_value

        FROM summary
        GROUP BY metric
        ORDER BY metric
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "deployment_id",
                "STRING",
                deployment_id,
            )
        ]
    )

    results = client.query(
        query,
        job_config=job_config,
    ).result()

    impact = []

    for row in results:

        before = row.before_value
        after = row.after_value

        if before is None or after is None:
            continue

        percent_change = ((after - before) / before) * 100

        impact.append(
            {
                "metric": row.metric,
                "before": round(before, 2),
                "after": round(after, 2),
                "percent_change": round(percent_change, 2),
            }
        )

    return impact


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