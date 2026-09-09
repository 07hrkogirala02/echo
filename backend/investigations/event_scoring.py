from datetime import datetime


# ---------------------------------------------------------
# EVENT CLASSIFICATION
# ---------------------------------------------------------

IMPACT_EVENTS = {
    "latency_spike",
    "error_rate_spike",
    "payment_failure_spike",
    "abandonment_spike",
    "conversion_drop",
    "revenue_impact",
}


COMPETING_EVENTS = {
    "payment_provider_outage",
    "database_incident",
    "database_outage",
    "network_outage",
    "infrastructure_failure",
    "third_party_api_outage",
    "configuration_change",
    "traffic_spike",
    "security_incident",
    "maintenance",
}


def classify_event(event_type):
    """
    Classifies an event into one of three categories:

    IMPACT_SIGNAL
    COMPETING_EVENT
    NEUTRAL_EVENT
    """

    if event_type == "deployment":
        return "DEPLOYMENT"

    if event_type in IMPACT_EVENTS:
        return "IMPACT_SIGNAL"

    if event_type in COMPETING_EVENTS:
        return "COMPETING_EVENT"

    return "NEUTRAL_EVENT"


# ---------------------------------------------------------
# TIMING SCORE
# ---------------------------------------------------------

def timing_score(minutes_from_deployment):
    """
    Scores how temporally close an event is to the deployment.

    Closer events receive higher scores.
    """

    minutes = abs(minutes_from_deployment)

    if minutes <= 5:
        return 100

    if minutes <= 15:
        return 90

    if minutes <= 30:
        return 75

    if minutes <= 60:
        return 55

    if minutes <= 120:
        return 30

    return 0


# ---------------------------------------------------------
# SERVICE RELEVANCE
# ---------------------------------------------------------

def service_score(
    event_service,
    deployment_service,
):
    """
    Determines whether the event occurred in the same
    service affected by the deployment.
    """

    if not event_service or not deployment_service:
        return 0

    if event_service == deployment_service:
        return 100

    return 40


# ---------------------------------------------------------
# EVENT TYPE RELEVANCE
# ---------------------------------------------------------

def event_type_score(event_type):
    """
    Estimates how strongly the event type could explain
    a production incident.
    """

    high_relevance = {
        "payment_provider_outage",
        "database_incident",
        "database_outage",
        "network_outage",
        "infrastructure_failure",
        "third_party_api_outage",
        "security_incident",
    }

    medium_relevance = {
        "configuration_change",
        "traffic_spike",
        "maintenance",
    }

    if event_type in high_relevance:
        return 100

    if event_type in medium_relevance:
        return 70

    if event_type in IMPACT_EVENTS:
        return 20

    return 30


# ---------------------------------------------------------
# OVERALL EVENT RELEVANCE
# ---------------------------------------------------------

def calculate_event_relevance(
    event,
    deployment_service,
):
    """
    Calculates a 0-100 relevance score for an event.

    The score combines:

    1. Timing
    2. Service relationship
    3. Event type relevance
    """

    classification = classify_event(
        event["event_type"]
    )

    timing = timing_score(
        event["minutes_from_deployment"]
    )

    service = service_score(
        event["service"],
        deployment_service,
    )

    event_type = event_type_score(
        event["event_type"]
    )

    score = (
        timing * 0.40
        + service * 0.30
        + event_type * 0.30
    )

    return {
        **event,

        "classification": classification,

        "timing_score": timing,

        "service_score": service,

        "event_type_score": event_type,

        "relevance_score": round(
            score,
            2,
        ),
    }


# ---------------------------------------------------------
# SCORE ALL EVENTS
# ---------------------------------------------------------

def score_events(
    events,
    deployment_service,
):
    """
    Classifies and scores all detected events.
    """

    scored_events = []

    for event in events:

        scored_event = calculate_event_relevance(
            event,
            deployment_service,
        )

        scored_events.append(
            scored_event
        )

    return sorted(
        scored_events,
        key=lambda event: event[
            "relevance_score"
        ],
        reverse=True,
    )


# ---------------------------------------------------------
# GET ONLY POTENTIAL COMPETING EVENTS
# ---------------------------------------------------------

def get_competing_events(
    events,
    deployment_service,
    minimum_score=60,
):
    """
    Returns only events classified as competing
    events and having sufficient relevance.
    """

    scored_events = score_events(
        events,
        deployment_service,
    )

    return [
        event
        for event in scored_events

        if (
            event["classification"]
            == "COMPETING_EVENT"

            and

            event["relevance_score"]
            >= minimum_score
        )
    ]