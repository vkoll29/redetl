import re


def get_target_value(target_score):
    tokens = re.split(r'[\s><=,]+', target_score)
    if len(tokens) > 1:
        # Extract the second token
        second_token = tokens[1]
        # Replace occurrences of ''YES'' with YES
        return second_token.replace("''YES''", "YES")
    return target_score
