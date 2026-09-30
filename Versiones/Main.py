
from datetime import datetime
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('gastos.db')

cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        concepto TEXT NOT NULL,
        monto INTEGER NOT NULL,
        categoria TEXT NOT NULL,
        fecha TEXT NOT NULL
    )
''')
conn.commit()

def mostrar_menu():
    print("==============================")
    print("   GESTOR DE GASTOS v1.0")
    print("==============================")
    print("1 - Agregar gasto")
    print("2 - Ver gastos")
    print("3 - Editar gasto")
    print("4 - Eliminar gasto")
    print("5 - Buscar por concepto")
    print("6 - Filtrar por categoría")
    print("7 - Filtrar por monto")
    print("8 - Filtrar por rango")
    print("9 - Ver total gastado")
    print("10 - ver estadisticas ")
    print("11 - Salir")

def mostrar_resultados(gastos):
    if not gastos:
        print("No se encontraron resultados.")
        return

    for id, concepto, monto, categoria, fecha in gastos:
        print(f"ID: {id}| Concepto: {concepto}| Monto: ${monto}| Categoría: {categoria}| Fecha: {fecha}")

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

    cursor.execute('''
        INSERT INTO gastos (concepto, monto, categoria, fecha)
        VALUES (?, ?, ?, ?)
    ''', (concepto, monto, categoria, fecha))
    conn.commit()

    print("Gasto registrado correctamente.")
    print(f"Concepto: {concepto}")
    print(f"Monto: ${monto}")
    print(f"Categoría: {categoria}")
    print(f"Fecha: {fecha}")


def ver_gastos():
    cursor.execute('SELECT * FROM gastos')
    gastos = cursor.fetchall()

    if len(gastos) == 0:
        print("No hay gastos registrados.")
        return

    print("Ver gastos")

    mostrar_resultados(gastos)

def filtrar_por_categoria():
    categoria = input("Ingrese la categoría a filtrar: ").strip()
    cursor.execute(
        'SELECT * FROM gastos WHERE LOWER(categoria) = LOWER(?)',
        (categoria,)
    )
    gastos_filtrados = cursor.fetchall()

    if len(gastos_filtrados) == 0:
        print(f"No hay gastos registrados en la categoría '{categoria}'.")
        return

    print(f"Gastos en la categoría '{categoria}':")

    mostrar_resultados(gastos_filtrados)

def filtrar_por_monto():
    while True:
        try:
            monto_minimo = int(input("Ingrese el monto mínimo a filtrar: "))

            if monto_minimo > 0:
                break
            else:
                print("Error: el monto debe ser un número positivo.")

        except ValueError:
            print("Error: ingrese un número válido.")

    cursor.execute('SELECT * FROM gastos WHERE monto >= ?', (monto_minimo,))
    gastos_filtrados = cursor.fetchall()

    if len(gastos_filtrados) == 0:
        print(f"No hay gastos registrados con monto mayor o igual a ${monto_minimo}.")
        return

    print(f"Gastos con monto mayor o igual a ${monto_minimo}:")

    mostrar_resultados(gastos_filtrados)

def filtrar_por_rango():
    while True:
        try:
            monto_minimo = int(input("Ingrese el monto mínimo a filtrar: "))
            monto_maximo = int(input("Ingrese el monto máximo a filtrar: "))

            if monto_minimo > 0 and monto_maximo > 0 and monto_minimo <= monto_maximo:
                break
            else:
                print("Error: los montos deben ser números positivos y el mínimo debe ser menor o igual al máximo.")

        except ValueError:
            print("Error: ingrese números válidos.")

    cursor.execute('SELECT * FROM gastos WHERE monto BETWEEN ? AND ?', (monto_minimo, monto_maximo))
    gastos_filtrados = cursor.fetchall()

    if len(gastos_filtrados) == 0:
        print(f"No hay gastos registrados con monto entre ${monto_minimo} y ${monto_maximo}.")
        return

    print(f"Gastos con monto entre ${monto_minimo} y ${monto_maximo}:")

    mostrar_resultados(gastos_filtrados)

def buscar_por_concepto():
    concepto_buscar = input("Ingrese el concepto a buscar: ").strip()

    cursor.execute('SELECT * FROM gastos WHERE concepto LIKE ?', (f'%{concepto_buscar}%',))
    gastos_encontrados = cursor.fetchall()

    if len(gastos_encontrados) == 0:
        print(f"No se encontraron gastos con el concepto '{concepto_buscar}'.")
        return

    print(f"Gastos encontrados con el concepto '{concepto_buscar}':")

    mostrar_resultados(gastos_encontrados)

def editar_gasto():
    ver_gastos()

    try:
        id_gasto = int(input("Ingrese el ID del gasto a editar: "))

        cursor.execute(
            "SELECT concepto, monto, categoria, fecha FROM gastos WHERE id = ?",
            (id_gasto,)
        )

        gasto = cursor.fetchone()
        if gasto:
            concepto, monto, categoria, fecha = gasto
            nuevo_concepto = input(f"Ingrese el nuevo concepto (actual: {concepto}): ").strip()
            nuevo_monto = input(f"Ingrese el nuevo monto (actual: ${monto}): ").strip()
            nueva_categoria = input(f"Ingrese la nueva categoría (actual: {categoria}): ").strip()

            if nuevo_concepto:
                if len(nuevo_concepto) >= 3:
                    concepto = nuevo_concepto

                else:
                    print("Error: el concepto debe tener al menos 3 caracteres.")
                    return

            if nuevo_monto.strip():
                try:
                    nuevo_monto = int(nuevo_monto.strip())

                    if nuevo_monto > 0:
                        monto = nuevo_monto
                    else:
                        print("Error: el monto debe ser un número positivo.")
                        return

                except ValueError:
                    print("Error: el monto debe ser un número válido.")
                    return

            if nueva_categoria.strip():
                if len(nueva_categoria.strip()) >= 3:
                    categoria = nueva_categoria.strip()
                else:
                    print("Error: la categoría debe tener al menos 3 caracteres.")
                    return

            cursor.execute(
                "UPDATE gastos SET concepto = ?, monto = ?, categoria = ? WHERE id = ?",
                (concepto, monto, categoria, id_gasto)
            )

            if cursor.rowcount == 0:
                print("ID inválido. No existe ese gasto.")
            else:
                conn.commit()
                print("Gasto editado correctamente.")

        else:
            print("ID inválido.")

    except ValueError:
        print("Error: ingrese un número válido.")

def ver_estadisticas():
    cursor.execute("SELECT COUNT(*) FROM gastos")
    cantidad_gastos = cursor.fetchone()[0]

    if cantidad_gastos == 0:
        print("No hay gastos registrados.")
        return

    cursor.execute("SELECT SUM(monto), AVG(monto), MAX(monto), MIN(monto) FROM gastos")
    total_gastado, promedio_gasto, gasto_maximo, gasto_minimo = cursor.fetchone()

    print("Estadísticas de gastos:")
    print(f"Total gastado: ${total_gastado}")
    print(f"Promedio de gasto: ${promedio_gasto:.2f}")
    print(f"Gasto máximo: ${gasto_maximo}")
    print(f"Gasto mínimo: ${gasto_minimo}")

    totales_por_categoria = {}
    cursor.execute("SELECT categoria, SUM(monto) FROM gastos GROUP BY categoria")
    for categoria, total in cursor.fetchall():
        totales_por_categoria[categoria] = total

    print("Totales por categoría:")
    for categoria, total in totales_por_categoria.items():
        print(f"  {categoria}: ${total}")
        porcentaje = (total / total_gastado) * 100
        print(f"  Porcentaje del total: {porcentaje:.2f}%")

    categoria_mayor_gasto = max(totales_por_categoria, key=totales_por_categoria.get)
    print(f"Categoría con mayor gasto: {categoria_mayor_gasto} (${totales_por_categoria[categoria_mayor_gasto]})")

def ver_total_gastado():
    cursor.execute("SELECT SUM(monto) FROM gastos")

    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"Total gastado: ${total}")

def eliminar_gasto():
    ver_gastos()

    try:
        id_gasto = int(input("Ingrese el ID del gasto a eliminar: "))

        cursor.execute(
            "DELETE FROM gastos WHERE id = ?",
            (id_gasto,)
        )

        if cursor.rowcount == 0:
            print("ID inválido. No existe ese gasto.")
        else:
            conn.commit()
            print("Gasto eliminado correctamente.")

    except ValueError:
        print("Error: ingrese un número válido.")



opcion = 0

while opcion != 11:
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
        editar_gasto()

    elif opcion == 4:
        eliminar_gasto()

    elif opcion == 5:
        buscar_por_concepto()

    elif opcion == 6:
        filtrar_por_categoria()

    elif opcion == 7:
        filtrar_por_monto()

    elif opcion == 8:
        filtrar_por_rango()

    elif opcion == 9:
        ver_total_gastado()

    elif opcion == 10:
        ver_estadisticas()

    elif opcion == 11:
        print("saliendo del programa...")
    
    else:
        print("Opción inválida")

conn.close()