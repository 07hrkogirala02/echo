from datetime import datetime, timezone
from statistics import mean


def magnitude_score(percent_change):
    """
    Converts the magnitude of a metric change into a 0-100 score.
    """

    change = abs(percent_change)

    if change >= 100:
        return 100

    if change >= 50:
        return 90

    if change >= 30:
        return 80

    if change >= 20:
        return 70

    if change >= 10:
        return 55

    if change >= 5:
        return 40

    if change >= 2:
        return 25

    return 10


def temporal_score(deployment_time, first_after_timestamp):
    """
    Measures how quickly a metric changed after deployment.
    """

    if not deployment_time or not first_after_timestamp:
        return 0

    deployment = datetime.fromisoformat(deployment_time)

    first_after = datetime.fromisoformat(
        first_after_timestamp
    )

    if deployment.tzinfo is None:
        deployment = deployment.replace(
            tzinfo=timezone.utc
        )

    if first_after.tzinfo is None:
        first_after = first_after.replace(
            tzinfo=timezone.utc
        )

    delay_minutes = (
        first_after - deployment
    ).total_seconds() / 60

    if delay_minutes < 0:
        return 0

    if delay_minutes <= 5:
        return 100

    if delay_minutes <= 15:
        return 90

    if delay_minutes <= 30:
        return 75

    if delay_minutes <= 60:
        return 50

    if delay_minutes <= 120:
        return 30

    return 10


def cross_layer_score(
    system_impact,
    product_impact,
    business_impact,
):
    """
    Measures how many analytical layers
    show meaningful change.
    """

    layers_with_change = 0

    if system_impact:

        if any(
            abs(item["percent_change"]) >= 5
            for item in system_impact
        ):
            layers_with_change += 1

    if product_impact:

        if any(
            abs(item["percent_change"]) >= 5
            for item in product_impact
        ):
            layers_with_change += 1

    if business_impact:

        if any(
            abs(item["percent_change"]) >= 5
            for item in business_impact
        ):
            layers_with_change += 1

    if layers_with_change == 3:
        return 100

    if layers_with_change == 2:
        return 75

    if layers_with_change == 1:
        return 50

    return 0


def directional_consistency_score(
    product_impact,
    business_impact,
):
    """
    Checks whether product and business metrics
    move in a logically consistent direction.
    """

    abandonment_increased = False
    conversion_decreased = False
    revenue_decreased = False

    for item in product_impact:

        if item["metric"] == "checkout_abandonment":
            abandonment_increased = (
                item["percent_change"] > 0
            )

        if item["metric"] == "checkout_conversion":
            conversion_decreased = (
                item["percent_change"] < 0
            )

    for item in business_impact:

        if item["metric"] == "revenue":
            revenue_decreased = (
                item["percent_change"] < 0
            )

    score = 0

    if abandonment_increased:
        score += 30

    if conversion_decreased:
        score += 30

    if revenue_decreased:
        score += 40

    return score


def calculate_evidence_score(
    system_impact,
    product_impact,
    business_impact,
):
    """
    Calculates Echo's overall evidence score.
    """

    all_impacts = (
        system_impact
        + product_impact
        + business_impact
    )

    if not all_impacts:

        return {
            "score": 0,
            "confidence": "INSUFFICIENT",
            "components": {
                "magnitude": 0,
                "temporal": 0,
                "cross_layer": 0,
                "directional_consistency": 0,
            },
        }

    # ----------------------------------------
    # 1. MAGNITUDE
    # ----------------------------------------

    magnitude_scores = [
        magnitude_score(
            item["percent_change"]
        )
        for item in all_impacts
    ]

    average_magnitude = mean(
        magnitude_scores
    )

    # ----------------------------------------
    # 2. TEMPORAL
    # ----------------------------------------

    temporal_scores = []

    for item in system_impact:

        deployment_time = item.get(
            "deployment_time"
        )

        first_after_timestamp = item.get(
            "first_after_timestamp"
        )

        if (
            deployment_time
            and first_after_timestamp
        ):

            temporal_scores.append(
                temporal_score(
                    deployment_time,
                    first_after_timestamp,
                )
            )

    if temporal_scores:

        temporal = mean(
            temporal_scores
        )

    else:

        temporal = 0

    # ----------------------------------------
    # 3. CROSS-LAYER
    # ----------------------------------------

    cross_layer = cross_layer_score(
        system_impact,
        product_impact,
        business_impact,
    )

    # ----------------------------------------
    # 4. DIRECTIONAL CONSISTENCY
    # ----------------------------------------

    directional = (
        directional_consistency_score(
            product_impact,
            business_impact,
        )
    )

    # ----------------------------------------
    # FINAL SCORE
    # ----------------------------------------

    final_score = (
        average_magnitude * 0.25
        + temporal * 0.25
        + cross_layer * 0.25
        + directional * 0.25
    )

    final_score = round(
        final_score,
        2,
    )

    # ----------------------------------------
    # CONFIDENCE LEVEL
    # ----------------------------------------

    if final_score >= 80:

        confidence = "VERY STRONG"

    elif final_score >= 60:

        confidence = "STRONG"

    elif final_score >= 40:

        confidence = "MODERATE"

    else:

        confidence = "WEAK"

    return {
        "score": final_score,
        "confidence": confidence,
        "components": {
            "magnitude": round(
                average_magnitude,
                2,
            ),
            "temporal": round(
                temporal,
                2,
            ),
            "cross_layer": cross_layer,
            "directional_consistency": directional,
        },
    }