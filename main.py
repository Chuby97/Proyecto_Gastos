from menu import mostrar_menu
from menu_principal import seleccionar_proyecto
import gastos_comunes
import usuarios
import os

while True:
    ruta = seleccionar_proyecto()
    if not ruta:
        print("Saliendo...")
        break
    gastos_comunes.configurar_ruta_gastos_comunes(os.path.join(ruta, "gastos_comunes.json"))
    usuarios.configurar_ruta_usuarios(os.path.join(ruta, "usuarios.json"))
    mostrar_menu(ruta)