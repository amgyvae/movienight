def calculate_group_score(scores):
    if not scores:
        return 0

    average = sum(scores) / len(scores)
    minimum = min(scores)

    group_score = 0.6 * average + 0.4 * minimum

    return round(group_score, 2)


def calculate_final_score(scores, popularity):
    group_score = calculate_group_score(scores)

    final_score = group_score + 0.2 * popularity

    return final_score