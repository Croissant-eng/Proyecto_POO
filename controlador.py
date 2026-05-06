from modelo import Proyecto, TareaSimple, Prioridad, dt, timedelta

class ControladorTareas:
    def __init__(self, modelo_usuario, vista_app):
        """
        COMPOSICIÓN: El controlador recibe y almacena las referencias 
        del modelo y la vista para coordinarlos.
        """
        self.usuario = modelo_usuario
        self.vista = vista_app
        
        # Conectamos los botones de la vista con los métodos de este controlador
        self.vista.btn_add_proyecto.configure(command=self.procesar_nuevo_proyecto)
        self.vista.btn_add_tarea.configure(command=self.procesar_nueva_tarea)
        self.vista.btn_completar.configure(command=self.marcar_tarea_listo)
        self.vista.btn_eliminar.configure(command=self.eliminar_tarea_actual)

    def procesar_nuevo_proyecto(self):
        # 1. Obtener datos de la Vista
        nombre = self.vista.entry_proyecto.get().strip()
        
        if nombre:
            # 2. Lógica del Modelo: Crear el objeto Proyecto
            # Asignamos una fecha límite por defecto de 30 días
            fecha_lim = dt.now() + timedelta(days=30)
            nuevo_p = Proyecto(nombre, "Proyecto creado desde la interfaz", fecha_lim)
            
            # 3. Actualizar el Modelo de datos
            self.usuario.agregar_proyecto(nuevo_p)
            
            # 4. Limpiar y refrescar la Vista
            self.vista.entry_proyecto.delete(0, 'end')
            self.vista.proyecto_activo = nuevo_p # Sincronizamos el estado visual
            self.actualizar_interfaz_completa()

    def procesar_nueva_tarea(self):
        # 1. Obtener datos de la Vista
        titulo = self.vista.entry_tarea.get().strip()
        prioridad_str = self.vista.combo_prioridad.get()
        
        # Mapeo de texto de la vista a los Enums del modelo
        mapeo_prioridad = {
            "BAJA": Prioridad.BAJA,
            "MEDIA": Prioridad.MEDIA,
            "ALTA": Prioridad.ALTA
        }
        
        if titulo and self.vista.proyecto_activo:
            # 2. Crear el objeto Tarea usando las clases del modelo
            nueva_t = TareaSimple(
                titulo, 
                "Tarea pendiente", 
                dt.now() + timedelta(days=7), 
                mapeo_prioridad.get(prioridad_str, Prioridad.MEDIA)
            )
            
            # 3. Vincular la tarea al proyecto activo en el Modelo
            proyecto_actual = self.vista.proyecto_activo
            proyecto_actual.agregar_Tarea(nueva_t)
            
            # 4. Refrescar Vista
            self.vista.entry_tarea.delete(0, 'end')
            self.actualizar_interfaz_completa()

    def marcar_tarea_listo(self):
        # Verificamos si hay una tarea seleccionada en la vista
        if self.vista.tarea_seleccionada:
            # Ejecutamos el método del modelo para cambiar el estado
            self.vista.tarea_seleccionada.completar()
            self.actualizar_interfaz_completa()

    def eliminar_tarea_actual(self):
        if self.vista.proyecto_activo and self.vista.tarea_seleccionada:
            # El controlador gestiona la eliminación a través del modelo
            proyecto = self.vista.proyecto_activo
            tarea = self.vista.tarea_seleccionada
            
            # Buscamos y removemos la tarea de la lista del modelo
            if tarea in proyecto.tareas:
                proyecto.tareas.remove(tarea)
                self.vista.tarea_seleccionada = None
                self.actualizar_interfaz_completa()

    def actualizar_interfaz_completa(self):
        """
        Sincroniza los datos actuales del modelo con lo que se muestra.
        """
        # Actualizamos la lista de proyectos de la vista con los del usuario
        self.vista.proyectos = self.usuario.proyectos
        self.vista.actualizar_todo()
