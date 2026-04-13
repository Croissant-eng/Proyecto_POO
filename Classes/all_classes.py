from enum import Enum
from datetime import datetime as dt

"""
Importamos los modulos enum y date porque:
        *De la parte de Enum:
            -Nos permite trabajar con numeros asignados a un significado
            -Nos permite evadir errores de rango o de TypeError
        *De la parte de datetime:
            -Nos permite trabajar con fechas y horas y no solo con str´s
            -Le da mas robustez a nuestro codigo y a las clases
"""

# Enums para prioridad y estado
class Prioridad(Enum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3
    CRITICA = 4
    """
    El usuario puede ingresar 
    como parametro de Prioridad ya sea
    (1, 2, ...) ó Estado.(Baja, Media, ...)"""

class Estado(Enum):
    PENDIENTE = 'pendiente'
    EN_PROGRESO = "en_progreso"
    COMPLETADA = 'completada'

class Frecuencia(Enum):
    Diaria = 1
    Semanal = 7
    Mensual = 30

# Calse base Tarea
class Tarea:
    def __init__(self, titulo: str, descripcion: str, fecha_lim: dt, prioridad: Prioridad):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_lim = fecha_lim
        self._prioridad = prioridad
        self._estado = Estado.PENDIENTE    #
        self.fecha_creacion = dt.now()     # Nos da la fecha acutal en formato año-mes-dia
    
    @property
    def estado(self):
        return self._estado
    
    @property
    def prioridad(self):
        return self._prioridad

    def completar(self):
        """Marca una tarea como completada"""
        self._estado = Estado.COMPLETADA
    
    def reabrir(self):
        """Reabre una tarea completada"""
        if self._estado == Estado.COMPLETADA:
            self._estado = Estado.PENDIENTE
        else:
            raise ValueError('You can reopen a task that´s already open')

    def dias_restantes(self):
        """Calcula los dias restantes hasta la fecha limite"""
        hoy = dt.now()
        delta = self.fecha_lim - hoy
        return delta.days             # Devuelve un numero entero
    
    def esta_vencida(self):
        """Verifica si la tarea esta vencida"""
        return (dt.now() > self.fecha_lim) and (self._estado != Estado.COMPLETADA)
    
    def __repr__(self):
        cadena = f'La tarea: {self.titulo}\n'
        cadena += f'Su estado es: {self._estado}'
        cadena += f'Tiene como Prioridad: {self._prioridad.name}\n'
        cadena += f'Y su fecha limite es: {self.fecha_lim}'
        return cadena
