import tkinter as tk
from tkinter import ttk


class PanelProgreso(ttk.Frame):
    def __init__(self, contenedor):
        super().__init__(contenedor)

        self.porcentaje = tk.DoubleVar(value=0)
        self.estado = tk.StringVar(value="Listo para descargar")

        self.barra = ttk.Progressbar(
            self,
            variable=self.porcentaje,
            maximum=100,
            mode="determinate"
        )
        self.barra.pack(fill="x")

        self.etiqueta_porcentaje = ttk.Label(self, text="0 %")
        self.etiqueta_porcentaje.pack(pady=(5, 0))

        self.etiqueta_estado = ttk.Label(
            self,
            textvariable=self.estado
        )
        self.etiqueta_estado.pack()

    def actualizar(self, estado, porcentaje=None):
        self.estado.set(estado)

        if porcentaje is not None:
            valor = max(0, min(100, porcentaje))
            self.porcentaje.set(valor)
            self.etiqueta_porcentaje.config(text=f"{valor:.1f} %")