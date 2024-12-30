# Funciones auxiliares (opcional)

def validar_monto(monto):
    if monto <= 0:
        raise ValueError('El monto debe ser mayor a cero.')