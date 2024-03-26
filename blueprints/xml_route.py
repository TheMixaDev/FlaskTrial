from flask import Blueprint, Response, request

from classes.DictionaryNullable import DictionaryNullable
from utils.xml_converter import dict_to_xml
from mappers.xml_mapper import map_response

xml_blueprint = Blueprint('xml', __name__)


@xml_blueprint.route("/xml", methods=['POST'])
def xml_handler():
    if not request.is_json:
        return Response("Route only accepts application/json data", 400)
    try:
        data = DictionaryNullable(request.get_json())
        response = map_response(data)
        return Response(dict_to_xml(response, "EntrantChoice"), mimetype='application/xml')
    except ImportError as e:
        return Response(f"Invalid property value provided: {str(e.msg)}", 400)
    except:
        return Response("Invalid JSON data provided", 400)
