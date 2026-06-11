class ReporteDTO:
    """
    DTO para transferir datos del formulario detallado entre capas.
    Incluye coordenadas (latitud/longitud) para ubicar el reporte en el mapa.
    """
    def __init__(self, nombre, cedula, direccion, descripcion, imagen_file,
                 latitud, longitud, usuario_id):
        self.nombre = nombre
        self.cedula = cedula
        self.direccion = direccion
        self.descripcion = descripcion
        self.imagen_file = imagen_file  # objeto FileStorage de Flask (puede ser None)
        self.latitud = latitud
        self.longitud = longitud
        self.usuario_id = usuario_id

    @staticmethod
    def from_form(form, files, usuario_id):
        """Construye un ReporteDTO desde request.form y request.files."""
        lat = form.get("latitud", "").strip()
        lng = form.get("longitud", "").strip()

        return ReporteDTO(
            nombre=form.get("nombre", "").strip(),
            cedula=form.get("cedula", "").strip(),
            direccion=form.get("direccion", "").strip(),
            descripcion=form.get("descripcion", "").strip(),
            imagen_file=files.get("imagen"),
            latitud=float(lat) if lat else None,
            longitud=float(lng) if lng else None,
            usuario_id=usuario_id
        )

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "cedula": self.cedula,
            "direccion": self.direccion,
            "descripcion": self.descripcion,
            "imagen_file": self.imagen_file.filename if self.imagen_file else None,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "usuario_id": self.usuario_id
        }