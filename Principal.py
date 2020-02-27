import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sqlite3 as dbapi


class VentanaPrincipal():
    def __init__(self):
        builder = Gtk.Builder()

        builder.add_from_file("principalGLADE.glade")

        ventanaPrincipal = builder.get_object("ventanaPrincipal")

        # MOSTRAMOS LA VENTANA PRINCIPAL
        ventanaPrincipal.show_all()

        # PONEMOS EL EVENTO DE SALIDA A LA VENTANA PRINCIPAL
        ventanaPrincipal.connect("destroy", Gtk.main_quit)

    # FUNCIONES


class VentanaGestion():
    def __init__(self):
        "BD AQUI, PRIMERO LA CREAMOS CON SUS DATOS Y LUEGO SIMPLEMENTE LA LEEMOS Y OPERAMOS CON ELLA EN CASO NECESARIO"
        "TENDREMOS QUE TENERLA ABIERTA PARA QUE AL CLICKAR EN UN BOTÓN PODAMOS ACTIVAR EL EVENTO DE INSERTAR/BORRAR/MODIFICAR"

        print("Versión DBAPI:")

        print(dbapi.apilevel)

        # Ver el "Modo de Thread" de nuestro sqlite
        """
        1 --> single-thread
        2 --> multi-thread  Se pueden usar varios threads PERO solo uno se podrá conectar a la BD a la vez  
        3 --> Serialized  Se pueden usar con la BD varios threads sin restrinciones"""
        print(dbapi.threadsafety)

        print(dbapi.paramstyle)

        try:
            bd1 = dbapi.connect("baseDatosPrueba.dat")
            # Para trabajar con la BD creada, necesitamos cerar un "cursor" para ella
            cursor = bd1.cursor()

            # CREAMOS TABLA:
            cursor.execute(
                "create table clientes(dni text,nombre text, apellido1 text, apellido2 text, direc text, telf text)")
            bd1.commit()

            # INSERTAMOS
            listaClientes = [('31143-U', 'Jandro', 'Perez', 'Alvarez', 'Avenida1', '555444777'),
                             ('22222-A', 'Pepe', 'Gonzalez', 'Rivas', 'Avenida2', '111222333')]

            # OJO!!! "cursor.executemany()" recorre las listas y sus valores uno a uno y los mete en la BD
            cursor.executemany("INSERT INTO clientes VALUES(?,?,?,?,?,?)", listaClientes)

            bd1.commit()

        # EXCEPCIONES
        except dbapi.OperationalError as errorOperacion:
            print("Error (OperationalError): " + str(errorOperacion))
        except dbapi.DatabaseError as errorBD:
            print("Error (DataBaseError): " + str(errorBD))

        finally:
            # UNA VEZ ACABADAS LAS OPERACIONES, DEBEMOS CERRAR PRIMERO EL CURSOS Y FINALMENTE LA BD SIEMPRE (finally)
            cursor.close()
            bd1.close()


# EMPEZAMOS ABRIENDO LA PRINCIPAL, PROBAR A VER QUE PASA SI PONEMOS OTRA CLASE
if __name__ == "__main__":
    VentanaGestion()
    Gtk.main()
