import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest as pt

from xml2spread.utils import get_fecha_factura, get_id_factura, get_item_factura

fc_roots = []
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
    fc_roots.append(root)


# @pt.mark.skip
@pt.mark.parametrize(
    "xml_root,expected_id", [(root, id) for root, id in zip(fc_roots, ids)]
)
def test_get_id_facutra(xml_root, expected_id):
    assert get_id_factura(xml_root) == expected_id


# @pt.mark.skip
@pt.mark.parametrize(
    "xml_root,expected_fecha", [(root, fecha) for root, fecha in zip(fc_roots, fechas)]
)
def test_get_fecha_factura(xml_root, expected_fecha):
    assert get_fecha_factura(xml_root) == expected_fecha


# @pt.mark.skip
def test_get_one_item_factura():
    output = get_item_factura(fc_roots[-1])
    expected_item = [["TUBO INOX 101.6X1.5X6000MM C-304 BRILLANTE", 6]]

    assert output == expected_item


# @pt.mark.skip
def test_get_two_item_factura():
    output = get_item_factura(fc_roots[4])
    expected_item = [
        ["TUBO INOX 50.8X1.5X6000MM C-304 BRILLANTE", 60],
        ["TUBO INOX 38.1X1.5X6000MM C-304 BRILLANTE", 50],
    ]

    assert output == expected_item


# @pt.mark.skip
def test_get_three_item_factura():
    output = get_item_factura(fc_roots[6])
    expected_item = [
        ["TUBO INOX 50.8X1.5X6000MM C-304 BRILLANTE", 2],
        ["TUBO INOX 15.9X1.56X6000MM C-304 BRILLANTE", 10],
        ["TUBO INOX 15.9X1.5X6000MM C-3904 BRILLANTE", 1],
    ]

    assert output == expected_item
