def calculate_health_score(results):

    score = 0

    for sensor in results.values():

        if sensor["status"] == "GREEN":
            score += 10

        elif sensor["status"] == "YELLOW":
            score += 5

    max_score = len(results) * 10

    return round((score / max_score) * 100, 2)