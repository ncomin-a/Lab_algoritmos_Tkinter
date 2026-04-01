import tkinter as tk
from tkinter import messagebox
import math

# Función para agregar texto al Entry
def presionar(valor):
    actual = entrada.get()
    entrada.delete(0, tk.END)
    entrada.insert(0, actual + str(valor))

# Función para limpiar pantalla
def limpiar():
    entrada.delete(0, tk.END)

# Función para calcular resultado
def calcular():
    try:
        expresion = entrada.get()

        # Validación: evitar letras
        for c in expresion:
            if c.isalpha():
                raise ValueError("Entrada inválida")

        # Reemplazos para operaciones
        expresion = expresion.replace("^", "**")

        resultado = eval(expresion)

        entrada.delete(0, tk.END)
        entrada.insert(0, str(resultado))

    except ZeroDivisionError:
        messagebox.showerror("Error", "No se puede dividir por cero")
        limpiar()
    except:
        messagebox.showerror("Error", "Entrada inválida")
        limpiar()

# Función raíz cuadrada
def raiz():
    try:
        valor = float(entrada.get())
        if valor < 0:
            raise ValueError
        resultado = math.sqrt(valor)
        entrada.delete(0, tk.END)
        entrada.insert(0, str(resultado))
    except:
        messagebox.showerror("Error", "No se puede calcular la raíz")
        limpiar()

# Ventana principal
ventana = tk.Tk()
ventana.title("Calculadora")

# Pantalla (Entry)
entrada = tk.Entry(ventana, font=("Arial", 18), bd=10, relief="ridge", justify="right")
entrada.pack(fill="both", padx=10, pady=10)

# Frame de botones
frame = tk.Frame(ventana)
frame.pack()

# Botones (matriz)
botones = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('0', '.', '^', '+')
]

for fila in botones:
    fila_frame = tk.Frame(frame)
    fila_frame.pack()
    for boton in fila:
        tk.Button(
            fila_frame,
            text=boton,
            width=5,
            height=2,
            font=("Arial", 14),
            command=lambda b=boton: presionar(b)
        ).pack(side="left", padx=2, pady=2)

# Botones especiales
tk.Button(frame, text="C", width=5, height=2, font=("Arial", 14), command=limpiar).pack(side="left", padx=2, pady=2)
tk.Button(frame, text="√", width=5, height=2, font=("Arial", 14), command=raiz).pack(side="left", padx=2, pady=2)
tk.Button(frame, text="=", width=5, height=2, font=("Arial", 14), command=calcular).pack(side="left", padx=2, pady=2)

ventana.mainloop()