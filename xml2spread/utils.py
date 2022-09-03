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


def get_fecha_factura(root: ET.Element) -> str:
    factura_fecha = root.findtext("cbc:IssueDate", namespaces=namespaces)
    factura_fecha = datetime.strptime(str(factura_fecha), "%Y-%m-%d").strftime(
        "%d/%m/%Y"
    )

    return factura_fecha


def get_item_factura(root: ET.Element) -> List[List]:
    items: List[List] = []
    invoice_lines = root.findall("cac:InvoiceLine", namespaces=namespaces)

    for line in invoice_lines:
        cantidad = int(
            float(str(line.findtext("cbc:InvoicedQuantity", namespaces=namespaces)))
        )

        item = line.find("cac:Item", namespaces=namespaces)

        if item is not None:
            descripcion = item.findtext("cbc:Description", namespaces=namespaces)
            items.append([descripcion, cantidad])

    return items


if __name__ == "__main__":
    pass
