class PublicacionDTO:
    """
    DTO para transferir datos de una publicacion del dashboard.
    """
    def __init__(self, descripcion, usuario_id):
        self.descripcion = descripcion
        self.usuario_id = usuario_id

    @staticmethod
    def from_form(form, usuario_id):
        """Construye un PublicacionDTO desde request.form."""
        return PublicacionDTO(
            descripcion=form.get("descripcion", "").strip(),
            usuario_id=usuario_id
        )

    @staticmethod
    def from_row(row):
        """Construye un PublicacionDTO desde un sqlite3.Row para lectura."""
        return PublicacionDTO(
            descripcion=row["descripcion"],
            usuario_id=row["usuario_id"]
        )

    def to_dict(self):
        return {
            "descripcion": self.descripcion,
            "usuario_id": self.usuario_id
        }
