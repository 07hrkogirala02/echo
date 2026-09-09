import csv
from datetime import datetime, timedelta
from pathlib import Path


DATA_DIR = Path(__file__).parent


def write_csv(filename, rows, fieldnames):
    path = DATA_DIR / filename

    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {path}")


# ---------------------------------------------------------
# DEPLOYMENTS
# ---------------------------------------------------------

def generate_deployments():
    return [
        {
            "deployment_id": "DEP-4821",
            "service": "checkout-service",
            "version": "v2.4.1",
            "feature": "Checkout V2",
            "environment": "production",
            "deployment_time": "2026-08-15 10:00:00",
        },
        {
            "deployment_id": "DEP-4822",
            "service": "checkout-service",
            "version": "v2.4.2",
            "feature": "Checkout Payment Optimization",
            "environment": "production",
            "deployment_time": "2026-08-16 10:00:00",
        },
        {
            "deployment_id": "DEP-4817",
            "service": "search-service",
            "version": "v3.2.0",
            "feature": "Search Optimization",
            "environment": "production",
            "deployment_time": "2026-08-12 14:00:00",
        },
        {
            "deployment_id": "DEP-4809",
            "service": "auth-service",
            "version": "v1.8.3",
            "feature": "Authentication Update",
            "environment": "production",
            "deployment_time": "2026-08-10 09:30:00",
        },
    ]


# ---------------------------------------------------------
# SYSTEM METRICS
# ---------------------------------------------------------

def generate_system_metrics():

    rows = []

    # =====================================================
    # DEP-4821 — BAD DEPLOYMENT
    # =====================================================

    timestamps_4821 = [
        datetime(2026, 8, 15, 9, 0) + timedelta(minutes=15 * i)
        for i in range(13)
    ]

    latency_4821 = [
        205, 210, 208, 212, 211,
        238, 252, 260, 264, 267, 265, 269, 266
    ]

    payment_failures_4821 = [
        2.0, 2.1, 2.0, 2.1, 2.1,
        2.4, 2.8, 3.1, 3.4, 3.5, 3.4, 3.5, 3.4
    ]

    error_rate_4821 = [
        0.8, 0.9, 0.8, 0.9, 0.9,
        1.1, 1.4, 1.7, 1.9, 2.0, 2.0, 2.1, 2.0
    ]

    for timestamp, latency, payment, error in zip(
        timestamps_4821,
        latency_4821,
        payment_failures_4821,
        error_rate_4821,
    ):
        rows.extend([
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "service": "checkout-service",
                "metric": "api_latency",
                "value": latency,
                "unit": "ms",
                "deployment_id": "DEP-4821",
            },
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "service": "checkout-service",
                "metric": "payment_failure_rate",
                "value": payment,
                "unit": "percent",
                "deployment_id": "DEP-4821",
            },
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "service": "checkout-service",
                "metric": "error_rate",
                "value": error,
                "unit": "percent",
                "deployment_id": "DEP-4821",
            },
        ])

    # =====================================================
    # DEP-4822 — HEALTHY DEPLOYMENT
    # =====================================================

    timestamps_4822 = [
        datetime(2026, 8, 16, 9, 0) + timedelta(minutes=15 * i)
        for i in range(13)
    ]

    latency_4822 = [
        210, 211, 209, 212, 210,
        211, 213, 212, 211, 214, 212, 213, 211
    ]

    payment_failures_4822 = [
        2.1, 2.0, 2.1, 2.0, 2.1,
        2.1, 2.2, 2.1, 2.0, 2.1, 2.1, 2.2, 2.1
    ]

    error_rate_4822 = [
        0.85, 0.86, 0.84, 0.85, 0.86,
        0.87, 0.86, 0.85, 0.86, 0.87, 0.86, 0.85, 0.86
    ]

    for timestamp, latency, payment, error in zip(
        timestamps_4822,
        latency_4822,
        payment_failures_4822,
        error_rate_4822,
    ):
        rows.extend([
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "service": "checkout-service",
                "metric": "api_latency",
                "value": latency,
                "unit": "ms",
                "deployment_id": "DEP-4822",
            },
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "service": "checkout-service",
                "metric": "payment_failure_rate",
                "value": payment,
                "unit": "percent",
                "deployment_id": "DEP-4822",
            },
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "service": "checkout-service",
                "metric": "error_rate",
                "value": error,
                "unit": "percent",
                "deployment_id": "DEP-4822",
            },
        ])

    return rows


# ---------------------------------------------------------
# PRODUCT METRICS
# ---------------------------------------------------------

def generate_product_metrics():

    rows = []

    # DEP-4821
    timestamps_4821 = [
        datetime(2026, 8, 15, 9, 0) + timedelta(minutes=15 * i)
        for i in range(13)
    ]

    conversion_4821 = [
        8.5, 8.4, 8.5, 8.4, 8.4,
        8.3, 8.1, 8.0, 7.8, 7.7, 7.8, 7.7, 7.8
    ]

    abandonment_4821 = [
        10.8, 11.0, 10.9, 11.0, 11.0,
        11.4, 12.0, 13.0, 14.0, 14.2, 14.1, 14.3, 14.0
    ]

    for timestamp, conversion, abandonment in zip(
        timestamps_4821,
        conversion_4821,
        abandonment_4821,
    ):
        rows.extend([
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "metric": "checkout_conversion",
                "value": conversion,
                "unit": "percent",
                "segment": "all",
                "deployment_id": "DEP-4821",
            },
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "metric": "checkout_abandonment",
                "value": abandonment,
                "unit": "percent",
                "segment": "all",
                "deployment_id": "DEP-4821",
            },
        ])

    # DEP-4822
    timestamps_4822 = [
        datetime(2026, 8, 16, 9, 0) + timedelta(minutes=15 * i)
        for i in range(13)
    ]

    conversion_4822 = [
        8.4, 8.5, 8.4, 8.5, 8.5,
        8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.6
    ]

    abandonment_4822 = [
        10.9, 10.8, 10.9, 10.8, 10.9,
        10.8, 10.9, 10.8, 10.9, 10.8, 10.9, 10.8, 10.9
    ]

    for timestamp, conversion, abandonment in zip(
        timestamps_4822,
        conversion_4822,
        abandonment_4822,
    ):
        rows.extend([
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "metric": "checkout_conversion",
                "value": conversion,
                "unit": "percent",
                "segment": "all",
                "deployment_id": "DEP-4822",
            },
            {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "metric": "checkout_abandonment",
                "value": abandonment,
                "unit": "percent",
                "segment": "all",
                "deployment_id": "DEP-4822",
            },
        ])

    return rows


# ---------------------------------------------------------
# BUSINESS METRICS
# ---------------------------------------------------------

def generate_business_metrics():

    rows = []

    # DEP-4821
    timestamps_4821 = [
        datetime(2026, 8, 15, 9, 0) + timedelta(minutes=15 * i)
        for i in range(13)
    ]

    revenue_4821 = [
        4200000, 4210000, 4190000, 4200000, 4200000,
        4150000, 4080000, 3990000, 3850000, 3820000,
        3800000, 3790000, 3800000
    ]

    for timestamp, value in zip(timestamps_4821, revenue_4821):
        rows.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "metric": "revenue",
            "value": value,
            "unit": "INR",
            "deployment_id": "DEP-4821",
        })

    # DEP-4822
    timestamps_4822 = [
        datetime(2026, 8, 16, 9, 0) + timedelta(minutes=15 * i)
        for i in range(13)
    ]

    revenue_4822 = [
        4200000, 4210000, 4205000, 4210000, 4205000,
        4215000, 4210000, 4215000, 4220000, 4215000,
        4220000, 4215000, 4220000
    ]

    for timestamp, value in zip(timestamps_4822, revenue_4822):
        rows.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "metric": "revenue",
            "value": value,
            "unit": "INR",
            "deployment_id": "DEP-4822",
        })

    return rows


# ---------------------------------------------------------
# EVENTS
# ---------------------------------------------------------

def generate_events():

    return [
        # DEP-4821
        {
            "timestamp": "2026-08-15 10:00:00",
            "event_type": "deployment",
            "service": "checkout-service",
            "description": "Checkout V2 deployed",
            "deployment_id": "DEP-4821",
        },
        {
            "timestamp": "2026-08-15 10:15:00",
            "event_type": "latency_spike",
            "service": "checkout-service",
            "description": "API latency exceeded baseline",
            "deployment_id": "DEP-4821",
        },
        {
            "timestamp": "2026-08-15 10:30:00",
            "event_type": "payment_failure_spike",
            "service": "checkout-service",
            "description": "Payment failures exceeded baseline",
            "deployment_id": "DEP-4821",
        },
        {
            "timestamp": "2026-08-15 10:45:00",
            "event_type": "abandonment_spike",
            "service": "checkout-service",
            "description": "Checkout abandonment exceeded baseline",
            "deployment_id": "DEP-4821",
        },
        {
            "timestamp": "2026-08-15 11:00:00",
            "event_type": "conversion_drop",
            "service": "checkout-service",
            "description": "Checkout conversion dropped below baseline",
            "deployment_id": "DEP-4821",
        },
        {
            "timestamp": "2026-08-15 11:00:00",
            "event_type": "revenue_impact",
            "service": "checkout-service",
            "description": "Revenue dropped below expected level",
            "deployment_id": "DEP-4821",
        },

        # DEP-4822
        {
            "timestamp": "2026-08-16 10:00:00",
            "event_type": "deployment",
            "service": "checkout-service",
            "description": "Checkout Payment Optimization deployed",
            "deployment_id": "DEP-4822",
        },
    ]


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    write_csv(
        "deployments.csv",
        generate_deployments(),
        [
            "deployment_id",
            "service",
            "version",
            "feature",
            "environment",
            "deployment_time",
        ],
    )

    write_csv(
        "system_metrics.csv",
        generate_system_metrics(),
        [
            "timestamp",
            "service",
            "metric",
            "value",
            "unit",
            "deployment_id",
        ],
    )

    write_csv(
        "product_metrics.csv",
        generate_product_metrics(),
        [
            "timestamp",
            "metric",
            "value",
            "unit",
            "segment",
            "deployment_id",
        ],
    )

    write_csv(
        "business_metrics.csv",
        generate_business_metrics(),
        [
            "timestamp",
            "metric",
            "value",
            "unit",
            "deployment_id",
        ],
    )

    write_csv(
        "events.csv",
        generate_events(),
        [
            "timestamp",
            "event_type",
            "service",
            "description",
            "deployment_id",
        ],
    )


if __name__ == "__main__":
    main()