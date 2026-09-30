from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from Database import (
    buscar_gastos_db,
    obtener_total,
    obtener_estadisticas,
    obtener_gastos_por_categoria,
    agregar_gasto,
    editar_gasto,
    eliminar_gasto_db,
    obtener_gastos,
    cerrar_conexion
)

def cerrar_aplicacion():
    cerrar_conexion()
    ventana.destroy()

ventana = tk.Tk()
ventana.title("Gestor de Gastos")
ventana.geometry("700x500")
ventana.configure(bg="#E8DFC8")

id_seleccionado = None

marco_principal = tk.Frame(ventana, bg="#E8DFC8")
marco_principal.pack(fill="both", expand=True)

canvas = tk.Canvas(
    marco_principal,
    bg="#E8DFC8",
    highlightthickness=0
)

scrollbar_principal = ttk.Scrollbar(
    marco_principal,
    orient="vertical",
    command=canvas.yview
)

scrollable_frame = tk.Frame(
    canvas,
    bg="#E8DFC8"
)

scrollable_frame.bind(
    "<Configure>",
    lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

canvas.configure(
    yscrollcommand=scrollbar_principal.set
)

canvas.pack(side="left", fill="both", expand=True)
scrollbar_principal.pack(side="right", fill="y")

def mover_scroll(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", mover_scroll)
ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

titulo = tk.Label(
    scrollable_frame,
    text="GESTOR DE GASTOS",
    font=("Arial", 18, "bold"),
    bg="#E8DFC8",
    fg="#1F1F1F"
)
titulo.pack(pady=5)

subtitulo = tk.Label(
    scrollable_frame,
    text="Controlá tus gastos de forma simple",
    bg="#E8DFC8",
    fg="#1F1F1F", font=("Arial", 12, "bold")
)
subtitulo.pack()

marco_gasto = tk.LabelFrame(
    scrollable_frame,
    text="Gasto",
    padx=10,
    pady=5,
    bg="#E8DFC8",
    fg="#1F1F1F", font=("Arial", 10, "bold")
)
marco_gasto.pack(pady=10)

tk.Label(marco_gasto, text="Concepto:", bg="#E8DFC8", fg="#1F1F1F", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
entrada_concepto = tk.Entry(marco_gasto)
entrada_concepto.grid(row=0, column=1, padx=5, pady=5)

tk.Label(marco_gasto, text="Monto:", bg="#E8DFC8", fg="#1F1F1F", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
entrada_monto = tk.Entry(marco_gasto)
entrada_monto.grid(row=1, column=1, padx=5, pady=5)

tk.Label(marco_gasto, text="Categoría:", bg="#E8DFC8", fg="#1F1F1F", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
entrada_categoria = tk.Entry(marco_gasto)
entrada_categoria.grid(row=2, column=1, padx=5, pady=5)

entrada_concepto.bind("<Return>", lambda event: enter_presionado())
entrada_monto.bind("<Return>", lambda event: enter_presionado())
entrada_categoria.bind("<Return>", lambda event: enter_presionado())

marco_busqueda = tk.LabelFrame(
    scrollable_frame,
    text="Búsqueda",
    padx=10,
    pady=5,
    bg="#E8DFC8",
    fg="#1F1F1F", font=("Arial", 10, "bold")
)
marco_busqueda.pack(pady=10)

tk.Label(marco_busqueda, text="Buscar:", bg="#E8DFC8", fg="#1F1F1F", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
entrada_busqueda = tk.Entry(marco_busqueda)
entrada_busqueda.grid(row=0, column=1, padx=5, pady=5)
entrada_busqueda.bind("<Return>", lambda event: buscar_gastos())

def mostrar_gastos(gastos):

    for item in tabla.get_children():
        tabla.delete(item)

    for id, concepto, monto, categoria, fecha in gastos:
        monto_formateado = f"$ {monto:,}".replace(",", ".")

        tabla.insert(
            "",
            "end",
            values=(id, concepto, monto_formateado, categoria, fecha)
        )

def boton_presionado():
    gastos = obtener_gastos()
    mostrar_gastos(gastos)

def buscar_gastos():
    busqueda = entrada_busqueda.get().strip()

    if busqueda:
        gastos = buscar_gastos_db(busqueda)
    else:
        gastos = obtener_gastos()

    mostrar_gastos(gastos)

def ver_total_gui():
    total = obtener_total()

    detalle.config(text=f"Total gastado: ${total}")

def ver_estadisticas_gui():
    cantidad, total, promedio, maximo = obtener_estadisticas()

    if cantidad == 0:
        detalle.config(text="No hay gastos registrados.")
        return

    detalle.config(
        text=f"Cantidad: {cantidad} | "
             f"Total: ${total:.0f} | "
             f"Promedio: ${promedio:.0f} | "
             f"Máximo: ${maximo}"
    )

def ver_gastos_por_categoria_gui():
    resultados = obtener_gastos_por_categoria()

    if not resultados:
        detalle.config(text="No hay gastos registrados.")
        return

    total_general = obtener_total()

    texto = "\n".join(
        f"{categoria}: ${total:,.0f} — {(total / total_general) * 100:.1f}%"
        .replace(",", ".")
        for categoria, total in resultados
    )

    detalle.config(text=texto)

def gasto_seleccionado():
    global id_seleccionado

    seleccion = tabla.selection()

    if seleccion:
        item = tabla.item(seleccion[0])
        id, concepto, monto, categoria, fecha = item["values"]

        id_seleccionado = id

        entrada_concepto.delete(0, tk.END)
        entrada_concepto.insert(0, concepto)

        entrada_monto.delete(0, tk.END)
        monto = str(monto).replace("$", "").replace(".", "").strip()
        entrada_monto.insert(0, monto)

        entrada_categoria.delete(0, tk.END)
        entrada_categoria.insert(0, categoria)

        detalle.config(text=f"Gasto seleccionado: ID {id}")
    else:
        id_seleccionado = None

def enter_presionado():
    if id_seleccionado is not None:
        editar_gasto_gui()
    else:
        agregar_gasto_gui()

def editar_gasto_gui():
    global id_seleccionado
    seleccion = tabla.selection()

    if not seleccion:
        detalle.config(text="No se ha seleccionado ningún gasto.")
        return

    item = tabla.item(seleccion[0])
    id = item["values"][0]

    concepto = entrada_concepto.get()
    monto = entrada_monto.get()
    categoria = entrada_categoria.get()

    if len(concepto.strip()) < 3:
        detalle.config(text="El concepto debe tener al menos 3 caracteres.")
        return

    try:
        monto = int(monto)

    except ValueError:
        detalle.config(text="ERROR: el monto debe ser un número entero.")
        return

    if monto <= 0:
        detalle.config(text="El monto debe ser mayor a 0.")
        return

    if len(categoria.strip()) < 3:
        detalle.config(text="La categoría debe tener al menos 3 caracteres.")
        return

    resultado = editar_gasto(id, concepto, monto, categoria)

    if resultado:
        tabla.selection_remove(tabla.selection())

        id_seleccionado = None

        boton_presionado()

        entrada_concepto.delete(0, tk.END)
        entrada_monto.delete(0, tk.END)
        entrada_categoria.delete(0, tk.END)

        detalle.config(text="Gasto editado correctamente.")

    else:
        detalle.config(text="No se pudo editar el gasto.")

def eliminar_gasto():
    seleccion = tabla.selection()

    if seleccion:
        item = tabla.item(seleccion[0])
        id = item["values"][0]

        confirmar = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar este gasto?")

        if confirmar:
            resultado = eliminar_gasto_db(id)

            if resultado:
                tabla.selection_remove(tabla.selection())

                boton_presionado()
                detalle.config(text="Gasto eliminado correctamente.")

            else:
                detalle.config(text="No se pudo eliminar el gasto.")
    else:
        detalle.config(text="No seleccionaste ningún gasto.")

def limpiar_campos():
    global id_seleccionado

    entrada_concepto.delete(0, tk.END)
    entrada_monto.delete(0, tk.END)
    entrada_categoria.delete(0, tk.END)
    entrada_busqueda.delete(0, tk.END)

    id_seleccionado = None

    tabla.selection_remove(tabla.selection())
    
    detalle.config(text="")
    
def agregar_gasto_gui():
    concepto = entrada_concepto.get()
    monto = entrada_monto.get()
    categoria = entrada_categoria.get()

    if len(concepto.strip()) < 3:
        detalle.config(text="El concepto debe tener al menos 3 caracteres.")
        return

    try:
       monto = int(monto)

    except ValueError:
        detalle.config(text="ERROR: el monto debe ser un número entero.")
        return

    if monto <= 0:
        detalle.config(text="El monto debe ser mayor a 0.")
        return
    if len(categoria.strip()) < 3:
        detalle.config(text="La categoría debe tener al menos 3 caracteres.")
        return
    
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    resultado = agregar_gasto(concepto, monto, categoria, fecha)

    if resultado:
        boton_presionado()

        entrada_concepto.delete(0, tk.END)
        entrada_monto.delete(0, tk.END)
        entrada_categoria.delete(0, tk.END)

        detalle.config(text="Gasto agregado correctamente.")

    else:
        detalle.config(text="No se pudo agregar el gasto.")

marco_acciones = tk.LabelFrame(
    scrollable_frame,
    text="Acciones",
    padx=10,
    pady=5,
    bg="#E8DFC8",
    fg="#1F1F1F", font=("Arial", 10, "bold")
)
marco_acciones.pack(pady=10)

boton_ver = tk.Button(
    marco_acciones,
    text="Ver gastos",
    command=boton_presionado,
    width=11,
    height=1,
    font=("Arial", 10, "bold"), bg="#7A8565", fg="#1F1F1F"
)
boton_ver.grid(row=0, column=0, padx=5, pady=5)

boton_buscar = tk.Button(
    marco_acciones,
    text="Buscar",
    command=buscar_gastos,
    width=11,
    height=1,
    font=("Arial", 10, "bold"), bg="#7A8565", fg="#1F1F1F"
)
boton_buscar.grid(row=0, column=1, padx=5, pady=5)

boton_limpiar = tk.Button(
    marco_acciones,
    text="Limpiar",
    command=limpiar_campos,
    width=11,
    height=1,
    font=("Arial", 10, "bold"), bg="#7A8565", fg="#1F1F1F"
)
boton_limpiar.grid(row=0, column=2, padx=5, pady=5)

boton_agregar = tk.Button(
    marco_acciones,
    text="Agregar gasto",
    command=agregar_gasto_gui,
    width=11,
    height=1,
    font=("Arial", 10, "bold"), bg="#7A8565", fg="#1F1F1F"
)
boton_agregar.grid(row=1, column=0, padx=5, pady=5)

boton_editar = tk.Button(
    marco_acciones,
    text="Editar gasto",
    command=editar_gasto_gui,
    width=11,
    height=1,
    font=("Arial", 10, "bold"), bg="#7A8565", fg="#1F1F1F"
)
boton_editar.grid(row=1, column=1, padx=5, pady=5)

boton_eliminar = tk.Button(
    marco_acciones,
    text="Eliminar gasto",
    command=eliminar_gasto,
    width=11,
    height=1,
    font=("Arial", 10, "bold"), bg="#7A8565", fg="#1F1F1F"
)
boton_eliminar.grid(row=1, column=2, padx=5, pady=5)

marco_resumen = tk.LabelFrame(
    scrollable_frame,
    text="Resumen",
    padx=10,
    pady=5,
    bg="#E8DFC8",
    fg="#1F1F1F", font=("Arial", 10, "bold")
)
marco_resumen.pack(pady=10)

boton_total = tk.Button(
    marco_resumen,
    text="Total gastado",
    command=ver_total_gui,
    width=11,
    height=1,
    font=("Arial", 10, "bold"), bg="#7A8565", fg="#1F1F1F"
)
boton_total.grid(row=0, column=0, padx=5, pady=5)

boton_estadisticas = tk.Button(
    marco_resumen,
    text="Estadísticas",
    command=ver_estadisticas_gui,
    width=11,
    height=1,
    font=("Arial", 10, "bold"), bg="#7A8565", fg="#1F1F1F"
)
boton_estadisticas.grid(row=0, column=1, padx=5, pady=5)

boton_categoria = tk.Button(
    marco_resumen,
    text="Por categoría",
    command=ver_gastos_por_categoria_gui,
    width=11,
    height=1,
    font=("Arial", 10, "bold"), bg="#7A8565", fg="#1F1F1F"
)
boton_categoria.grid(row=0, column=2, padx=5, pady=5)

detalle = tk.Label(scrollable_frame, text="", bg="#E8DFC8", fg="#1F1F1F", font=("Arial", 10, "bold"))
detalle.pack()

estilo = ttk.Style()

estilo.theme_use("clam")

estilo.configure(
    "Treeview",
    background="#E8DFC8",
    foreground="#1F1F1F",
    fieldbackground="#E8DFC8",
    rowheight=25, font=("Arial", 10, "bold")
)

estilo.configure(
    "Treeview.Heading",
    background="#7A8565",
    foreground="#1F1F1F",
    font=("Arial", 10, "bold")
)

estilo.map(
    "Treeview",
    background=[
        ("selected", "#7A8565")
    ],
    foreground=[
        ("selected", "#1F1F1F")
    ]
)
marco_tabla = tk.Frame(scrollable_frame)
marco_tabla.pack(fill="both", expand=True, padx=10, pady=10)

tabla = ttk.Treeview(marco_tabla, show="headings")
tabla.pack(side="left", fill="both", expand=True)

scroll_tabla = ttk.Scrollbar(
    marco_tabla,
    orient="vertical",
    command=tabla.yview
)
scroll_tabla.pack(side="right", fill="y")

tabla.configure(yscrollcommand=scroll_tabla.set)

# Definir las columnas de la tabla
tabla["columns"] = ("ID", "Concepto", "Monto", "Categoría", "Fecha")

# Establecer los encabezados de las columnas
tabla.heading("ID", text="ID")
tabla.heading("Concepto", text="Concepto")
tabla.heading("Monto", text="Monto")
tabla.heading("Categoría", text="Categoría")
tabla.heading("Fecha", text="Fecha")

tabla.column("ID", width=40, anchor="center")
tabla.column("Concepto", width=150, anchor="w")
tabla.column("Monto", width=100, anchor="e")
tabla.column("Categoría", width=120, anchor="w")
tabla.column("Fecha", width=150, anchor="center")

tabla.bind("<<TreeviewSelect>>", lambda event: gasto_seleccionado())

ventana.mainloop()