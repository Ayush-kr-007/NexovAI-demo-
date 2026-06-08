import json
from pathlib import Path

LEAD_FILE = "lead.json"


def save_lead(data):

    with open(LEAD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_lead():

    if not Path(LEAD_FILE).exists():
        return {}

    with open(LEAD_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_score(interest, budget, timeline):

    score = 0

    interest = str(interest).upper()

    if "YES" in interest or "INTERESTED" in interest:
        score += 40

    elif "MAYBE" in interest:
        score += 20

    try:
        budget_num = int(
            "".join(filter(str.isdigit, str(budget)))
        )
    except:
        budget_num = 0

    if budget_num >= 100000:
        score += 30

    elif budget_num >= 50000:
        score += 20

    else:
        score += 10

    timeline = str(timeline).lower()

    if "1 month" in timeline:
        score += 30

    elif "3 month" in timeline:
        score += 20

    else:
        score += 10

    if score >= 80:
        lead_type = "HOT"

    elif score >= 50:
        lead_type = "WARM"

    else:
        lead_type = "COLD"

    return score, lead_type