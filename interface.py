# Código de la interfaz gráfica

import tkinter as tk
from tkinter import ttk
from movimientos import agregar_movimiento, calcular_saldo, obtener_historial

def agregar_movimiento_gui(descripcion_entry, monto_entry, saldo_label):
    descripcion = descripcion_entry.get()
    try:
        monto = float(monto_entry.get())
        agregar_movimiento(descripcion, monto)
        descripcion_entry.delete(0, tk.END)
        monto_entry.delete(0, tk.END)
        actualizar_saldo(saldo_label)
    except ValueError:
        print('Error: El monto debe ser un número válido')

def actualizar_saldo(saldo_label):
    saldo = calcular_saldo()
    saldo_label.config(text=f'Saldo: S/. {saldo:.2f}')

def mostrar_historial(historial_text):
    historial_text.delete(1.0, tk.END)
    historial = obtener_historial()
    for movimiento in historial:
        historial_text.insert(tk.END, f"{movimiento['fecha']} - {movimiento['descripcion']} - S/. {movimiento['monto']}\n")

def iniciar_gui():
    # Crear la ventana principal
    root = tk.Tk()
    root.title('Gestor de Finanzas')
    root.geometry('500x500') # Tamaño de la ventana

    # Configurar un tema com tkk
    style = ttk.Style(root)
    style.configure('TButton', font=('Helvetica', 12), padding=10)
    style.configure('TLabel', font=('Helvetica', 12), padding=5)
    style.configure('TEntry', font=('Helvetica', 12), padding=5)

    # Crear los elementos de la interfaz usando frames para mejor organización
    main_frame = ttk.Frame(root, padding='10')
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame para la descripción y monto
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill=tk.X, pady=10)

    descripcion_label = ttk.Label(input_frame, text='Descripción:')
    descripcion_label.grid(row=0, column=0, sticky=tk.W, padx=10)

    descripcion_entry = ttk.Entry(input_frame, width=40)
    descripcion_entry.grid(row=0, column=1, padx=10)

    monto_label = ttk.Label(input_frame, text='Monto:')
    monto_label.grid(row=1, column=0, sticky=tk.W, padx=10)

    monto_entry = ttk.Entry(input_frame, width=40)
    monto_entry.grid(row=1, column=1, padx=10)

    # Frame para mostrar el saldo
    saldo_frame = ttk.Frame(main_frame)
    saldo_frame.pack(fill=tk.X, pady=10)

    saldo_label = ttk.Label(saldo_frame, text='Saldo: S/. 0.00', font=('Helvetica', 14, 'bold'))
    saldo_label.pack()

    # frame para los botones
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=10)

    agregar_button = ttk.Button(button_frame, text='Agregar Movimiento', command=lambda: agregar_movimiento_gui(descripcion_entry, monto_entry, saldo_label))
    agregar_button.pack(side=tk.LEFT, padx=10)

    historial_button = ttk.Button(button_frame, text='Mostrar Historial', command=lambda: mostrar_historial(historial_text))
    historial_button.pack(side=tk.LEFT, padx=10)

    # Frame para el historial
    historial_frame = ttk.Frame(main_frame)
    historial_frame.pack(fill=tk.BOTH, pady=10, expand=True)

    historial_text = tk.Text(historial_frame, height=10, width=40, wrap=tk.WORD, font=('Helvetica', 12))
    historial_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Agregar barra de desplazamiento (scroll) al historial
    scroll = ttk.Scrollbar(historial_frame, orient='vertical', command=historial_text.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    historial_text.config(yscrollcommand=scroll.set)

    # Iniciar la interfaz gráfica
    root.mainloop()