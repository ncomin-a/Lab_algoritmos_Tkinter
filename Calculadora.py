import tkinter as tk
from tkinter import ttk, messagebox
import math

root = tk.Tk()
root.title("Calculadora")
root.geometry("500x600")
root.resizable(False, False)

numero = tk.StringVar()
valor1 = None
operacion = None


def obtener_numero():
    contenido = numero.get().strip()

    if not contenido:
        raise ValueError("La pantalla está vacía.")

    if any(c.isalpha() for c in contenido):
        raise ValueError("No se permiten letras.")

    try:
        return float(contenido)
    except ValueError:
        raise ValueError("Entrada no válida.")


def mostrar_resultado(valor):
    numero.set(str(round(valor, 4)))


def ejecutar_operacion():
    global valor1, operacion

    try:
        valor2 = obtener_numero()

        if operacion is None or valor1 is None:
            raise ValueError("Seleccione una operación primero.")

        if operacion == "+":
            resultado = valor1 + valor2
        elif operacion == "-":
            resultado = valor1 - valor2
        elif operacion == "*":
            resultado = valor1 * valor2
        elif operacion == "/":
            if valor2 == 0:
                raise ZeroDivisionError("No se puede dividir entre cero.")
            resultado = valor1 / valor2
        elif operacion == "^":
            resultado = valor1 ** valor2
        else:
            raise ValueError("Operación no reconocida.")

        mostrar_resultado(resultado)
        valor1 = None
        operacion = None

    except ZeroDivisionError as e:
        messagebox.showerror("Error", str(e))
        numero.set("")
        valor1 = None
        operacion = None
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        numero.set("")
        valor1 = None
        operacion = None

def click_boton(texto):
    global valor1, operacion

    if texto in "0123456789.":
        numero.set(numero.get() + texto)

    elif texto in "+-*/^":
        try:
            valor1 = obtener_numero()
            operacion = texto
            numero.set("")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            numero.set("")

    elif texto == "√":
        try:
            valor = obtener_numero()
            if valor < 0:
                raise ValueError("No existe raíz cuadrada de un número negativo.")
            mostrar_resultado(math.sqrt(valor))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            numero.set("")

    elif texto == "=":
        ejecutar_operacion()

    elif texto == "C":
        numero.set("")
        valor1 = None
        operacion = None

    elif texto == "⌫":
        contenido = numero.get()
        numero.set(contenido[:-1])


def calcular_enter(event=None):
    ejecutar_operacion()


mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

entry_frame = ttk.Frame(mainframe, borderwidth=5, relief="sunken")
entry_frame.grid(column=0, row=0, columnspan=4, padx=5, pady=10, sticky="nsew")

numero_entry = ttk.Entry(entry_frame, width=30, textvariable=numero, justify="right", font=("Arial", 18))
numero_entry.grid(column=0, row=0, padx=5, pady=5, ipady=8)

botones = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
    ("C", 5, 0), ("^", 5, 1), ("√", 5, 2), ("⌫", 5, 3),
]

for texto, fila, columna in botones:
    boton = tk.Button(
        mainframe,
        text=texto,
        font=("Arial", 14, "bold"),
        width=5,
        height=2,
        command=lambda t=texto: click_boton(t)
    )
    boton.grid(row=fila, column=columna, padx=4, pady=4, sticky="nsew")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

for i in range(4):
    mainframe.columnconfigure(i, weight=1)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.bind("<Return>", calcular_enter)

root.mainloop()