def get_target_score(target_score):
    tokens = target_score.split(',')
    if len(tokens) > 1:
        return tokens[1].strip()
    return None
