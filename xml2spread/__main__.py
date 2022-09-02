from tkinter import ttk

from xml2spread.actions import on_closing_action, select_action
from xml2spread.globals import ROOT_WIN


def main():
    ROOT_WIN.title("Convertidor de XMLs de Facturas")

    btn_select_files = ttk.Button(
        ROOT_WIN,
        text="Seleccionar",
        command=select_action,
    )

    lbl_message = ttk.Label(
        ROOT_WIN,
        text="Seleccione una carpeta de facturas y un archivo donde guardar los resultados",
    )

    lbl_message.pack()
    btn_select_files.pack(expand=True)

    ROOT_WIN.protocol("WM_DELETE_WINDOW", on_closing_action)
    ROOT_WIN.mainloop()


if __name__ == "__main__":
    main()
