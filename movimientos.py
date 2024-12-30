# Lógica de los movimientos

import datetime

# Lista para almacenar los movimientos
movimientos = []

def agregar_movimiento(descripcion, monto):
    # Registrar el movimiento
    fecha = datetime.date.today().strftime('%Y-%m-%d')
    movimientos.append({'descripcion': descripcion, 'monto': monto, 'fecha': fecha})

def calcular_saldo():
    return sum(m['monto'] for m in movimientos)

def obtener_historial():
    return movimientos