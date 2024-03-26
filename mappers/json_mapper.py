import json

from classes.DictionaryNullable import DictionaryNullable

with open("static/dummy_response_data.json", "r", encoding="utf-8") as file:
    dummy_data = json.load(file)


def passport_index(i):
    if i == 0:
        return ""
    elif i == 1:
        return "old_"
    elif i == 2:
        return "paid_"
    return "additional_"


def address_index(i):
    if i == 0:
        return ""
    if i == 1:
        return "second_"
    return "additional_"


def map_passport(data, prefix):
    return {
        f"{prefix}passport_type_id": data['IdDocumentType'],
        f"{prefix}passport_series": data['DocSeries'],
        f"{prefix}passport_number": data['DocNumber'],
        f"{prefix}passport_begda": data['IssueDate'],
        f"{prefix}passport_endda": None,
        f"{prefix}passport_org_code": None,
        f"{prefix}passport_issued_by": data['DocOrganization'],
    }


def map_address(data, prefix):
    splitted = DictionaryNullable({})
    if data is not None and data['FullAddr'] is not None:
        splitted = DictionaryNullable({i: part for i, part in enumerate(data['FullAddr'].split(' '))})
    return {
        f"{prefix}residence_country_id": data['IdRegion'],
        f"{prefix}kladr_1": None,
        f"{prefix}kladr_2": None,
        f"{prefix}kladr_3": None,
        f"{prefix}kladr_4": None,
        f"{prefix}address_txt1": splitted[0],
        f"{prefix}address_txt2": splitted[1],
        f"{prefix}address_txt3": splitted[2],
        f"{prefix}address_txt4": splitted[3],
        f"{prefix}street": splitted[4],
        f"{prefix}house": splitted[5],
        f"{prefix}building": splitted[6],
        f"{prefix}letter": splitted[7],
        f"{prefix}building2": splitted[8],
        f"{prefix}flat": splitted[9],
        f"{prefix}post_index": splitted[10],
        f"has_no_{prefix}street": False if splitted[4] is None else True,
        f"has_no_{prefix}house": False if splitted[5] is None else True,
    }


def update_with_array(result, map_function, array, limit):
    for i in range(limit):
        document = DictionaryNullable({})
        if i < len(array):
            document = DictionaryNullable(array[i])
        result.update(map_function(document, passport_index(i)))


def map_entrant(data):
    result = {
        "id": data['Guid'],
        "user_id": data['IdObject'],
        "first_name": data['Name'],
        "second_name": data['Surname'],
        "middle_name": data['Patronymic'],
        "dict_sex_id": data['IdGender'],
        "birthday": data['Birthday'],
        "citizenship_id": data['IdOksm'],
        "motherland": data['Birthplace'],
        "email": data['Email'],
        "tel_mobile": data['Phone'],
        "tel_mobile_frn": data['Phone'],
        "institution_country_id": DictionaryNullable(data['FreeEducationReason'])['IdOksmFreeEducationReason'],
        "applied_by": DictionaryNullable(data['FreeEducationReason'])['IdFreeEducationReason'],
        "diploma_date": data['DateAvailabilityEduDoc'],
        "snils": data['Snils'],
        "has_original_edu_diploma": data['AvailabilityEduDoc'],
        "is_without_snils": False if len(data['Snils']) > 0 else True,
        "has_another_living_address": len(data['AddressList']) > 1,
        "has_old_passport": len(data['DocumentList']) > 1,
        "paid_by_another_human": len(data['DocumentList']) > 2,
        "created_at": None,
        "updated_at": None,
    }

    update_with_array(result, map_passport, data['DocumentList'], 3)
    update_with_array(result, map_address, data['AddressList'], 2)
    result.update(dummy_data)

    return result
