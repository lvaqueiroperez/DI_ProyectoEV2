import gi

# SI SE CIERRA EL PROGRAMA, PUES SE CERRARÁN TODAS LAS VENTANAS
# PODEMOS PONER BOTONES DE "VOLVER AL MENÚ PRINCIPAL" EN CADA INTERFAz
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# OJO !! PONER CBOX EN SERVICIOS Y ACABAR TODOS ANTES DE PONERSE CON LA SEGUNDA PARTE DEL PROYECTO
# VENTANA PRINCIPAL
class VentanaPrincipal():
    """
    Clase en la que se creará la ventana principal de la aplicación usando los
    componentes y variables necesarios.
    """
    def __init__(self):
        builder = Gtk.Builder()

        builder.add_from_file("principalGLADE.glade")

        self.ventanaPrincipal = builder.get_object("ventanaPrincipal")

        self.btnGestion = builder.get_object("btnGestion")
        self.btnServicios = builder.get_object("btnServicios")

        # PASAMOS COMO PARÁMETRO LA VENTANA A ESCONDER, EN LA FUNCIÓN HAREMOS QUE SE MUESTRE LA OTRA
        self.btnGestion.connect("clicked", self.on_btnGestion_clicked, self.ventanaPrincipal)
        self.btnServicios.connect("clicked", self.on_btnServicios_clicked, self.ventanaPrincipal)

        # MOSTRAMOS LA VENTANA PRINCIPAL
        self.ventanaPrincipal.show_all()

        # PONEMOS EL EVENTO DE SALIDA A LA VENTANA PRINCIPAL
        self.ventanaPrincipal.connect("destroy", Gtk.main_quit)

    # FUNCIONES DE CAMBIO DE VENTANAS

    def on_btnGestion_clicked(self, boton, ventana):
        """
        Función que controla el comportamiento del botón "self.btnGestion".
        Al pulsar el botón, se cerrará la ventana actual y se abrirá la ventana de "Gestión de clientes"

        :param boton:
        :param ventana: la ventana actual para poder cerrarla

        """
        # PARA CAMBIAR DE VENTANAS TENEMOS QUE IMPORTARLAS PRIMERO
        from ventanas.Gestion import VentanaGestion

        ventanaGestion = VentanaGestion()
        # ventanaGestion.connect("delete-event", self.on_destroy)
        # ventanaGestion.connect("destroy", self.on_destroy)
        ventanaGestion.show_all()
        ventana.hide()

    def on_btnServicios_clicked(self, boton, ventana):
        """
        Función que controla el comportamiento del botón "self.btnServicios".
        Al pulsar el botón, se cerrará la ventana actual y se abrirá la ventana de "Servicios"

        :param boton:
        :param ventana: la ventana actual para poder cerrarla
        :return:
        """
        from ventanas.Servicios import VentanaServicios

        ventanaServicios = VentanaServicios()
        ventanaServicios.show_all()
        ventana.hide()


# EMPEZAMOS ABRIENDO LA PRINCIPAL, PROBAR A VER QUE PASA SI PONEMOS OTRA CLASE
if __name__ == "__main__":
    VentanaPrincipal()
    # VentanaGestion()
    # VentanaServicios()
    Gtk.main()
