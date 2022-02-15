from choices import choices


def get_object_by_id(object_id, object_list):
    return list(filter(lambda obj: obj["id"] == object_id, object_list))[0]


questions = [
    { "id": 1, "choices": [ get_object_by_id(1, choices), get_object_by_id(2, choices) ] },
    { "id": 2, "choices": [ get_object_by_id(3, choices), get_object_by_id(4, choices) ] },
    { "id": 3, "choices": [ get_object_by_id(5, choices), get_object_by_id(6, choices) ] },
    { "id": 4, "choices": [ get_object_by_id(7, choices), get_object_by_id(8, choices) ] },
    { "id": 5, "choices": [ get_object_by_id(9, choices), get_object_by_id(10, choices) ] },
    { "id": 6, "choices": [ get_object_by_id(11, choices), get_object_by_id(12, choices) ] },
    { "id": 7, "choices": [ get_object_by_id(13, choices), get_object_by_id(14, choices) ] },
    { "id": 8, "choices": [ get_object_by_id(15, choices), get_object_by_id(16, choices) ] },
    { "id": 9, "choices": [ get_object_by_id(17, choices), get_object_by_id(18, choices) ] },
    { "id": 10, "choices": [ get_object_by_id(19, choices), get_object_by_id(20, choices) ] },
    { "id": 11, "choices": [ get_object_by_id(21, choices), get_object_by_id(22, choices) ] },
    { "id": 12, "choices": [ get_object_by_id(23, choices), get_object_by_id(24, choices) ] },
    { "id": 13, "choices": [ get_object_by_id(25, choices), get_object_by_id(26, choices) ] },
    { "id": 14, "choices": [ get_object_by_id(27, choices), get_object_by_id(28, choices) ] },
    { "id": 15, "choices": [ get_object_by_id(29, choices), get_object_by_id(30, choices) ] },
    { "id": 16, "choices": [ get_object_by_id(31, choices), get_object_by_id(32, choices) ] },
    { "id": 17, "choices": [ get_object_by_id(33, choices), get_object_by_id(34, choices) ] },
    { "id": 18, "choices": [ get_object_by_id(35, choices), get_object_by_id(36, choices) ] },
    { "id": 19, "choices": [ get_object_by_id(37, choices), get_object_by_id(38, choices) ] },
    { "id": 20, "choices": [ get_object_by_id(39, choices), get_object_by_id(40, choices) ] },
]



