import json

with open("static/dict_document_type_cls.json", "r", encoding="utf-8") as file:
    document_types = json.load(file)


def find_document_by_id(id_value):
    for obj in document_types:
        if obj["Id"] == id_value:
            return obj
    return None
