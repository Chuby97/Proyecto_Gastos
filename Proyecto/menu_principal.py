import os
import json
import shutil

BASE_DIR = "proyectos"

def listar_proyectos():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    proyectos = [nombre for nombre in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, nombre))]
    return proyectos

def crear_proyecto(nombre):
    ruta = os.path.join(BASE_DIR, nombre)
    if os.path.exists(ruta):
        print("YA EXISTE UN PROYECTO CON ESE NOMBRE")
        return None
    os.makedirs(ruta)
    with open(os.path.join(ruta, "usuarios.json"), "w") as f:
        json.dump([], f, indent = 4)
    with open(os.path.join(ruta, "gastos_comunes.json"), "w") as f:
        data = {
            "total" : 0,
            "historial" : []
        }
        json.dump(data, f, indent = 4)
    print(f"Proyecto '{nombre}' creado correctamente.")
    return ruta

def resetear_proyecto(nombre):
    ruta = os.path.join(BASE_DIR, nombre)
    if not os.path.exists(ruta):
        print(f"El proyecto '{nombre}' no existe.")
        return
    if not os.path.isdir(ruta):
        print(f"'{nombre}' no es una carpeta de proyecto.")
        return

    confirm = input(f"¿Seguro que querés borrar todo el proyecto '{nombre}'? (s/n): ").strip().lower()
    if confirm == "s":
        shutil.rmtree(ruta)
        print(f"Proyecto '{nombre}' eliminado con éxito.")
    else:
        print("Operación cancelada.")

def resetear_todos_los_proyectos():
    confirm = input(f"¿Seguro que querés borrar todos los proyectos?  (s/n): ").strip().lower()
    if confirm == "s":
        if not os.path.exists(BASE_DIR):
            print("No existe la carpeta de proyectos.")
            return

        for nombre in os.listdir(BASE_DIR):
            ruta = os.path.join(BASE_DIR, nombre)
            if os.path.isdir(ruta):
                shutil.rmtree(ruta)
                print(f"Carpeta '{nombre}' eliminada.")
            else:
                os.remove(ruta)
                print(f"Archivo '{nombre}' eliminado.")
        print("Todos los proyectos han sido reseteados.")
    else:
        print("Operación cancelada.")

def seleccionar_proyecto():
    while True:
        print("Menu Proyectos:")
        print("\n1) Entrar a proyecto existente")
        print("2) Crear nuevo proyecto")
        print("3) Borrar proyecto en específico")
        print("4) Borrar todos los proyectos")
        print("10) Salir")
        opcion = int(input("Elige una opcion: "))

        if opcion == 1:
            proyectos = listar_proyectos()
            if not proyectos:
                print("ATENCIÓN: no hay proyectos creados todavía.")
                continue
            print("\nProyectos disponibles:")
            for p in proyectos:
                print(f"-   {p}")
            elegido = input("Escribe el nombre exacto del proyecto: ").strip().lower()
            if elegido in proyectos:
                print(f"Accediendo a proyecto '{elegido}'...")
                return os.path.join(BASE_DIR, elegido)
            else:
                print("Proyecto elegido no encontrado. Intenta nuevamente.")
        elif opcion == 2:
            nombre_nuevo = input("Nombre para el nuevo proyecto: ").strip().lower()
            ruta = crear_proyecto(nombre_nuevo)
            if ruta:
                return ruta
        elif opcion == 3:
            proyectos = listar_proyectos()
            if not proyectos:
                print("ATENCIÓN: no hay proyectos creados todavía.")
                continue
            print("\nProyectos disponibles:")
            for p in proyectos:
                print(f"-   {p}")
            elegido = input("Escribe el nombre exacto del proyecto: ").strip().lower()
            if elegido in proyectos:
                resetear_proyecto(elegido)
            else:
                print("Proyecto elegido no encontrado. Intenta nuevamente.")
        elif opcion == 4:
            resetear_todos_los_proyectos()
        elif opcion == 10:
            return None
            break
        else:
            print("Opcion inválida.")
