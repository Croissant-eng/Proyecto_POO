from enum import Enum
from datetime import datetime as dt
from datetime import timedelta

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
    (1, 2, ...) ó Estado.(Baja, Media, ...)
    """

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
    def __init__(self, titulo: str, descripcion: str, 
                 fecha_lim: dt, prioridad: Prioridad):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_lim = fecha_lim
        self._prioridad = prioridad
        self._estado = Estado.PENDIENTE    # En la creacion del objeto ya se inicializa su estado
        self.fecha_creacion = dt.now()     # Nos da la fecha acutal en formato año-mes-dia
    
    @property
    def estado(self):
        return self._estado
    
    @property
    def prioridad(self):
        return self._prioridad

    def completar(self):
        """Changes the status of a homework/task to COMPLETE"""
        self._estado = Estado.COMPLETADA
    
    def reabrir(self):
        """Reopens a taks/homework"""
        if self._estado == Estado.COMPLETADA:
            self._estado = Estado.PENDIENTE
        else:
            raise ValueError('You can reopen a task that´s already open')

    def dias_restantes(self):
        """Counts how many days the homework/task has left"""
        hoy = dt.now()
        delta = self.fecha_lim - hoy
        return delta.days             # Devuelve un numero entero
    
    def esta_vencida(self):
        """
        Checks if the homework/task 
        its expired and returns True or False
        rather it is or not"""
        return (dt.now() > self.fecha_lim) and (self._estado != Estado.COMPLETADA)
    
    def __repr__(self):
        """Repr method of the class"""
        cadena = f'La tarea: {self.titulo}\n'
        cadena += f'Su estado es: {self._estado}'
        cadena += f'Tiene como Prioridad: {self._prioridad.name}\n'
        cadena += f'Y su fecha limite es: {self.fecha_lim}'
        return cadena


class TareaSimple(Tarea):
    

    def __init__(self, titulo : str, descripcion : str, 
                 prioridad : Prioridad, fecha_lim : dt):
        super.__init(titulo, descripcion, prioridad, fecha_lim)
    
    def completar(self):
        super().completar()
        print(f'Tarea Simple {self.titulo} ha sido completada')
    
class TareaRecurrente(Tarea):


    def __init__(self, titulo: str, descripcion: str,
                 prioridad: Prioridad, fecha_lim: dt,
                 frecuencia : Frecuencia):
        super.__init__(titulo, descripcion, prioridad, fecha_lim)
        self.frecuencia = frecuencia
    
    def completar(self):
        """
        In this subclass what´s fuction does different 
        from its mother class or the other subclass 
        its that it restarts the homework/task status 
        back to PENDIENTE and its fecha_lim gets moved forward
        by the number of days the user put.
        """
        super().completar()
        self.ultima_completada = dt.now()
        self.fecha_lim = self.fecha_lim + timedelta(days=self.frecuencia.value)
        self.estado = Estado.PENDIENTE