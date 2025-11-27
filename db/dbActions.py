import psycopg2
from db.conexion import get_connection

def insertar_cv(nombre_persona, nombre_archivo, texto_cv):
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
            INSERT INTO cvs (nombre_persona, nombre_archivo, texto_cv)
            VALUES (%s, %s, %s);
        """

        cur.execute(query, (nombre_persona, nombre_archivo, texto_cv))
        conn.commit()

    except Exception as e:
        print(" Error insertando CV:", e)

    finally:
        if cur: cur.close()
        if conn: conn.close()

def contar_cvs():
    """Devuelve cuántos registros hay en la tabla cvs."""
    total = 0
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM cvs;")
        total = cur.fetchone()[0]
        cur.close()
        conn.close()
    except Exception as e:
        print(" Error contando CVs:", e)

    return total