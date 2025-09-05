"""Contains functions for analyzing financial data."""

from typing import Dict, Any, Tuple, List

def _get_metric_analysis(info: Dict[str, Any], metric_key: str, thresholds: List, labels: List, category: str) -> Tuple[str, int, str, str]:
    """Helper to analyze a single metric against thresholds."""
    value = info.get(metric_key)
    if not isinstance(value, (int, float)):
        return "N/A", 0, "off", ""

    lower_is_better = category in ["valuation", "health", "pb"]

    if (lower_is_better and value < thresholds[0]) or (not lower_is_better and value > thresholds[0]):
        return labels[0], 2, "normal", f"Good {category}: {labels[0]}"
    elif (lower_is_better and value <= thresholds[1]) or (not lower_is_better and value >= thresholds[1]):
        return labels[1], 1, "off", f"Fair {category}: {labels[1]}"
    else:
        return labels[2], 0, "inverse", f"Poor {category}: {labels[2]}"


def analyze_advanced_metrics(info: Dict[str, Any]) -> Tuple[Dict, Dict]:
    """
    Analyzes key metrics and returns UI data and a summary for conclusion.
    """
    results, scores, pros, cons = {}, {}, [], []

    # --- Metric Definitions ---
    METRIC_CONFIG = {
        'valuation': ('forwardPE', [15, 25], ["Good Value", "Fairly Valued", "Overvalued"], "Attractive valuation (Low P/E)", "Potentially overvalued (High P/E)"),
        'profitability': ('returnOnEquity', [0.15, 0.10], ["High", "Moderate", "Low"], "High profitability (strong ROE)", "Low profitability"),
        'health': ('debtToEquity', [100, 200], ["Healthy", "Moderate Risk", "High Risk"], "Solid financial health (low debt)", "High financial risk (high debt)"),
        'pb': ('priceToBook', [1, 3], ["Low (Potential Value)", "Fair", "High"], "Price is below book value (P/B < 1)", "High price relative to book value (P/B > 3)"),
        'growth': ('revenueGrowth', [0.05, 0], ["Growing", "Stable", "Shrinking"], "Strong revenue growth", "Shrinking revenues"),
    }

    # --- Process Metrics ---
    for key, (api_name, thresholds, labels, pro_msg, con_msg) in METRIC_CONFIG.items():
        value = info.get(api_name)
        status, score, color = "N/A", 0, "off"

        if isinstance(value, (int, float)):
            lower_is_better = key in ['valuation', 'health', 'pb']
            if (lower_is_better and value < thresholds[0]) or (not lower_is_better and value > thresholds[0]):
                status, score, color = labels[0], 2, "normal"
                pros.append(pro_msg)
            elif (lower_is_better and value <= thresholds[1]) or (not lower_is_better and value >= thresholds[1]):
                status, score, color = labels[1], 1, "off"
            else:
                status, score, color = labels[2], 0, "inverse"
                cons.append(con_msg)
        
        scores[key] = score
        # Special formatting for display value
        display_value = f"{value * 100:.1f}%" if key in ['profitability', 'growth'] else f"{value:.2f}" if isinstance(value, (int, float)) else "N/A"
        results[key] = {'value': display_value, 'delta': status, 'delta_color': color}

    # --- Dividend (Special Case) ---
    yield_val, payout = info.get("dividendYield"), info.get("payoutRatio")
    div_value, div_delta_text, div_delta_color = "N/A", "N/A", "off"
    if isinstance(yield_val, float):
        div_value = f"{yield_val * 100:.2f}%"
    if isinstance(payout, float):
        div_delta_text = f"Payout: {payout * 100:.0f}%"
        if 0 < payout < 0.75:
            scores['div'], div_delta_color = 2, "normal"
            pros.append("Sustainable dividend payout")
        elif payout <= 1:
            scores['div'], div_delta_color = 1, "off"
            cons.append("High dividend payout (use caution)")
        else:
            scores['div'], div_delta_color = 0, "inverse"
            cons.append("Unsustainable dividend")

    results['dividend'] = {'value': div_value, 'delta': div_delta_text, 'delta_color': div_delta_color}

    analysis_summary = {"scores": scores, "pros": pros, "cons": cons}
    return results, analysis_summary