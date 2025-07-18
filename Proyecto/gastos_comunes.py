import json
import os
from datetime import date

ARCHIVO_GASTOS_COMUNES = "gastos_comunes.json"

#SE SUPONE LO HACE AUTOMATICO MENU PRINCIPAL AHORA
#def inicializar_archivo_gastos_comunes():
#    if not os.path.exists(ARCHIVO_GASTOS_COMUNES):
#        with open (ARCHIVO_GASTOS_COMUNES, "w") as f:
#            data = {
#                "total" : 0,
#                "historial" : []
#            }
#            json.dump(data, f, indent = 4)

def configurar_ruta_gastos_comunes(ruta):
    global ARCHIVO_GASTOS_COMUNES
    ARCHIVO_GASTOS_COMUNES = ruta

def cargar_gastos_comunes ():
    with open(ARCHIVO_GASTOS_COMUNES, "r") as f:
        return json.load(f)

def guardar_gastos_comunes(gastos):
    with open(ARCHIVO_GASTOS_COMUNES, "w") as f:
        json.dump(gastos, f, indent=4)

def agregar_gastos_comunes(monto, desc):
    gastos = cargar_gastos_comunes()

    nuevo_gasto={
        "fecha" : date.today().isoformat(),
        "descripcion" : desc,
        "monto" : monto
    }

    gastos["total"] += monto
    gastos["historial"].append(nuevo_gasto)

    guardar_gastos_comunes(gastos)

def listar_gastos_comunes():
    gastos = cargar_gastos_comunes()

    print(f"El total de gastos comunes es: ${gastos['total']}")
    print("Hisorial de Gastos:")
    for h in gastos['historial']:
        print(f"-   {h['fecha']} | {h['descripcion']} | {h['monto']}")

def archivar_y_resetear_gastos_comunes():
    gastos = cargar_gastos_comunes()
    historial_mes = []
    historial_mes.append({
        "total" : gastos['total'],
        "historial" : gastos['historial']
    })

    gastos['total'] = 0
    gastos['historial'] = []

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
    nombre_archivo_historial = f"gastos_comunes_historial_{mes_anterior_str}".json

    with open(nombre_archivo_historial, "w") as f:
        json.dump(historial_mes, f, indent = 4)

    with open (ARCHIVO_GASTOS_COMUNES, "w") as f:
        json.dump(gastos, f, indent = 4)

    print(f"Historial de gastos comunes archivado en '{nombre_archivo_historial}'.")
    print("Gastos comunes reseteados correctamente.")

def limpiar_archivo_gastos_comunes():
    with open (ARCHIVO_GASTOS_COMUNES, "w") as f:
            data = {
                "total" : 0,
                "historial" : []
            }
            json.dump(data, f, indent = 4)
    print("El archivo quedo limpio")