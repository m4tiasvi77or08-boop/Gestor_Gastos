# Gestor de Gastos

Aplicación de escritorio desarrollada en **Python** para registrar, consultar y administrar gastos personales.

El proyecto comenzó como una aplicación de consola utilizando archivos CSV y evolucionó hasta convertirse en una aplicación gráfica con **Tkinter** y almacenamiento de datos mediante **SQLite**.

## Funcionalidades

* Agregar gastos
* Editar gastos
* Eliminar gastos
* Buscar gastos por concepto, categoría o monto
* Filtrar información
* Calcular el total gastado
* Consultar estadísticas
* Agrupar gastos por categoría
* Seleccionar gastos desde una tabla
* Validación de datos
* Manejo de errores de base de datos
* Persistencia de información mediante SQLite

## Tecnologías

* **Python**
* **SQLite**
* **Tkinter**
* **SQL**
* **PyInstaller**
* **Git / GitHub**

## Estructura del proyecto

```text
Gestor_Gastos/
│
├── Interfaz.py          # Interfaz gráfica de la aplicación
├── Database.py          # Conexión y operaciones con SQLite
├── requirements.txt     # Dependencias del proyecto
├── README.md            # Documentación
│
├── Versiones/           # Versiones anteriores desarrolladas durante el proyecto
│
└── dist/
    └── Gestor_Gastos.exe
```

> La carpeta `dist` y la base de datos local no forman parte del repositorio público.

## Base de datos

La aplicación utiliza **SQLite** para almacenar los gastos.

Cada instalación puede utilizar su propia base de datos local. Si el archivo `gastos.db` no existe, SQLite lo crea automáticamente al ejecutar la aplicación.

La base de datos utilizada durante el desarrollo no se incluye en el repositorio para mantener separados los datos personales del código fuente.

## Ejecutar el proyecto

### Desde Python

Se requiere Python instalado en el equipo.

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
python Interfaz.py
```

### Ejecutable

También se puede generar y ejecutar una versión independiente utilizando **PyInstaller**.

El ejecutable generado es:

```text
Gestor_Gastos.exe
```

## Aprendizajes aplicados

Este proyecto fue desarrollado como práctica integral de programación en Python y permitió aplicar:

* Variables y estructuras de datos
* Funciones
* Validación de entradas
* Manejo de excepciones
* Archivos CSV
* Bases de datos SQLite
* Consultas SQL
* Operaciones CRUD
* Interfaces gráficas con Tkinter
* Separación de lógica e interfaz
* Manejo de eventos
* Empaquetado de aplicaciones con PyInstaller
* Control de versiones con Git
* Publicación de proyectos en GitHub

## Evolución del proyecto

El proyecto se desarrolló progresivamente:

**Consola → CSV → SQLite → Tkinter → PyInstaller → Git/GitHub**

Esto permitió transformar un programa inicial de consola en una aplicación de escritorio completa.

## Estado

**Versión 1.0 — Finalizada**

Proyecto desarrollado como parte de mi aprendizaje práctico de Python y desarrollo de aplicaciones de escritorio.
