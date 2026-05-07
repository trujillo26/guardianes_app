import os
from datetime import datetime
from werkzeug.utils import secure_filename
from models.reporte_dao import ReporteDAO
from dto.reporte_dto import ReporteDTO
from strategies.validacion_strategy import (
    ValidacionReporte, ValidacionCedula,
    ValidacionImagen, ValidadorCompuesto
)

UPLOAD_FOLDER = os.path.join("static", "uploads")

# Estrategia de validación compuesta para reportes
_validador = ValidadorCompuesto([
    ValidacionReporte(),
    ValidacionCedula(),
    ValidacionImagen()
])

class ReporteService:

    @staticmethod
    def crear(dto: ReporteDTO):
        """
        Recibe un ReporteDTO, lo valida con Strategy y lo persiste.
        Guarda la imagen en disco si viene adjunta.
        """
        _validador.validar(dto)

        imagen_path = None
        if dto.imagen_file and dto.imagen_file.filename:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(dto.imagen_file.filename)
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{ts}_{filename}"
            dto.imagen_file.save(os.path.join(UPLOAD_FOLDER, filename))
            imagen_path = filename

        data = (
            dto.nombre,
            dto.cedula,
            dto.direccion,
            dto.descripcion,
            imagen_path,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Pendiente",
            dto.usuario_id
        )
        ReporteDAO.create(data)
