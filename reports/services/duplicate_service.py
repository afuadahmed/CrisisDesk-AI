import re
from difflib import SequenceMatcher

from reports.models import Report


DUPLICATE_THRESHOLD = 0.75


def normalize_text(text):
    if not text:
        return ""

    text = text.lower().strip()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text


def calculate_text_similarity(text1, text2):
    normalized_text1 = normalize_text(text1)
    normalized_text2 = normalize_text(text2)

    if not normalized_text1 or not normalized_text2:
        return 0.0

    sequence_score = SequenceMatcher(
        None,
        normalized_text1,
        normalized_text2,
    ).ratio()

    words1 = set(normalized_text1.split())
    words2 = set(normalized_text2.split())

    if words1 or words2:
        word_score = len(
            words1.intersection(words2)
        ) / len(
            words1.union(words2)
        )
    else:
        word_score = 0.0

    final_similarity = (
        sequence_score * 0.60
        + word_score * 0.40
    )

    return float(final_similarity)


def calculate_semantic_similarity(text1, text2):
    return calculate_text_similarity(
        text1,
        text2,
    )


def detect_duplicate(
    description,
    location,
    category,
):
    existing_reports = Report.objects.all()

    best_match = None
    highest_score = 0.0

    for report in existing_reports:
        description_score = (
            calculate_text_similarity(
                description,
                report.description,
            )
        )

        location_score = (
            calculate_text_similarity(
                location,
                report.location,
            )
        )

        category_score = (
            1.0
            if category == report.category
            else 0.0
        )

        final_score = (
            description_score * 0.60
            + location_score * 0.25
            + category_score * 0.15
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