from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def calcular_total_invertido(cursos_pagados):
    """
    Calcula el total invertido basado en el número de cursos pagados
    Cada curso cuesta $380 MXN
    """
    try:
        cantidad_cursos = len(cursos_pagados)
        total = cantidad_cursos * 380
        return f"${total:,}"
    except:
        return "$0"

@register.filter
def calcular_porcentaje_progreso(cursos_pagados):
    """
    Calcula el porcentaje de progreso basado en cursos completados
    """
    try:
        cantidad_cursos = len(cursos_pagados)
        # Por ahora retornamos un porcentaje fijo, pero se puede personalizar
        return min(cantidad_cursos * 10, 100)
    except:
        return 0
