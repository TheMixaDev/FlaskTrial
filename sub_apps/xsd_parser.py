from xmlschema import XMLSchema

xsd_schema = XMLSchema("Add_Entrant_List.xsd")
root_element_name = next(iter(xsd_schema.elements))
root_element = xsd_schema.elements[f"{root_element_name}"]


def element_to_dict(element):
    data = {}
    for child in element.iterchildren():
        if child.type is not None and child.type.is_simple():
            data[child.name] = None
        else:
            data[child.name] = element_to_dict(child)
    return data


if __name__ == "__main__":
    xml_structure_dict = element_to_dict(root_element)
    print(xml_structure_dict)
