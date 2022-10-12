from tkinter.messagebox import askokcancel, askyesno, showinfo

from xml2spread.globals import DIRECTORY_FILES, RESULT_FILES, ROOT_WIN
from xml2spread.procedures import extract_and_write, selector


def select_action():
    zip_files = ""
    result_files_name = ""

    retry = True
    while retry:
        zip_files, retry = selector("open", "zip", retry)

    if not zip_files:
        return

    retry = True
    while retry:
        result_files_name, retry = selector("save", "csv", retry)

    if not result_files_name:
        return

    extract_and_write(zip_files, result_files_name)

    DIRECTORY_FILES.set("\n".join(zip_files))
    RESULT_FILES.set(str(result_files_name))

    showinfo(
        title="Archivos procesados",
        message=f"Se guardaron los resultados en {result_files_name}",
    )

    continuing = askyesno(
        title="Continuar", message="Quieres continuar exportando facturas?"
    )
    if not continuing:
        ROOT_WIN.destroy()


def on_closing_action():
    if askokcancel("Salir", "Quieres salir?"):
        ROOT_WIN.destroy()


if __name__ == "__main__":
    pass
