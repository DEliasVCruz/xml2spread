import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory
from tkinter.filedialog import askopenfilenames, asksaveasfilename
from tkinter.messagebox import askretrycancel
from zipfile import ZipFile

from xml2spread.utils import get_fecha_factura, get_id_factura, get_item_factura, get_tax_info, get_client_name


def extract_and_write(files, result_files_name: tuple[str] | str):

    with TemporaryDirectory() as tmpdirname:

        detail_items = []
        facturas_monto = []

        for file in files:
            with ZipFile(file, mode="r") as archive:
                for member_file in archive.namelist():
                    if member_file.endswith(".XML"):
                        archive.extract(member_file, path=tmpdirname)

        temp_files_dir = Path(tmpdirname)

        for file in temp_files_dir.iterdir():
            root = ET.parse(file).getroot()
            id = get_id_factura(root)
            fecha = get_fecha_factura(root)
            items = get_item_factura(root)

            factura_monto: list[float | str | list] = [id, fecha, get_client_name(root)]
            factura_monto.extend(list(get_tax_info(root)))

            facturas_monto.append(factura_monto)

            for item in items:
                item.extend([id, fecha])

            detail_items.extend(items)

        file = Path(str(result_files_name))
        file = file.parent / file.stem
        detalle_file = f"{str(file)}_detalle.csv"
        ammount_file = f"{str(file)}_montos.csv"

        with open(detalle_file, mode="w") as file:
            csv_writer = csv.writer(file, delimiter=",")

            csv_writer.writerow(["Descripcion", "Cantidad", "Factura", "Fecha"])
            for item in detail_items:
                csv_writer.writerow(item)

        with open(ammount_file, mode="w") as file:
            csv_writer = csv.writer(file, delimiter=",")

            csv_writer.writerow(["Factura", "Fecha", "Cliente", "Base Imponible", "IGV", "Total"])
            for factura in facturas_monto:
                csv_writer.writerow(factura)


def selector(action: str, file_type: str, retry: bool) -> tuple[tuple[str] | str, bool]:

    if action == "open":
        selection = askopenfilenames(
            title=f"Seleccione los archivos {file_type}",
            filetypes=(
                (f"Archivos {file_type}", f"*.{file_type}"),
                ("Todos los archivos", "*.*"),
            ),
        )
    else:
        selection = asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=file_type,
            filetypes=(
                (f"Archivos {file_type}", f"*.{file_type}"),
                ("Todos los archivos", "*.*"),
            ),
            title="Seleccione nombre para archivos a guardar",
        )

    if selection:
        retry = False
    else:
        retry = askretrycancel(
            title="Problema seleccion archivos",
            message="No se ha seleccionado un archivo, quiere volver a seleccionar?",
        )

    return (selection, retry)


if __name__ == "__main__":
    pass
