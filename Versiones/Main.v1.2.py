def mostrar_menu():
	print("==============================")
	print("   GESTOR DE GASTOS v1.0")
	print("==============================")
	print("1 - Agregar gasto")
	print("2 - Ver gastos")
	print("3 - Ver total gastado")
	print("4 - Salir")

opcion = 0

gastos = []

while opcion != 4:
	mostrar_menu()
	try:
		opcion = int(input("Elegí una opción: "))
	except ValueError:
		print("Error: ingrese un número válido.")
		continue

	if opcion == 1:
		print("Agregar gastos")
		concepto = input("ingrese el concepto del gasto: ")
		monto = int(input("ingrese el monto del gasto: "))
		gastos.append((concepto, monto))
		print("Gasto registrado correctamente: ")
		print(f"Concepto: {concepto}")
		print(f"Monto:${monto}")
	elif opcion == 2:
		print("Ver gastos")
		for concepto, monto in gastos:
			print(f"Concepto: {concepto}, Monto: ${monto}")
	elif opcion == 3:
		total = sum(monto for _, monto in gastos)
		print(f"Total gastado: ${total}")
	elif opcion == 4:
		print("Salir")
	else:
		print("opcion invalida")