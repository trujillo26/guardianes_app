from db import get_conn

class UserDAO:

    @staticmethod
    def find_by_email(correo):
        conn = get_conn()
        user = conn.execute(
            "SELECT * FROM usuarios WHERE correo=?",
            (correo,)
        ).fetchone()
        conn.close()
        return user

    @staticmethod
    def create(nombre, correo, password):
        conn = get_conn()
        conn.execute(
            "INSERT INTO usuarios(nombre,correo,password) VALUES(?,?,?)",
            (nombre, correo, password)
        )
        conn.commit()
        conn.close()