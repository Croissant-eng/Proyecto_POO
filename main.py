from datetime import datetime, timedelta
from Classes.all_classes import (
    Tarea, TareaSimple, TareaRecurrente, Proyecto,
    Usuario, Notificacion, GestorTareas, Prioridad, Frecuencia, Estado
)

# Inicializamos el sistema
Gestor = GestorTareas()

# Creamos un usuario
usuario1 = Usuario(nombre='Aquiles')
Gestor.registrarUsuario(usuario=usuario1)

# Creamos un proyecto
proyecto = Proyecto(nombre='Proyecto1', descripcion='Primer Proyecto', 
                    fecha_lim=datetime.now() + timedelta(days=30))
usuario1.agregar_proyecto(proyecto)

# Creamos tareas
tareasimple = TareaSimple(titulo='Terminar Proyecto', descripcion='Implementar OOP',
                          prioridad=Prioridad.MEDIA, fecha_lim=datetime.now() + timedelta(days=4))

tarearecurrente = TareaRecurrente(titulo='Aprender Python', descripcion='Aprendizaje Constante en python',
                                  prioridad=Prioridad.MEDIA, fecha_lim=datetime.now() + timedelta(days=3),
                                  frecuencia=Frecuencia.Semanal)

# Agregamos Tareas al Proyecto
proyecto.agregar_Tarea(tareasimple)
proyecto.agregar_Tarea(tarearecurrente)

# Simulamos el flujo de trabajo
tareasimple.completar()
tarearecurrente.completar()

# Generamos notificaciones
Gestor.generar_notificaciones(usuario1)

# Mostramos resultados
# 8. Mostrar resultados
print("\n=== REPORTES DEL SISTEMA ===")
print(Gestor.reporte_general())
print("\nNotificaciones del usuario:")
for notif in usuario1.notificaciones:
    print(notif)
print("\nTareas próximas a vencer:")
for tarea in Gestor.tareas_proximas_a_vencer():
    print(f"- {tarea.titulo} (Vence: {tarea.fecha_lim.strftime('%Y-%m-%d')})")

# Test final de codigo de clases