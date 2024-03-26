## Flask Conversion Service

### Overview

This Flask server provides conversion between JSON and XML formats.

### Requirements

- Python 3.11
- Flask
- xmlschema

### Installation
*Installation guide for Linux subsystems and WSL*
1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```
2. Install the required libraries:
```bash
pip install -r requirements.txt
```

### Usage

1. Run the Flask application:
```bash
python3 main.py
```
2. Send POST requests to the following endpoints:
- `/json`: Convert XML data to JSON.
- `/xml`: Convert JSON data to XML.

**Note:** The request `Content-Type` header should be set to `application/json` for JSON data and `application/xml` for XML data.

### XML Validation

XML validation panic with XSD schemas is optional and can be controlled by the `XML_VALIDATION_ENABLED` configuration parameter in `config.py`.

### Configuration

The application configuration is stored in `config.py`. You can modify the following parameter:

- `XML_VALIDATION_ENABLED`: Controls whether XML panic is performed (default: `False`).

### File Structure

```
flask_conversion_service/
├── blueprints/
│ ├── json_route.py
│ └── xml_route.py
├── classes/
│ └── DictionaryNullable.py
├── config.py
├── main.py
├── mappers/
│ ├── json_mapper.py
│ └── xml_mapper.py
├── static/
│ └── dict_document_type_cls.json
├── utils/
│ ├── document_type.py
│ ├── validator.py
│ └── xml_converter.py
└── venv/ # Virtual environment (if created)
```

### Notes

Some JSON keys do not directly map to XML tags by name. Full manual mapping provided in `mappers` modules.

**Direct JSON to XML parsing:**

| XML Name | JSON Name |
|-|-|
| SubdivisionCode | passport_org_code |
| IdOksm | citizenship_id |
| Surname | second_name |
| Name | first_name |
| Patronymic | middle_name |
| ExpirationDate | passport_endda |
| ProlongationDate | passport_begda |
| IdDocumentType | passport_type_id |
| DocSeries | passport_series |
| DocNumber | passport_number |
| IssueDate | passport_begda |
| DocOrganization | passport_issued_by |
| Snils | snils |
| IdGender | dict_sex_id |
| Birthday | birthday |
| Birthplace | motherland |
| Phone | tel_mobile |
| Email | email |
| IdOksm | citizenship_id |
| FreeEducationReason | *(nested dictionary)* |
| - IdFreeEducationReason | applied_by |
| - IdOksmFreeEducationReason | institution_country_id |

**Direct XML to JSON parsing:**
| JSON Name | XML Name |
|-|-|
| passport_type_id | IdDocumentType |
| passport_series | DocSeries |
| passport_number | DocNumber |
| passport_begda | IssueDate |
| passport_issued_by | DocOrganization |
| residence_country_id | IdRegion |
| birthday | Birthday |
| email | Email |
| tel_mobile| Phone |
| tel_mobile_frn | Phone|
| has_original_edu_diploma | AvailabilityEduDoc |
| has_another_living_address | AddressList  |
| has_old_passport| DocumentList  |

### Example Requests

Postman collection with requests and examples can be accessed at `FlaskTrial.postman_collection.json` file.

**Convert JSON to XML:**

```
curl -X POST -H "Content-Type: application/json" -d @app_info.json http://localhost:5000/xml
```

**Convert XML to JSON:**

```
curl -X POST -H "Content-Type: application/xml" -d @get_entrant_list.xml http://localhost:5000/json
```
