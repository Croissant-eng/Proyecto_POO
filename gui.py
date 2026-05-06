import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App:
    def __init__(self):
        self.app = ctk.CTk()

        self.app.title("Gestor de Tareas")
        self.app.geometry("900x750")
        self.app.configure(fg_color="#F4F7FB")

        self.proyectos = []
        self.proyecto_activo = None
        self.tarea_seleccionada = None

        self.crear_layout()

    def crear_layout(self):
        self.sidebar = ctk.CTkFrame(self.app, width=170, corner_radius=0, fg_color="#0B1533")
        self.sidebar.pack(side="left", fill="y")

        self.main = ctk.CTkFrame(self.app, fg_color="#F4F7FB")
        self.main.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(self.sidebar, text="📋", font=("Arial", 40)).pack(pady=(25, 5))

        ctk.CTkLabel(
            self.sidebar,
            text="Gestor de Tareas",
            text_color="white",
            font=("Arial", 17, "bold")
        ).pack(pady=(0, 25))

        for texto in ["General"]:
            ctk.CTkButton(
                self.sidebar,
                text=texto,
                width=140,
                height=35,
                fg_color="#4F46E5",
                anchor="w"
            ).pack(pady=6)

        self.resumen = ctk.CTkFrame(self.sidebar, fg_color="#13224A", corner_radius=12)
        self.resumen.pack(side="bottom", fill="x", padx=12, pady=15)

        self.lbl_resumen = ctk.CTkLabel(
            self.resumen,
            text="",
            text_color="white",
            justify="left"
        )
        self.lbl_resumen.pack(padx=12, pady=12)

        ctk.CTkLabel(
            self.main,
            text="Gestor de Tareas",
            font=("Arial", 28, "bold"),
            text_color="#111827"
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.main,
            text="Organiza tus proyectos y tareas de manera eficiente",
            text_color="#64748B"
        ).pack(anchor="w", pady=(0, 15))

        self.crear_cards()
        self.crear_contenido()
        self.actualizar_todo()

    def crear_cards(self):
        self.cards = ctk.CTkFrame(self.main, fg_color="transparent")
        self.cards.pack(fill="x", pady=5)

        self.lbl_proyectos = self.card("📁", "Proyectos", "0")
        self.lbl_tareas = self.card("✅", "Tareas", "0")
        self.lbl_pendientes = self.card("🕒", "Pendientes", "0")
        self.lbl_completadas = self.card("🚩", "Completadas", "0")

    def card(self, icono, titulo, numero):
        card = ctk.CTkFrame(
            self.cards,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.pack(side="left", expand=True, fill="x", padx=5)

        ctk.CTkLabel(card, text=icono, font=("Arial", 26)).pack(pady=(10, 0))

        ctk.CTkLabel(
            card,
            text=titulo,
            text_color="#64748B",
            font=("Arial", 12, "bold")
        ).pack()

        lbl = ctk.CTkLabel(
            card,
            text=numero,
            font=("Arial", 24, "bold"),
            text_color="#111827"
        )
        lbl.pack(pady=(0, 10))

        return lbl

    def crear_contenido(self):
        body = ctk.CTkFrame(self.main, fg_color="transparent")
        body.pack(fill="both", expand=True, pady=10)

        izquierda = ctk.CTkFrame(body, fg_color="white", corner_radius=14)
        izquierda.pack(side="left", fill="both", expand=True, padx=(0, 8))

        derecha = ctk.CTkFrame(body, fg_color="white", corner_radius=14)
        derecha.pack(side="right", fill="both", expand=True, padx=(8, 0))

        ctk.CTkLabel(
            izquierda,
            text="Mis Proyectos",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self.entry_proyecto = ctk.CTkEntry(
            izquierda,
            placeholder_text="Nombre del proyecto"
        )
        self.entry_proyecto.pack(fill="x", padx=15, pady=5)

        # LINEA MODIFICADA: Asignado a self.btn_add_proyecto
        self.btn_add_proyecto = ctk.CTkButton(
            izquierda,
            text="+ Nuevo Proyecto",
            command=self.agregar_proyecto
        )
        self.btn_add_proyecto.pack(fill="x", padx=15, pady=5)

        self.lista_proyectos = ctk.CTkScrollableFrame(izquierda, fg_color="#F8FAFC")
        self.lista_proyectos.pack(fill="both", expand=True, padx=15, pady=10)

        ctk.CTkLabel(
            derecha,
            text="Tareas del Proyecto",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self.entry_tarea = ctk.CTkEntry(
            derecha,
            placeholder_text="Título de la tarea"
        )
        self.entry_tarea.pack(fill="x", padx=15, pady=5)

        self.combo_prioridad = ctk.CTkComboBox(
            derecha,
            values=["BAJA", "MEDIA", "ALTA"]
        )
        self.combo_prioridad.set("MEDIA")
        self.combo_prioridad.pack(fill="x", padx=15, pady=5)

        # LINEA MODIFICADA: Asignado a self.btn_add_tarea
        self.btn_add_tarea = ctk.CTkButton(
            derecha,
            text="+ Agregar Tarea",
            command=self.agregar_tarea
        )
        self.btn_add_tarea.pack(fill="x", padx=15, pady=5)

        self.lista_tareas = ctk.CTkScrollableFrame(derecha, fg_color="#F8FAFC")
        self.lista_tareas.pack(fill="both", expand=True, padx=15, pady=10)

        botones = ctk.CTkFrame(derecha, fg_color="transparent")
        botones.pack(fill="x", padx=15, pady=(0, 10))

        # LINEA MODIFICADA: Asignado a self.btn_completar
        self.btn_completar = ctk.CTkButton(
            botones,
            text="Completar",
            fg_color="#16A34A",
            command=self.completar_tarea
        )
        self.btn_completar.pack(side="left", expand=True, fill="x", padx=3)

        # LINEA MODIFICADA: Asignado a self.btn_eliminar
        self.btn_eliminar = ctk.CTkButton(
            botones,
            text="Eliminar",
            fg_color="#EF4444",
            command=self.eliminar_tarea
        )
        self.btn_eliminar.pack(side="left", expand=True, fill="x", padx=3)

    def agregar_proyecto(self):
        nombre = self.entry_proyecto.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Escribe el nombre del proyecto.")
            return
        proyecto = {"nombre": nombre, "tareas": []}
        self.proyectos.append(proyecto)
        self.proyecto_activo = proyecto
        self.entry_proyecto.delete(0, "end")
        self.actualizar_todo()

    def obtener_proyecto_independiente(self):
        for proyecto in self.proyectos:
            if proyecto.nombre == "Tareas independientes":
                return proyecto
        proyecto = {"nombre": "Tareas independientes", "tareas": []}
        self.proyectos.append(proyecto)
        return proyecto

    def agregar_tarea(self):
        titulo = self.entry_tarea.get().strip()
        prioridad = self.combo_prioridad.get()
        if not titulo:
            messagebox.showerror("Error", "Escribe el título de la tarea.")
            return
        tarea = {"titulo": titulo, "prioridad": prioridad, "estado": "PENDIENTE"}
        if self.proyecto_activo is None:
            proyecto = self.obtener_proyecto_independiente()
            proyecto["tareas"].append(tarea)
            self.proyecto_activo = proyecto
        else:
            self.proyecto_activo["tareas"].append(tarea)
        self.entry_tarea.delete(0, "end")
        self.actualizar_todo()

    def seleccionar_proyecto(self, proyecto):
        self.proyecto_activo = proyecto
        self.tarea_seleccionada = None
        self.actualizar_todo()

    def seleccionar_tarea(self, tarea):
        self.tarea_seleccionada = tarea
        self.actualizar_todo()

    def completar_tarea(self):
        if self.tarea_seleccionada is None:
            messagebox.showerror("Error", "Selecciona una tarea.")
            return
        self.tarea_seleccionada["estado"] = "COMPLETADA"
        self.actualizar_todo()

    def eliminar_tarea(self):
        if self.proyecto_activo is None or self.tarea_seleccionada is None:
            messagebox.showerror("Error", "Selecciona una tarea.")
            return
        self.proyecto_activo["tareas"].remove(self.tarea_seleccionada)
        self.tarea_seleccionada = None
        self.actualizar_todo()

    def actualizar_todo(self):
        self.actualizar_proyectos()
        self.actualizar_tareas()
        self.actualizar_resumen()

    def actualizar_proyectos(self):
        for widget in self.lista_proyectos.winfo_children():
            widget.destroy()
        for proyecto in self.proyectos:
            color = "#DBEAFE" if proyecto == self.proyecto_activo else "white"
            ctk.CTkButton(
                self.lista_proyectos,
                text=proyecto.nombre,
                fg_color=color,
                text_color="#1F2A44",
                hover_color="#BFDBFE",
                anchor="w",
                command=lambda p=proyecto: self.seleccionar_proyecto(p)
            ).pack(fill="x", pady=4, padx=4)

    def actualizar_tareas(self):
        for widget in self.lista_tareas.winfo_children():
            widget.destroy()
        if self.proyecto_activo is None:
            ctk.CTkLabel(
                self.lista_tareas,
                text="No hay proyecto seleccionado.\nSi agregas una tarea, será independiente.",
                text_color="#64748B"
            ).pack(pady=20)
            return
        for tarea in self.proyecto_activo.tareas:
            texto = f'{tarea.titulo} | {tarea.prioridad.name} | {tarea.estado.name}'
            color = "#DCFCE7" if tarea.estado.name == "COMPLETADA" else "white"
            if tarea == self.tarea_seleccionada:
                color = "#EEF2FF"
            ctk.CTkButton(
                self.lista_tareas,
                text=texto,
                fg_color=color,
                text_color="#1F2A44",
                hover_color="#DBEAFE",
                anchor="w",
                command=lambda t=tarea: self.seleccionar_tarea(t)
            ).pack(fill="x", pady=4, padx=4)

    def actualizar_resumen(self):
        total_proyectos = len(self.proyectos)

        todas = []
        for proyecto in self.proyectos:
            todas += proyecto.tareas

        total_tareas = len(todas)
        completadas = len([t for t in todas if t.estado.name == "COMPLETADA"])
        pendientes = total_tareas - completadas

        self.lbl_proyectos.configure(text=str(total_proyectos))
        self.lbl_tareas.configure(text=str(total_tareas))
        self.lbl_pendientes.configure(text=str(pendientes))
        self.lbl_completadas.configure(text=str(completadas))

        self.lbl_resumen.configure(
            text=f"Resumen rápido\n\n"
                f"Proyectos: {total_proyectos}\n"
                f"Tareas: {total_tareas}\n"
                f"Completadas: {completadas}\n"
                f"Pendientes: {pendientes}"
        )

    def run(self):
        self.app.mainloop()
