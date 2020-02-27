import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class VentanaPrincipal():
    def __init__(self):
        builder = Gtk.Builder()

        builder.add_from_file("principalGLADE.glade")

        ventanaPrincipal = builder.get_object("ventanaPrincipal")

        # ACTIVAMOS NUESTRA INTERFAZ GRÁFICA

        ventanaPrincipal.show_all()

    #FALTA PONER EL ON EXIT ETC

    #FUNCIONES

if __name__ == "__main__":
    VentanaPrincipal()
    Gtk.main()
