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

def mostrar_historial(treeview):
    # Limpiar el árbol antes de mostrar los nuevos movimientos
    for row in treeview.get_children():
        treeview.delete(row)

    # Obtener el historial de movimientos
    historial = obtener_historial()

    if not historial:
        treeview.insert('', 'end', values=('No hay movimientos registrados', '', '', ''))
    else:
        for movimiento in historial:
            tipo = "Ingreso" if movimiento['tipo'] == 'Ingreso' else "Gasto"
            # Insertar los datos en el Treeview
            if tipo == "Ingreso":
                treeview.insert('', 'end', values=(movimiento['fecha'], f"{movimiento['monto']:.2f}", movimiento['descripcion'], tipo), tags=('ingreso',))
            else:
                treeview.insert('', 'end', values=(movimiento['fecha'], f"{movimiento['monto']:.2f}", movimiento['descripcion'], tipo), tags=('gasto',))

def iniciar_gui():
    # Crear la ventana principal
    root = tk.Tk()
    root.title('Gestor de Finanzas')
    root.geometry('700x600') # Tamaño de la ventana
    root.config(bg='#e0f7fa') # Fondo de la ventana

    # Configurar un tema com tkk
    style = ttk.Style(root)
    style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=10, background='#26c6da', relief='flat', foreground='#ffffff')
    style.map('TButton', background=[('active', '#00bcd4')])
    style.configure('TLabel', font=('Helvetica', 12), padding=5, background='#e0f7fa', foreground='#00796b')
    style.configure('TEntry', font=('Helvetica', 12), padding=5, relief='flat')
    style.configure('TText', font=('Helvetica', 12), padding=5)

    # Crear los elementos de la interfaz usando frames para mejor organización
    main_frame = ttk.Frame(root, padding='20', style='TFrame')
    main_frame.grid(row=0, column=0, sticky='nsew')

    # Configurar el comportamiento de las filas y columnas para que se expandan
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

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
    saldo_frame.grid(row=1, column=0, pady=15, sticky='nsew')

    saldo_label = ttk.Label(saldo_frame, text='Saldo: S/. 0.00', font=('Helvetica', 14, 'bold'), foreground='#004d40')
    saldo_label.grid(row=0, column=0, columnspan=3, sticky='nsew')

    # frame para los botones
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=0, pady=15, sticky='ew')

    agregar_button = ttk.Button(button_frame, text='Agregar Movimiento', command=lambda: agregar_movimiento_gui(descripcion_entry, monto_entry, tipo_var, saldo_label))
    agregar_button.grid(row=0, column=0, padx=20)

    historial_button = ttk.Button(button_frame, text='Mostrar Historial', command=lambda: mostrar_historial(treeview))
    historial_button.grid(row=0, column=1, padx=20)

    # Frame para el historial
    historial_frame = ttk.Frame(main_frame)
    historial_frame.grid(row=3, column=0, pady=15, sticky='nsew')

    # Crear el Treeview para mostrar el historial
    columns = ('Fecha', 'Valor', 'Descripción', 'Tipo de Movimiento')
    treeview = ttk.Treeview(historial_frame, columns=columns, show='headings')

    # Configurar las columnas
    treeview.heading('Fecha', text='Fecha')
    treeview.heading('Valor', text='Valor')
    treeview.heading('Descripción', text='Descripción')
    treeview.heading('Tipo de Movimiento', text='Tipo de Movimiento')

    treeview.column('Fecha', width=150, anchor='w')
    treeview.column('Valor', width=100, anchor='e')
    treeview.column('Descripción', width=250, anchor='w')
    treeview.column('Tipo de Movimiento', width=150, anchor='e')

    treeview.grid(row=0, column=0, sticky='nsew')

    # Agregar barra de desplazamiento (scroll) al Treeview
    scroll = ttk.Scrollbar(historial_frame, orient='vertical', command=treeview.yview)
    scroll.grid(row=0, column=1, sticky='ns')

    # Vincular el scrollbar al Text widget
    treeview.config(yscrollcommand=scroll.set)

    # Definir colores de tags
    treeview.tag_configure('ingreso', background='#e3f2fd') # Azul suave
    treeview.tag_configure('gasto', background='#ffcdd2') # Rojo suave

    # Iniciar la interfaz gráfica
    root.mainloop()