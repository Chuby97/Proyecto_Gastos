from usuarios import imprimir_usuarios, crear_usuario, listar_usuarios, listar_gastos_usuarios, agregar_gasto_usuario, limpiar_archivo, archivar_y_resetear_usuarios
from gastos_comunes import imprimir_gasto_comun, agregar_gastos_comunes, limpiar_archivo_gastos_comunes, listar_gastos_comunes, archivar_y_resetear_gastos_comunes
from datetime import date, datetime
import os
import json

def diferencia_meses(mes1, mes2):
    # mes1 y mes2 en formato "YYYY-MM" NO OLVIDAR ESTE DETALLE
    y1, m1 = map(int, mes1.split("-"))
    y2, m2 = map(int, mes2.split("-"))
    return abs((y1 - y2) * 12 + (m1 - m2))

def cargar_control_backup(ruta):
    if not os.path.exists(os.path.join(ruta, "control_backups.json")):
        hoy = date.today()
        mes = hoy.month
        año = hoy.year
        if mes == 1:
            mes_anterior = 12
            año_anterior = año - 1
        else:
            mes_anterior = mes - 1
            año_anterior = año
        mes_anterior_str = f"{año_anterior}-{mes_anterior:02d}"
        data = {
                "ultimo_backup" : mes_anterior_str
            }
        with open(os.path.join(ruta, "control_backups.json"), "w") as f:
            json.dump(data, f, indent = 4)
    with open(os.path.join(ruta, "control_backups.json"), "r") as f:
        return json.load(f)

def guardar_control_backup(ruta, ultimo):
    with open(os.path.join(ruta, "control_backups.json"), "w") as f:
        json.dump(ultimo, f, indent = 4)

def chequear_necesidad_backup(ruta):
    ultimo_mes = cargar_control_backup(ruta)
    mes_actual = datetime.now().strftime("%Y-%m")
    ruta_historial_gastos_comunes = os.path.join(ruta, "historial_gastos_comunes")
    ruta_gastos = os.path.join(ruta, "gastos_comunes.json")
    ruta_historial_usuarios = os.path.join(ruta, "historial_usuarios")
    ruta_usuarios = os.path.join(ruta, "usuarios.json")

    diferencia = diferencia_meses(mes_actual, ultimo_mes['ultimo_backup'])
    if diferencia >= 2:
        print("Realizando backup mensual automático")
        ok = archivar_y_resetear_gastos_comunes(ruta_historial_gastos_comunes)
        ok = ok and archivar_y_resetear_usuarios(ruta_historial_usuarios)
        if ok:
            print("Backup realizado correctamente")
        else:
            print("Error inesperado")
            return None
        ultimo_mes['ultimo_backup'] = mes_actual
        guardar_control_backup(ruta, ultimo_mes)
        return True
    return False


def backup(ruta):
    print("Realizando backup mensual automático")
    ruta_historial_gastos_comunes = os.path.join(ruta, "historial_gastos_comunes")
    ruta_historial_usuarios = os.path.join(ruta, "historial_usuarios")
    ok = archivar_y_resetear_gastos_comunes(ruta_historial_gastos_comunes)
    ok = ok and archivar_y_resetear_usuarios(ruta_historial_usuarios)
    if ok:
        print("Backup realizado correctamente")
    else:
        print("Error inesperado")
        return None
    return True

def mostrar_historial(ruta, anio, mes):
    print("Ingresando al historial...\n")
    ruta_historial_gastos_comunes = os.path.join(ruta, "historial_gastos_comunes")
    ruta_historial_usuarios = os.path.join(ruta, "historial_usuarios")
    mes_str = f"{anio}-{mes:02d}"

    ok = False

    for archivo in os.listdir(ruta_historial_gastos_comunes):
        if archivo.endswith("_gastos_comunes.json"):
            if archivo.startswith(mes_str):
                ruta_archivo = os.path.join(ruta_historial_gastos_comunes, archivo)
                print(f"El historial de gastos comunes del mes {mes} del año {anio} es:\n")
                ok = imprimir_gasto_comun(ruta_archivo)
    if not ok:
        print("No se encontro dicho historial de gastos comunes")
    ok = False

    for archivo in os.listdir(ruta_historial_usuarios):
        if archivo.endswith("_usuarios.json"):
            if archivo.startswith(mes_str):
                ruta_archivo = os.path.join(ruta_historial_usuarios, archivo)
                print(f"El historial de usuarios del mes {mes} del año {anio}")
                ok = imprimir_usuarios(ruta_archivo)
    if not ok:
        print("No se encontro dicho historial de usuarios")

def mostrar_menu(ruta):
    chequear_necesidad_backup(ruta)
    while True:
        print("----- MENU -----\n")
        print("1. Agregar Gasto Comun")
        print("2. Agregar Gasto Peronal")
        print("3. Agregar Usuario")
        print("4. Listar Gastos Comunes")
        print("5. Listar Gastos de Usuarios")
        print("6. Mostrar historial")
        print("10. Salir")
        op = int(input("Ingrese numero de la operacion que desea realizar: "))
        if op == 1:
            monto = int(input("Ingrese monto del gasto: "))
            desc = input("Ingrese descripcion del gasto: ")
            agregar_gastos_comunes(monto, desc)
            print("Operacion realizada con exito")
            print("Se agregaron $" + str(monto) + " a gastos comunes")

        elif op == 2:
            print("Usuarios:")
            listar_usuarios()
            nombre = input("Ingrese su usuario: ")
            contra = input("Ingrese su contraseña: ")
            monto = float(input("Ingrese monto del gasto: "))
            descripcion = input("Ingrese una descripcion del gasto: ")
            ok = agregar_gasto_usuario(nombre, contra, monto, descripcion)
            if ok:
                print("Operacion realizada con exito")
            else:
                print("Operacion fallida")

        elif op == 3:
            print("----- Creacion de Usuario -----")
            nombre = input("Ingrese el nombre del usuario: ")
            contra = input("Ingrese contraseña: ")
            ok = crear_usuario(nombre, contra)
            if ok:
                print("Se creo el usuario: " + nombre + " con exito")
            else:
                print("El nombre de usuario ya esta usado, intente con otro nombre")

        elif op == 4:
            listar_gastos_comunes()

        elif op == 5:
            listar_gastos_usuarios()

        elif op == 6:
            print("Ingrese los datos del historial que busca: ")
            anio = int(input("Año: "))
            mes = int(input("Mes: "))
            mostrar_historial(ruta, anio, mes)
        elif op == 10:
            print("Saliendo...")
            break

        elif op == 998:
            backup(ruta)

        elif op == 999:
            limpiar_archivo()

        else:
            print("Opcion invalida, intente ingresar unicamente los numeros de las opcion que se muestran en el menu :)")