from pathlib import Path


def centrar_ventana(ventana, referencia=None):
    ventana.update_idletasks()

    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()

    if referencia is None:
        x = (ventana.winfo_screenwidth() - ancho) // 2
        y = (ventana.winfo_screenheight() - alto) // 2
    else:
        referencia.update_idletasks()

        x = (
            referencia.winfo_rootx()
            + (referencia.winfo_width() - ancho) // 2
        )
        y = (
            referencia.winfo_rooty()
            + (referencia.winfo_height() - alto) // 2
        )

    ventana.geometry(f"{ancho}x{alto}{x:+d}{y:+d}")

def aplicar_icono(ventana):
    ruta_icono = Path(__file__).resolve().parent / "icono_AM.ico"
    ventana.iconbitmap(default=str(ruta_icono))
