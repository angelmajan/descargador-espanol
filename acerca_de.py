import tkinter as tk
from tkinter import ttk
import webbrowser
from ventanas import centrar_ventana


def mostrar_acerca_de(ventana_principal):
    dialogo = tk.Toplevel(ventana_principal)
    dialogo.title("Acerca de")
    dialogo.resizable(False, False)
    dialogo.transient(ventana_principal)

    contenido = ttk.Frame(dialogo, padding=20)
    contenido.pack(fill="both", expand=True)

    ttk.Label(
        contenido,
        text="Descargador de vídeos en español",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=(0, 10))

    ttk.Label(
        contenido,
        text="Desarrollado por Ángel Maján"
    ).pack(pady=(0, 15))

    ttk.Button(
        contenido,
        text="Web: https://angelmajan.es/",
        command=lambda: webbrowser.open(
            "https://angelmajan.es/"
        )
    ).pack(fill="x", pady=5)

    ttk.Button(
        contenido,
        text="Correo: angel@angelmajan.es",
        command=lambda: webbrowser.open(
            "mailto:angel@angelmajan.es"
        )
    ).pack(fill="x", pady=5)

    ttk.Button(
        contenido,
        text="Cerrar",
        command=dialogo.destroy
    ).pack(pady=(15, 0))
    centrar_ventana(dialogo, ventana_principal)