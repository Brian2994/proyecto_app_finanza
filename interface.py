# Código de la interfaz gráfica

def agregar_movimiento_gui(descripcion_entry, monto_entry, saldo_label):
    descripcion = descripcion_entry.get()
    monto = float(monto_entry.get())
    agregar_movimiento(descripcion, monto)
    descripcion_entry.delete(0, tk.END)
    monto_entry.delete(0, tk.END)
    actualizar_saldo(saldo_label)

def actualizar_saldo(saldo_label):
    saldo = calcular_saldo()
    saldo_label.config(text=f'Saldo: ${saldo:.2f}')

def mostrar_historial(historial_text):
    historial_text.delete(1.0, tk.END)
    historial = obtener_historial()
    for movimiento in historial:
        historial_text.insert(tk.END, f"{movimiento['fecha']} - {movimiento['descripcion']} - ${movimiento['monto']}\n")

def iniciar_gui():
    # Crear la ventana principal
    root = tk.Tk()
    root.title('Gestor de Finanzas')

    # Crear los elementos de la interfaz
    descripcion_label = tk.Label(root, text='Descripción:')
    descripcion_label.pack()

    descripcion_entry = tk.Entry(root)
    descripcion_entry.pack()

    monto_label = tk.Label(root, text='Monto:')
    monto_label.pack()

    monto_entry = tk.Entry(root)
    monto_entry.pack()

    saldo_label = tk.Label(root, text='Saldo: $0.00')
    saldo_label.pack()

    agregar_button = tk.Button(root, text='Agregar Movimiento', command=lambda: agregar_movimiento_gui(descripcion_entry, monto_entry, saldo_label))
    agregar_button.pack()

    historial_button = tk.Button(root, text='Mostrar Historial', command=lambda: mostrar_historial(historial_text))
    historial_button.pack()

    historial_text = tk.Text(root, height=10, width=40)
    historial_text.pack()

    # Iniciar la interfaz gráfica
    root.mainloop()
import tkinter as tk
from movimientos import agregar_movimiento, calcular_saldo, obtener_historial
