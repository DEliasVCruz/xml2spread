import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Tuple

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


def get_tax_info(root: ET.Element) -> Tuple[float, float, float]:
    tax_elem = root.find("cac:TaxTotal", namespaces=namespaces)

    tax_info = tax_elem.find("cac:TaxSubtotal", namespaces=namespaces) if tax_elem is not None else None

    base_imponible, igv = [float(str(value.text)) for value in tax_info[:2]] if tax_info is not None else (None, None)
    total = (base_imponible + igv) if (base_imponible is not None) and (igv is not None) else 0

    return (base_imponible or 0, igv or 0, round(number=total, ndigits=2))


def get_client_name(root: ET.Element) -> str:
    customer = root.find("cac:AccountingCustomerParty", namespaces=namespaces)
    party = customer.find("cac:Party", namespaces=namespaces) if customer is not None else None
    entity = party.find("cac:PartyLegalEntity", namespaces=namespaces) if party is not None else None
    name = entity.findtext("cbc:RegistrationName", namespaces=namespaces) if entity is not None else None

    return (name or "")


if __name__ == "__main__":
    pass
