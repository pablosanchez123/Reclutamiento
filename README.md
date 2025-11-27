# 🧠 Simulador de Reclutamiento con Inteligencia Artificial

Este proyecto es un sistema de escritorio desarrollado en Python que simula el proceso de reclutamiento de personal mediante inteligencia artificial. Evalúa automáticamente candidatos a partir de datos como currículums y respuestas a entrevistas, utilizando un modelo de Machine Learning entrenado previamente.

---

## 🚀 Funcionalidades

- 📄 Carga y análisis de CVs de forma automática.
- 🤖 Clasificación de candidatos según perfil profesional y compatibilidad.
- 🧠 Integración con modelos de ML para vectorizar y encontrar similitudes.
- 🖥 Interfaz gráfica de escritorio con PySide6.
- 📊 Generación de reportes de resultados y exportación en CSV.
- ☁️ Carga datos directamente en una base de datos en la nube
- 🗃  Almacenamiento de resultados en PostgeSQL mediante una maquina virtual de EC2 en AWS .

---

## 📁 Estructura del Proyecto

## 📁 Estructura del Proyecto

```
Reclutamiento/
├── 🧠 core/
│   ├── candidato.py
│   └── candidato_service.py
│
├── 📂 data/
│   ├── config/ → JSON con habilidades del reclutador
│   └── cvs/    → CVs almacenados localmente
│
├── 🗄️ db/
│   ├── conexion.py
│   └── dbActions.py
│
├── 🤖 ml/
│   └── ranking.py
│
├── 🖥️ ui/
│   ├── estilos.py
│   ├── ventanas.py
│   └── ventanasApps/
│       ├── Menu.py
│       ├── CargarCandidatos.py
│       ├── HabilidadesReclutador.py
│       └── VerResultados.py
│
├── 🔧 utils/
│   └── helpers.py
│   
├── main.py
├── README.md
└── requirements.txt
```



---

## ⚙️ Tecnologías Utilizadas

- Python 3.11
- PySide6 (interfaz gráfica)
- Scikit-learn (modelo ML)
- Pandas (manejo de datos)
- Joblib (cargar/guardar modelos)
- PostreSQL (base de datos en la nube)
- Máquina virtual de EC2 en AWS

---

## 🧪 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tuusuario/simulador_reclutamiento.git
cd simulador_reclutamiento
