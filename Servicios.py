import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import sqlite3 as dbapi


class VentanaServicios(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Servicios")
        self.set_default_size(800, 400)
        # GLADE
        self.builderCoche = Gtk.Builder()
        self.builderCoche.add_from_file("ServicioCoche.glade")

        self.builderMoto = Gtk.Builder()
        self.builderMoto.add_from_file("ServicioMoto.glade")

        self.builderPag3 = Gtk.Builder()
        self.builderPag3.add_from_file("pagina3Box.glade")

        # EMPEZAMOS EL TRY AQUÍ PARA QUE NOS PILLE EL MODELO
        try:
            # DEJAMOS CREADAS LAS VARIABLES DE BD
            self.bdSer = dbapi.connect("baseDatosPrueba.dat")
            # Para trabajar con la BD creada, necesitamos cerar un "cursor" para ella
            self.cursorSer = self.bdSer.cursor()

            # Creamos componente Notebook
            notebookSer = Gtk.Notebook()

            pagina1 = self.builderCoche.get_object("boxCoche")
            # PARA SEPARAR LOS ELEMENTOS DEL BORDE DE LA CAJA, PONEMOS UNA "ANCHURA DE BORDE" QUE LOS SEPARA
            pagina1.set_border_width(10)

            # Añadimos la "página" a nuestro notebook, pudiendo darle un título a la solapa:
            notebookSer.append_page(pagina1, Gtk.Label("Seguros Coche"))

            pagina2 = self.builderMoto.get_object("boxMoto")
            pagina2.set_border_width(10)
            notebookSer.append_page(pagina2, Gtk.Label("Seguros Moto"))

            pagina3 = self.builderPag3.get_object("boxPag3");

            # AQUÍ OBTENEMOS DEL BUILDER EL BOTÓN Y LE ASOCIAMOS SU FUNCIÓN

            pagina3.set_border_width(10)

            notebookSer.append_page(pagina3, Gtk.Label("Informe"))

            self.add(notebookSer)

            # Añadimos la función de salir de la ventana
            self.connect("destroy", Gtk.main_quit)

            # Y las mostramos
            self.show_all()




        except dbapi.OperationalError as errorOperacion:
            print("Error (OperationalError): " + str(errorOperacion))

        except dbapi.DatabaseError as errorBD:
            print("Error (DataBaseError): " + str(errorBD))

        finally:
            # UNA VEZ ACABADAS LAS OPERACIONES, DEBEMOS CERRAR PRIMERO EL CURSOS Y FINALMENTE LA BD SIEMPRE (finally)
            self.cursorSer.close()
            self.bdSer.close()


if __name__ == "__main__":
    # VentanaPrincipal()
    # VentanaGestion()
    VentanaServicios()
    Gtk.main()
