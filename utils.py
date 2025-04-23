def calculate_cyber_risk_metrics(
    controls_cost,
    revenue,
    user_count,
    monitoring_cost_per_user,
    base_sle,
    downtime_days,
    cost_per_day,
    aro_before_percent,
    aro_after_percent,
    maturity_level
):
    modifiers = {
        "Initial": 1.3,
        "Developing": 1.15,
        "Defined": 1.0,
        "Managed": 0.85,
        "Optimized": 0.7
    }

    aro_before = (aro_before_percent / 100.0) * modifiers[maturity_level]
    aro_after = (aro_after_percent / 100.0) * modifiers[maturity_level]

    user_breach_cost = user_count * monitoring_cost_per_user
    downtime_cost = downtime_days * cost_per_day
    sle = base_sle + user_breach_cost + downtime_cost

    ale_before = sle * aro_before
    ale_after = sle * aro_after
    risk_reduction = ale_before - ale_after
    roi = risk_reduction / controls_cost if controls_cost else 0

    return {
        "SLE": sle,
        "ALE_BEFORE": ale_before,
        "ALE_AFTER": ale_after,
        "RISK_REDUCTION": risk_reduction,
        "ROI": roi
    }
