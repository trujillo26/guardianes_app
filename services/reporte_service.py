import os
from datetime import datetime
from werkzeug.utils import secure_filename
from dto.reporte_dto import ReporteDTO
from strategies.validacion_strategy import (
    ValidacionReporte, ValidacionCedula,
    ValidacionImagen, ValidadorCompuesto
)
from workers.reporte_worker import encolar_reporte

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
        Valida el reporte (Strategy) y lo ENCOLA para ser guardado por
        el worker en segundo plano (patrón Productor-Consumidor),
        incluyendo su ubicación en el mapa de Bogotá.
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

        # Productor: encola el reporte (con coordenadas) en lugar de guardarlo directamente
        encolar_reporte(
            dto.nombre,
            dto.cedula,
            dto.direccion,
            dto.descripcion,
            imagen_path,
            dto.latitud,
            dto.longitud,
            dto.usuario_id
        )