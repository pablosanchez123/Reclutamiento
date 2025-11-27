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
