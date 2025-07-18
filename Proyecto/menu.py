from usuarios import crear_usuario, listar_usuarios, listar_gastos_usuarios, agregar_gasto_usuario, limpiar_archivo
from gastos_comunes import agregar_gastos_comunes, limpiar_archivo_gastos_comunes, listar_gastos_comunes

def mostrar_menu():
    while True:
        print("----- MENU -----\n")
        print("1. Agregar Gasto Comun")
        print("2. Agregar Gasto Peronal")
        print("3. Agregar Usuario")
        print("4. Listar Gastos Comunes")
        print("5. Listar Gastos de Usuarios")
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

        elif op == 10:
            print("Saliendo...")
            break

        elif op == 998:
            limpiar_archivo_gastos_comunes()

        elif op == 999:
            limpiar_archivo()

        else:
            print("Opcion invalida, intente ingresar unicamente los numeros de las opcion que se muestran en el menu :)")