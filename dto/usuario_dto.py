class UsuarioDTO:
    """
    DTO para transferir datos de usuario entre capas.
    Evita exponer el objeto Row de SQLite o datos sensibles (password).
    """
    def __init__(self, id, nombre, correo, rol):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.rol = rol

    @staticmethod
    def from_row(row):
        """Construye un UsuarioDTO a partir de un sqlite3.Row."""
        return UsuarioDTO(
            id=row["id"],
            nombre=row["nombre"],
            correo=row["correo"],
            rol=row["rol"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol
        }
