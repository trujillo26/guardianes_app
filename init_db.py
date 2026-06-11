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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS publicaciones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        fecha TEXT NOT NULL,
        usuario_id INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)

    # Tabla principal de reportes (formulario detallado + ubicación)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reportes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cedula TEXT NOT NULL,
        direccion TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        imagen TEXT,
        latitud REAL,
        longitud REAL,
        fecha TEXT NOT NULL,
        estado TEXT DEFAULT 'Pendiente',
        usuario_id INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """)

    # Migración suave: si la tabla reportes ya existía sin lat/lng, agregarlas
    cols = [c["name"] for c in cur.execute("PRAGMA table_info(reportes)").fetchall()]
    if "latitud" not in cols:
        cur.execute("ALTER TABLE reportes ADD COLUMN latitud REAL")
    if "longitud" not in cols:
        cur.execute("ALTER TABLE reportes ADD COLUMN longitud REAL")

    # Crear admin por defecto si no existe
    admin = cur.execute(
        "SELECT * FROM usuarios WHERE correo=?",
        ("admin@admin.com",)
    ).fetchone()

    if not admin:
        cur.execute("""
        INSERT INTO usuarios(nombre, correo, password, rol)
        VALUES(?,?,?,?)
        """, (
            "Admin",
            "admin@admin.com",
            generate_password_hash("1234"),
            "admin"
        ))

    conn.commit()
    conn.close()