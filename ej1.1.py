import tkinter as tk
from tkinter import ttk
import math


ventana = tk.Tk()
ventana.title("Calculadora")
ventana.geometry("500x600")

frame = ttk.Frame(ventana)
frame.pack()
# Tamaño del boton
frame['ancho'] = 500 
frame['alto'] = 400
# Distancias de la pantalla
frame['width'] = '500p'
# Relleno
frame['espacio'] = 5                # 5 pixels on all sides
frame['espacio'] = (5, 10)          # 5 on left and right, 10 on top and bottom    
frame['espacio'] = (5, 7, 10, 12)   # left: 5, top: 7, right: 10, bottom: 12
# borde
frame['borderwidth'] = 2
frame['relief'] = 'sunken'
# Etiqueta
label = ttk.Label(parent, text='Full name:')
# mostrar boton
resultsContents = StringVar()
label['textvariable'] = resultsContents
resultsContents.set('Initial value to display')


botones = [
    ("C", 0, 0), ("^", 0, 1), ("√", 0, 2), ("÷", 0, 3)
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3)
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("+", 2, 3)
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3)
    ("0", 4, 0), (".", 4, 1), ("<-", 4, 2), ("=", 4, 3)
    ]

def click_boton(valor):
    entrada_actual = ventana.get()
    ventana.delete(0, tk.END)
    ventana.insert(0, entrada_actual + str(valor))

def borrar():
    ventana.delete(0, tk.END)

def exponente():
    exponent = click_boton("**")

def raiz():
    pass

ventana.mainloop()