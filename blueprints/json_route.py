from flask import Blueprint, jsonify, request, Response

from classes.DictionaryNullable import DictionaryNullable
from utils.xml_converter import xml_to_dict
from mappers.json_mapper import map_entrant

json_blueprint = Blueprint('json', __name__)


@json_blueprint.route("/json", methods=['POST'])
def json_handler():
    if request.content_type != 'application/xml':
        return Response("Route accepts only application/xml data", 400)
    try:
        data = xml_to_dict(request.data)
        result = []
        for entry in data['SuccessResultList']:
            result.append(map_entrant(DictionaryNullable(entry)))
        return jsonify(result)
    except ImportError as e:
        return Response(f"Invalid property value provided: {e.msg}", 400)
    except:
        return Response("Invalid XML data provided", 400)
