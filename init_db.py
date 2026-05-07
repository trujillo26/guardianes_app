from db import get_conn
from werkzeug.security import generate_password_hash

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        correo TEXT UNIQUE,
        password TEXT,
        rol TEXT DEFAULT 'usuario'
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS incidentes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT,
        latitud REAL,
        longitud REAL,
        estado TEXT,
        fecha TEXT,
        usuario_id INTEGER
    )
    """)

    # Tabla para publicaciones del dashboard (texto libre desde Principal.html)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS publicaciones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        fecha TEXT NOT NULL,
        usuario_id INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)

    # Tabla para el formulario detallado (nombre, cedula, direccion, imagen)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reportes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cedula TEXT NOT NULL,
        direccion TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        imagen TEXT,
        fecha TEXT NOT NULL,
        estado TEXT DEFAULT 'Pendiente',
        usuario_id INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)

    admin = cur.execute(
        "SELECT * FROM usuarios WHERE correo=?",
        ("admin@admin.com",)
    ).fetchone()

    if not admin:
        cur.execute("""
        INSERT INTO usuarios(nombre,correo,password,rol)
        VALUES(?,?,?,?)
        """, (
            "Admin",
            "admin@admin.com",
            generate_password_hash("1234"),
            "admin"
        ))

    conn.commit()
    conn.close()
