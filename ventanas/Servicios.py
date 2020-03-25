import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sqlite3 as dbapi
# IMPORTS REPORTLAB
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.graphics.charts.piecharts import Pie


class VentanaServicios(Gtk.Window):
    """
    Clase donde se creará la ventana de "Servicios" usando las variables y componentes necesarios.
    """

    def __init__(self):

        Gtk.Window.__init__(self, title="Servicios")
        self.set_default_size(800, 400)
        # GLADE
        self.builderCoche = Gtk.Builder()
        self.builderCoche.add_from_file("./ventanas/ServicioCoche.glade")

        self.builderMoto = Gtk.Builder()
        self.builderMoto.add_from_file("./ventanas/ServicioMoto.glade")

        self.builderPag3 = Gtk.Builder()
        self.builderPag3.add_from_file("./ventanas/pagina3Box.glade")

        # EMPEZAMOS EL TRY AQUÍ PARA QUE NOS PILLE EL MODELO
        try:
            # DEJAMOS CREADAS LAS VARIABLES DE BD
            self.bdSer = dbapi.connect("./ventanas/baseDatosPrueba.dat")
            # Para trabajar con la BD creada, necesitamos cerar un "cursor" para ella
            self.cursorSer = self.bdSer.cursor()

            # CONTAMOS CUANTOS CLIENTES HAY EN TOTAL Y CUANTOS EN CADA SERVICIO, PARA TENER LAS ESTADÍSTICAS CLARAS

            self.cursorSer.execute("""SELECT COUNT(*) FROM clientes""")
            # OJO!! COUNT DEVUELVE EN FORMA DE TUPLAS, DONDE LA POSICIÓN [0] ES EL VALOR QUE BUSCAMOS
            numClientes = self.cursorSer.fetchone()
            print(numClientes)

            self.cursorSer.execute("""SELECT COUNT(*) FROM clientes WHERE servicio = 'Seguro Coche'""")

            numCoche = self.cursorSer.fetchone()
            print(numCoche)

            self.cursorSer.execute("""SELECT COUNT(*) FROM clientes WHERE servicio = 'Seguro Moto'""")

            numMoto = self.cursorSer.fetchone()
            print(numMoto)

            # AHORA QUE TENEMOS TODOS LOS NÚMEROS, CADA UNO EN SU LABEL

            lblCoche = self.builderCoche.get_object("lblAseguradosCoche")
            lblCoche.set_text("Número de Asegurados: " + str(numCoche[0]))

            lblMoto = self.builderMoto.get_object("lblAseguradosMoto")
            lblMoto.set_text("Número de Asegurados: " + str(numMoto[0]))

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

            notebookSer.append_page(pagina3, Gtk.Label("Informe/Volver"))

            # AÑADIMOS LA FUNCIONALIDAD DE GENERAR UN INFORME:

            self.btnInforme = self.builderPag3.get_object("btnInformeServicios")
            self.btnInforme.connect("clicked", self.on_btnInforme_clicked)

            # AÑADIMOS LA FUNCIONALIDAD DE VOLVER
            self.btnVolver2 = self.builderPag3.get_object("btnVolver2")
            self.btnVolver2.connect("clicked", self.on_btnVolver2_clicked, self)

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

    # FUNCIONES DE CAMBIO DE VENTANAS

    def on_btnVolver2_clicked(self, boton, ventana):
        """
        Función que controla el comportamiento del botón "btnVolver2".
        Oculta la ventana actual y vuelve a mostrar la ventana "Principal".

        :param boton:
        :param ventana: la ventana a cerrar
        :return:
        """
        # PARA CAMBIAR DE VENTANAS TENEMOS QUE IMPORTARLAS PRIMERO
        from ventanas.Principal import VentanaPrincipal

        ventanaPrincipal = VentanaPrincipal()
        ventana.hide()
        # CUANDO OCULTAMOS ESTA VENTANA, VUELVE A APARECER LA DE "PRINCIPAL" SIN DAR ERRORES (?)

    def on_btnInforme_clicked(self, boton):
        """
        Función que controla el comportamiento del botón "btnInforme".
        Genera un informe general sobre cuantos clientes hay registrados en cada servicio usando ReportLab.

        :param boton:
        :return:
        """
        print("Imprimiendo...")
        # añadimos un nuevo dibujo
        d2 = Drawing(300, 200)

        tarta = Pie()

        tarta.x = 65
        tarta.y = 15
        tarta.height = 170
        tarta.width = 170
        # tarta.data = [10.456, 20.234, 30.567, 40, 50]
        tarta.labels = ['Seguro Coche', 'Seguro Moto', 'Sin Seguro', 'Sin Seguro']
        # porciones
        # tarta.slices.strokeWidth = 0.5
        # tarta.slices[3].popout = 50
        # tarta.slices[3].strokeWidth = 5
        # tarta.slices[3].strokeDashArray = [5, 2]  # pixels de la linea (tamaño)
        # tarta.slices[3].labelRadius = 1.75
        # tarta.slices[3].fontColor = colors.red
        tarta.sideLabels = 0
        cores = [colors.blue, colors.red, colors.green]

        # coge cada elemento y le asigna un numero
        for i, color in enumerate(cores):
            tarta.slices[i].fillColor = color

        d2.add(tarta)

        doc = SimpleDocTemplate("./ventanas/informeGrafica.pdf", pagesize=A4)
        doc.build([d2])
        print("Impreso")


if __name__ == "__main__":
    # VentanaPrincipal()
    # VentanaGestion()
    VentanaServicios()
    Gtk.main()
