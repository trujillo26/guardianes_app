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
    
    @staticmethod
    def get_reportes_todos(estado=None):
        conn = get_conn()
        if estado and estado != "todos":
            data = conn.execute(
                "SELECT * FROM reportes WHERE estado = ? ORDER BY id DESC", (estado,)
            ).fetchall()
        else:
            data = conn.execute(
                "SELECT * FROM reportes ORDER BY id DESC"
            ).fetchall()
        conn.close()
        return data
    
    @staticmethod
    def get_reportes_aprobados():
        conn = get_conn()
        data = conn.execute(
            "SELECT * FROM reportes WHERE estado = 'Aprobado' ORDER BY id DESC"
        ).fetchall()
        conn.close()
        return data
    @staticmethod 
    def contar_por_estado():
        conn = get_conn()
        rows = conn.execute(""" SELECT estado, COUNT(*) as total FROM reportes GROUP BY estado """).fetchall()
        conn.close()
        conteo = {"Pendiente": 0, "Aprobados": 0, "Rechazados": 0, "total": 0}
        for row in rows:
            conteo[row["estado"]] = row["total"]
            conteo["total"] += row["total"]
        return conteo
    @staticmethod 
    def cambiar_estado(reporte_id, nuevo_estado):
        conn = get_conn()
        conn.execute("""
        UPDATE reportes SET estado = ? WHERE id = ?
        """, (nuevo_estado, reporte_id))
        conn.commit()
        conn.close()