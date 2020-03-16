import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import sqlite3 as dbapi

from reportlab.platypus import Table, Spacer, SimpleDocTemplate
from reportlab.lib.pagesizes import A4


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
                direc = elemento[3]
                telf = elemento[4]
                servicio = elemento[5]

                self.modelo.append([dni, nombre, apellido1, direc, telf, servicio])

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
        self.filtradoClientes = False
        modeloFiltrado = self.modelo.filter_new()
        # PONEMOS VISIBLE NUESTRO MODELO EN EL TREEVIEW
        modeloFiltrado.set_visible_func(self.clientes)

        # CONSTRUÍMOS EL TREE VIEW CON EL MODELO FILTRADO
        vista = Gtk.TreeView(model=modeloFiltrado)
        # Obtenemos las selecciones del TreeView y les asociamos un evento con una función que manejaremos más adelante
        seleccion = vista.get_selection()

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

        # CREAMOS COLUMNA NOMBRE
        columnaNombre = Gtk.TreeViewColumn('NOMBRE', celdaNombre, text=1)

        # CREAMOS CELDA TEXTO APELLIDO1
        celdaApellido1 = Gtk.CellRendererText()
        # CREAMOS COLUMNA PARA APELLIDO1
        columnaApellido1 = Gtk.TreeViewColumn('APELLIDO1', celdaApellido1, text=2)
        columnaApellido1.set_sort_column_id(0)  # si hacemos clic en la columna ocupacion la ordena

        # CREAMOS UNA CELDA TEXTO APELLIDO2
        celdaDirec = Gtk.CellRendererText()
        # celdaDirec.connect("toggled", self.on_celdaCheck_toggled, self.modelo)

        # Y UNA COLUMNA PARA EL APELLIDO2:

        columnaDirec = Gtk.TreeViewColumn('DIRECCION', celdaDirec, text=3)

        # CELDA PARA UNA DIRECCION:
        celdaTelf = Gtk.CellRendererText()
        # COLUMNA PARA DIRECCION
        columnaTelf = Gtk.TreeViewColumn('TELEFONO', celdaTelf, text=4)

        # CREAMOS UNA CELDA PARA TELF
        celdaServicio = Gtk.CellRendererText()

        # Y UNA COLUMNA PARA TELF
        columnaServicio = Gtk.TreeViewColumn('SERVICIO', celdaServicio, text=5)

        # AÑADIMOS AL TREE VIEW LAS COLUMNAS CON SUS CELDAS
        vista.append_column(columnaDni)
        vista.append_column(columnaNombre)
        vista.append_column(columnaApellido1)
        vista.append_column(columnaDirec)
        vista.append_column(columnaTelf)
        vista.append_column(columnaServicio)

        # MENÚ DE ABAJO: (HABRÁ QUE HACDER UN BOTÓN PARA UPDATE???? O IGUAL PODEMOS HACER EL APPEND EN EL MISMO MÉTODO CLICK)

        # ANTES DE NADA, EL BOTÓN DE MOSTRARLOS A TODOS
        # CON GLADE MENOS LA PARTE DE BUSCAR
        builder2 = Gtk.Builder()
        builder2.add_from_file("Gestion.glade")

        boxVParte1 = builder2.get_object("boxVParte1")

        # ELEMENTOS GLADE
        self.btnMostrarTodos = builder2.get_object("btnMostrarTodos")
        self.btnMostrarTodos.connect("clicked", self.on_btnTodos_clicked, self.modelo)

        self.txtDni = builder2.get_object("txtDni")
        self.txtNombre = builder2.get_object("txtNombre")
        self.txtApellido1 = builder2.get_object("txtApellido1")
        self.txtDirec = builder2.get_object("txtDirec")
        self.txtTelf = builder2.get_object("txtTelf")

        # PONEMOS UN CBOX PARA QUE EL USUARIO ESCOJA QUÉ TIPO DE SERVICIO DESEA (GLADE + python)
        # self.txtServicio = builder2.get_object("txtServicio")

        self.cboxServicioInsertar = builder2.get_object("cboxInsertar")
        # AÑADIMOS LOS ELEMENTOS AL CBOX

        # MODELO CBOX
        modeloServ = Gtk.ListStore(str)
        modeloServ.append(["Seguro Coche"])
        modeloServ.append(["Seguro Moto"])
        modeloServ.append([""])

        self.cboxServicioInsertar.set_model(modeloServ)

        # AÑADIMOS RENDERER AL CBOX
        rendererServ = Gtk.CellRendererText()
        self.cboxServicioInsertar.pack_start(rendererServ, True)

        # QUEREMOS QUE SE MUESTREN LOS CAMPOS, NO LOS NÚMEROS QUE HEMOS PUESTO, POR ESO PONEMOS UN 0, PORQUE EL PARÁMETRO ES EL PRIMERO QUE PUSIMOS EN EL MODELO
        self.cboxServicioInsertar.add_attribute(rendererServ, "text", 0)

        # TENEMOS QUE MODIFICAR LA FUNCIÓN AHORA QUE HEMOS PUESTO UN CBOX PARA EL CAMPO SERVICIOS !!!
        self.btnInsertar = builder2.get_object("btnInsertar")
        self.btnInsertar.connect("clicked", self.on_btnNovo_clicked, self.modelo, self.cboxServicioInsertar)

        self.txtDniBorrar = builder2.get_object("txtDniBorrar")
        self.btnBorrar = builder2.get_object("btnBorrar")
        self.btnBorrar.connect("clicked", self.on_btnBorrar_clicked, self.modelo)

        # AÑADIMOS LA FUNCIONALIDAD DE CONSULTAR
        boxH3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.cboxCampo = Gtk.ComboBox()
        self.btnBuscar = Gtk.Button("Buscar")
        self.btnBuscar.connect("clicked", self.on_btnBuscar_clicked, self.cboxCampo, self.modelo)

        # MODELO CBOX
        modeloCamp = Gtk.ListStore(str, int)
        modeloCamp.append(["dni", 1])
        modeloCamp.append(["nombre", 2])
        modeloCamp.append(["apellido1", 3])
        modeloCamp.append(["servicio", 4])
        modeloCamp.append(["direc", 5])
        modeloCamp.append(["telf", 6])

        self.cboxCampo.set_model(modeloCamp)

        # self.cboxCampo.connect("changed", self.on_cboxCampo_changed)

        # AÑADIMOS RENDERER AL CBOX
        renderer = Gtk.CellRendererText()
        self.cboxCampo.pack_start(renderer, True)

        # QUEREMOS QUE SE MUESTREN LOS CAMPOS, NO LOS NÚMEROS QUE HEMOS PUESTO, POR ESO PONEMOS UN 0, PORQUE EL PARÁMETRO ES EL PRIMERO QUE PUSIMOS EN EL MODELO
        self.cboxCampo.add_attribute(renderer, "text", 0)

        boxH3.pack_start(self.cboxCampo, True, False, 0)

        self.txtCampo = Gtk.Entry()
        boxH3.pack_start(self.txtCampo, True, False, 0)
        boxH3.pack_start(self.btnBuscar, True, False, 0)

        # AÑADIMOS BOTÓN PARA VOLVER AL MENÚ ANTERIOR

        self.btnVolver1 = builder2.get_object("btnVolver1")

        self.btnVolver1.connect("clicked", self.on_btnVolver1_clicked, self)

        # AÑADIMOS FUNCIONALIDAD DE GENERAR UN INFORME

        self.txtDniInforme = builder2.get_object("txtDniInforme")

        self.btnInformeGestion = builder2.get_object("btnInformeGestion")
        self.btnInformeGestion.connect("clicked", self.on_btnInformeGestion_clicked, self.txtDniInforme)

        # boxV.pack_start(boxH, True, False, 0)
        # boxV.pack_start(boxH2, True, False, 0)
        boxV.pack_start(boxVParte1, True, True, 0)
        boxV.pack_start(boxH3, True, False, 0)

        # AÑADIMOS LA CAJA A LA VENTANA PRINCIPAL
        self.add(boxV)

        # FALTA
        # MOSTRAMOS TODOS
        self.show_all()
        self.connect("destroy", Gtk.main_quit)

    # FUNCIONES PARA INFORMES:

    def on_btnInformeGestion_clicked(self, boton, dni):

        print("IMPRIMIENDO")
        # IMPLEMENTAMOS LA BD

        dniText = dni.get_text()
        print("DNI: " + dniText)

        try:

            self.bdInf = dbapi.connect("baseDatosPrueba.dat")
            self.cursorInf = self.bdInf.cursor()

            self.cursorInf.execute("""SELECT * FROM clientes WHERE dni='""" + dniText + """'""")

            for elemento in self.cursorInf.fetchall():
                dniInf = elemento[0]
                nombreInf = elemento[1]
                apellido1Inf = elemento[2]
                direcInf = elemento[3]
                telfInf = elemento[4]
                servicioInf = elemento[5]

                guion = []

                fila1 = ['', 'DNI', 'NOMBRE', 'APELLIDO1', 'DIRECCIÓN', 'TELF', 'SERVICIO']
                fila2 = ['', dniInf, nombreInf, apellido1Inf, direcInf, telfInf, servicioInf]

                taboa = Table([fila1, fila2])

                guion.append(taboa)

                doc = SimpleDocTemplate("informeCliente_" + dniInf + ".pdf", pagesize=A4, showBoundary=0)
                doc.build(guion)
                print("IMPRESO")

        except dbapi.OperationalError as errorOperacion:
            print("Error (OperationalError): " + str(errorOperacion))
        except dbapi.DatabaseError as errorBD:
            print("Error (DataBaseError): " + str(errorBD))

        finally:
            # UNA VEZ ACABADAS LAS OPERACIONES, DEBEMOS CERRAR PRIMERO EL CURSOS Y FINALMENTE LA BD SIEMPRE (finally)
            self.cursorInf.close()
            self.bdInf.close()

    # FUNCIONES DE CAMBIO DE VENTANAS

    def on_btnVolver1_clicked(self, boton, ventana):
        # PARA CAMBIAR DE VENTANAS TENEMOS QUE IMPORTARLAS PRIMERO
        from Principal import VentanaPrincipal

        ventanaPrincipal = VentanaPrincipal()
        ventana.hide()
        # CUANDO OCULTAMOS ESTA VENTANA, VUELVE A APARECER LA DE "PRINCIPAL" SIN DAR ERRORES (?)

    # FUNCIONES, NECESARIAS PARA QUE SE MUESTREN NUESTROS ELEMENTOS POR PANTALLA !!!!

    def on_btnNovo_clicked(self, boton, modelo, combo):

        # PODRÍAMOS MANEJAR ERRORES, COMO COMPROBAR QUE TODOS LOS CAMPOS ESTÁN RELLENADOS O ALGO ASÍ??

        # ANTES DE NADA OBTEBNEMOS EL VALOR SELECCIONADO DEL COMBOBOX
        cboxPunteroServ = combo.get_active_iter()

        cboxModeloServ = combo.get_model()

        # AL PARECER, EN SQLITE NO PODEMOS PONER LA CONDICIÓN CON UNA VARIABLE EXTERNA, SOLO EL VALOR DE LA CONDICIÓN
        # POR LO QUE TENDREMOS QUE TRABAJAR CON "IF"
        campo = cboxModeloServ[cboxPunteroServ][0]

        print(campo)

        # Y A LA BASE DE DATOS:
        try:
            bd2 = dbapi.connect("baseDatosPrueba.dat")
            # Para trabajar con la BD creada, necesitamos cerar un "cursor" para ella
            cursor2 = bd2.cursor()

            listaClientes = [(self.txtDni.get_text(),
                              self.txtNombre.get_text(),
                              self.txtApellido1.get_text(),
                              self.txtDirec.get_text(),
                              self.txtTelf.get_text(),
                              campo)
                             ]

            # OJO!!! "cursor.executemany()" recorre las listas y sus valores uno a uno y los mete en la BD
            cursor2.executemany("INSERT INTO clientes VALUES(?,?,?,?,?,?)", listaClientes)

            bd2.commit()

            # LO AÑADIMOS AL TREE VIEW
            modelo.append([self.txtDni.get_text(),
                           self.txtNombre.get_text(),
                           self.txtApellido1.get_text(),
                           self.txtDirec.get_text(),
                           self.txtTelf.get_text(),
                           campo]
                          )  # indice y columna

        except dbapi.OperationalError as errorOperacion:
            print("Error (OperationalError): " + str(errorOperacion))
        except dbapi.DatabaseError as errorBD:
            print("Error (DataBaseError): " + str(errorBD))
            self.txtDni.set_text("ERROR-DNI YA EXISTE")

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
    # HACER UN CLEAR DEL MODELO Y PONERLE LOS RESULTADOS DE LA BÚSQUEDA
    # PONER TODOS LOS RESULTADOS SI SE BUSCA CON LA CASILLA EN BLANCO??
    # BOTÓN PARA VOLVER A MOSTRAR TODOS LOS RESULTADOS !!!
    def on_btnBuscar_clicked(self, boton, combo, modelo):

        cboxPuntero = combo.get_active_iter()

        cboxModelo = combo.get_model()

        # AL PARECER, EN SQLITE NO PODEMOS PONER LA CONDICIÓN CON UNA VARIABLE EXTERNA, SOLO EL VALOR DE LA CONDICIÓN
        # POR LO QUE TENDREMOS QUE TRABAJAR CON "IF"
        campo = cboxModelo[cboxPuntero][0]

        # Ya tenemos el campo que usaremos para la consulta, ahora necesitamos su valor concreto

        valorCampo = self.txtCampo.get_text()

        print(campo)
        print(valorCampo)

        # NOS CONECTAMOS A LA BD:
        try:
            modelo.clear()
            self.bd4 = dbapi.connect("baseDatosPrueba.dat")
            self.cursor4 = self.bd4.cursor()
            print("s")

            if (campo == 'dni'):

                self.cursor4.execute("""SELECT * FROM clientes WHERE dni ='""" + valorCampo + """'""")

                for elemento in self.cursor4.fetchall():
                    dni = elemento[0]
                    nombre = elemento[1]
                    apellido1 = elemento[2]
                    direc = elemento[3]
                    telf = elemento[4]
                    servicio = elemento[5]

                    print(dni + 'a')
                    modelo.append([dni, nombre, apellido1, direc, telf, servicio])

            elif (campo == 'nombre'):

                self.cursor4.execute("""SELECT * FROM clientes WHERE nombre ='""" + valorCampo + """'""")

                for elemento in self.cursor4.fetchall():
                    dni = elemento[0]
                    nombre = elemento[1]
                    apellido1 = elemento[2]
                    direc = elemento[3]
                    telf = elemento[4]
                    servicio = elemento[5]

                    print(dni + 'a')
                    modelo.append([dni, nombre, apellido1, direc, telf, servicio])

            elif (campo == 'apellido1'):

                self.cursor4.execute("""SELECT * FROM clientes WHERE apellido1 ='""" + valorCampo + """'""")

                for elemento in self.cursor4.fetchall():
                    dni = elemento[0]
                    nombre = elemento[1]
                    apellido1 = elemento[2]
                    direc = elemento[3]
                    telf = elemento[4]
                    servicio = elemento[5]

                    print(dni + 'a')
                    modelo.append([dni, nombre, apellido1, direc, telf, servicio])

            elif (campo == 'servicio'):

                self.cursor4.execute("""SELECT * FROM clientes WHERE servicio ='""" + valorCampo + """'""")

                for elemento in self.cursor4.fetchall():
                    dni = elemento[0]
                    nombre = elemento[1]
                    apellido1 = elemento[2]
                    apellido2 = elemento[3]
                    direc = elemento[4]
                    telf = elemento[5]

                    print(dni + 'a')
                    modelo.append([dni, nombre, apellido1, apellido2, direc, telf])

            elif (campo == 'direc'):

                self.cursor4.execute("""SELECT * FROM clientes WHERE direc ='""" + valorCampo + """'""")

                for elemento in self.cursor4.fetchall():
                    dni = elemento[0]
                    nombre = elemento[1]
                    apellido1 = elemento[2]
                    apellido2 = elemento[3]
                    direc = elemento[4]
                    telf = elemento[5]

                    print(dni + 'a')
                    modelo.append([dni, nombre, apellido1, apellido2, direc, telf])

            elif (campo == 'telf'):

                self.cursor4.execute("""SELECT * FROM clientes WHERE telf ='""" + valorCampo + """'""")

                for elemento in self.cursor4.fetchall():
                    dni = elemento[0]
                    nombre = elemento[1]
                    apellido1 = elemento[2]
                    apellido2 = elemento[3]
                    direc = elemento[4]
                    telf = elemento[5]

                    print(dni + 'a')
                    modelo.append([dni, nombre, apellido1, apellido2, direc, telf])




        except dbapi.OperationalError as errorOperacion:
            print("Error (OperationalError): " + str(errorOperacion))
        except dbapi.DatabaseError as errorBD:
            print("Error (DataBaseError): " + str(errorBD))

        finally:
            # UNA VEZ ACABADAS LAS OPERACIONES, DEBEMOS CERRAR PRIMERO EL CURSOS Y FINALMENTE LA BD SIEMPRE (finally)
            self.cursor4.close()
            self.bd4.close()

    def on_btnTodos_clicked(self, boton, modelo):

        modelo.clear()

        try:

            self.bd5 = dbapi.connect("baseDatosPrueba.dat")
            self.cursor5 = self.bd5.cursor()

            self.cursor5.execute("""SELECT * FROM clientes""")

            for elemento in self.cursor5.fetchall():
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
            self.cursor5.close()
            self.bd5.close()

    # SIN ESTA FUNCIÓN NO SE MUESTRA???
    def clientes(self, modelo, punteiro, a):
        if self.filtradoClientes is None or self.filtradoClientes is False:
            return True
        else:
            return self.modelo[punteiro][2]


# UTILIDADES BD:
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
           "create table clientes(dni text primary key,nombre text, apellido1 text, direc text, telf text, servicio text)")
       bd1.commit()

       # INSERTAMOS
       listaClientes = [('31143-U', 'Jandro', 'Alvarez', 'Avenida1', '555444777', 'Almacen'),
                        ('22222-A', 'Pepe', 'Gonzalez', 'Avenida2', '111222333', 'Seguro')]

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
if __name__ == "__main__":
    # VentanaPrincipal()
    VentanaGestion()
    # VentanaServicios()
    Gtk.main()
