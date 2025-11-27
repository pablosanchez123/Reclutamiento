# ui/ventanasApps/VerResultados.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PySide6.QtCore import Qt

from ml.ranking import ranking_candidatos  # usamos el modelo multi-idioma


class VerResultados(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resultados de Candidatos")
        self.setFixedSize(900, 500)
        self.setStyleSheet("background-color: #121212; color: white;")

        # ------- Título -------
        self.titulo = QLabel("Ranking de Candidatos")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("""
            font-size: 20pt;
            font-weight: bold;
            margin-bottom: 10px;
        """)

        # ------- Etiqueta de estado / mensajes -------
        self.lbl_estado = QLabel("")
        self.lbl_estado.setAlignment(Qt.AlignCenter)
        self.lbl_estado.setStyleSheet("font-size: 10pt; color: #cccccc; margin-bottom: 5px;")

        # ------- Tabla de resultados -------
        self.tabla = QTableWidget()
        # Posición, Nombre, Archivo, Puntaje, Similitud raw, Idioma
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "Posición",
            "Nombre",
            "Archivo",
            "Similitud (%) raw",
            "Idioma CV"
        ])

        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla.setStyleSheet("""
            QHeaderView::section {
                background-color: #1e1e1e;
                color: white;
                padding: 4px;
                border: 1px solid #333333;
            }
            QTableWidget {
                gridline-color: #333333;
                font-size: 10pt;
            }
        """)

        # ------- Botones -------
        self.btn_refrescar = QPushButton("Refrescar")
        self.btn_refrescar.setFixedWidth(140)
        self.btn_refrescar.setStyleSheet(self._estilo_boton())
        self.btn_refrescar.clicked.connect(self.cargar_resultados)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setFixedWidth(140)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #a60606;
                color: white;
                font-weight: bold;
                font-size: 11pt;
                padding: 8px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c11c1c;
            }
        """)
        self.btn_volver.clicked.connect(self.close)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(self.btn_refrescar)
        layout_botones.addWidget(self.btn_volver)

        # ------- Layout principal -------
        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(10)
        layout_principal.addWidget(self.titulo)
        layout_principal.addWidget(self.lbl_estado)
        layout_principal.addWidget(self.tabla)
        layout_principal.addLayout(layout_botones)

        self.setLayout(layout_principal)

        # Cargar datos al abrir
        self.cargar_resultados()

    def _estilo_boton(self):
        return """
            QPushButton {
                background-color: #000000;
                color: white;
                font-size: 11pt;
                padding: 8px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """

    def cargar_resultados(self):
        try:
            df = ranking_candidatos()
        except Exception as e:
            self.tabla.setRowCount(0)
            self.lbl_estado.setText(f"❌ Error generando resultados: {e}")
            return

        if df.empty:
            self.tabla.setRowCount(0)
            self.lbl_estado.setText("⚠ No hay resultados que mostrar (no hay CVs o habilidades).")
            return

        self.tabla.setRowCount(len(df))

        for fila, row in df.iterrows():
            item_pos = QTableWidgetItem(str(fila + 1))
            item_pos.setTextAlignment(Qt.AlignCenter)

            item_nombre = QTableWidgetItem(str(row["nombre_persona"]))
            item_archivo = QTableWidgetItem(str(row["nombre_archivo"]))

            sim_raw = float(row["similitud_raw"])
            item_sim = QTableWidgetItem(f"{sim_raw * 100:.2f} %")
            item_sim.setTextAlignment(Qt.AlignCenter)

            idioma = row["idioma"]
            idioma_legible = "Español" if idioma == "es" else "Inglés"
            item_idioma = QTableWidgetItem(idioma_legible)
            item_idioma.setTextAlignment(Qt.AlignCenter)

            self.tabla.setItem(fila, 0, item_pos)
            self.tabla.setItem(fila, 1, item_nombre)
            self.tabla.setItem(fila, 2, item_archivo)
            self.tabla.setItem(fila, 3, item_sim)
            self.tabla.setItem(fila, 4, item_idioma)

        self.lbl_estado.setText("✅ Resultados actualizados correctamente.")

