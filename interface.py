# Código de la interfaz gráfica

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils import validar_monto
from movimientos import agregar_movimiento, calcular_saldo, obtener_historial

def limpiar_campos(descripcion_entry, monto_entry):
    descripcion_entry.delete(0, tk.END)
    monto_entry.delete(0, tk.END)


def agregar_movimiento_gui(descripcion_entry, monto_entry, tipo_var, saldo_label):
    descripcion = descripcion_entry.get()
    try:
        monto = float(monto_entry.get())

        # Validar el monto
        validar_monto(monto) # Llama a la función que valida que el monto sea mayor a cero

        # Asegurarnos de que el monto sea positivo para los ingresos
        if tipo_var.get() == 'Ingreso':
            pass


        # Si el tipo seleccionado es 'Gasto', convertimos el monto a negativo
        elif tipo_var.get() == 'Gasto':
            monto = -abs(monto) # Convertimos a valor negativo de manera explícita

        # Agregar el movimiento, pasamos también el tipo
        agregar_movimiento(descripcion, monto, tipo_var.get())

        # Limpiar los campos de entrada
        limpiar_campos(descripcion_entry, monto_entry)

        # Actualizar el salgo
        actualizar_saldo(saldo_label)

    except ValueError:
        messagebox.showerror('Error', 'El monto debe ser un número válido')

def actualizar_saldo(saldo_label):
    saldo = calcular_saldo()
    saldo_label.config(text=f'Saldo: S/. {saldo:.2f}')

def mostrar_historial(historial_text):
    # Verificar si historial_text es válido antes de modificarlo
    if not historial_text:
        print('Error: El widget historial_text no está inicializado.')
        return
    
    # Limpiar el historial antes de mostrar los nuevos movimientos
    historial_text.config(state=tk.NORMAL)
    historial_text.delete(1.0, tk.END) # Limpiar el contenido del historial

    # Obtener el historial de movimientos
    historial = obtener_historial()

    if not historial:
        historial_text.insert(tk.END, 'No hay movimientos registrados.\n')
    else:
        for movimiento in historial:
            tipo = "Ingreso" if movimiento['tipo'] == 'Ingreso' else "Gasto"
            historial_text.insert(tk.END, f"{movimiento['fecha']} - S/. {movimiento['monto']:.2f} - {movimiento['descripcion']} - {tipo}\n")

    historial_text.config(state=tk.DISABLED)

def iniciar_gui():
    # Crear la ventana principal
    root = tk.Tk()
    root.title('Gestor de Finanzas')
    root.geometry('600x600') # Tamaño de la ventana
    root.config(bg='#f4f4f9') # Fondo de la ventana

    # Configurar un tema com tkk
    style = ttk.Style(root)
    style.configure('TButton', font=('Arial', 12), padding=10, background='#4CAF50', relief='flat')
    style.map('TButton', background=[('active', '#45a049')])
    style.configure('TLabel', font=('Arial', 12), padding=5, background='#f4f4f9')
    style.configure('TEntry', font=('Arial', 12), padding=5)

    # Crear los elementos de la interfaz usando frames para mejor organización
    main_frame = ttk.Frame(root, padding='20', style='TFrame')
    main_frame.grid(row=0, column=0, sticky='nsew')

    # Frame para la descripción y monto
    input_frame = ttk.Frame(main_frame)
    input_frame.grid(row=0, column=0, padx=10, pady=15, sticky='ew')

    descripcion_label = ttk.Label(input_frame, text='Descripción:', anchor='w')
    descripcion_label.grid(row=0, column=0, sticky=tk.W, padx=10)

    descripcion_entry = ttk.Entry(input_frame, width=40)
    descripcion_entry.grid(row=0, column=1, padx=10)

    monto_label = ttk.Label(input_frame, text='Monto:', anchor='w')
    monto_label.grid(row=1, column=0, sticky=tk.W, padx=10)

    monto_entry = ttk.Entry(input_frame, width=40)
    monto_entry.grid(row=1, column=1, padx=10)

    # Opciones para seleccionar tipo de movimiento (Ingreso o Gasto)
    tipo_label = ttk.Label(input_frame, text='Tipo de Movimiento:')
    tipo_label.grid(row=2, column=0, sticky=tk.W, padx=10)

    tipo_var = tk.StringVar(value='Ingreso') # Valor por defecto es 'Ingreso'
    ingreso_radiobutton = ttk.Radiobutton(input_frame, text='Ingreso', variable=tipo_var, value='Ingreso')
    ingreso_radiobutton.grid(row=2, column=1, padx=10, sticky=tk.W)

    gasto_radiobutton = ttk.Radiobutton(input_frame, text='Gasto', variable=tipo_var, value='Gasto')
    gasto_radiobutton.grid(row=2, column=2, padx=10, sticky=tk.W)

    # Frame para mostrar el saldo
    saldo_frame = ttk.Frame(main_frame)
    saldo_frame.grid(row=1, column=0, pady=15, sticky='ew')

    saldo_label = ttk.Label(saldo_frame, text='Saldo: S/. 0.00', font=('Arial', 14, 'bold'))
    saldo_label.grid(row=0, column=0)

    # frame para los botones
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=0, pady=15, sticky='ew')

    agregar_button = ttk.Button(button_frame, text='Agregar Movimiento', command=lambda: agregar_movimiento_gui(descripcion_entry, monto_entry, tipo_var, saldo_label))
    agregar_button.grid(row=0, column=0, padx=20)

    historial_button = ttk.Button(button_frame, text='Mostrar Historial', command=lambda: mostrar_historial(historial_text))
    historial_button.grid(row=0, column=1, padx=20)

    # Frame para el historial
    historial_frame = ttk.Frame(main_frame)
    historial_frame.grid(row=3, column=0, pady=15, sticky='nsew')

    # Crear el widget Text para mostrar el historial
    historial_text = tk.Text(historial_frame, height=10, width=40, wrap=tk.WORD, font=('Arial', 12))
    historial_text.grid(row=0, column=0, sticky='nsew')

    # Agregar barra de desplazamiento (scroll) al historial
    scroll = ttk.Scrollbar(historial_frame, orient='vertical', command=historial_text.yview)
    scroll.grid(row=0, column=1, sticky='ns')

    # Vincular el scrollbar al Text widget
    historial_text.config(yscrollcommand=scroll.set)

    # Iniciar la interfaz gráfica
    root.mainloop()