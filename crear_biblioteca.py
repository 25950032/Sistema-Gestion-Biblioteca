
import sqlite3

# Conectar con la base de datos
conexion = sqlite3.connect("biblioteca.db")

# Crear cursor
cursor = conexion.cursor()

# Crear tabla libros
cursor.execute("""
CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    categoria TEXT,
    disponible INTEGER DEFAULT 1
)
""")

# Crear tabla lectores
cursor.execute("""
CREATE TABLE IF NOT EXISTS lectores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT UNIQUE
)
""")

# Crear tabla prestamos
cursor.execute("""
CREATE TABLE IF NOT EXISTS prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_libro INTEGER NOT NULL,
    id_lector INTEGER NOT NULL,
    fecha_prestamo TEXT NOT NULL,
    fecha_devolucion TEXT,
    FOREIGN KEY (id_libro) REFERENCES libros(id),
    FOREIGN KEY (id_lector) REFERENCES lectores(id)
)
""")

# Guardar cambios
conexion.commit()

# Cerrar conexión
conexion.close()

print("Base de datos y tablas creadas correctamente.")
