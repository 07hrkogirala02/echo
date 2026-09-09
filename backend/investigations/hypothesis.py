from typing import List, Dict


def _average_impact(impacts: List[Dict]) -> float:
    """
    Calculate the average absolute percentage change
    across available impact metrics.
    """

    changes = [
        abs(item["percent_change"])
        for item in impacts
        if item.get("percent_change") is not None
    ]

    if not changes:
        return 0.0

    return sum(changes) / len(changes)


def _has_negative_business_impact(business_impact: List[Dict]) -> bool:
    """
    Check whether business metrics deteriorated after deployment.
    """

    for item in business_impact:
        if item.get("percent_change", 0) < 0:
            return True

    return False


def _has_negative_product_impact(product_impact: List[Dict]) -> bool:
    """
    Check whether product metrics deteriorated after deployment.
    """

    for item in product_impact:
        if item.get("percent_change", 0) < 0:
            return True

    return False


def _has_strong_system_impact(system_impact: List[Dict]) -> bool:
    """
    Check whether at least one system metric changed significantly.
    """

    for item in system_impact:
        if abs(item.get("percent_change", 0)) >= 20:
            return True

    return False


def _find_competing_events(
    competing_events: List[Dict],
) -> List[Dict]:
    """
    Return events that occurred before the deployment.
    """

    return [
        event
        for event in competing_events
        if event.get("minutes_from_deployment", 0) < 0
    ]


def generate_hypotheses(
    deployment: Dict,
    system_impact: List[Dict],
    product_impact: List[Dict],
    business_impact: List[Dict],
    competing_events: List[Dict],
    evidence_score: float,
) -> List[Dict]:

    hypotheses = []

    competing = _find_competing_events(competing_events)

    strong_system = _has_strong_system_impact(system_impact)
    negative_product = _has_negative_product_impact(product_impact)
    negative_business = _has_negative_business_impact(business_impact)

    system_strength = _average_impact(system_impact)
    product_strength = _average_impact(product_impact)
    business_strength = _average_impact(business_impact)

    # ---------------------------------------------------------
    # HYPOTHESIS 1 — DEPLOYMENT CAUSED THE IMPACT
    # ---------------------------------------------------------

    deployment_score = 0

    if strong_system:
        deployment_score += 25

    if negative_product:
        deployment_score += 20

    if negative_business:
        deployment_score += 20

    if evidence_score >= 80:
        deployment_score += 25

    elif evidence_score >= 60:
        deployment_score += 15

    elif evidence_score >= 40:
        deployment_score += 8

    # Penalize the deployment hypothesis if a strong
    # competing event happened before deployment.

    if competing:
        deployment_score -= 25

    deployment_score = max(0, min(100, deployment_score))

    deployment_reason = (
        f"The deployment is associated with "
        f"{len(system_impact)} system impact signals, "
        f"{len(product_impact)} product impact signals, "
        f"and {len(business_impact)} business impact signal(s)."
    )

    if competing:
        deployment_reason += (
            f" However, {len(competing)} competing event(s) "
            f"occurred before the deployment."
        )

    hypotheses.append(
        {
            "hypothesis": "Deployment caused the observed impact",
            "type": "DEPLOYMENT",
            "score": round(deployment_score, 2),
            "confidence": (
                "HIGH"
                if deployment_score >= 75
                else "MEDIUM"
                if deployment_score >= 50
                else "LOW"
            ),
            "reason": deployment_reason,
            "evidence": {
                "system_impact_strength": round(system_strength, 2),
                "product_impact_strength": round(product_strength, 2),
                "business_impact_strength": round(business_strength, 2),
                "evidence_score": evidence_score,
                "competing_events": len(competing),
            },
        }
    )

    # ---------------------------------------------------------
    # HYPOTHESIS 2 — EXTERNAL EVENT CAUSED THE IMPACT
    # ---------------------------------------------------------

    if competing:

        strongest_event = competing[0]

        external_score = 40

        # Event occurring very close to deployment is stronger.
        minutes_before = abs(
            strongest_event.get("minutes_from_deployment", 0)
        )

        if minutes_before <= 5:
            external_score += 30

        elif minutes_before <= 15:
            external_score += 20

        elif minutes_before <= 30:
            external_score += 10

        # Payment/provider failures are especially relevant
        # to checkout/payment-related incidents.

        event_type = strongest_event.get("event_type", "")

        if "payment" in event_type.lower():
            external_score += 20

        external_score = max(0, min(100, external_score))

        hypotheses.append(
            {
                "hypothesis": (
                    f"External event caused or contributed to the impact: "
                    f"{strongest_event.get('description', 'Unknown event')}"
                ),
                "type": "COMPETING_EVENT",
                "score": round(external_score, 2),
                "confidence": (
                    "HIGH"
                    if external_score >= 75
                    else "MEDIUM"
                    if external_score >= 50
                    else "LOW"
                ),
                "reason": (
                    f"The event occurred "
                    f"{minutes_before} minute(s) before the deployment "
                    f"and may independently explain downstream degradation."
                ),
                "evidence": strongest_event,
            }
        )

    # ---------------------------------------------------------
    # SORT HYPOTHESES
    # ---------------------------------------------------------

    hypotheses.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    # Add rank.

    for index, hypothesis in enumerate(hypotheses, start=1):
        hypothesis["rank"] = index

    return hypotheses