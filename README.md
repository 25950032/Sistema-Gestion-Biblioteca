# Sistema de Gestión de Biblioteca

**Autora:** Andrea Kohn

## Descripción

Aplicación de escritorio desarrollada en Python para administrar una biblioteca mediante una base de datos SQLite.

El sistema permite gestionar libros, lectores, préstamos y devoluciones desde un menú interactivo en la terminal.

## Funcionalidades

- Registrar libros.
- Consultar el catálogo de libros.
- Buscar libros por título o autor.
- Registrar lectores.
- Consultar lectores.
- Buscar lectores por nombre, apellido o correo electrónico.
- Registrar préstamos.
- Consultar préstamos activos.
- Registrar devoluciones.
- Controlar la disponibilidad de los libros.
- Evitar registros duplicados de libros y correos electrónicos.

## Tecnologías utilizadas

- Python
- SQLite
- SQL
- Visual Studio Code
- Git y GitHub

## Estructura del proyecto

```text
Sistema-Gestion-Biblioteca/
│
├── crear_biblioteca.py
├── menu_biblioteca.py
├── README.md
├── .gitignore
└── biblioteca.db (base de datos local, no incluida en GitHub)
```

## Instalación y ejecución

1. Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

2. Ingresar a la carpeta del proyecto:

```bash
cd Sistema-Gestion-Biblioteca
```

3. Crear la base de datos:

```bash
python crear_biblioteca.py
```

4. Ejecutar el sistema:

```bash
python menu_biblioteca.py
```

## Base de datos

El proyecto utiliza SQLite y contiene tres tablas:

- **libros:** almacena información de los libros y su disponibilidad.
- **lectores:** almacena los datos de los lectores.
- **prestamos:** registra los préstamos y las fechas de devolución.

## Autora

**Andrea Kohn**

Proyecto desarrollado con fines educativos para practicar programación en Python, consultas SQL y gestión de bases de datos SQLite.
