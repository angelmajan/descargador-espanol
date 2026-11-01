import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import json
import yt_dlp
import threading
from queue import Queue, Empty

ventana = tk.Tk()
ventana.title("Descargador de vídeos - Ángel Maján")
ventana.geometry("650x400")
ventana.resizable(False, False)

etiqueta = ttk.Label(ventana, text="Enlace del vídeo:")
etiqueta.pack(padx=20, pady=(20, 5), anchor="w")

entrada_url = ttk.Entry(ventana)
entrada_url.pack(padx=20, fill="x")
entrada_url.focus_set()

carpeta_programa = Path(__file__).resolve().parent
archivo_config = carpeta_programa / "config.json"
carpeta_inicial = carpeta_programa / "VIDEOS DESCARGADOS"
carpeta_ffmpeg = carpeta_programa / "ffmpeg"

def cargar_carpeta():
    try:
        contenido = archivo_config.read_text(encoding="utf-8")
        datos = json.loads(contenido)

        if isinstance(datos, dict):
            ruta = datos.get("carpeta_destino")

            if isinstance(ruta, str) and ruta.strip():
                return ruta

    except (OSError, ValueError):
        pass

    return str(carpeta_inicial)


carpeta_destino = tk.StringVar(value=cargar_carpeta())


def elegir_carpeta():
    seleccion = filedialog.askdirectory(
        parent=ventana,
        title="Selecciona la carpeta de descarga",
        initialdir=carpeta_destino.get()
    )

    if seleccion:
        carpeta_destino.set(seleccion)

        try:
            datos = {"carpeta_destino": seleccion}
            contenido = json.dumps(
                datos,
                ensure_ascii=False,
                indent=4
            )
            archivo_config.write_text(contenido, encoding="utf-8")

        except OSError:
            messagebox.showwarning(
                "No se pudo guardar",
                "La carpeta se usará durante esta sesión, "
                "pero no se pudo guardar para la próxima."
            )
            

            
def crear_opciones(carpeta):
    return {
        "outtmpl": str(
            Path(carpeta) / "%(title)s [%(id)s].%(ext)s"
        ),
        "ffmpeg_location": str(carpeta_ffmpeg),
        
        "js_runtimes": {
    "deno": {
        "path": str(carpeta_programa / "deno.exe")
    }
},

        "format": (
            "bestvideo+bestaudio[language^=es]/"
            "best[language^=es]/"
            "bestvideo+bestaudio/best"
        ),
        "merge_output_format": "mkv",
        "noplaylist": True,
    }


# def descargar():
#     url = entrada_url.get().strip()

#     if not url:
#         messagebox.showwarning(
#             "Falta el enlace",
#             "Pega el enlace del vídeo antes de descargar."
#         )
#         return

#     messagebox.showinfo(
#         "Enlace recibido",
#         f"El enlace que has introducido es:\n\n{url}"
#     )

resultados = Queue()


def realizar_descarga(url, carpeta):
    try:
        Path(carpeta).mkdir(parents=True, exist_ok=True)
        opciones = crear_opciones(carpeta)

        with yt_dlp.YoutubeDL(opciones) as descargador:
            codigo = descargador.download([url])

        if codigo != 0:
            raise RuntimeError("No se pudo completar la descarga.")

    except Exception as error:
        resultados.put(("error", str(error)))

    else:
        resultados.put(("correcto", carpeta))


def comprobar_resultado():
    try:
        estado, mensaje = resultados.get_nowait()

    except Empty:
        ventana.after(200, comprobar_resultado)
        return

    boton_descargar.config(state="normal", text="Descargar")
    boton_carpeta.config(state="normal")
    entrada_url.config(state="normal")

    if estado == "correcto":
        messagebox.showinfo(
            "Descarga completada",
            f"El vídeo está guardado en:\n\n{mensaje}",
            parent=ventana
        )
    else:
        messagebox.showerror(
            "Error de descarga",
            mensaje,
            parent=ventana
        )


def descargar():
    url = entrada_url.get().strip()

    if not url:
        messagebox.showwarning(
            "Falta el enlace",
            "Pega el enlace del vídeo antes de descargar.",
            parent=ventana
        )
        return

    for nombre in ("ffmpeg.exe", "ffprobe.exe"):
        if not (carpeta_ffmpeg / nombre).is_file():
            messagebox.showerror(
                "Falta FFmpeg",
                f"No se encuentra {nombre} en:\n\n{carpeta_ffmpeg}",
                parent=ventana
            )
            return

    carpeta = carpeta_destino.get()

    boton_descargar.config(state="disabled", text="Descargando...")
    boton_carpeta.config(state="disabled")
    entrada_url.config(state="disabled")

    hilo = threading.Thread(
        target=realizar_descarga,
        args=(url, carpeta),
        daemon=True
    )
    hilo.start()

    ventana.after(200, comprobar_resultado)



etiqueta_carpeta = ttk.Label(ventana, text="Guardar en:")
etiqueta_carpeta.pack(padx=20, pady=(20, 5), anchor="w")

campo_carpeta = ttk.Entry(
    ventana,
    textvariable=carpeta_destino,
    state="readonly"
)
campo_carpeta.pack(padx=20, fill="x")

boton_carpeta = ttk.Button(
    ventana,
    text="Elegir carpeta",
    command=elegir_carpeta
)
boton_carpeta.pack(pady=10)



boton_descargar = ttk.Button(
    ventana,
    text="Descargar",
    command=descargar
)
boton_descargar.pack(pady=20)

ventana.mainloop()
#cambio 01 1.0.5