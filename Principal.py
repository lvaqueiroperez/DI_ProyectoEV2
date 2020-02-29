import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import sqlite3 as dbapi


# VENTANA PRINCIPAL
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


# VENTANA DE GESTIÓN (aquí haremos todos lo relacionado con la BD)
# TreeView aquí
class VentanaGestion(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gestión de Clientes")
        self.set_default_size(800, 600)

        boxV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.modelo = Gtk.ListStore(str, str, str, str, str, str)

        # PARA HACER EL APPEND, NECESITAMOS CONSEGUIR LOS DATOS DE LA BD, LOS GUARDAREMOS EN VARIABLES STR

        # ************************BD**********************************
        bd1 = dbapi.connect("baseDatosPrueba.dat")
        # Para trabajar con la BD creada, necesitamos cerar un "cursor" para ella
        cursor = bd1.cursor()

        # Para devolver (seleccionar) valores en una BD o tabla de una BD:
        cursor.execute("""SELECT * FROM clientes""")
        # Esto nos dará el primer valor de la tabla en una tupla tras hacer el select deseado
        # print(cursor.fetchone())
        # Esto nos dará todos los datos que hayamos seleccionado en el select:
        # print(cursor.fetchall())
        # Y esto los n primeros resultados del select:
        # print(cursor.fetchmany(2))

        # Los resultados se devuelven en una lista (o lista de tuplas si hay varios valores), podemos iterar con ellos !!!

        for elemento in cursor.fetchall():
            dni = elemento[0]
            nombre = elemento[1]
            apellido1 = elemento[2]
            apellido2 = elemento[3]
            direc = elemento[4]
            telf = elemento[5]

            self.modelo.append([dni,nombre,apellido1,apellido2,direc,telf])

        # ************************************************************
        # FILTROS (AHORA NUESTRO MODELO ESTARÁ FILTRADO Y SE PASARÁ A LLAMAR "modeloFIltrado")
        self.filtradoOcupacion = False
        modeloFiltrado = self.modelo.filter_new()
        # PONEMOS VISIBLE NUESTRO MODELO EN EL TREEVIEW
        modeloFiltrado.set_visible_func(self.ocupacion)
        self.modelo.set_sort_func(0, self.ordeAlfabetico)

        # MODELO EXTRA
        modeloCat = Gtk.ListStore(str, int)
        modeloCat.append(["*", 1])
        modeloCat.append(["**", 2])
        modeloCat.append(["***", 3])
        modeloCat.append(["****", 4])
        modeloCat.append(["*****", 5])

        # CONSTRUÍMOS EL TREE VIEW CON EL MODELO FILTRADO
        vista = Gtk.TreeView(model=modeloFiltrado)
        # Obtenemos las selecciones del TreeView y les asociamos un evento con una función que manejaremos más adelante
        seleccion = vista.get_selection()
        seleccion.connect("changed", self.on_vista_changed)
        # Ponemos el TreeView en nuestra box
        boxV.pack_start(vista, True, True, 0)

        # CREAMOS UNA CELDA DE TEXTO PARA EL DNI
        celdaText = Gtk.CellRendererText()
        celdaText.set_property("editable", False)

        # CREAMOS UNA COLUMNA PARA EL TREEVIEW CON EL DNI
        columnaDni = Gtk.TreeViewColumn('DNI', celdaText,
                                          text=0)  # OJO!!! de la columna del modelo qué columna va a mostrar la vista: la 0 "Hotel ..."

        # CREAMOS CELDA TEXTO NOMBRE
        celdaNombre = Gtk.CellRendererText()
        celdaNombre.set_property("editable", False)
        celdaNombre.connect("edited", self.on_celdaDireccion_edited, self.modelo)

        # CREAMOS COLUMNA NOMBRE
        columnaNombre = Gtk.TreeViewColumn('NOMBRE', celdaNombre, text=1)

        #CREAMOS CELDA TEXTO APELLIDO1
        celdaApellido1 = Gtk.CellRendererText()
        #CREAMOS COLUMNA PARA APELLIDO1
        columnaApellido1 = Gtk.TreeViewColumn('APELLIDO1', celdaApellido1, text=2)
        columnaApellido1.set_sort_column_id(0)  # si hacemos clic en la columna ocupacion la ordena

        # CREAMOS UNA CELDA TEXTO APELLIDO2
        celdaApellido2 = Gtk.CellRendererText()
        #celdaApellido2.connect("toggled", self.on_celdaCheck_toggled, self.modelo)

        #Y UNA COLUMNA PARA EL APELLIDO2:

        columnaApellido2 = Gtk.TreeViewColumn('APELLIDO2', celdaApellido2, text=3)

        #CELDA PARA UNA DIRECCION:
        celdaDireccion = Gtk.CellRendererText()
        # COLUMNA PARA DIRECCION
        columnaDireccion = Gtk.TreeViewColumn('DIRECCION', celdaDireccion, text = 4)

        # CREAMOS UNA CELDA PARA TELF
        celdaTelf = Gtk.CellRendererText()

        # Y UNA COLUMNA PARA TELF
        columnaTelf = Gtk.TreeViewColumn('TELEFONO', celdaTelf, text=5)



        vista.append_column(columnaDni)  # añadir al treeview la columna
        vista.append_column(columnaNombre)
        vista.append_column(columnaApellido1)
        vista.append_column(columnaApellido2)
        vista.append_column(columnaDireccion)
        vista.append_column(columnaTelf)


        # MENÚ DE ABAJO:
        boxH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.txtHotel = Gtk.Entry()
        self.txtDireccion = Gtk.Entry()
        self.txtOcupacion = Gtk.Entry()
        self.chkMascota = Gtk.CheckButton()
        self.cmbCategoria = Gtk.ComboBox()
        btnNovo = Gtk.Button("Novo")
        btnNovo.connect("clicked", self.on_btnNovo_clicked, self.modelo)
        boxH.pack_start(self.txtHotel, True, False, 0)
        boxH.pack_start(self.txtDireccion, True, False, 0)
        boxH.pack_start(self.txtOcupacion, True, False, 0)
        boxH.pack_start(self.chkMascota, True, False, 0)
        boxH.pack_start(self.cmbCategoria, True, False, 0)
        boxH.pack_start(btnNovo, True, False, 0)
        boxV.pack_start(boxH, True, False, 0)
        caixaFiltro = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.chkFiltro = Gtk.CheckButton(label='Filtro ocupación')
        self.chkFiltro.connect("toggled", self.on_chkFiltro_toggled, modeloFiltrado)
        caixaFiltro.pack_start(self.chkFiltro, True, True, 0)

        boxV.pack_start(caixaFiltro, True, False, 0)

        self.cmbCategoria.set_model(modeloCat)
        self.cmbCategoria.pack_start(celdaText, True)
        self.cmbCategoria.add_attribute(celdaText, "text", 0)

        # AÑADIMOS LA CAJA A LA VENTANA PRINCIPAL
        self.add(boxV)

        # FALTA
        # MOSTRAMOS TODOS
        self.show_all()
        self.connect("destroy", Gtk.main_quit)

        # FUNCIONES, NECESARIAS PARA QUE SE MUESTREN NUESTROS ELEMENTOS POR PANTALLA !!!!

    def on_celdaCheck_toggled(self, control, fila, modelo):  # nos deja marcar/desmarcar las opciones
        """"""

    def on_celdaDireccion_edited(self, control, fila, texto, modelo):  # podemos editar la celda de direcciones
        """"""

    def on_btnNovo_clicked(self, boton, modelo):
        """"""

    def on_celdaCombo_changed(self, control, posicion, indice, modelo, modeloCat):
        """"""

    def on_vista_changed(self, seleccion):
        """"""

    # SIN ESTA FUNCIÓN NO SE MUESTRA???
    def ocupacion(self, modelo, punteiro, a):
        if self.filtradoOcupacion is None or self.filtradoOcupacion is False:
            return True
        else:
            return self.modelo[punteiro][2]

    def on_chkFiltro_toggled(self, control, modeloFiltrado):
        """"""

    def ordeAlfabetico(modelo, fila1, fila2, datosUsuario):
        """"""

    """
    # ABRIR Y CERRAR LA BD CUANDO SE HAGA CADA OPERACIÓN
    #CREAR LA TABLA DE LA BD E INSERTAR 2 FILAS DE EJEMPLO:
    print("Versión DBAPI:")

    print(dbapi.apilevel)

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
    """


# EMPEZAMOS ABRIENDO LA PRINCIPAL, PROBAR A VER QUE PASA SI PONEMOS OTRA CLASE
if __name__ == "__main__":
    VentanaGestion()
    Gtk.main()
