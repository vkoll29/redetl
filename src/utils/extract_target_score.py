def get_target_score(target_score):
    if target_score is None:
        return None
    tokens = target_score.split(',')
    if len(tokens) > 1:
        return tokens[1].strip()
    return None
