import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest as pt

from xml2spread.utils import get_fecha_factura, get_id_factura, get_item_factura

roots = []
ids = []

fechas = [
    "30/07/2022",
    "22/07/2022",
    "11/07/2022",
    "22/07/2022",
    "22/07/2022",
    "30/07/2022",
    "14/07/2022",
    "11/07/2022",
    "09/07/2022",
    "09/07/2022",
]

for file in Path().cwd().joinpath("tests", "fixtures", "xml_facturas").iterdir():
    root = ET.parse(file).getroot()
    factura_id = re.findall(r"E001-\d{4}", file.name)
    ids.append(factura_id[0])
    roots.append(root)


@pt.mark.parametrize(
    "xml_root,expected_id", [(root, id) for root, id in zip(roots, ids)]
)
def test_get_id_facutra(xml_root, expected_id):
    assert get_id_factura(xml_root) == expected_id


@pt.mark.parametrize(
    "xml_root,expected_fecha", [(root, fecha) for root, fecha in zip(roots, fechas)]
)
def test_get_fecha_factura(xml_root, expected_fecha):
    assert get_fecha_factura(xml_root) == expected_fecha


