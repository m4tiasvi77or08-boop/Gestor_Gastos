import sqlite3
import os

ruta_db = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "gastos.db"
)

conn = sqlite3.connect(ruta_db)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        concepto TEXT NOT NULL,
        monto INTEGER NOT NULL,
        categoria TEXT NOT NULL,
        fecha TEXT NOT NULL
    )
""")

conn.commit()

def cerrar_conexion():
    conn.close()

def obtener_total():
    cursor.execute("SELECT SUM(monto) FROM gastos")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    return total

def obtener_estadisticas():
    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(monto),
            AVG(monto),
            MAX(monto)
        FROM gastos
    """)

    cantidad, total, promedio, maximo = cursor.fetchone()

    return cantidad, total, promedio, maximo

def agregar_gasto(concepto, monto, categoria, fecha):
    try:
        cursor.execute(
            """
            INSERT INTO gastos (concepto, monto, categoria, fecha)
            VALUES (?, ?, ?, ?)
            """,
            (concepto, monto, categoria, fecha)
        )

        conn.commit()

    except sqlite3.Error as error:
        print(f"Error en la base de datos: {error}")
        return False

    return True

def editar_gasto(id, concepto, monto, categoria):
    try:
        cursor.execute(
            """
            UPDATE gastos
            SET concepto = ?, monto = ?, categoria = ?
            WHERE id = ?
            """,
            (concepto, monto, categoria, id)
        )

        conn.commit()

    except sqlite3.Error as error:
        print(f"Error en la base de datos: {error}")
        return False
    
    return True

def eliminar_gasto_db(id):
    try:
        cursor.execute(
            "DELETE FROM gastos WHERE id = ?",
            (id,)
        )
        conn.commit()
    except sqlite3.Error as error:
        print(f"Error en la base de datos: {error}")
        return False
    return True

def obtener_gastos():
    cursor.execute("SELECT * FROM gastos ORDER BY id DESC")
    return cursor.fetchall()

def buscar_gastos_db(busqueda):
    cursor.execute(
        """
        SELECT * FROM gastos
        WHERE concepto LIKE ?
           OR categoria LIKE ?
           OR CAST(monto AS TEXT) LIKE ?
        ORDER BY id DESC
        """,
        (
            f"%{busqueda}%",
            f"%{busqueda}%",
            f"%{busqueda}%"
        )
    )

    return cursor.fetchall()

def obtener_gastos_por_categoria():
    cursor.execute("""
        SELECT categoria, SUM(monto)
        FROM gastos
        GROUP BY categoria
        ORDER BY SUM(monto) DESC
    """)

    return cursor.fetchall()