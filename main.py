from modelo import Usuario, GestorTareas
from gui import App
from controlador import ControladorTareas

def iniciar_aplicacion():
    # 1. Instanciamos el Modelo
    # Creamos al usuario que tendrá la sesión activa
    usuario_estudiante = Usuario("Usuario Ibero")
    
    # Registramos al usuario en el Gestor de Tareas global
    gestor_sistema = GestorTareas()
    gestor_sistema.registrarUsuario(usuario_estudiante)
    
    # 2. Instanciamos la Vista (La interfaz gráfica)
    vista_interfaz = App()
    
    # 3. Creamos el Controlador
    # Para que pueda coordinar las acciones del usuario.
    controlador = ControladorTareas(usuario_estudiante, vista_interfaz)
    
    # 4. Ejecución del loop principal
    vista_interfaz.run()

if __name__ == "__main__":
    iniciar_aplicacion()
