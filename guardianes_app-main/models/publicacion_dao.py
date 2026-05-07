from db import get_conn

class PublicacionDAO:

    @staticmethod
    def create(data):
        conn = get_conn()
        conn.execute("""
        INSERT INTO publicaciones(descripcion, fecha, usuario_id)
        VALUES(?,?,?)
        """, data)
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_conn()
        data = conn.execute(
            "SELECT * FROM publicaciones ORDER BY id DESC"
        ).fetchall()
        conn.close()
        return data
