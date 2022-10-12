import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest as pt

from xml2spread.utils import (
    get_tax_info,
    get_fecha_factura,
    get_id_factura,
    get_item_factura,
    get_client_name
)

fc_roots = []
mnt_roots = []
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

ammount_values = [(35.61, 6.41, 42.02), (5796.61, 1043.39, 6840.00), (4766.10, 857.9, 5624.00)]
client_names = ["TRINY RENTAL SOCIEDAD ANONIMA CERRADA", "INVERSION INOX GASPAR E.I.R.L.", "COMERCIALIZADORA & INVERSIONES CONDOR  S.A.C."]

for file in Path().cwd().joinpath("tests", "fixtures", "xml_facturas").iterdir():
    root = ET.parse(file).getroot()
    factura_id = re.findall(r"E001-\d{4}", file.name)
    ids.append(factura_id[0])
    fc_roots.append(root)

for file in Path().cwd().joinpath("tests", "fixtures", "xml_montos").iterdir():
    root = ET.parse(file).getroot()
    mnt_roots.append(root)


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


# @pt.mark.skip
@pt.mark.parametrize(
    "xml_root,expected_ammounts",
    [(root, ammounts) for root, ammounts in zip(mnt_roots, ammount_values)],
)
def test_get_tax_info(xml_root, expected_ammounts):
    output = get_tax_info(xml_root)
    assert output == expected_ammounts


# @pt.mark.skip
@pt.mark.parametrize(
    "xml_root,expected_names",
    [(root, name) for root, name in zip(mnt_roots, client_names)],
)
def test_get_client_name(xml_root, expected_names):
    output = get_client_name(xml_root)
    assert output == expected_names
