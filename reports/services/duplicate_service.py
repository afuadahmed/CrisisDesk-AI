from difflib import SequenceMatcher

from reports.models import Report


DUPLICATE_THRESHOLD = 0.62


def calculate_text_similarity(text1, text2):
    text1 = (text1 or "").lower().strip()
    text2 = (text2 or "").lower().strip()

    return SequenceMatcher(
        None,
        text1,
        text2,
    ).ratio()


def normalize_location(location):
    location = (location or "").lower().strip()

    replacements = {
        ",": " ",
        "-": " ",
        "dhaka": "",
        "ঢাকা": "",
        "১০": "10",
    }

    for old, new in replacements.items():
        location = location.replace(old, new)

    return " ".join(location.split())


def calculate_location_similarity(location1, location2):
    location1 = normalize_location(location1)
    location2 = normalize_location(location2)

    if not location1 or not location2:
        return 0.0

    if location1 == location2:
        return 1.0

    if location1 in location2 or location2 in location1:
        return 1.0

    return calculate_text_similarity(
        location1,
        location2,
    )


def detect_duplicate(description, location, category):
    existing_reports = Report.objects.all()

    best_match = None
    highest_score = 0.0

    for report in existing_reports:
        existing_description = (
            report.summary or report.description
        )

        description_score = calculate_text_similarity(
            description,
            existing_description,
        )

        location_score = calculate_location_similarity(
            location,
            report.location,
        )

        category_score = (
            1.0
            if category == report.category
            else 0.0
        )

        final_score = (
            description_score * 0.45
            + location_score * 0.35
            + category_score * 0.20
        )

        if final_score > highest_score:
            highest_score = final_score
            best_match = report

    if (
        best_match
        and highest_score >= DUPLICATE_THRESHOLD
    ):
        return {
            "possible_duplicate": True,
            "matched_report": best_match,
            "similarity_score": round(
                highest_score,
                4,
            ),
        }

    return {
        "possible_duplicate": False,
        "matched_report": None,
        "similarity_score": round(
            highest_score,
            4,
        ),
    }