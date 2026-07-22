def generate_recommendations(results):

    recommendations = []

    for sensor, details in results.items():

        if details["status"] == "RED":

            recommendations.append(
                f"{sensor} requires immediate attention."
            )

        elif details["status"] == "YELLOW":

            recommendations.append(
                f"{sensor} should be serviced soon."
            )

    if not recommendations:

        recommendations.append(
            "Vehicle is in excellent condition."
        )

    return recommendations


def _join_names(names):
    """Turns ['A', 'B', 'C'] into 'A, B and C' (or 'A and B', or just 'A')."""
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " and " + names[-1]


def generate_summary_paragraphs(vehicle_id, score, results):
    """
    Builds a realistic, paragraph-style condition summary for the vehicle,
    in place of a flat bullet-point list. Returns a list of paragraph strings.
    """
    total = len(results)
    green = [name for name, d in results.items() if d["status"] == "GREEN"]
    yellow = [name for name, d in results.items() if d["status"] == "YELLOW"]
    red = [name for name, d in results.items() if d["status"] == "RED"]

    if score >= 85:
        condition_phrase = "in excellent overall condition"
    elif score >= 65:
        condition_phrase = "in generally good condition, with a few areas that need attention"
    elif score >= 40:
        condition_phrase = "showing noticeable signs of wear and needs prompt attention"
    else:
        condition_phrase = "in poor condition and needs immediate servicing"

    paragraphs = []

    paragraphs.append(
        f"Vehicle {vehicle_id} is currently {condition_phrase}, with an overall "
        f"health score of {score}% based on {total} monitored parameters."
    )

    if green:
        paragraphs.append(
            f"{len(green)} of {total} parameters, including {_join_names(green)}, "
            f"are operating within their ideal range and require no action at this time."
        )

    if yellow:
        verb = "are" if len(yellow) != 1 else "is"
        noun = "parameters" if len(yellow) != 1 else "parameter"
        paragraphs.append(
            f"{len(yellow)} {noun} - {_join_names(yellow)} - {verb} approaching "
            f"the upper limit of the safe range. These should be inspected and, "
            f"if needed, serviced at the next scheduled maintenance visit to "
            f"prevent them from developing into a more serious issue."
        )

    if red:
        verb = "have" if len(red) != 1 else "has"
        noun = "parameters" if len(red) != 1 else "parameter"
        paragraphs.append(
            f"{len(red)} {noun} - {_join_names(red)} - {verb} moved beyond the "
            f"safe operating range and {'require' if len(red) != 1 else 'requires'} "
            f"immediate attention. Continuing to operate the vehicle without "
            f"addressing these could increase the risk of breakdown or further "
            f"mechanical damage, and a service visit is strongly recommended as "
            f"soon as possible."
        )
    else:
        paragraphs.append(
            "No parameters are currently in a critical state, so there are no "
            "immediate safety concerns as of this report."
        )

    return paragraphs