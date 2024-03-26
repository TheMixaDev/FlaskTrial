import utils.validator

from flask import current_app
from utils.document_type import find_document_by_id


def map_fields(data, document):
    if document is None:
        return {}
    xml_names = {
        "SubdivisionCode": "passport_org_code",
        "IdOksm": "citizenship_id",
        "Surname": "second_name",
        "Name": "first_name",
        "Patronymic": "middle_name",
        "ExpirationDate": "passport_endda",
        "ProlongationDate": "passport_begda"
    }
    result = {}
    for field in document['FieldsDescription']['fields']:
        field_data = data[xml_names[field['xml_name']]]
        if field['type'] == 'character':
            field_data = utils.validator.string(field_data, 1024)
        elif field['type'] == 'integer':
            field_data = utils.validator.positive_integer(field_data)
        elif field['type'] == 'date':
            field_data = utils.validator.date(field_data)
        if field['not_null'] and (len(str(field_data)) < 1 or field_data == -1):
            if current_app.config['XML_VALIDATION_ENABLED']:
                raise ImportError(data[xml_names[field['xml_name']]])
        result[field['xml_name']] = field_data
    return result


def map_document(data):
    document_id = utils.validator.positive_integer(data['passport_type_id'])+100000
    document = find_document_by_id(document_id)
    return {
        'IdDocumentType': document_id,
        'DocName': document['Name'] if document is not None else "",
        'DocSeries': utils.validator.string(data['passport_series'], 20),
        'DocNumber': utils.validator.string(data['passport_number'], 50),
        'IssueDate': utils.validator.date(data['passport_begda']),
        'DocOrganization': utils.validator.string(data['passport_issued_by'], 500),
        'Fields': map_fields(data, document)
    }


def map_address(data, prefix):
    address = {
        'IsRegistration': len(prefix) == 0,
        'FullAddr': utils.validator.string((
                        utils.validator.parse_null(data[f'{prefix}street']) + ' ' +
                        utils.validator.parse_null(data[f'{prefix}house']) + ' ' +
                        utils.validator.parse_null(data[f'{prefix}building']) + ' ' +
                        utils.validator.parse_null(data[f'{prefix}letter']) + ' ' +
                        utils.validator.parse_null(data[f'{prefix}building2']) + ' ' +
                        utils.validator.parse_null(data[f'{prefix}flat']) + ' ' +
                        utils.validator.parse_null(data[f'{prefix}post_index'])
                    ), 1024),
        'IdRegion': utils.validator.positive_integer(data[f'{prefix}residence_country_id']),
        'City': utils.validator.string((
                        utils.validator.parse_null(data[f'{prefix}address_txt1']) + ' ' +
                        utils.validator.parse_null(data[f'{prefix}address_txt2']) + ' ' +
                        utils.validator.parse_null(data[f'{prefix}address_txt3']) + ' ' +
                        utils.validator.parse_null(data[f'{prefix}address_txt4'])
                ), 256)
    }
    if len(address['FullAddr']) == 0:
        return None
    return address


def map_addresses(data):
    result = {}
    main_address = map_address(data, "")
    if main_address is not None:
        result['Address'] = main_address
    if data['has_another_living_address']:
        second_address = map_address(data, "second_")
        if second_address is not None:
            result['Address__clone'] = second_address
    return result


def map_response(data):
    return {
        'Guid': data['id'],
        'AddEntrant': {
            'Identification': map_document(data),
            'Snils': utils.validator.snils(data['snils']),
            'IdGender': utils.validator.positive_integer(data['dict_sex_id']),
            'Birthday': utils.validator.date(data['birthday']),
            'Birthplace': utils.validator.string(data['motherland'], 500),
            'Phone': utils.validator.string(data['tel_mobile'], 120),
            'Email': utils.validator.string(data['email'], 150),
            'IdOksm': utils.validator.positive_integer(data['citizenship_id']),
            'FreeEducationReason': {
                'IdFreeEducationReason': utils.validator.positive_integer(data['applied_by']),
                'IdOksmFreeEducationReason': utils.validator.positive_integer(data['institution_country_id'])
            },
            'AddressList': map_addresses(data)
        }
    }