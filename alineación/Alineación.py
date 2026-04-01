import tkinter as tk
import os
from PIL import Image, ImageTk

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
ANCHO = 600
ALTO = 770
TAM_X = 100
TAM_Y = 106

# Ruta assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")

# Nombres de imágenes
NOMBRES = [
    "Charlie.png", "Cobra.png", "davo.png", "Frionaldo.png",
    "Janson.png", "Maduro.png", "Momo.png", "Pessi.png",
    "Speed.png", "Walter.png", "YO YO YO Mr White.png"  # renombrado
]

# Formación 4-4-2
POSICIONES = [
    (250, 650),
    (100, 500), (200, 500), (300, 500), (400, 500),
    (80, 350), (180, 350), (320, 350), (420, 350),
    (180, 200), (320, 200)
]

# -----------------------------
# CLASE JUGADOR
# -----------------------------
class Jugador:
    def __init__(self, root, img, x, y, app):
        self.root = root
        self.app = app

        self.label = tk.Label(root, image=img, bd=0)
        self.label.image = img
        self.label.place(x=x, y=y, width=TAM_X, height=TAM_Y)

        self.label.bind("<Button-1>", self.click)
        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<ButtonRelease-1>", self.drop)

        self.offset_x = 0
        self.offset_y = 0

    def click(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def drag(self, event):
        x = self.label.winfo_x() + event.x - self.offset_x
        y = self.label.winfo_y() + event.y - self.offset_y
        self.label.place(x=x, y=y)

    def drop(self, event):
        x = self.label.winfo_x()
        y = self.label.winfo_y()

        # intercambio
        for otro in self.app.jugadores:
            if otro is self:
                continue

            ox = otro.label.winfo_x()
            oy = otro.label.winfo_y()

            if abs(x - ox) < TAM_X // 2 and abs(y - oy) < TAM_Y // 2:
                self.label.place(x=ox, y=oy)
                otro.label.place(x=x, y=y)
                return

        # volver a posición cercana
        pos = min(POSICIONES, key=lambda p: (p[0]-x)**2 + (p[1]-y)**2)
        self.label.place(x=pos[0], y=pos[1])


# -----------------------------
# APP
# -----------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Alineación táctica")
        self.root.geometry(f"{ANCHO}x{ALTO}")
        self.root.resizable(False, False)

        # -----------------------------
        # CANCHA (resize)
        # -----------------------------
        ruta_cancha = os.path.join(ASSETS, "cancha.png")

        img_cancha = Image.open(ruta_cancha)
        img_cancha = img_cancha.resize((ANCHO, ALTO), Image.LANCZOS)

        self.cancha_img = ImageTk.PhotoImage(img_cancha)

        fondo = tk.Label(root, image=self.cancha_img)
        fondo.place(x=0, y=0, width=ANCHO, height=ALTO)

        # -----------------------------
        # JUGADORES (resize)
        # -----------------------------
        self.jugadores = []
        self.imagenes = []

        for i in range(11):
            ruta_img = os.path.join(ASSETS, NOMBRES[i])

            img_pil = Image.open(ruta_img)
            img_pil = img_pil.resize((TAM_X, TAM_Y), Image.LANCZOS)

            img = ImageTk.PhotoImage(img_pil)
            self.imagenes.append(img)

            x, y = POSICIONES[i]
            jugador = Jugador(root, img, x, y, self)
            self.jugadores.append(jugador)


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()