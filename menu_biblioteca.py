
import sqlite3
from datetime import datetime
import re

# Conectar con la base de datos
def conectar():
    conexion = sqlite3.connect("biblioteca.db")

    # Activar las claves foráneas
    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion

# Buscar libros por título o autor
def buscar_libro():

    print("\n===== BUSCAR LIBRO =====")

    busqueda = input("Ingrese el título o autor: ").strip()

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT * FROM libros
        WHERE titulo LIKE ? OR autor LIKE ?
    """, (f"%{busqueda}%", f"%{busqueda}%"))

    libros = cursor.fetchall()

    if libros:
        for libro in libros:
            print("-------------------------")
            print("ID:", libro[0])
            print("Título:", libro[1])
            print("Autor:", libro[2])
            print("Categoría:", libro[3])
            print("Disponible:" if libro[4] == 1 else "Prestado")
    else:
        print("No se encontraron libros.")

    conexion.close()


# Registrar un libro
def registrar_libro():

    print("\n===== REGISTRAR LIBRO =====")

    titulo = input("Título del libro: ").strip()
    autor = input("Autor: ").strip()
    categoria = input("Categoría: ").strip()

    if not titulo or not autor:
        print("El título y el autor son obligatorios.")
        return

    conexion = conectar()
    cursor = conexion.cursor()
        # Verificar si el libro ya existe
    cursor.execute("""
        SELECT id
        FROM libros
        WHERE LOWER(titulo) = LOWER(?)
        AND LOWER(autor) = LOWER(?)
    """, (titulo, autor))

    libro_existente = cursor.fetchone()

    if libro_existente is not None:
        print("Este libro ya está registrado.")
        conexion.close()
        return

    cursor.execute("""
        INSERT INTO libros (titulo, autor, categoria)
        VALUES (?, ?, ?)
    """, (titulo, autor, categoria))

    conexion.commit()
    conexion.close()

    print("¡Libro registrado correctamente!")

# Consultar todos los libros
def consultar_libros():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM libros")

    libros = cursor.fetchall()

    print("\n===== CATALOGO DE LIBROS =====")

    if libros:
        for libro in libros:
            print("-------------------------")
            print("ID:", libro[0])
            print("Título:", libro[1])
            print("Autor:", libro[2])
            print("Categoría:", libro[3])

            if libro[4] == 1:
                print("Disponibilidad: Disponible")
            else:
                print("Disponibilidad: Prestado")
    else:
        print("No hay libros registrados.")
        
    conexion.close()
    
# Registrar un lector
def registrar_lector():
    print("\n===== REGISTRAR LECTOR =====")

    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    email = input("Correo electrónico: ").strip()

    if not nombre or not apellido:
        print("El nombre y el apellido son obligatorios.")
        return
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        print("El correo electrónico no tiene un formato válido.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    # Verificar si el correo ya está registrado
    cursor.execute(
        "SELECT id FROM lectores WHERE email = ?",
        (email,)
    )

    lector_existente = cursor.fetchone()

    if lector_existente:
        print("Este correo electrónico ya está registrado.")
        conexion.close()
        return

    # Registrar el lector
    cursor.execute("""
        INSERT INTO lectores (nombre, apellido, email)
        VALUES (?, ?, ?)
    """, (nombre, apellido, email))

    conexion.commit()
    conexion.close()

    print("¡Lector registrado correctamente!")    
    


# Consultar todos los lectores
def consultar_lectores():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM lectores")
    lectores = cursor.fetchall()

    print("\n===== LISTADO DE LECTORES =====")

    if lectores:
        for lector in lectores:
            print("-------------------------")
            print("ID:", lector[0])
            print("Nombre:", lector[1])
            print("Apellido:", lector[2])
            print("Email:", lector[3])
    else:
        print("No hay lectores registrados.")
        
    conexion.close() 
    
# Buscar lectores
def buscar_lector():

    print("\n===== BUSCAR LECTOR =====")

    busqueda = input("Ingrese nombre, apellido o email: ").strip()

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT * FROM lectores
        WHERE nombre LIKE ?
        OR apellido LIKE ?
        OR email LIKE ?
    """, (
        f"%{busqueda}%",
        f"%{busqueda}%",
        f"%{busqueda}%"
    ))

    lectores = cursor.fetchall()

    if lectores:
        for lector in lectores:
            print("-------------------------")
            print("ID:", lector[0])
            print("Nombre:", lector[1])
            print("Apellido:", lector[2])
            print("Email:", lector[3])
    else:
        print("No se encontraron lectores.")

    conexion.close()   
   
# Registrar un préstamo
def registrar_prestamo():
    print("\n===== REGISTRAR PRESTAMO =====")

    id_libro = input("ID del libro: ")
    id_lector = input("ID del lector: ")

    fecha = datetime.now().strftime("%Y-%m-%d")

    conexion = conectar()
    cursor = conexion.cursor()

    # Verificar que el libro exista y esté disponible
    cursor.execute(
        "SELECT disponible FROM libros WHERE id = ?", (id_libro,)
    )
    libro = cursor.fetchone()

    if libro is None:
        print("El libro no existe.")
        conexion.close()
        return

    if libro[0] == 0:
        print("El libro ya está prestado.")
        conexion.close()
        return

    # Verificar que el lector exista
    cursor.execute(
        "SELECT id FROM lectores WHERE id = ?", (id_lector,)
    )
    lector = cursor.fetchone()

    if lector is None:
        print("El lector no existe.")
        conexion.close()
        return
# Verificar que no exista otro préstamo activo
    cursor.execute("""
        SELECT id
        FROM prestamos
        WHERE id_libro = ?
        AND fecha_devolucion IS NULL
    """, (id_libro,))

    prestamo_activo = cursor.fetchone()

    if prestamo_activo is not None:
        print("Este libro ya tiene un préstamo activo.")
        conexion.close()
        return
    
    # Registrar el préstamo
    cursor.execute("""
        INSERT INTO prestamos (id_libro, id_lector, fecha_prestamo)
        VALUES (?, ?, ?)
    """, (id_libro, id_lector, fecha))

    # Marcar el libro como prestado
    cursor.execute(
        "UPDATE libros SET disponible = 0 WHERE id = ?", (id_libro,)
    )

    conexion.commit()
    conexion.close()

    print("¡Préstamo registrado correctamente!")
    

# Consultar préstamos activos
def consultar_prestamos_activos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            prestamos.id,
            libros.titulo,
            lectores.nombre,
            lectores.apellido,
            prestamos.fecha_prestamo
        FROM prestamos
        INNER JOIN libros
            ON prestamos.id_libro = libros.id
        INNER JOIN lectores
            ON prestamos.id_lector = lectores.id
        WHERE prestamos.fecha_devolucion IS NULL
    """)

    prestamos = cursor.fetchall()

    print("\n===== PRESTAMOS ACTIVOS =====")

    if prestamos:
        for prestamo in prestamos:
            print("-------------------------")
            print("ID del préstamo:", prestamo[0])
            print("Libro:", prestamo[1])
            print("Lector:", prestamo[2], prestamo[3])
            print("Fecha del préstamo:", prestamo[4])
    else:
        print("No hay préstamos activos.")

    conexion.close()
    


# Registrar devolución de un libro
def registrar_devolucion():
    print("\n===== REGISTRAR DEVOLUCION =====")

    id_prestamo = input("ID del préstamo: ")

    conexion = conectar()
    cursor = conexion.cursor()

    # Buscar el préstamo
    cursor.execute("""
        SELECT id_libro
        FROM prestamos
        WHERE id = ? AND fecha_devolucion IS NULL
    """, (id_prestamo,))

    prestamo = cursor.fetchone()

    if prestamo is None:
        print("El préstamo no existe o ya fue devuelto.")
        conexion.close()
        return

    id_libro = prestamo[0]

    # Registrar la fecha de devolución
    fecha = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        UPDATE prestamos
        SET fecha_devolucion = ?
        WHERE id = ?
    """, (fecha, id_prestamo))

    # Verificar si quedan otros préstamos activos
    cursor.execute("""
        SELECT id
        FROM prestamos
        WHERE id_libro = ?
        AND fecha_devolucion IS NULL
    """, (id_libro,))
    
    otro_prestamo = cursor.fetchone()

    # Liberar el libro solamente si no tiene préstamos activos
    if otro_prestamo is None:
        cursor.execute("""
            UPDATE libros
            SET disponible = 1
            WHERE id = ?
        """, (id_libro,))

    # Guardar los cambios
    conexion.commit()
    conexion.close()

    print("¡Devolución registrada correctamente!")



# Sincronizar disponibilidad de los libros
def sincronizar_disponibilidad():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE libros
        SET disponible = CASE
            WHEN EXISTS (
                SELECT 1
                FROM prestamos
                WHERE prestamos.id_libro = libros.id
                AND prestamos.fecha_devolucion IS NULL
            )
            THEN 0
            ELSE 1
        END
    """)

    conexion.commit()
    conexion.close()

    print("Disponibilidad de libros actualizada.")
    


# MENÚ PRINCIPAL

def menu_principal():

    while True:

        print("\n===== SISTEMA DE GESTIÓN DE BIBLIOTECA =====")
        print("1. Registrar libro")
        print("2. Consultar libros")
        print("3. Buscar libro")
        print("4. Registrar lector")
        print("5. Consultar lectores")
        print("6. Buscar lector")
        print("7. Registrar préstamo")
        print("8. Consultar préstamos activos")
        print("9. Registrar devolución")
        print("10. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            registrar_libro()

        elif opcion == "2":
            consultar_libros()

        elif opcion == "3":
            buscar_libro()

        elif opcion == "4":
            registrar_lector()

        elif opcion == "5":
            consultar_lectores()

        elif opcion == "6":
            buscar_lector()

        elif opcion == "7":
            registrar_prestamo()

        elif opcion == "8":
            consultar_prestamos_activos()

        elif opcion == "9":
            registrar_devolucion()

        elif opcion == "10":
            print("¡Gracias por utilizar la biblioteca!")
            break

        else:
            print("Opción incorrecta. Intente nuevamente.")


# Ejecutar el programa
menu_principal()
