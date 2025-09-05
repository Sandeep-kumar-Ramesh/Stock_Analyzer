# 📄 analysis.py

"""Contains functions for analyzing financial data and generating insights."""

from typing import Dict, Any

def analyze_advanced_metrics(info: Dict[str, Any]) -> tuple:
    """Analyzes key metrics and returns UI data, scores, pros, and cons."""
    scores, pros, cons = {}, [], []
    results = {}

    # 1. Valuation
    forward_pe = info.get("forwardPE")
    val_value, val_delta_text, val_delta_color = "N/A", "N/A", "off"
    if isinstance(forward_pe, (int, float)):
        val_value = f"{forward_pe:.2f}"
        if 0 < forward_pe < 15: val_delta_text, scores['val'], val_delta_color, _ = "Good Value", 2, "normal", pros.append("Attractive valuation (Low P/E)")
        elif 15 <= forward_pe <= 25: val_delta_text, scores['val'], val_delta_color = "Fairly Valued", 1, "off"
        else: val_delta_text, scores['val'], val_delta_color, _ = "Overvalued", 0, "inverse", cons.append("Potentially overvalued (High P/E)")
    results['valuation'] = {'value': val_value, 'delta': val_delta_text, 'delta_color': val_delta_color}

    # 2. Profitability
    roe, margins = info.get("returnOnEquity"), info.get("grossMargins")
    prof_value, prof_delta_text, prof_delta_color = "N/A", "N/A", "off"
    if isinstance(roe, (int, float)) and isinstance(margins, (int, float)):
        score = (1 if roe > 0.15 else 0) + (1 if margins > 0.4 else 0)
        prof_delta_text = f"ROE: {roe*100:.1f}%"
        if score == 2: prof_value, scores['prof'], prof_delta_color, _ = "High", 2, "normal", pros.append("High profitability (strong ROE & margins)")
        elif score == 1: prof_value, scores['prof'], prof_delta_color = "Moderate", 1, "off"
        else: prof_value, scores['prof'], prof_delta_color, _ = "Low", 0, "inverse", cons.append("Low profitability")
    elif isinstance(roe, (int, float)): prof_delta_text = f"ROE: {roe*100:.1f}%"
    results['profitability'] = {'value': prof_value, 'delta': prof_delta_text, 'delta_color': prof_delta_color}

    # 3. Financial Health
    debt_equity = info.get("debtToEquity")
    health_value, health_delta_text, health_delta_color = "N/A", "N/A", "off"
    if isinstance(debt_equity, (int, float)):
        health_value = f"{debt_equity:.1f}"
        if debt_equity < 100: health_delta_text, scores['health'], health_delta_color, _ = "Healthy", 2, "normal", pros.append("Solid financial health (low debt)")
        elif 100 <= debt_equity < 200: health_delta_text, scores['health'], health_delta_color, _ = "Moderate Risk", 1, "off", cons.append("Moderate debt levels")
        else: health_delta_text, scores['health'], health_delta_color, _ = "High Risk", 0, "inverse", cons.append("High financial risk (high debt)")
    results['health'] = {'value': health_value, 'delta': health_delta_text, 'delta_color': health_delta_color}
    
    # 4. Price-to-Book
    pb = info.get("priceToBook")
    pb_value, pb_delta_text, pb_delta_color = "N/A", "N/A", "off"
    if isinstance(pb, (int, float)) and pb > 0:
        pb_value = f"{pb:.2f}"
        if pb < 1: pb_delta_text, scores['pb'], pb_delta_color, _ = "Low (Potential Value)", 2, "normal", pros.append("Price is below book value (P/B < 1)")
        elif pb <= 3: pb_delta_text, scores['pb'], pb_delta_color = "Fair", 1, "off"
        else: pb_delta_text, scores['pb'], pb_delta_color, _ = "High", 0, "inverse", cons.append("High price relative to book value (P/B > 3)")
    results['pb'] = {'value': pb_value, 'delta': pb_delta_text, 'delta_color': pb_delta_color}

    # 5. Dividend
    yield_val, payout = info.get("dividendYield"), info.get("payoutRatio")
    div_value, div_delta_text, div_delta_color = "N/A", "N/A", "off"
    if isinstance(yield_val, (int, float)): div_value = f"{yield_val*100:.2f}%"
    if isinstance(payout, (int, float)):
        div_delta_text = f"Payout: {payout*100:.0f}%"
        if 0 < payout < 0.75: scores['div'], div_delta_color, _ = 2, "normal", pros.append("Sustainable dividend payout")
        elif 0.75 <= payout <= 1: scores['div'], div_delta_color, _ = 1, "off", cons.append("High dividend payout (use caution)")
        elif payout > 1 or payout < 0: scores['div'], div_delta_color, _ = 0, "inverse", cons.append("Unsustainable dividend (payout > 100% or negative)")
    results['dividend'] = {'value': div_value, 'delta': div_delta_text, 'delta_color': div_delta_color}

    # 6. Growth
    growth = info.get("revenueGrowth")
    growth_value, growth_delta_text, growth_delta_color = "N/A", "N/A", "off"
    if isinstance(growth, (int, float)):
        growth_value = f"{growth*100:.1f}%"
        if growth > 0.05: growth_delta_text, scores['growth'], growth_delta_color, _ = "Growing", 2, "normal", pros.append(f"Strong revenue growth ({growth*100:.1f}%)")
        elif 0 < growth <= 0.05: growth_delta_text, scores['growth'], growth_delta_color = "Stable", 1, "off"
        else: growth_delta_text, scores['growth'], growth_delta_color, _ = "Shrinking", 0, "inverse", cons.append(f"Shrinking revenues ({growth*100:.1f}%)")
    results['growth'] = {'value': growth_value, 'delta': growth_delta_text, 'delta_color': growth_delta_color}

    return results, scores, pros, cons

def generate_conclusion(analysis: dict):
    """Generates an HTML-formatted conclusion based on analysis scores."""
    scores, pros, cons = analysis.get("scores", {}), analysis.get("pros", []), analysis.get("cons", [])
    if not scores or not (num_metrics := len(scores)):
        return '<p><strong>Final Conclusion:</strong> Not enough data to form a conclusion.</p>'
    avg_score_percent = (sum(scores.values()) / (num_metrics * 2)) * 100
    if avg_score_percent > 70: verdict_text, color = "Positive Outlook", "#28a745"
    elif avg_score_percent > 40: verdict_text, color = "Mixed Signals", "#ffc107"
    else: verdict_text, color = "Caution Advised", "#dc3545"
    pros_html = "".join([f"<li>✅ {pro}</li>" for pro in pros]) if pros else "<li>No significant strengths identified.</li>"
    cons_html = "".join([f"<li>❌ {con}</li>" for con in cons]) if cons else "<li>No significant weaknesses identified.</li>"
    return f"""<div style="background-color: #273342; padding: 15px; border-radius: 8px; border-left: 6px solid {color};">
        <p style="margin: 0 0 10px 0; font-size: 1.1em;"><strong>Verdict:</strong> <strong style="color:{color};">{verdict_text}</strong></p>
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 250px; padding-right: 10px;"><strong style="color:#28a745;">Potential Strengths:</strong><ul style="padding-left: 20px; margin-top: 5px; margin-bottom: 5px;">{pros_html}</ul></div>
            <div style="flex: 1; min-width: 250px; padding-left: 10px;"><strong style="color:#dc3545;">Potential Weaknesses:</strong><ul style="padding-left: 20px; margin-top: 5px; margin-bottom: 5px;">{cons_html}</ul></div>
        </div></div>"""