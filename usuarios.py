import json
import os
from datetime import date

ARCHIVO_USUARIOS = "usuarios.json"

def configurar_ruta_usuarios(ruta):
    global ARCHIVO_USUARIOS
    ARCHIVO_USUARIOS = ruta

def cargar_usuarios():
    with open(ARCHIVO_USUARIOS, "r") as f:
        return json.load(f)

def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

def crear_usuario(nombre, contra):
    usuarios = cargar_usuarios()
    
    for u in usuarios:
        if u["nombre"] == nombre:
            return False
    
    nuevo = {
        "nombre" : nombre, 
        "contra" : contra,
        "gastos" : 0.0,
        "historial" : []
    }

    usuarios.append(nuevo)
    guardar_usuarios(usuarios)
    return True

def listar_usuarios():
    usuarios = cargar_usuarios()
    
    for u in usuarios:
        print(f"-{u['nombre']}")

def listar_gastos_usuarios():
    usuarios = cargar_usuarios()

    for u in usuarios:
        print(f"Usuario: {u['nombre']}  Gastos: {u['gastos']}")
        if "historial" in u and u['historial']:
            print("Hisorial de gastos: ")
            for g in u['historial']:
                print(f"-   {g['fecha']} | {g['descripcion']} | {g['monto']}")
        else:
            print("Sin detalle de los gastos registrados")

def agregar_gasto_usuario(nombre, contra, monto, descripcion):
    usuarios = cargar_usuarios()

    for u in usuarios:
        if u['nombre'] == nombre:
            if u['contra'] != contra:
                print("Contraseña Incorrecta")
                return False
            u['gastos'] += monto
            gasto_detalle = {
                "fecha" : date.today().isoformat(),
                "descripcion" : descripcion,
                "monto" : monto
            }
            if "historial" not in u:
                u['historial'] = []
            u['historial'].append(gasto_detalle)
            guardar_usuarios(usuarios)
            print(f"Gasto agregado a {nombre}. Total: ${u['gastos']}")
            return True

    print("Usuario no encontrado")
    return False

def imprimir_usuarios(ruta):
    with open(ruta, "r") as f:
        usuarios = json.load(f)
    for u in usuarios:
        print(f"Usuario: {u['nombre']}  Gastos: {u['gastos']}")
        if "historial" in u and u['historial']:
            print("Hisorial de gastos: ")
            for g in u['historial']:
                print(f"-   {g['fecha']} | {g['descripcion']} | {g['monto']}")
        else:
            print("Sin detalle de los gastos registrados")
    return True

def archivar_y_resetear_usuarios(ruta_historial):
    usuarios = cargar_usuarios()
    historial_mes = []
    for u in usuarios:
        historial_mes.append({
            "nombre" : u['nombre'],
            "gastos" : u['gastos'],
            "historial" : u['historial']
        })
        u['gastos'] = 0
        u['historial'] = []

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
    nombre_archivo_historial = f"{mes_anterior_str}_usuarios.json"
    with open(os.path.join(ruta_historial, nombre_archivo_historial), "w") as f:
        json.dump(historial_mes, f, indent=4)
    
    with open(ARCHIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)
    
    print(f"Historial archivado en '{nombre_archivo_historial}'.")
    print("Usuarios reseteados correctamente.")
    return True

def limpiar_archivo():
    with open(ARCHIVO_USUARIOS, "w") as f:
        json.dump([],f)
    print("El archivo quedo limpio")