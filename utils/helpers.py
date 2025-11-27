import shutil
import os
import fitz
from db.conexion import get_connection

def copiar_archivo(origen, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy2(origen, destino)
    return destino

def limpiar_cvs():
        ruta = os.path.abspath("data/cvs")
        try:
          for nombre in os.listdir(ruta):
            archivo = os.path.join(ruta, nombre)
            if os.path.isfile(archivo):
                os.remove(archivo)
        except Exception as e:
         print("Error limpiando cvs:", e)

def limpiarJSON():
        ruta = os.path.abspath("data/config")
        try:
            for nombre in os.listdir(ruta):
                archivo = os.path.join(ruta, nombre)
                # Elimina solo archivos .json
                if os.path.isfile(archivo) and nombre.lower().endswith(".json"):
                    os.remove(archivo)
        except Exception as e:
            print("Error limpiando archivos JSON:", e)


def limpiar_tabla_cvs():
    #Borra todos los registros de la base de datos
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM cvs;")
        conn.commit()
        cur.close()
        conn.close()
        print(" Tabla 'cvs' limpiada correctamente.")
    except Exception as e:
        print(" Error limpiando tabla cvs:", e)



def extraer_texto_pdf(ruta_pdf: str) -> str:

    texto_final = []

    try:
        with fitz.open(ruta_pdf) as pdf:
            for pagina in pdf:
                texto_pag = pagina.get_text() or ""
                texto_final.append(texto_pag)

        return "\n".join(texto_final)

    except Exception as e:
        print(f" Error leyendo PDF {ruta_pdf}: {e}")
        return ""

def limpiarDatos():
    limpiar_cvs()
    limpiar_tabla_cvs()
    limpiarJSON()
    print("Datos totalmente eliminados")
