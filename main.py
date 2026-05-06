import sys
from pathlib import Path


# Asegura que Python pueda encontrar los archivos del proyecto
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# Tu archivo Guiproy.py importa desde "Modelo".
# Como tu Modelo.py actual busca "Classes.all_classes", hacemos que "Modelo"
# apunte directamente a all_classes.py para que no marque error de importación.
try:
    import all_classes as Modelo
    sys.modules["Modelo"] = Modelo
except Exception as error:
    print("ERROR: No se pudo cargar all_classes.py")
    print(f"Detalle: {error}")
    sys.exit(1)


# Importa la ventana principal de la interfaz gráfica
try:
    from Guiproy import AppGestorTareas
except ModuleNotFoundError as error:
    if "customtkinter" in str(error):
        print("ERROR: Falta instalar customtkinter.")
        print("Instálalo con este comando:")
        print("    pip install customtkinter")
    else:
        print("ERROR: No se pudo importar Guiproy.py")
        print(f"Detalle: {error}")
    sys.exit(1)
except Exception as error:
    print("ERROR: Ocurrió un problema al cargar la interfaz.")
    print(f"Detalle: {error}")
    sys.exit(1)


def main():
    """Arranca la aplicación."""
    app = AppGestorTareas()
    app.mainloop()


if __name__ == "__main__":
    main()