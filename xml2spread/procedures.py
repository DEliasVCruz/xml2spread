import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory
from tkinter.filedialog import askopenfilenames, asksaveasfilename
from tkinter.messagebox import askretrycancel
from zipfile import ZipFile

from xml2spread.utils import get_fecha_factura, get_id_factura, get_item_factura


def extract_and_write(files, result_file: tuple[str] | str):

    with TemporaryDirectory() as tmpdirname:

        for file in files:
            with ZipFile(file, mode="r") as archive:
                for member_file in archive.namelist():
                    if member_file.endswith(".XML"):
                        archive.extract(member_file, path=tmpdirname)

        temp_files_dir = Path(tmpdirname)

        with open(str(result_file), mode="w") as file:
            csv_writer = csv.writer(file, delimiter=",")

            csv_writer.writerow(["Descripcion", "Cantidad", "Factura", "Fecha"])

            for file in temp_files_dir.iterdir():
                root = ET.parse(file).getroot()
                id = get_id_factura(root)
                fecha = get_fecha_factura(root)
                items = get_item_factura(root)
                for item in items:
                    item.extend([id, fecha])
                    csv_writer.writerow(item)


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
            title="Seleccione archivo a guardar",
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
