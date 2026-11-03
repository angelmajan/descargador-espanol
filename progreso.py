import tkinter as tk
from tkinter import ttk


class PanelProgreso(ttk.Frame):
    def __init__(self, contenedor):
        super().__init__(contenedor)


#Estilo personalizado para la barra de progreso
        estilo = ttk.Style(self)

        estilo.element_create(
            "Angel.Progressbar.trough",
            "from", "clam", "Horizontal.Progressbar.trough"
        )
        estilo.element_create(
            "Angel.Progressbar.pbar",
            "from", "clam", "Horizontal.Progressbar.pbar"
        )

        estilo.layout(
            "Angel.Horizontal.TProgressbar",
            [
                (
                    "Angel.Progressbar.trough",
                    {
                        "sticky": "nswe",
                        "children": [
                            (
                                "Angel.Progressbar.pbar",
                                {"side": "left", "sticky": "ns"}
                            )
                        ]
                    }
                )
            ]
        )

        estilo.configure(
            "Angel.Horizontal.TProgressbar",
            background="#FF00FF",
            lightcolor="#FF00FF",
            darkcolor="#FF00FF",
            troughcolor="#E6E6E6",
            bordercolor="#B5B5B5"
        )
#-------------------------------------

        self.porcentaje = tk.DoubleVar(value=0)
        self.estado = tk.StringVar(value="Listo para descargar")

        self.barra = ttk.Progressbar(
            self,
            style="Angel.Horizontal.TProgressbar", #Aplicar el estilo personalizado
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