"""Generates a formatted conclusion based on analysis scores."""

def generate_conclusion(analysis: dict):
    """Generates an HTML-formatted conclusion based on analysis scores."""
    scores, pros, cons = analysis.get("scores", {}), analysis.get("pros", []), analysis.get("cons", [])
    
    if not scores:
        return '<p><strong>Final Conclusion:</strong> Not enough data to form a conclusion.</p>'
        
    num_metrics = len(scores)
    avg_score_percent = (sum(scores.values()) / (num_metrics * 2)) * 100

    if avg_score_percent > 70:
        verdict_text, color = "Positive Outlook", "#28a745"
    elif avg_score_percent > 40:
        verdict_text, color = "Mixed Signals", "#ffc107"
    else:
        verdict_text, color = "Caution Advised", "#dc3545"

    pros_html = "".join([f"<li>✅ {pro}</li>" for pro in pros]) if pros else "<li>No significant strengths identified.</li>"
    cons_html = "".join([f"<li>❌ {con}</li>" for con in cons]) if cons else "<li>No significant weaknesses identified.</li>"
    
    return f"""
    <div style="background-color: #273342; padding: 15px; border-radius: 8px; border-left: 6px solid {color};">
        <p style="margin: 0 0 10px 0; font-size: 1.1em;">
            <strong>Verdict:</strong> <strong style="color:{color};">{verdict_text}</strong>
        </p>
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 250px; padding-right: 10px;">
                <strong style="color:#28a745;">Potential Strengths:</strong>
                <ul style="padding-left: 20px; margin-top: 5px; margin-bottom: 5px;">{pros_html}</ul>
            </div>
            <div style="flex: 1; min-width: 250px; padding-left: 10px;">
                <strong style="color:#dc3545;">Potential Weaknesses:</strong>
                <ul style="padding-left: 20px; margin-top: 5px; margin-bottom: 5px;">{cons_html}</ul>
            </div>
        </div>
    </div>
    """