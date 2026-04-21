# Ejemplo 1 de ejecucion e interaccion entre clases

from datetime import datetime, timedelta
from Classes.all_classes import (Tarea, TareaSimple, TareaRecurrente, Proyecto, Prioridad, Frecuencia, Estado)

# Creamos Tareas
tarea_simple = TareaSimple(titulo='Finalizar all_classes.py', 
                           descripcion='Implementar Clases POO', 
                           prioridad=Prioridad.ALTA,
                           fecha_lim=datetime.now() + timedelta(days=2))

tarea_recurrente = TareaRecurrente(titulo='Aprender Python y customtkinter', 
                                   descripcion='Dedicar 30 min al dia a aprender estas dos', 
                                   prioridad=Prioridad.MEDIA, 
                                   fecha_lim=datetime.now(), 
                                   frecuencia=Frecuencia.Diaria)

# Crear Proyecto
proyecto = Proyecto(nombre='Proyecto POO', 
                    descripcion='Proyecto final de Programacion 2', 
                    fecha_lim=datetime.now() + timedelta(weeks=2))

# Agregamos Tareas Al Proyecto
proyecto.agregar_Tarea(tarea_simple)
proyecto.agregar_Tarea(tarea_recurrente)

# Completamos Tareas
tarea_simple.completar()
tarea_recurrente.completar()

# Verificar resultados
print("\n=== Estado del proyecto ===")
print(proyecto)
print("\nTareas pendientes:")
for tarea in proyecto.tareas_pendientes():
    print(f"- {tarea.titulo} (Estado: {tarea.estado.value})")

print("\nPorcentaje de avance:", proyecto.porcentaje_avance(), "%")