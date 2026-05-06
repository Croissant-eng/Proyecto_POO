import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime as dt

from Classes.all_classes import (
    GestorTareas,
    Usuario,
    Proyecto,
    TareaSimple,
    TareaRecurrente,
    Prioridad,
    Frecuencia,
    Estado,
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AppGestorTareas(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestor de Tareas")
        self.geometry("1200x800")
        self.minsize(1200, 700)
        self.configure(fg_color="white")

        self.gestor = GestorTareas()
        self.usuario_activo = None
        self.proyecto_activo = None
        self.tarea_seleccionada_idx = None
        self.proyecto_buttons = []
        self.tarea_widgets = []

        self._crear_interfaz()
        self.mostrar_vista("Resumen")

    # ──────────────────────────────────────────
    # LAYOUT PRINCIPAL
    # ──────────────────────────────────────────
    def _crear_interfaz(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._crear_sidebar()
        self._crear_contenedor_vistas()

    # ──────────────────────────────────────────
    # SIDEBAR
    # ──────────────────────────────────────────
    def _crear_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0, fg_color="#003153")
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(self.sidebar, text="📋", font=ctk.CTkFont(size=40),
                     text_color="#8B5CF6").pack(pady=(25, 5))
        ctk.CTkLabel(self.sidebar, text="Gestor de Tareas",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="white").pack(pady=(0, 20))

        self.nav_buttons = {}
        for texto in ["Resumen", "Proyectos", "Tareas", "Notificaciones", "Reportes"]:
            btn = ctk.CTkButton(
                self.sidebar, text=texto, width=190, height=40, corner_radius=10,
                fg_color="transparent", hover_color="#4338CA", anchor="w",
                command=lambda t=texto: self.mostrar_vista(t)
            )
            btn.pack(padx=18, pady=6)
            self.nav_buttons[texto] = btn

        # Resumen rápido siempre visible en sidebar
        self.resumen_card = ctk.CTkFrame(self.sidebar, fg_color="#13224A", corner_radius=14,
                                         border_width=1, border_color="#223568")
        self.resumen_card.pack(fill="x", padx=14, pady=(30, 18), side="bottom")

        ctk.CTkLabel(self.resumen_card, text="Resumen rápido",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="white").pack(anchor="w", padx=14, pady=(14, 10))

        self.lbl_side_proyectos   = ctk.CTkLabel(self.resumen_card, text="Proyectos: 0",        text_color="white", anchor="w")
        self.lbl_side_tareas      = ctk.CTkLabel(self.resumen_card, text="Tareas totales: 0",   text_color="white", anchor="w")
        self.lbl_side_completadas = ctk.CTkLabel(self.resumen_card, text="Completadas: 0",       text_color="white", anchor="w")
        self.lbl_side_pendientes  = ctk.CTkLabel(self.resumen_card, text="Pendientes: 0",        text_color="white", anchor="w")
        self.lbl_side_proximas    = ctk.CTkLabel(self.resumen_card, text="Próximas a vencer: 0", text_color="white", anchor="w")

        for lbl in [self.lbl_side_proyectos, self.lbl_side_tareas,
                    self.lbl_side_completadas, self.lbl_side_pendientes]:
            lbl.pack(fill="x", padx=14, pady=2)
        self.lbl_side_proximas.pack(fill="x", padx=14, pady=(2, 14))

    # ──────────────────────────────────────────
    # CONTENEDOR DE VISTAS
    # ──────────────────────────────────────────
    def _crear_contenedor_vistas(self):
        self.contenedor = ctk.CTkFrame(self, fg_color="#F4F7FB", corner_radius=0)
        self.contenedor.grid(row=0, column=1, sticky="nsew")
        self.contenedor.grid_columnconfigure(0, weight=1)
        self.contenedor.grid_rowconfigure(1, weight=1)

        self._crear_header()

        self.vistas = {}
        self._crear_vista_resumen()
        self._crear_vista_proyectos()
        self._crear_vista_tareas()
        self._crear_vista_notificaciones()
        self._crear_vista_reportes()

    # ──────────────────────────────────────────
    # HEADER COMPARTIDO
    # ──────────────────────────────────────────
    def _crear_header(self):
        header = ctk.CTkFrame(self.contenedor, fg_color="#F4F7FB")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(18, 8))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(header, text="Gestor de Tareas",
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color="#111827").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text="Organiza tus proyectos y tareas de manera eficiente",
                     font=ctk.CTkFont(size=13), text_color="#64748B").grid(row=1, column=0, sticky="w")

        user_box = ctk.CTkFrame(header, fg_color="#F4F7FB")
        user_box.grid(row=0, column=1, rowspan=2, sticky="e")

        self.lbl_usuario = ctk.CTkLabel(user_box, text="Usuario activo:\nNinguno",
                                        font=ctk.CTkFont(size=13, weight="bold"),
                                        text_color="#1F2A44", justify="left")
        self.lbl_usuario.grid(row=0, column=0, padx=(0, 15))

        ctk.CTkButton(user_box, text="Cerrar Sesión", fg_color="#EF4444",
                      hover_color="#DC2626", width=120,
                      command=self.cerrar_sesion).grid(row=0, column=1)

    # ──────────────────────────────────────────
    # NAVEGACIÓN
    # ──────────────────────────────────────────
    def mostrar_vista(self, nombre):
        for frame in self.vistas.values():
            frame.grid_remove()
        for texto, btn in self.nav_buttons.items():
            btn.configure(fg_color="#4F46E5" if texto == nombre else "transparent")
        self.vistas[nombre].grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 20))
        self.actualizar_dashboard()

    # ══════════════════════════════════════════
    # VISTA: RESUMEN
    # ══════════════════════════════════════════
    def _crear_vista_resumen(self):
        frame = ctk.CTkFrame(self.contenedor, fg_color="#F4F7FB")
        frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        frame.grid_rowconfigure(1, weight=1)

        self.card_proyectos  = self._crear_card_stat(frame, 0, "📁", "Proyectos",         "0", "Activos")
        self.card_tareas     = self._crear_card_stat(frame, 1, "✅", "Tareas totales",     "0", "Todas tus tareas")
        self.card_pendientes = self._crear_card_stat(frame, 2, "🕒", "Pendientes",         "0", "Por completar")
        self.card_proximas   = self._crear_card_stat(frame, 3, "🚩", "Próximas a vencer",  "0", "En 3 días")

        info = ctk.CTkFrame(frame, fg_color="white", corner_radius=16,
                            border_width=1, border_color="#E5E7EB")
        info.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=(12, 0))
        ctk.CTkLabel(
            info,
            text="👋  Bienvenido al Gestor de Tareas.\n\nUsa el menú lateral para navegar entre secciones:\n"
                 "  • Proyectos → crear usuario y proyectos\n"
                 "  • Tareas    → agregar y gestionar tareas del proyecto activo\n"
                 "  • Notificaciones → ver alertas de tareas próximas a vencer\n"
                 "  • Reportes  → generar reporte general",
            font=ctk.CTkFont(size=14),
            text_color="#334155",
            justify="left"
        ).pack(anchor="nw", padx=24, pady=20)

        self.vistas["Resumen"] = frame

    def _crear_card_stat(self, parent, col, icono, titulo, numero, subtitulo):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=16,
                            border_width=1, border_color="#E5E7EB")
        card.grid(row=0, column=col, padx=8, pady=6, sticky="nsew")

        ctk.CTkLabel(card, text=icono, font=ctk.CTkFont(size=30)).grid(
            row=0, column=0, rowspan=3, padx=18, pady=18)
        ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#334155").grid(row=0, column=1, sticky="w", pady=(16, 0))

        lbl_num = ctk.CTkLabel(card, text=numero,
                               font=ctk.CTkFont(size=26, weight="bold"), text_color="#111827")
        lbl_num.grid(row=1, column=1, sticky="w")

        ctk.CTkLabel(card, text=subtitulo, font=ctk.CTkFont(size=11),
                     text_color="#64748B").grid(row=2, column=1, sticky="w", pady=(0, 16))

        card.lbl_num = lbl_num
        return card

    # ══════════════════════════════════════════
    # VISTA: PROYECTOS
    # ══════════════════════════════════════════
    def _crear_vista_proyectos(self):
        frame = ctk.CTkFrame(self.contenedor, fg_color="#F4F7FB")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Mis Proyectos",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#1F2A44").grid(row=0, column=0, sticky="w", pady=(0, 10))

        body = ctk.CTkFrame(frame, fg_color="#F4F7FB")
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # ── Izquierdo: formularios ──
        left = ctk.CTkFrame(body, fg_color="white", corner_radius=16,
                            border_width=1, border_color="#E5E7EB")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Crear Usuario",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#1F2A44").grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        self.entry_usuario = ctk.CTkEntry(left, placeholder_text="Nombre del usuario")
        self.entry_usuario.grid(row=1, column=0, sticky="ew", padx=16, pady=6)

        ctk.CTkButton(left, text="Crear usuario", fg_color="#4F46E5", hover_color="#4338CA",
                      command=self.crear_usuario).grid(row=2, column=0, sticky="ew", padx=16, pady=(4, 16))

        ctk.CTkFrame(left, fg_color="#E5E7EB", height=1).grid(row=3, column=0, sticky="ew", padx=16)

        ctk.CTkLabel(left, text="Nuevo Proyecto",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#1F2A44").grid(row=4, column=0, sticky="w", padx=16, pady=(14, 6))

        self.entry_nombre_proyecto = ctk.CTkEntry(left, placeholder_text="Nombre del proyecto")
        self.entry_nombre_proyecto.grid(row=5, column=0, sticky="ew", padx=16, pady=6)

        self.entry_desc_proyecto = ctk.CTkEntry(left, placeholder_text="Descripción del proyecto")
        self.entry_desc_proyecto.grid(row=6, column=0, sticky="ew", padx=16, pady=6)

        self.entry_fecha_proyecto = ctk.CTkEntry(left, placeholder_text="Fecha límite (YYYY-MM-DD)")
        self.entry_fecha_proyecto.grid(row=7, column=0, sticky="ew", padx=16, pady=6)
        self.entry_fecha_proyecto.insert(0, "2026-12-31")

        ctk.CTkButton(left, text="+ Nuevo Proyecto", fg_color="#4F46E5", hover_color="#4338CA",
                      command=self.crear_proyecto).grid(row=8, column=0, sticky="ew", padx=16, pady=(8, 16))

        # ── Derecho: lista de proyectos ──
        right = ctk.CTkFrame(body, fg_color="white", corner_radius=16,
                             border_width=1, border_color="#E5E7EB")
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(right, text="Lista de Proyectos",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#1F2A44").grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        self.lista_proyectos = ctk.CTkScrollableFrame(right, fg_color="#F8FAFC")
        self.lista_proyectos.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

        self.vistas["Proyectos"] = frame

    # ══════════════════════════════════════════
    # VISTA: TAREAS
    # ══════════════════════════════════════════
    def _crear_vista_tareas(self):
        frame = ctk.CTkFrame(self.contenedor, fg_color="#F4F7FB")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_rowconfigure(0, weight=1)

        # ── Izquierdo: formulario nueva tarea ──
        form = ctk.CTkFrame(frame, fg_color="white", corner_radius=16,
                            border_width=1, border_color="#E5E7EB")
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(form, text="Agregar Nueva Tarea",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#1F2A44").grid(row=0, column=0, sticky="w", padx=16, pady=(14, 10))

        self.entry_titulo = ctk.CTkEntry(form, placeholder_text="Título")
        self.entry_titulo.grid(row=1, column=0, sticky="ew", padx=16, pady=6)

        self.text_desc_tarea = ctk.CTkTextbox(form, height=80)
        self.text_desc_tarea.grid(row=2, column=0, sticky="ew", padx=16, pady=6)

        self.entry_fecha_tarea = ctk.CTkEntry(form, placeholder_text="Fecha límite (YYYY-MM-DD)")
        self.entry_fecha_tarea.grid(row=3, column=0, sticky="ew", padx=16, pady=6)
        self.entry_fecha_tarea.insert(0, "2026-12-31")

        self.combo_prioridad = ctk.CTkComboBox(form, values=["BAJA", "MEDIA", "ALTA", "CRITICA"])
        self.combo_prioridad.grid(row=4, column=0, sticky="ew", padx=16, pady=6)
        self.combo_prioridad.set("MEDIA")

        self.combo_tipo = ctk.CTkComboBox(form, values=["Simple", "Recurrente"],
                                          command=self.cambiar_tipo_tarea)
        self.combo_tipo.grid(row=5, column=0, sticky="ew", padx=16, pady=6)
        self.combo_tipo.set("Simple")

        self.combo_frecuencia = ctk.CTkComboBox(form, values=["Diaria", "Semanal", "Mensual"],
                                                state="disabled")
        self.combo_frecuencia.grid(row=6, column=0, sticky="ew", padx=16, pady=6)
        self.combo_frecuencia.set("Diaria")

        ctk.CTkButton(form, text="Agregar Tarea", fg_color="#4F46E5", hover_color="#4338CA",
                      height=42, command=self.agregar_tarea).grid(
            row=7, column=0, sticky="ew", padx=16, pady=(12, 16))

        # ── Derecho: tabla de tareas ──
        tabla_panel = ctk.CTkFrame(frame, fg_color="white", corner_radius=16,
                                   border_width=1, border_color="#E5E7EB")
        tabla_panel.grid(row=0, column=1, sticky="nsew")
        tabla_panel.grid_columnconfigure(0, weight=1)
        tabla_panel.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(tabla_panel, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        top.grid_columnconfigure(0, weight=1)

        self.lbl_titulo_tabla = ctk.CTkLabel(top, text="Tareas del proyecto: Ninguno",
                                             font=ctk.CTkFont(size=18, weight="bold"),
                                             text_color="#1F2A44")
        self.lbl_titulo_tabla.grid(row=0, column=0, sticky="w")

        self.tabla_frame = ctk.CTkScrollableFrame(tabla_panel, fg_color="#F8FAFC")
        self.tabla_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 10))

        acciones = ctk.CTkFrame(tabla_panel, fg_color="transparent")
        acciones.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 16))
        acciones.grid_columnconfigure(3, weight=1)

        ctk.CTkButton(acciones, text="✅ Completar", fg_color="#16A34A", hover_color="#15803D",
                      command=self.completar_tarea).grid(row=0, column=0, padx=(0, 10))
        ctk.CTkButton(acciones, text="🗑 Eliminar", fg_color="#EF4444", hover_color="#DC2626",
                      command=self.eliminar_tarea).grid(row=0, column=1, padx=(0, 10))
        ctk.CTkButton(acciones, text="🔄 Actualizar", fg_color="#E2E8F0", text_color="#1F2A44",
                      hover_color="#CBD5E1",
                      command=self.actualizar_tabla_tareas).grid(row=0, column=4)

        self.vistas["Tareas"] = frame

    # ══════════════════════════════════════════
    # VISTA: NOTIFICACIONES
    # ══════════════════════════════════════════
    def _crear_vista_notificaciones(self):
        frame = ctk.CTkFrame(self.contenedor, fg_color="#F4F7FB")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Notificaciones",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#1F2A44").grid(row=0, column=0, sticky="w", pady=(0, 10))

        card = ctk.CTkFrame(frame, fg_color="white", corner_radius=16,
                            border_width=1, border_color="#E5E7EB")
        card.grid(row=1, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(card, text="Notificaciones Recientes",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color="#1F2A44").grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))

        self.texto_notificaciones = ctk.CTkTextbox(card)
        self.texto_notificaciones.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 12))

        ctk.CTkButton(card, text="🔔 Ver Notificaciones", fg_color="#4F46E5", hover_color="#4338CA",
                      command=self.mostrar_notificaciones).grid(
            row=2, column=0, sticky="ew", padx=16, pady=(0, 16))

        self.vistas["Notificaciones"] = frame

    # ══════════════════════════════════════════
    # VISTA: REPORTES
    # ══════════════════════════════════════════
    def _crear_vista_reportes(self):
        frame = ctk.CTkFrame(self.contenedor, fg_color="#F4F7FB")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Reportes",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#1F2A44").grid(row=0, column=0, sticky="w", pady=(0, 10))

        card = ctk.CTkFrame(frame, fg_color="white", corner_radius=16,
                            border_width=1, border_color="#E5E7EB")
        card.grid(row=1, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(card, text="Reporte General",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color="#1F2A44").grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))

        self.texto_reporte = ctk.CTkTextbox(card)
        self.texto_reporte.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 12))

        ctk.CTkButton(card, text="📊 Generar Reporte Completo", fg_color="#4F46E5",
                      hover_color="#4338CA",
                      command=self.mostrar_reporte).grid(
            row=2, column=0, sticky="ew", padx=16, pady=(0, 16))

        self.vistas["Reportes"] = frame

    # ──────────────────────────────────────────
    # LÓGICA / ACCIONES
    # ──────────────────────────────────────────
    def parsear_fecha(self, texto):
        try:
            return dt.strptime(texto.strip(), "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener formato YYYY-MM-DD")

    def cambiar_tipo_tarea(self, valor):
        if valor == "Recurrente":
            self.combo_frecuencia.configure(state="normal")
        else:
            self.combo_frecuencia.set("Diaria")
            self.combo_frecuencia.configure(state="disabled")

    def limpiar_formulario_tarea(self):
        self.entry_titulo.delete(0, "end")
        self.text_desc_tarea.delete("1.0", "end")
        self.entry_fecha_tarea.delete(0, "end")
        self.entry_fecha_tarea.insert(0, "2026-12-31")
        self.combo_prioridad.set("MEDIA")
        self.combo_tipo.set("Simple")
        self.combo_frecuencia.set("Diaria")
        self.combo_frecuencia.configure(state="disabled")

    def cerrar_sesion(self):
        self.usuario_activo = None
        self.proyecto_activo = None
        self.tarea_seleccionada_idx = None
        self.lbl_usuario.configure(text="Usuario activo:\nNinguno")
        self.lbl_titulo_tabla.configure(text="Tareas del proyecto: Ninguno")
        self.texto_reporte.delete("1.0", "end")
        self.texto_notificaciones.delete("1.0", "end")
        self.actualizar_lista_proyectos()
        self.actualizar_tabla_tareas()
        self.actualizar_dashboard()

    def crear_usuario(self):
        nombre = self.entry_usuario.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Debes escribir un nombre de usuario.")
            return
        self.usuario_activo = Usuario(nombre)
        self.gestor.registrarUsuario(self.usuario_activo)
        self.lbl_usuario.configure(text=f"Usuario activo:\n{nombre}")
        self.entry_usuario.delete(0, "end")
        self.actualizar_dashboard()
        messagebox.showinfo("Éxito", f"Usuario '{nombre}' creado correctamente.")

    def crear_proyecto(self):
        if self.usuario_activo is None:
            messagebox.showerror("Error", "Primero debes crear un usuario.")
            return
        nombre = self.entry_nombre_proyecto.get().strip()
        descripcion = self.entry_desc_proyecto.get().strip()
        fecha_texto = self.entry_fecha_proyecto.get().strip()
        if not nombre or not fecha_texto:
            messagebox.showerror("Error", "Debes capturar nombre y fecha límite del proyecto.")
            return
        try:
            fecha_lim = self.parsear_fecha(fecha_texto)
            proyecto = Proyecto(nombre, descripcion, fecha_lim)
            self.usuario_activo.agregar_proyecto(proyecto)
            self.entry_nombre_proyecto.delete(0, "end")
            self.entry_desc_proyecto.delete(0, "end")
            self.entry_fecha_proyecto.delete(0, "end")
            self.entry_fecha_proyecto.insert(0, "2026-12-31")
            self.actualizar_lista_proyectos()
            self.actualizar_dashboard()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_lista_proyectos(self):
        for btn in self.proyecto_buttons:
            btn.destroy()
        self.proyecto_buttons.clear()
        if not self.usuario_activo:
            return
        for i, proyecto in enumerate(self.usuario_activo.proyectos):
            btn = ctk.CTkButton(
                self.lista_proyectos,
                text=proyecto.nombre,
                anchor="w",
                height=42,
                corner_radius=10,
                fg_color="#DBEAFE" if proyecto == self.proyecto_activo else "white",
                text_color="#1F2A44",
                hover_color="#BFDBFE",
                border_width=1,
                border_color="#D1D5DB",
                command=lambda idx=i: self.seleccionar_proyecto(idx),
            )
            btn.pack(fill="x", padx=6, pady=6)
            self.proyecto_buttons.append(btn)

    def seleccionar_proyecto(self, indice):
        if self.usuario_activo is None:
            return
        self.proyecto_activo = self.usuario_activo.proyectos[indice]
        self.tarea_seleccionada_idx = None
        self.lbl_titulo_tabla.configure(text=f"Tareas: {self.proyecto_activo.nombre}")
        self.actualizar_lista_proyectos()
        self.actualizar_tabla_tareas()
        # Al seleccionar un proyecto, navegar automáticamente a Tareas
        self.mostrar_vista("Tareas")

    def agregar_tarea(self):
        if self.proyecto_activo is None:
            messagebox.showerror("Error", "Debes seleccionar un proyecto desde la sección 'Proyectos'.")
            return
        titulo = self.entry_titulo.get().strip()
        descripcion = self.text_desc_tarea.get("1.0", "end").strip()
        fecha_texto = self.entry_fecha_tarea.get().strip()
        prioridad_texto = self.combo_prioridad.get().strip()
        tipo_tarea = self.combo_tipo.get().strip()
        if not titulo or not fecha_texto:
            messagebox.showerror("Error", "Completa título y fecha límite.")
            return
        try:
            fecha_lim = self.parsear_fecha(fecha_texto)
            prioridad = Prioridad[prioridad_texto]
            if tipo_tarea == "Simple":
                tarea = TareaSimple(titulo, descripcion, fecha_lim, prioridad)
            else:
                frecuencia = Frecuencia[self.combo_frecuencia.get().strip()]
                tarea = TareaRecurrente(titulo, descripcion, fecha_lim, prioridad, frecuencia)
            self.proyecto_activo.agregar_Tarea(tarea)
            self.limpiar_formulario_tarea()
            self.actualizar_tabla_tareas()
            self.actualizar_dashboard()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def seleccionar_tarea(self, indice):
        self.tarea_seleccionada_idx = indice
        self.actualizar_tabla_tareas()

    def actualizar_tabla_tareas(self):
        for widget in self.tarea_widgets:
            widget.destroy()
        self.tarea_widgets.clear()
        if self.proyecto_activo is None:
            return
        headers = ["Título", "Tipo", "Prioridad", "Estado", "Fecha límite", "Días"]
        for col, h in enumerate(headers):
            lbl = ctk.CTkLabel(self.tabla_frame, text=h,
                               font=ctk.CTkFont(size=13, weight="bold"), text_color="#334155")
            lbl.grid(row=0, column=col, padx=8, pady=(8, 10), sticky="w")
            self.tarea_widgets.append(lbl)
        for i, tarea in enumerate(self.proyecto_activo.tareas, start=1):
            tipo = "Simple" if isinstance(tarea, TareaSimple) else "Recurrente"
            estado = tarea.estado.value
            fecha = tarea.fecha_lim.strftime("%Y-%m-%d")
            dias = "Completada" if tarea.estado == Estado.COMPLETADA else str(tarea.dias_restantes())
            selected = (self.tarea_seleccionada_idx == i - 1)
            fg = "#EEF2FF" if selected else "white"
            for col, valor in enumerate([tarea.titulo, tipo, tarea.prioridad.name, estado, fecha, dias]):
                btn = ctk.CTkButton(
                    self.tabla_frame,
                    text=str(valor),
                    fg_color=fg,
                    text_color="#1F2A44",
                    hover_color="#DBEAFE",
                    anchor="w" if col == 0 else "center",
                    corner_radius=8,
                    height=34,
                    command=lambda idx=i - 1: self.seleccionar_tarea(idx),
                )
                btn.grid(row=i, column=col, padx=6, pady=4, sticky="ew")
                self.tarea_widgets.append(btn)

    def obtener_tarea_seleccionada(self):
        if self.proyecto_activo is None or self.tarea_seleccionada_idx is None:
            return None
        if self.tarea_seleccionada_idx >= len(self.proyecto_activo.tareas):
            return None
        return self.proyecto_activo.tareas[self.tarea_seleccionada_idx]

    def completar_tarea(self):
        tarea = self.obtener_tarea_seleccionada()
        if tarea is None:
            messagebox.showerror("Error", "Selecciona una tarea.")
            return
        try:
            tarea.completar()
            self.actualizar_tabla_tareas()
            self.actualizar_dashboard()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_tarea(self):
        tarea = self.obtener_tarea_seleccionada()
        if tarea is None:
            messagebox.showerror("Error", "Selecciona una tarea.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la tarea '{tarea.titulo}'?"):
            return
        self.proyecto_activo.eliminar_tarea(tarea)
        self.tarea_seleccionada_idx = None
        self.actualizar_tabla_tareas()
        self.actualizar_dashboard()

    def mostrar_reporte(self):
        try:
            reporte = self.gestor.reporte_general()
            if self.proyecto_activo:
                reporte += f"\nProyecto activo: {self.proyecto_activo.nombre}\n"
                reporte += f"Avance del proyecto: {self.proyecto_activo.porcentaje_avance():.1f}%\n"
            self.texto_reporte.delete("1.0", "end")
            self.texto_reporte.insert("1.0", reporte)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_notificaciones(self):
        if self.usuario_activo is None:
            messagebox.showerror("Error", "No hay usuario activo.")
            return
        self.usuario_activo.notificaciones.clear()
        self.gestor.generar_notificaciones(self.usuario_activo)
        self.texto_notificaciones.delete("1.0", "end")
        if not self.usuario_activo.notificaciones:
            self.texto_notificaciones.insert("1.0", "No hay notificaciones nuevas.")
            return
        texto = ""
        for notif in self.usuario_activo.notificaciones:
            texto += str(notif) + "\n\n"
        self.texto_notificaciones.insert("1.0", texto)

    def actualizar_dashboard(self):
        if self.usuario_activo is None:
            total_proyectos = total_tareas = completadas = pendientes = proximas = 0
        else:
            total_proyectos = len(self.usuario_activo.proyectos)
            todas = self.usuario_activo.todas_las_tareas()
            total_tareas = len(todas)
            completadas = len([t for t in todas if t.estado == Estado.COMPLETADA])
            pendientes = total_tareas - completadas
            proximas = len([
                t for t in todas
                if not t.esta_vencida() and t.estado != Estado.COMPLETADA and 0 <= t.dias_restantes() <= 3
            ])

        self.card_proyectos.lbl_num.configure(text=str(total_proyectos))
        self.card_tareas.lbl_num.configure(text=str(total_tareas))
        self.card_pendientes.lbl_num.configure(text=str(pendientes))
        self.card_proximas.lbl_num.configure(text=str(proximas))

        self.lbl_side_proyectos.configure(text=f"Proyectos: {total_proyectos}")
        self.lbl_side_tareas.configure(text=f"Tareas totales: {total_tareas}")
        self.lbl_side_completadas.configure(text=f"Completadas: {completadas}")
        self.lbl_side_pendientes.configure(text=f"Pendientes: {pendientes}")
        self.lbl_side_proximas.configure(text=f"Próximas a vencer: {proximas}")


if __name__ == "__main__":
    app = AppGestorTareas()
    app.mainloop()
