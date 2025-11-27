import sys
from PySide6.QtWidgets import QApplication
from ui.ventanasApps.Menu import MenuPrincipal


def iniciar_aplicacion():
    #Inicia la aplicacion de PySide6
    app = QApplication(sys.argv)
    #Muestra inicialmente el menu principal
    ventana_menu = MenuPrincipal()
    ventana_menu.show()

    sys.exit(app.exec())

