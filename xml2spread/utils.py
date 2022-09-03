import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List

namespaces = {
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
}


def get_id_factura(root: ET.Element) -> str:
    factura_id = root.findtext("cbc:ID", namespaces=namespaces)

    return str(factura_id)


