from util.utilities import topic_dict_create


def response(*args):
    final_response = {}
    for each in args:
        final_response.update(each)

    topics = set(topic_dict_create().values())

    source_to_remove = []
    for each in final_response.keys():
        if each.endswith('source'):
            source_to_remove.append(each)

    for each in source_to_remove:
        final_response.pop(each)

    for each in topics:
        if not final_response.get(each):
            final_response[each] = False
    return final_response
