import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# -----------------------------
# ARCHIVO DE DATOS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

# -----------------------------
# APP
# -----------------------------
class InventarioApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario")
        self.root.geometry("900x500")

        self.datos = []
        self.cargar_datos()

        # -----------------------------
        # PANEL IZQUIERDO
        # -----------------------------
        frame_izq = ttk.LabelFrame(root, text="Panel de Operaciones")
        frame_izq.place(x=10, y=10, width=300, height=480)

        ttk.Label(frame_izq, text="Producto").pack(pady=5)
        self.cod = ttk.Entry(frame_izq)
        self.cod.pack()

        ttk.Label(frame_izq, text="Descripción").pack(pady=5)
        self.desc = ttk.Entry(frame_izq)
        self.desc.pack()

        ttk.Label(frame_izq, text="Precio").pack(pady=5)
        self.precio = ttk.Entry(frame_izq)
        self.precio.pack()

        ttk.Label(frame_izq, text="Categoría").pack(pady=5)
        self.cat = ttk.Entry(frame_izq)
        self.cat.pack()

        ttk.Label(frame_izq, text="Cantidad").pack(pady=5)
        self.cant = ttk.Spinbox(frame_izq, from_=0, to=1000)
        self.cant.pack()

        ttk.Button(frame_izq, text="Guardar", command=self.crear).pack(pady=5)
        ttk.Button(frame_izq, text="Modificar", command=self.modificar).pack(pady=5)
        ttk.Button(frame_izq, text="Borrar", command=self.borrar).pack(pady=5)

        # -----------------------------
        # PANEL DERECHO
        # -----------------------------
        frame_der = ttk.LabelFrame(root, text="Inventario")
        frame_der.place(x=320, y=10, width=560, height=480)

        columnas = ("producto", "descripcion", "precio", "categoria", "cantidad")

        self.tree = ttk.Treeview(frame_der, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col, command=lambda c=col: self.ordenar(c))
            self.tree.column(col, width=100)

        self.tree.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(frame_der, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.bind("<ButtonRelease-1>", self.seleccionar)

        # alerta visual
        self.tree.tag_configure("bajo", background="tomato")

        self.refrescar()

    # -----------------------------
    # CARGAR DATOS (FIX JSON)
    # -----------------------------
    def cargar_datos(self):
        if not os.path.exists(DATA_FILE):
            # crear archivo automáticamente
            with open(DATA_FILE, "w") as f:
                json.dump([], f)
            self.datos = []
            return

        try:
            with open(DATA_FILE, "r") as f:
                contenido = f.read().strip()

                if contenido:
                    self.datos = json.loads(contenido)
                else:
                    self.datos = []

        except json.JSONDecodeError:
            messagebox.showwarning("Advertencia", "JSON corrupto. Se reinicia.")
            self.datos = []

    # -----------------------------
    # GUARDAR DATOS
    # -----------------------------
    def guardar_datos(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.datos, f, indent=4)

    # -----------------------------
    # REFRESCAR TABLA
    # -----------------------------
    def refrescar(self, datos=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        datos = datos if datos else self.datos

        for d in datos:
            tag = "bajo" if int(d["cantidad"]) < 5 else ""

            self.tree.insert("", "end", values=(
                d["codigo"],
                d["descripcion"],
                d["precio"],
                d["categoria"],
                d["cantidad"]
            ), tags=(tag,))

    # -----------------------------
    # CREATE
    # -----------------------------
    def crear(self):
        codigo = self.cod.get()
        descripcion = self.desc.get()
        precio = self.precio.get()
        categoria = self.cat.get()
        cantidad = self.cant.get()

        if not codigo or not descripcion:
            messagebox.showerror("Error", "Campos obligatorios vacíos")
            return

        for d in self.datos:
            if d["codigo"] == codigo:
                messagebox.showerror("Error", "Código duplicado")
                return

        nuevo = {
            "codigo": codigo,
            "descripcion": descripcion,
            "precio": precio,
            "categoria": categoria,
            "cantidad": cantidad
        }

        self.datos.append(nuevo)
        self.guardar_datos()
        self.refrescar()
        self.limpiar()

    # -----------------------------
    # READ
    # -----------------------------
    def seleccionar(self, event):
        item = self.tree.selection()
        if item:
            valores = self.tree.item(item)["values"]

            self.cod.delete(0, tk.END)
            self.cod.insert(0, valores[0])

            self.desc.delete(0, tk.END)
            self.desc.insert(0, valores[1])

            self.precio.delete(0, tk.END)
            self.precio.insert(0, valores[2])

            self.cat.delete(0, tk.END)
            self.cat.insert(0, valores[3])

            self.cant.delete(0, tk.END)
            self.cant.insert(0, valores[4])

    # -----------------------------
    # UPDATE
    # -----------------------------
    def modificar(self):
        codigo = self.cod.get()

        for d in self.datos:
            if d["codigo"] == codigo:
                d["descripcion"] = self.desc.get()
                d["precio"] = self.precio.get()
                d["categoria"] = self.cat.get()
                d["cantidad"] = self.cant.get()
                break

        self.guardar_datos()
        self.refrescar()

    # -----------------------------
    # DELETE
    # -----------------------------
    def borrar(self):
        codigo = self.cod.get()

        for i in range(len(self.datos)):
            if self.datos[i]["codigo"] == codigo:
                del self.datos[i]
                break

        self.guardar_datos()
        self.refrescar()
        self.limpiar()

    # -----------------------------
    # LIMPIAR
    # -----------------------------
    def limpiar(self):
        for campo in [self.cod, self.desc, self.precio, self.cat]:
            campo.delete(0, tk.END)
        self.cant.delete(0, tk.END)

    # -----------------------------
    # ORDENAR
    # -----------------------------
    def ordenar(self, col):
        self.datos.sort(key=lambda x: x[col])
        self.refrescar()


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()