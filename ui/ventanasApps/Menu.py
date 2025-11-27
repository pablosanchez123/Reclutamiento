import sys
import os
from ui.ventanasApps.CargarCandidatos import CargarCandidatos
from ui.ventanasApps.VerResultados import VerResultados
from utils.helpers import limpiarDatos
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
)
from PySide6.QtCore import Qt

RUTA_JSON = "data/config/habilidades_reclutador.json"


class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.ventana_candidatos = CargarCandidatos()
        self.resultados = VerResultados()

        self.setWindowTitle("Menú Principal")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        self.titulo = QLabel("Simulador de Reclutamiento")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("""
            font-size: 20pt;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 30px;
        """)

        # Botones
        self.btn_cargar = QPushButton("Cargar Candidatos")
        self.btn_resultados = QPushButton("Ver Resultados")
        self.btn_reiniciar = QPushButton("Reiniciar Prueba")
        self.btn_salir = QPushButton("Salir")

        boton_estilo = """
            QPushButton {
                background-color: #000000;
                color: white;
                font-size: 14pt;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #222222;
            }
        """

        for boton in [self.btn_cargar, self.btn_reiniciar, self.btn_salir,self.btn_resultados]:
            boton.setFixedWidth(250)
            boton.setStyleSheet(boton_estilo)



        # Conexiones
        self.btn_cargar.clicked.connect(self.cargar_candidatos)
        self.btn_resultados.clicked.connect(self.ver_resultados)
        self.btn_reiniciar.clicked.connect(self.reiniciar_prueba)
        self.btn_salir.clicked.connect(self.close)

        # Agregar al layout
        layout.addWidget(self.titulo)
        layout.addWidget(self.btn_cargar, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_resultados, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_reiniciar, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_salir, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        #Desactivar botón si no existe el JSON

        self.verificar_habilidades()

    def verificar_habilidades(self):
        #Revisa si existe el JSON, si no desactiva le botón
        if os.path.exists(RUTA_JSON):
            self.btn_resultados.setEnabled(True)
            self.btn_resultados.setStyleSheet("""
                QPushButton {
                    background-color: #000000;
                    color: white;
                    font-size: 14pt;
                    padding: 10px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #222222;
                }
            """)
        else:
            self.btn_resultados.setEnabled(False)
            self.btn_resultados.setStyleSheet("""
                QPushButton {
                    background-color: #3a3a3a;
                    color: #777777;
                    font-size: 14pt;
                    padding: 10px;
                    border-radius: 8px;
                }
            """)

    def cargar_candidatos(self):
        self.ventana_candidatos.show()


    def ver_resultados(self):
        # Revisa nuevamente en caso de haber cambiado el JSON
        self.verificar_habilidades()

        if not os.path.exists(RUTA_JSON):
            QMessageBox.warning(self, "Faltan datos",
                                "Primero debe configurar las habilidades del reclutador.")
            return

        self.resultados.show()


    def reiniciar_prueba(self):
        respuesta = QMessageBox.question(
            #Despliega una ventana que asegura el programa que si quiere borrar toda la informacion
            self,
            "Reiniciar prueba",
            "¿Estás seguro de que deseas borrar TODOS los CVs, JSON y datos guardados?\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            #Si la respuesta es si borra toda la información disponible en el programa
            try:
                limpiarDatos()
                QMessageBox.information(self, "Reiniciado", "El sistema ha sido reiniciado correctamente.")
                self.verificar_habilidades()  # vuelve a verificar para deshabilitar el boton si es necesario
            except Exception as e:
                print("Error al reiniciar datos:", e)
                QMessageBox.critical(self, "Error", "Ocurrió un error al intentar reiniciar los datos.")
