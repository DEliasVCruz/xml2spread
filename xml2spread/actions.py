from tkinter.messagebox import askokcancel, askyesno, showinfo

from xml2spread.globals import DIRECTORY_FILES, RESULT_FILES, ROOT_WIN
from xml2spread.procedures import extract_and_write, selector


def select_action():
    zip_files = ""
    result_file = ""

    retry = True
    while retry:
        zip_files, retry = selector("open", "zip", retry)

    if not zip_files:
        return

    retry = True
    while retry:
        result_file, retry = selector("save", "csv", retry)

    if not result_file:
        return

    extract_and_write(zip_files, result_file)

    DIRECTORY_FILES.set("\n".join(zip_files))
    RESULT_FILES.set(str(result_file))

    showinfo(
        title="Archivos procesados",
        message=f"Se guardaron los resultados en {result_file}",
    )

    continuing = askyesno(
        title="Continuar", message="Quieres continuar exportando facturas?"
    )
    if not continuing:
        ROOT_WIN.destroy()


