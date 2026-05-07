class ReporteDTO:
    """
    DTO para transferir datos del formulario detallado entre capas.
    Encapsula todos los campos del reporte incluyendo la imagen.
    """
    def __init__(self, nombre, cedula, direccion, descripcion, imagen_file, usuario_id):
        self.nombre = nombre
        self.cedula = cedula
        self.direccion = direccion
        self.descripcion = descripcion
        self.imagen_file = imagen_file  # objeto FileStorage de Flask (puede ser None)
        self.usuario_id = usuario_id

    @staticmethod
    def from_form(form, files, usuario_id):
        """Construye un ReporteDTO desde request.form y request.files."""
        return ReporteDTO(
            nombre=form.get("nombre", "").strip(),
            cedula=form.get("cedula", "").strip(),
            direccion=form.get("direccion", "").strip(),
            descripcion=form.get("descripcion", "").strip(),
            imagen_file=files.get("imagen"),
            usuario_id=usuario_id
        )

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "cedula": self.cedula,
            "direccion": self.direccion,
            "descripcion": self.descripcion,
            "imagen_file": self.imagen_file.filename if self.imagen_file else None,
            "usuario_id": self.usuario_id
        }
