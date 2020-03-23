from setuptools import setup,find_packages

descripcion_larga = open('Readme.rst').read()

setup(
    name = "ProyectoEV2",
    version = "0.12",
    author = "Luis",
    author_email = "lvaqueiroperez@danielcastelao.org",
    url = "https://www.danielcastelao.org",
    license = "GLP",
    platforms = "Unix",
    clasifiers = ["Development Status :: 3 - Alpha",
                  "Environment :: Console",
                  "Topic :: Software Development :: Libraries",
                  "License :: OSI Aproved :: GNU General Public License",
                  "Programming Language :: Python :: 3.4",
                  "Operating System :: Linux Ubuntu"
                  ],
    description = "Aplicación para el Proyecto de la EV2",
    long_description = descripcion_larga,
    keywords = "empaquetado instalador paquetes",
    # PARA AÑADIR ARCHIVOS QUE NO SON DE CÓDIGO: (ver manifest)
    include_package_data=True,
    packages = ['ventanas','Documentacion'],#OTRA FORMA: packages = find_packages(exclude= ['*.test','*.test.*']) podemo excluír lo que queramos
    package_data = {
        'ventanas' : 'notas.txt'
    },
    entry_points = {'console_scripts': ['Principal = ventanas.Principal: main',],}

)