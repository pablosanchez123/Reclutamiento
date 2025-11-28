import os
import json
import pandas as pd
from langdetect import detect
from deep_translator import GoogleTranslator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from db.conexion import get_connection

RUTA_HABILIDADES = "data/config/habilidades_reclutador.json"

# Dos funciones de utilidad para el sistema

def detectar_idioma(texto: str) -> str:

    try:
        idioma = detect(texto)
        if idioma.startswith("en"):
            return "en"
        return "es"
    except:
        return "es"     # fallback: español


def traducir(texto: str, destino: str) -> str:

    try:
        return GoogleTranslator(source="auto", target=destino).translate(texto)
    except:
        return texto   # fallback: deja como está



# Funciones de carga de datos

def cargar_cvs_desde_db():
    conn = get_connection()
    df = pd.read_sql("SELECT nombre_persona, nombre_archivo, texto_cv FROM cvs", conn)
    conn.close()
    return df


def cargar_habilidades():

    with open(RUTA_HABILIDADES, "r", encoding="utf-8") as f:
        habilidades = json.load(f)

    palabras = []
    for h in habilidades:
        palabra = h["habilidad"]
        importancia = h["importancia"].lower()

        rep = 3 if importancia == "alta" else 2 if importancia == "media" else 1
        palabras.extend([palabra] * rep)

    return " ".join(palabras)


#Modelo de rankeo

def ranking_candidatos():
    df = cargar_cvs_desde_db()
    texto_habilidades_es = cargar_habilidades()

    resultados = []

    for idx, row in df.iterrows():
        cv_texto = row["texto_cv"].lower()

        # Detecta idioma
        idioma = detectar_idioma(cv_texto)

        # Prepara habilidades en el idioma correcto
        if idioma == "en":
            texto_habilidades = traducir(texto_habilidades_es, "en").lower()
        else:
            texto_habilidades = texto_habilidades_es.lower()

        # Vectorización
        corpus = [cv_texto, texto_habilidades]
        vectorizer = TfidfVectorizer()
        vectores = vectorizer.fit_transform(corpus)

        cv_vec = vectores[0]
        hab_vec = vectores[1]

        sim = float(cosine_similarity(cv_vec, hab_vec)[0][0])

        resultados.append({
            "nombre_persona": row["nombre_persona"],
            "nombre_archivo": row["nombre_archivo"],
            "similitud_raw": sim,
            "idioma": idioma
        })

    df_out = pd.DataFrame(resultados)

    # Ordena por similitud descendente
    df_out = df_out.sort_values(by="similitud_raw", ascending=False).reset_index(drop=True)

    return df_out
