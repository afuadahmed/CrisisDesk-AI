# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# from reports.models import Report


# DUPLICATE_THRESHOLD = 0.75

# model = SentenceTransformer(
#     "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# )


# def calculate_semantic_similarity(text1, text2):
#     embeddings = model.encode([text1, text2])

#     similarity = cosine_similarity(
#         [embeddings[0]],
#         [embeddings[1]]
#     )[0][0]

#     return float(similarity)


# def detect_duplicate(description, location, category):
#     existing_reports = Report.objects.all()

#     best_match = None
#     highest_score = 0

#     for report in existing_reports:
#         description_score = calculate_semantic_similarity(
#             description,
#             report.description
#         )

#         location_score = calculate_semantic_similarity(
#             location,
#             report.location
#         )

#         category_score = (
#             1.0 if category == report.category else 0.0
#         )

#         final_score = (
#             description_score * 0.60
#             + location_score * 0.25
#             + category_score * 0.15
#         )

#         if final_score > highest_score:
#             highest_score = final_score
#             best_match = report

#     if best_match and highest_score >= DUPLICATE_THRESHOLD:
#         return {
#             "possible_duplicate": True,
#             "matched_report": best_match,
#             "similarity_score": round(highest_score, 4),
#         }

#     return {
#         "possible_duplicate": False,
#         "matched_report": None,
#         "similarity_score": round(highest_score, 4),
#     }

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from reports.models import Report


DUPLICATE_THRESHOLD = 0.75

_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

    return _model


def calculate_semantic_similarity(text1, text2):
    model = get_model()

    embeddings = model.encode([text1, text2])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(similarity)


def detect_duplicate(description, location, category):
    existing_reports = Report.objects.all()

    best_match = None
    highest_score = 0

    for report in existing_reports:
        description_score = calculate_semantic_similarity(
            description,
            report.description
        )

        location_score = calculate_semantic_similarity(
            location,
            report.location
        )

        category_score = (
            1.0 if category == report.category else 0.0
        )

        final_score = (
            description_score * 0.60
            + location_score * 0.25
            + category_score * 0.15
        )

        if final_score > highest_score:
            highest_score = final_score
            best_match = report

    if best_match and highest_score >= DUPLICATE_THRESHOLD:
        return {
            "possible_duplicate": True,
            "matched_report": best_match,
            "similarity_score": round(highest_score, 4),
        }

    return {
        "possible_duplicate": False,
        "matched_report": None,
        "similarity_score": round(highest_score, 4),
    }