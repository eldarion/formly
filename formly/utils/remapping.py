import json


def create_answer_list(fieldresults):

    answer_list = []

    for result in fieldresults:
        if type(result.answer['answer']) is not dict:
            answers = json.loads(result.answer['answer'])
        else:
            answers = result.answer['answer']

        if type(answers) is unicode:
            answer_list.append(answers.strip().upper())
        else:
            for answer in answers:
                answer_list.append(answer.strip().upper())

    # Quickly remove duplicates
    return list(set(answer_list))
