from db import get_conn

class IncidenteDAO:

    @staticmethod
    def create(data):
        conn = get_conn()
        conn.execute("""
        INSERT INTO incidentes(
        descripcion,latitud,longitud,estado,fecha,usuario_id
        ) VALUES(?,?,?,?,?,?)
        """, data)
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_conn()
        data = conn.execute(
            "SELECT * FROM incidentes ORDER BY id DESC"
        ).fetchall()
        conn.close()
        return data