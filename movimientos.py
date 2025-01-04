# Lógica de los movimientos

from datetime import datetime

# Lista para almacenar los movimientos
movimientos = []

# Función para agregar un movimiento
def agregar_movimiento(descripcion, monto, tipo):
    fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    if tipo == 'Ingreso':
        # Agregar el ingreso (monto positivo)
        movimientos.append({'descripcion': descripcion, 'monto': monto, 'tipo': tipo, 'fecha': fecha_actual})
    elif tipo == 'Gasto':
        # Agregar el gasto (monto negativo)
        movimientos.append({'descripcion': descripcion, 'monto': monto, 'tipo': tipo, 'fecha': fecha_actual})

def calcular_saldo():
    saldo = 0
    for movimiento in movimientos:
        saldo += movimiento['monto'] # suma los ingresos y resta los gastos
    return saldo

def obtener_historial():
    return movimientos