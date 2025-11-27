import os
import json
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QComboBox, QListWidget, QListWidgetItem, QMessageBox, QLineEdit
)
from PySide6.QtCore import Qt

RUTA_CONFIG = os.path.abspath("data/config")
RUTA_HABILIDADES = os.path.join(RUTA_CONFIG, "habilidades_reclutador.json")


class HabilidadesReclutador(QWidget):
    # Crea la ventana para que el reclutador ingrese las palabras clave que se van a revisar contra los cvs

    def __init__(self):
        super().__init__()

        #Titulo de la pestaña
        self.setWindowTitle("Habilidades deseadas por el reclutador")
        self.setFixedSize(650, 500)
        self.setStyleSheet("background-color: #121212; color: white;")

        os.makedirs(RUTA_CONFIG, exist_ok=True)


        self.lbl_titulo = QLabel("Configurar habilidades deseadas")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setStyleSheet("""
            font-size: 20pt;
            font-weight: bold;
            margin-bottom: 10px;
        """)

        self.lbl_desc = QLabel(
            "Agrega las habilidades que deseas que tenga el candidato.\n"
            "Luego el modelo revisará los CVs y los calificará del 1 al 10 según estas preferencias."
        )
        self.lbl_desc.setAlignment(Qt.AlignCenter)
        self.lbl_desc.setStyleSheet("font-size: 10pt; color: #cccccc;")

        # Entrada de nueva habilidad
        self.txt_habilidad = QLineEdit()
        self.txt_habilidad.setPlaceholderText("Ej: Python, Liderazgo, Análisis de datos...")

        self.cmb_importancia = QComboBox()
        self.cmb_importancia.addItems(["Baja", "Media", "Alta"])

        self.btn_agregar = QPushButton("Agregar habilidad")
        self.btn_agregar.setStyleSheet(self._estilo_boton())
        self.btn_agregar.clicked.connect(self.agregar_habilidad)

        fila_agregar = QHBoxLayout()
        fila_agregar.addWidget(self.txt_habilidad)
        fila_agregar.addWidget(self.cmb_importancia)
        fila_agregar.addWidget(self.btn_agregar)

        #Lista de habilidades agregadas
        self.lista_habilidades = QListWidget()
        self.lista_habilidades.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                border-radius: 6px;
            }
        """)

        # Botón para eliminar habilidad seleccionada
        self.btn_eliminar = QPushButton("Eliminar seleccionada")
        self.btn_eliminar.setStyleSheet(self._estilo_boton_rojo())
        self.btn_eliminar.clicked.connect(self.eliminar_habilidad)

        # Botones inferiores
        self.btn_guardar = QPushButton("Guardar preferencias")
        self.btn_guardar.setStyleSheet(self._estilo_boton())
        self.btn_guardar.clicked.connect(self.guardar_habilidades)

        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.setStyleSheet(self._estilo_boton_rojo())
        self.btn_cerrar.clicked.connect(self.close)

        fila_botones = QHBoxLayout()
        fila_botones.addStretch()
        fila_botones.addWidget(self.btn_guardar)
        fila_botones.addWidget(self.btn_cerrar)


        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(15)
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.lbl_desc)
        layout.addLayout(fila_agregar)
        layout.addWidget(self.lista_habilidades)
        layout.addWidget(self.btn_eliminar, alignment=Qt.AlignRight)
        layout.addLayout(fila_botones)

        self.setLayout(layout)

        # Carga habilidades previas si existen
        self.cargar_habilidades_guardadas()


    def _estilo_boton(self):
        return """
            QPushButton {
                background-color: #000000;
                color: white;
                font-size: 11pt;
                padding: 8px 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """

    def _estilo_boton_rojo(self):
        return """
            QPushButton {
                background-color: #a60606;
                color: white;
                font-size: 11pt;
                padding: 8px 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #c11c1c;
            }
        """

    def agregar_habilidad(self):
        texto = self.txt_habilidad.text().strip()
        importancia = self.cmb_importancia.currentText()

        #Revisa si el texto es nulo por si el campo esta vacio
        if not texto:
            QMessageBox.warning(self, "Campo vacío", "Escribe una habilidad antes de agregarla.")
            return

        #Las palabras o frases clave tienen un nivel de importancia, si la importancia es alta el modelo le da mas puntaje al cv si coincide
        item_text = f"{texto}  |  Importancia: {importancia}"
        self.lista_habilidades.addItem(QListWidgetItem(item_text))

        self.txt_habilidad.clear()
        self.txt_habilidad.setFocus()

    def eliminar_habilidad(self):
        item = self.lista_habilidades.currentItem()
        if not item:
            QMessageBox.information(self, "Sin selección", "Selecciona una habilidad para eliminar.")
            return
        fila = self.lista_habilidades.row(item)
        self.lista_habilidades.takeItem(fila)

    def guardar_habilidades(self):
        habilidades = []

        for i in range(self.lista_habilidades.count()):
            item = self.lista_habilidades.item(i).text()
            # Formato: "Python  |  Importancia: Alta"
            partes = item.split("|")
            habilidad = partes[0].strip()
            importancia = partes[1].replace("Importancia:", "").strip() if len(partes) > 1 else "Media"

            habilidades.append({
                "habilidad": habilidad,
                "importancia": importancia
            })

        try:
            with open(RUTA_HABILIDADES, "w", encoding="utf-8") as f:
                json.dump(habilidades, f, ensure_ascii=False, indent=4)

            QMessageBox.information(self, "Guardado",
                                    "Las habilidades del reclutador se han guardado correctamente.\n"
                                    "Tu modelo de ML puede leer este archivo JSON para calificar los CVs.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron guardar las habilidades:\n{e}")

    def cargar_habilidades_guardadas(self):
        if not os.path.exists(RUTA_HABILIDADES):
            return

        try:
            with open(RUTA_HABILIDADES, "r", encoding="utf-8") as f:
                habilidades = json.load(f)

            for h in habilidades:
                habilidad = h.get("habilidad", "")
                importancia = h.get("importancia", "Media")
                texto = f"{habilidad}  |  Importancia: {importancia}"
                self.lista_habilidades.addItem(QListWidgetItem(texto))

        except Exception as e:
            print("Error cargando habilidades guardadas:", e)
