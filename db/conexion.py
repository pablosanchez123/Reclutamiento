import psycopg2


def get_connection():
    return psycopg2.connect(
        host="13.220.111.18",
        port=5432,
        dbname="reclutamiento_db",
        user="pablo",
        password="todo123pato"
    )

def probar_conexion():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(" Conectado a PostgreSQL:", version[0])
        cur.close()
        conn.close()
    except Exception as e:
        print(" Error conectando:", e)





