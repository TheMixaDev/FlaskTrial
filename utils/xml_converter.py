from xml.etree import ElementTree


def to_xml(parent, data):
    for key, value in data.items():
        if isinstance(value, dict):
            child = ElementTree.SubElement(parent, key.split("__clone")[0])
            to_xml(child, value)
        else:
            ElementTree.SubElement(parent, key.split("__clone")[0]).text = str(value)


def dict_to_xml(dict_data, root_tag="root"):
    root = ElementTree.Element(root_tag)
    to_xml(root, dict_data)
    return ElementTree.tostring(root, encoding='utf8', method='xml')


def to_dict(element):
    data = {}
    for child in element:
        if child.tag == "DocumentList" or child.tag == "AddressList" or child.tag == "SuccessResultList":
            data[child.tag] = [to_dict(item) for item in child]
        elif child.tag == "FreeEducationReason":
            data[child.tag] = to_dict(child)
        else:
            data[child.tag] = child.text.strip() if child.text else None
    return data


def xml_to_dict(xml_data):
    return to_dict(ElementTree.fromstring(xml_data))
