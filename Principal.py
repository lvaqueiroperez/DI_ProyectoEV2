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
        # EMPEZAMOS EL TRY AQUÍ PARA QUE NOS PILLE EL MODELO
        try:
            Gtk.Window.__init__(self, title="Gestión de Clientes")
            self.set_default_size(800, 600)

            boxV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            # TENEMOS QUE DECLARAR EL MODELO DENTRO DEL TRY PARA QUE LO PILLE ???
            self.modelo = Gtk.ListStore(str, str, str, str, str, str)

            # PARA HACER EL APPEND, NECESITAMOS CONSEGUIR LOS DATOS DE LA BD, LOS GUARDAREMOS EN VARIABLES STR
            """OJO!! LOS CAMPOS INSERTADOS EN EL TREE VIEW HACEN QUE LA VENTANA SE AGRANDE CUANTOS MÁS SEAN, HACER ALGO PARA QUE
              APAREZCA UNA BARRA SLIDER"""

            # ************************BD**********************************

            self.bd1 = dbapi.connect("baseDatosPrueba.dat")
            # Para trabajar con la BD creada, necesitamos cerar un "cursor" para ella
            self.cursor = self.bd1.cursor()

            # Para devolver (seleccionar) valores en una BD o tabla de una BD:
            self.cursor.execute("""SELECT * FROM clientes""")
            # Esto nos dará el primer valor de la tabla en una tupla tras hacer el select deseado
            # print(cursor.fetchone())
            # Esto nos dará todos los datos que hayamos seleccionado en el select:
            # print(cursor.fetchall())
            # Y esto los n primeros resultados del select:
            # print(cursor.fetchmany(2))

            # Los resultados se devuelven en una lista (o lista de tuplas si hay varios valores), podemos iterar con ellos !!!

            for elemento in self.cursor.fetchall():
                dni = elemento[0]
                nombre = elemento[1]
                apellido1 = elemento[2]
                apellido2 = elemento[3]
                direc = elemento[4]
                telf = elemento[5]

                self.modelo.append([dni, nombre, apellido1, apellido2, direc, telf])

        except dbapi.OperationalError as errorOperacion:
            print("Error (OperationalError): " + str(errorOperacion))

        except dbapi.DatabaseError as errorBD:
            print("Error (DataBaseError): " + str(errorBD))

        finally:
            # UNA VEZ ACABADAS LAS OPERACIONES, DEBEMOS CERRAR PRIMERO EL CURSOS Y FINALMENTE LA BD SIEMPRE (finally)
            self.cursor.close()
            self.bd1.close()

            # *************************FIN BD***********************************

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

        # NECESITAMOS QUE LOS DATOS DEL TREE VIEW SE MUESTREN EN UNA VENTANA CON UN SCROLL DE MANERA CÓMODA:
        # CREAMOS UN FRAME DONDE LOS PONDREMOS
        frameClientes = Gtk.Frame()
        frameClientes.set_label("Clientes")
        boxV.pack_start(frameClientes, True, True, 0)
        # PARA EL SCROLL:
        ventanaScroll = Gtk.ScrolledWindow()
        ventanaScroll.set_hexpand(True)
        ventanaScroll.set_vexpand(True)
        # AÑADIMOS AL SCROLL EL TREE VIEW, Y LUEGO AL FRAME EL SCROLL
        ventanaScroll.add(vista)
        frameClientes.add(ventanaScroll)
        # FINALMENTE PONEMOS EL FRAME EN NUESTRA BOX PRINCIPAL
        boxV.pack_start(frameClientes, True, True, 0)

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

        # CREAMOS CELDA TEXTO APELLIDO1
        celdaApellido1 = Gtk.CellRendererText()
        # CREAMOS COLUMNA PARA APELLIDO1
        columnaApellido1 = Gtk.TreeViewColumn('APELLIDO1', celdaApellido1, text=2)
        columnaApellido1.set_sort_column_id(0)  # si hacemos clic en la columna ocupacion la ordena

        # CREAMOS UNA CELDA TEXTO APELLIDO2
        celdaApellido2 = Gtk.CellRendererText()
        # celdaApellido2.connect("toggled", self.on_celdaCheck_toggled, self.modelo)

        # Y UNA COLUMNA PARA EL APELLIDO2:

        columnaApellido2 = Gtk.TreeViewColumn('APELLIDO2', celdaApellido2, text=3)

        # CELDA PARA UNA DIRECCION:
        celdaDireccion = Gtk.CellRendererText()
        # COLUMNA PARA DIRECCION
        columnaDireccion = Gtk.TreeViewColumn('DIRECCION', celdaDireccion, text=4)

        # CREAMOS UNA CELDA PARA TELF
        celdaTelf = Gtk.CellRendererText()

        # Y UNA COLUMNA PARA TELF
        columnaTelf = Gtk.TreeViewColumn('TELEFONO', celdaTelf, text=5)

        # AÑADIMOS AL TREE VIEW LAS COLUMNAS CON SUS CELDAS
        vista.append_column(columnaDni)
        vista.append_column(columnaNombre)
        vista.append_column(columnaApellido1)
        vista.append_column(columnaApellido2)
        vista.append_column(columnaDireccion)
        vista.append_column(columnaTelf)

        # MENÚ DE ABAJO: (HABRÁ QUE HACDER UN BOTÓN PARA UPDATE???? O IGUAL PODEMOS HACER EL APPEND EN EL MISMO MÉTODO CLICK)
        # PARA AÑADIR CLIENTES A LA BD:
        # BOX DONDE PONDREMOS TODOS LO NECESARIO
        boxH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.txtDni = Gtk.Entry()
        self.txtNombre = Gtk.Entry()
        self.txtApellido1 = Gtk.Entry()
        self.txtApellido2 = Gtk.Entry()
        self.txtDirec = Gtk.Entry()
        self.txtTelf = Gtk.Entry()
        # BOTÓN DE INSERCCIÓN DE UN NUEVO CLIENTE
        btnNuevo = Gtk.Button("Insertar Cliente")
        btnNuevo.connect("clicked", self.on_btnNovo_clicked, self.modelo)

        boxH.pack_start(self.txtDni, True, False, 0)
        boxH.pack_start(self.txtNombre, True, False, 0)
        boxH.pack_start(self.txtApellido1, True, False, 0)
        boxH.pack_start(self.txtApellido2, True, False, 0)
        boxH.pack_start(self.txtDirec, True, False, 0)
        boxH.pack_start(self.txtTelf, True, False, 0)
        boxH.pack_start(btnNuevo, True, False, 0)

        # AÑADIMOS LA FUNCIONALIDAD DE BORRAR
        boxH2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.txtDniBorrar = Gtk.Entry()
        self.btnBorrar = Gtk.Button("Borrar Cliente")
        # BORRAREMOS TAMBIÉN DE LA BASE DE DATOS EL CLIENTE Y REFRESCAREMOS EL TREE VIEW DIRECTAMENTE
        self.btnBorrar.connect("clicked", self.on_btnBorrar_clicked, self.modelo)

        boxH2.pack_start(self.txtDniBorrar, True, False, 0)
        boxH2.pack_start(self.btnBorrar, True, False, 0)

        # AÑADIMOS LA FUNCIONALIDAD DE CONSULTAR
        boxH3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.cboxCampo = Gtk.ComboBox()

        # MODELO CBOX
        modeloCamp = Gtk.ListStore(str, int)
        modeloCamp.append(["dni", 1])
        modeloCamp.append(["nombre", 2])
        modeloCamp.append(["apellido1", 3])
        modeloCamp.append(["apellido2", 4])
        modeloCamp.append(["direc", 5])
        modeloCamp.append(["telf", 6])

        self.cboxCampo.set_model(modeloCamp)

        self.cboxCampo.connect("changed", self.on_cboxCampo_changed)

        # AÑADIMOS RENDERER AL CBOX
        renderer = Gtk.CellRendererText()
        self.cboxCampo.pack_start(renderer, True)

        # QUEREMOS QUE SE MUESTREN LOS CAMPOS, NO LOS NÚMEROS QUE HEMOS PUESTO, POR ESO PONEMOS UN 0, PORQUE EL PARÁMETRO ES EL PRIMERO QUE PUSIMOS EN EL MODELO
        self.cboxCampo.add_attribute(renderer, "text", 0)

        #POR ÚLTIMO, HACEMOS QUE SE MUESTRE EL DNI POR DEFECTO EN EL CBOX (????)


        boxH3.pack_start(self.cboxCampo, True, False, 0)

        self.txtCampo = Gtk.Entry()
        boxH3.pack_start(self.txtCampo, True, False, 0)

        boxV.pack_start(boxH, True, False, 0)
        boxV.pack_start(boxH2, True, False, 0)
        boxV.pack_start(boxH3, True, False, 0)

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

        # PODRÍAMOS MANEJAR ERRORES, COMO COMPROBAR QUE TODOS LOS CAMPOS ESTÁN RELLENADOS O ALGO ASÍ??
        # LO AÑADIMOS AL TREE VIEW
        modelo.append([self.txtDni.get_text(),
                       self.txtNombre.get_text(),
                       self.txtApellido1.get_text(),
                       self.txtApellido2.get_text(),
                       self.txtDirec.get_text(),
                       self.txtTelf.get_text()]
                      )  # indice y columna

        # Y A LA BASE DE DATOS:
        try:
            bd2 = dbapi.connect("baseDatosPrueba.dat")
            # Para trabajar con la BD creada, necesitamos cerar un "cursor" para ella
            cursor2 = bd2.cursor()

            listaClientes = [(self.txtDni.get_text(),
                              self.txtNombre.get_text(),
                              self.txtApellido1.get_text(),
                              self.txtApellido2.get_text(),
                              self.txtDirec.get_text(),
                              self.txtTelf.get_text())
                             ]

            # OJO!!! "cursor.executemany()" recorre las listas y sus valores uno a uno y los mete en la BD
            cursor2.executemany("INSERT INTO clientes VALUES(?,?,?,?,?,?)", listaClientes)

            bd2.commit()

        except dbapi.OperationalError as errorOperacion:
            print("Error (OperationalError): " + str(errorOperacion))
        except dbapi.DatabaseError as errorBD:
            print("Error (DataBaseError): " + str(errorBD))

        finally:
            # UNA VEZ ACABADAS LAS OPERACIONES, DEBEMOS CERRAR PRIMERO EL CURSOS Y FINALMENTE LA BD SIEMPRE (finally)
            cursor2.close()
            bd2.close()

    def on_btnBorrar_clicked(self, boton, modelo):

        cliente = (self.txtDniBorrar.get_text())

        # BORRAMOS EL CLIENTE ESPECIFICADO DE LA BD Y REFRESCAMOS EL TREE VIEW
        try:
            self.bd3 = dbapi.connect("baseDatosPrueba.dat")
            self.cursor3 = self.bd3.cursor()

            # ESTE EN CONCRETO NO IBA BIEN CON LAS INTERROGACIONES
            self.cursor3.execute("""DELETE FROM clientes WHERE dni = '""" + cliente + """'""")
            self.bd3.commit()

            # REFRESCAMOS
            modelo.clear()

            self.cursor3.execute("""SELECT * FROM clientes""")

            for elemento in self.cursor3.fetchall():
                dni = elemento[0]
                nombre = elemento[1]
                apellido1 = elemento[2]
                apellido2 = elemento[3]
                direc = elemento[4]
                telf = elemento[5]

                self.modelo.append([dni, nombre, apellido1, apellido2, direc, telf])

            self.bd3.commit()

        except dbapi.OperationalError as errorOperacion:
            print("Error (OperationalError): " + str(errorOperacion))
        except dbapi.DatabaseError as errorBD:
            print("Error (DataBaseError): " + str(errorBD))

        finally:
            # UNA VEZ ACABADAS LAS OPERACIONES, DEBEMOS CERRAR PRIMERO EL CURSOS Y FINALMENTE LA BD SIEMPRE (finally)
            self.cursor3.close()
            self.bd3.close()

    # PARA CONSULTAR:
    # EN UN COMBOBOX ESCOGEREMOS EL CAMPO POR EL QUE QUEREMOS CONSULTAR Y EN UN TXT ESPECIFICAREMOS EL CAMPO
    def on_cboxCampo_changed(self):
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
