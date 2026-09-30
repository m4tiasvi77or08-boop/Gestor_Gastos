import csv
from datetime import datetime


def mostrar_menu():
    print("==============================")
    print("   GESTOR DE GASTOS v1.0")
    print("==============================")
    print("1 - Agregar gasto")
    print("2 - Ver gastos")
    print("3 - Ver total gastado")
    print("4 - Salir")
    print("5 - Eliminar gasto")
    print("6 - Filtrar por categoría")


def agregar_gasto():
    print("Agregar gastos")

    while True:
        concepto = input("Ingrese el concepto del gasto: ")

        if len(concepto.strip()) >= 3:
            break
        else:
            print("Error: el concepto debe tener al menos 3 caracteres.")

    concepto = concepto.strip()

    while True:
        try:
            monto = int(input("Ingrese el monto del gasto: "))

            if monto > 0:
                break
            else:
                print("Error: el monto debe ser un número positivo.")

        except ValueError:
            print("Error: ingrese un número válido.")

    while True:
        categoria = input("Ingrese la categoría del gasto: ")

        if len(categoria.strip()) >= 3:
            break
        else:
            print("Error: la categoría debe tener al menos 3 caracteres.")

    categoria = categoria.strip()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    gastos.append((concepto, monto, categoria, fecha))

    archivo = open("gastos.csv", "a", newline="")
    writer = csv.writer(archivo)

    writer.writerow([concepto, monto, categoria, fecha])

    archivo.close()

    print("Gasto registrado correctamente.")
    print(f"Concepto: {concepto}")
    print(f"Monto: ${monto}")
    print(f"Categoría: {categoria}")
    print(f"Fecha: {fecha}")


def ver_gastos():
    if len(gastos) == 0:
        print("No hay gastos registrados.")
        return

    print("Ver gastos")

    for i, (concepto, monto, categoria, fecha) in enumerate(gastos, start=1):
        print(f"{i}. Concepto: {concepto}, Monto: ${monto}, Categoría: {categoria}, Fecha: {fecha}")


def filtrar_por_categoria():
    categoria = input("Ingrese la categoría a filtrar: ")

    gastos_filtrados = [
        gasto for gasto in gastos
        if gasto[2].lower() == categoria.lower()
    ]

    if len(gastos_filtrados) == 0:
        print(f"No hay gastos registrados en la categoría '{categoria}'.")
        return

    print(f"Gastos en la categoría '{categoria}':")

    for i, (concepto, monto, categoria, fecha) in enumerate(gastos_filtrados, start=1):
        print(f"{i}. Concepto: {concepto}, Monto: ${monto}, Categoría: {categoria}, Fecha: {fecha}")


def ver_total_gastado():
    total = sum(monto for _, monto, _, _ in gastos)

    print(f"Total gastado: ${total}")


def eliminar_gasto():
    ver_gastos()

    try:
        indice = int(input("Ingrese el número del gasto a eliminar: ")) - 1

        if 0 <= indice < len(gastos):
            gastos.pop(indice)
            guardar_gastos()

            print("Gasto eliminado correctamente.")

        else:
            print("Índice inválido.")

    except ValueError:
        print("Error: ingrese un número válido.")


def guardar_gastos():
    archivo = open("gastos.csv", "w", newline="")
    writer = csv.writer(archivo)

    for concepto, monto, categoria, fecha in gastos:
        writer.writerow([concepto, monto, categoria, fecha])

    archivo.close()


opcion = 0

gastos = []


archivo = open("gastos.csv", "r", newline="")
reader = csv.reader(archivo)

for linea in reader:
    concepto, monto, categoria, fecha = linea
    gastos.append((concepto, int(monto), categoria, fecha))

archivo.close()


while opcion != 4:
    mostrar_menu()

    try:
        opcion = int(input("Elegí una opción: "))

    except ValueError:
        print("Error: ingrese un número válido.")
        continue

    if opcion == 1:
        agregar_gasto()

    elif opcion == 2:
        ver_gastos()

    elif opcion == 3:
        ver_total_gastado()

    elif opcion == 4:
        print("Salir")

    elif opcion == 5:
        eliminar_gasto()

    elif opcion == 6:
        filtrar_por_categoria()

    else:
        print("Opción inválida")