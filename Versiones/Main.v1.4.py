from datetime import datetime


def mostrar_menu():
	print("==============================")
	print("   GESTOR DE GASTOS v1.0")
	print("==============================")
	print("1 - Agregar gasto")
	print("2 - Ver gastos")
	print("3 - Ver total gastado")
	print("4 - Salir")
def agregar_gasto():
	print("Agregar gastos")
	concepto = input("Ingrese el concepto del gasto: ")
	monto = int(input("Ingrese el monto del gasto: "))
	categoria = input("Ingrese la categoría del gasto: ")
	fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	gastos.append((concepto, monto, categoria, fecha))
	archivo = open("gastos.csv", "a")
	archivo.write(f"{concepto},{monto},{categoria},{fecha}\n")
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
def ver_total_gastado():
	total = sum(monto for _, monto, _, _ in gastos)
	print(f"Total gastado: ${total}")

opcion = 0

gastos = []

archivo = open("gastos.csv", "r")

for linea in archivo:
	concepto, monto, categoria, fecha = linea.strip().split(",")
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
	else:
		print("opcion invalida")