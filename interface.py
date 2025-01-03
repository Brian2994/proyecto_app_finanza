# Código de la interfaz gráfica

import tkinter as tk
from tkinter import ttk
from movimientos import agregar_movimiento, calcular_saldo, obtener_historial

def agregar_movimiento_gui(descripcion_entry, monto_entry, tipo_var, saldo_label):
    descripcion = descripcion_entry.get()
    try:
        monto = float(monto_entry.get())

        # Asegurarnos de que el monto sea positivo para los ingresos
        if tipo_var.get() == 'Ingreso':
            monto = abs(monto) # Convertimos a valor absoluto si es ingreso


        # Si el tipo seleccionado es 'Gasto', convertimos el monto a negativo
        if tipo_var.get() == 'Gasto':
            monto = abs(monto) # Convertimos a valor absoluto para que sea siempre un valor positivo
            monto = -monto # Ahora lo hacemos negativo para el gasto

        # Agregar el movimiento, pasamos también el tipo
        agregar_movimiento(descripcion, monto, tipo_var.get())

        # Limpiar los campos de entrada
        descripcion_entry.delete(0, tk.END)
        monto_entry.delete(0, tk.END)

        # Actualizar el salgo
        actualizar_saldo(saldo_label)

    except ValueError:
        print('Error: El monto debe ser un número válido')

def actualizar_saldo(saldo_label):
    saldo = calcular_saldo()
    saldo_label.config(text=f'Saldo: S/. {saldo:.2f}')

def mostrar_historial(historial_frame):
    # Limpiar el historial antes de mostrar los nuevos movimientos
    for widget in historial_frame.winfo_children():
        widget.destroy()

    historial = obtener_historial()
    for movimiento in historial:
        tipo = "Ingreso" if movimiento['tipo'] == 'Ingreso' else "Gasto"

        # Frame para cada movimiento
        historial_entry = ttk.Frame(historial_frame)
        historial_entry.pack(fill=tk.X, pady=5)

        # Formatear la fecha
        fecha = movimiento['fecha']

        # Label para la fecha (izquierda)
        fecha_label = ttk.Label(historial_entry, text=fecha, font=('Arial', 12))
        fecha_label.pack(side=tk.LEFT, padx=10)

        # Label para monto y tipo (izquierda)
        monto_label = ttk.Label(historial_entry, text=f"S/. {movimiento['monto']:.2f} - {tipo}", font=('Arial', 12))
        monto_label.pack(side=tk.LEFT, padx=10)

        # Label para la descripción (derecha), color gris
        descripcion_label = ttk.Label(historial_entry, text=movimiento['descripcion'], font=('Arial', 12), foreground='gray')
        descripcion_label.pack(side=tk.RIGHT, padx=10)

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
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame para la descripción y monto
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill=tk.X, pady=15)

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
    saldo_frame.pack(fill=tk.X, pady=15)

    saldo_label = ttk.Label(saldo_frame, text='Saldo: S/. 0.00', font=('Arial', 14, 'bold'))
    saldo_label.pack()

    # frame para los botones
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=15)

    agregar_button = ttk.Button(button_frame, text='Agregar Movimiento', command=lambda: agregar_movimiento_gui(descripcion_entry, monto_entry, tipo_var, saldo_label))
    agregar_button.pack(side=tk.LEFT, padx=20)

    historial_button = ttk.Button(button_frame, text='Mostrar Historial', command=lambda: mostrar_historial(historial_text))
    historial_button.pack(side=tk.LEFT, padx=20)

    # Frame para el historial
    historial_frame = ttk.Frame(main_frame)
    historial_frame.pack(fill=tk.BOTH, pady=15, expand=True)

    # Crear el widget Text para mostrar el historial
    historial_text = tk.Text(historial_frame, height=10, width=40, wrap=tk.WORD, font=('Arial', 12))
    historial_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Agregar barra de desplazamiento (scroll) al historial
    scroll = ttk.Scrollbar(historial_frame, orient='vertical', command=historial_text.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Vincular el scrollbar al Text widget
    historial_text.config(yscrollcommand=scroll.set)

    # Iniciar la interfaz gráfica
    root.mainloop()