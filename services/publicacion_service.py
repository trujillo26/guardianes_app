from datetime import datetime
from models.publicacion_dao import PublicacionDAO
from dto.publicacion_dto import PublicacionDTO
from strategies.validacion_strategy import ValidacionPublicacion, ValidadorCompuesto

# Estrategia de validación para publicaciones
_validador = ValidadorCompuesto([
    ValidacionPublicacion()
])

class PublicacionService:

    @staticmethod
    def crear(dto: PublicacionDTO):
        """
        Recibe un PublicacionDTO, lo valida con Strategy y lo persiste.
        """
        _validador.validar(dto)

        data = (
            dto.descripcion,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dto.usuario_id
        )
        PublicacionDAO.create(data)
