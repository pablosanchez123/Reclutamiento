import os
import shutil
import atexit
from utils.helpers import extraer_texto_pdf
from core.candidato_service import guardar_candidato
from core.candidato import Candidato
from ui.ventanasApps.HabilidadesReclutador import HabilidadesReclutador
from db.dbActions import contar_cvs
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QLineEdit
)
from PySide6.QtCore import Qt

class CargarCandidatos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cargar Candidatos")
        self.setFixedSize(600, 450)
        self.setStyleSheet("background-color: #121212; color: white;")

        self.archivos_cargados = 0
        self.ruta_archivo = ""
        self.nombre_persona = ""

        # Título
        self.titulo = QLabel("Cargar Candidatos")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 22pt; font-weight: bold; margin-bottom: 20px;")

        # --- Campo para nombre del candidato ---
        self.lbl_nombre = QLabel("Nombre del candidato:")
        self.lbl_nombre.setAlignment(Qt.AlignLeft)
        self.lbl_nombre.setStyleSheet("font-size: 12pt;")

        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Ejemplo: Juan Pérez")
        self.txt_nombre.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                padding: 8px;
                font-size: 12pt;
                border-radius: 6px;
            }
        """)

        # Botón seleccionar archivo
        self.btn_seleccionar = QPushButton("Seleccionar Archivo")
        self.btn_seleccionar.setFixedWidth(250)
        self.btn_seleccionar.setStyleSheet(self._estilo_boton())
        self.btn_seleccionar.clicked.connect(self.seleccionar_archivo)

        # Botón procesar
        self.btn_procesar = QPushButton("Procesar Resultados")
        self.btn_procesar.setFixedWidth(250)
        self.btn_procesar.setStyleSheet(self._estilo_boton())
        self.btn_procesar.clicked.connect(self.configurar_habilidades)

        # Texto de resultado
        self.lbl_resultado = QLabel("")
        self.lbl_resultado.setAlignment(Qt.AlignCenter)
        self.lbl_resultado.setStyleSheet("color: #cccccc; font-size: 12pt;")

        # Etiqueta de archivos cargados
        self.lbl_cargados = QLabel("Archivos cargados: 0")
        self.lbl_cargados.setStyleSheet("font-size: 10pt;")

        # Botón volver
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setFixedSize(100, 32)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #a60606;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #c11c1c;
            }
        """)
        self.btn_volver.clicked.connect(self.volver_menu_principal)

        # Layout principal
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        layout.addWidget(self.titulo)
        layout.addWidget(self.lbl_nombre)
        layout.addWidget(self.txt_nombre)
        layout.addWidget(self.btn_seleccionar, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_procesar, alignment=Qt.AlignCenter)
        layout.addWidget(self.lbl_resultado)
        layout.addWidget(self.lbl_cargados)

        # Espaciador mas botón volver
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_volver)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        self.actualizar_conteo_cvs()

    def volver_menu_principal(self):
        self.hide()

    def configurar_habilidades(self):
        self.ventana_habilidades = HabilidadesReclutador()
        self.ventana_habilidades.show()

    def actualizar_conteo_cvs(self):
        """Consulta la BD y actualiza el label de archivos cargados."""
        try:
            total = contar_cvs()
            self.archivos_cargados = total
            self.lbl_cargados.setText(f"Archivos cargados: {total}")
        except Exception as e:
            print("Error obteniendo conteo de CVs:", e)
            self.lbl_cargados.setText("Archivos cargados: ?")



    def _estilo_boton(self):
        return """
            QPushButton {
                background-color: #000000;
                color: white;
                font-size: 12pt;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """

    def seleccionar_archivo(self):
        # Lee el nombre del candidato antes de abrir archivo
        self.nombre_persona = self.txt_nombre.text().strip()
        #Si no se ha escrito el nombre no deja seleccionar el archivo
        if not self.nombre_persona:
            self.lbl_resultado.setText("⚠ Ingresa el nombre del candidato antes de seleccionar el archivo.")
            return

        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Archivo",
            os.getcwd(),
            "Archivos PDF (*.pdf)"
        )

        #Si el archivo es null termina la funcion
        if not archivo:
            return

        # Copia el archvio pdf a una carpeta interna en el proyecto donde almacena temporalmenmte para leerlo e ingresarlo a la BD
        if archivo:
            try:
                destinos_dir = "data/cvs/"
                os.makedirs(destinos_dir, exist_ok=True)
                nombre = os.path.basename(archivo)
                destino = os.path.join(destinos_dir, nombre)
                shutil.copy(archivo, destino)
                self.ruta_archivo = destino
                # Llama al metodo que extrae el texto "crudo" del archivo
                texto_cv = extraer_texto_pdf(self.ruta_archivo)
                if not texto_cv.strip():
                    self.lbl_resultado.setText(
                        "⚠ No se pudo extraer texto del PDF. ¿Es un PDF escaneado solo con imágenes?"
                    )
                    return
                #Arma un objeto candidato con la informacion del archivo, el nombre anteriormente  ingresado y la ruta del archivo
                candidato = Candidato(
                    nombre_persona=self.nombre_persona,
                    nombre_archivo=self.ruta_archivo,
                    texto_cv=texto_cv
                )
                #Guarda el candidato en la BD
                guardar_candidato(candidato)


                # Se guarda la ruta final dentro de data/cvs/
                self.ruta_archivo = destino
                self.archivos_cargados += 1
                self.lbl_cargados.setText(f"Archivos cargados: {self.archivos_cargados}")
                self.lbl_resultado.setText(
                    f"📄 Archivo seleccionado para: {self.nombre_persona}\n{os.path.basename(archivo)}"
                )

                # Limpia el campo de nombre después de subir el archivo
                self.txt_nombre.clear()
                self.nombre_persona = ""

            except Exception as e:
                print("Error al procesar e insertar el CV",e)
                self.lbl_resultado.setText(" Ocurrió un error al guardar el CV en la base de datos.")







