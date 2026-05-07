from db import get_conn

class ReporteDAO:

    @staticmethod
    def create(data):
        conn = get_conn()
        conn.execute("""
        INSERT INTO reportes(nombre, cedula, direccion, descripcion, imagen, fecha, estado, usuario_id)
        VALUES(?,?,?,?,?,?,?,?)
        """, data)
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_conn()
        data = conn.execute(
            "SELECT * FROM reportes ORDER BY id DESC"
        ).fetchall()
        conn.close()
        return data

    @staticmethod
    def get_by_id(reporte_id):
        conn = get_conn()
        row = conn.execute(
            "SELECT * FROM reportes WHERE id=?", (reporte_id,)
        ).fetchone()
        conn.close()
        return row
