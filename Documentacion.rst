==========================
Documentación Proyecto EV2
==========================
Principal.py
************
class VentanaPrincipal()
------------------------
Clase en la que se creará la ventana principal de la aplicación usando los
componentes y variables necesarios.

def on_btnGestion_clicked(self, boton, ventana):
------------------------------------------------
Función que controla el comportamiento del botón "self.btnGestion" ::

        from Gestion import VentanaGestion

        ventanaGestion = VentanaGestion()
        ventanaGestion.show_all()
        ventana.hide()

Al pulsar el botón, se cerrará la ventana actual y se abrirá la ventana de "Gestión de clientes"

Parámetros:

* self
* boton
* ventana: la ventana actual para poder cerrarla

def on_btnServicios_clicked(self, boton, ventana):
--------------------------------------------------
Función que controla el comportamiento del botón "self.btnServicios" ::

        from Gestion import VentanaGestion

        ventanaGestion = VentanaGestion()
        ventanaGestion.show_all()
        ventana.hide()

Al pulsar el botón, se cerrará la ventana actual y se abrirá la ventana de "Servicios"

Parámetros:

* self
* boton
* ventana: la ventana actual para poder cerrarla


Gestion.py
**********
class VentanaServicios()
------------------------
Clase donde se creará la ventana de Gestión de clientes con los componentes y variables necesarios.

def on_btnInformeGestion_clicked(self, boton, dni):
---------------------------------------------------
Función que controla el comportamiento del botón "btnInformeGestion".
Una vez pulsado el botón, se buscará en la base de datos el cliente correspondiente a partir del dni indicado y
se creará un informe con su información usando ReportLab.

Parámetros:

* self
* boton
* dni: el dni del cliente deseado

def on_btnVolver1_clicked(self, boton, ventana):
------------------------------------------------
Función que controla el comportamiento del botón "btnVolver1"
Una vez pulsado el botón, se cerrará la ventana actual y se abrirá la del menú principal anterior.

Parámetros:

* self
* boton
* ventana: la ventana a cerrar

def on_btnNovo_clicked(self, boton, modelo, combo):
---------------------------------------------------
Función que controla el comportamiento del botón "btnNovo"
Añade a la base de datos el cliente especificado por el usuario en las celdas de texto con todos sus datos, además
también lo añade al TreeView para que se pueda visualizar por pantalla.

Parámetros:

* self
* boton
* modelo: el modelo del TreeView
* combo: el dato seleccionado en el comboBox del campo "servicio"

def on_btnBorrar_clicked(self, boton, modelo):
----------------------------------------------
Función que controla el comportamiento del botón "btnBorrar"
Borra de la base de datos el cliente especificado por el usuario y también del TreeView.

Parámetros:

* self
* boton
* modelo: el modelo del TreeView

def on_btnBuscar_clicked(self, boton, combo, modelo):
-----------------------------------------------------
Función que controla el comportamiento del botón "btnBuscar"
Busca en la base de datos el cliente o clientes especificados por el usuario y los enseña en el TreeView

Parámetros:

* self
* boton
* combo: el dato seleccionado en el comboBox "campo"
* modelo: el modelo del TreeView

def on_btnTodos_clicked(self, boton, modelo):
---------------------------------------------
Función que controla el comportamiento del botón "btnTodos"
Busca en la base de datos todos los clientes y los muestra en el TreeView

Parámetros:

* self
* boton
* modelo: el modelo del TreeView

def clientes(self, modelo, punteiro, a):
----------------------------------------
Función que permite mostrar todos los elementos en el TreeView correctamente

Parámetros:

* self
* modelo: el modelo del TreeView
* punteiro
* a


Servicios.py
************
class VentanaServicios(Gtk.Window)
----------------------------------
Clase donde se creará la ventana de "Servicios" usando las variables y componentes necesarios

def on_btnVolver2_clicked(self, boton, ventana)
-----------------------------------------------
Función que controla el comportamiento del botón "btnVolver2"
Oculta la ventana actual y vuelve a mostrar la ventana "Principal"

Parámetros:

* self
* boton
* ventana: la ventana a cerrar

def on_btnInforme_clicked(self, boton)
--------------------------------------
Función que controla el comportamiento del botón "btnInforme"
Genera un informe general sobre cuantos clientes hay registrados en cada servicio usando ReportLab









