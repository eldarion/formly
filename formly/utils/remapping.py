def _normalize_answer(answer):
    answer = answer.strip().upper()
    return " ".join([a for a in answer.split(" ") if a])


def create_answer_list(fieldresults):

    answer_set = set()

    for result in fieldresults:
        answers = result.answer["answer"]

        for answer in answers:
            normalized_answer = _normalize_answer(answer)
            if normalized_answer:
                answer_set.add(normalized_answer)

    # Quickly remove duplicates
    return list(answer_set)
