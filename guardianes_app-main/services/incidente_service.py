from models.incidente_dao import IncidenteDAO
from datetime import datetime

class IncidenteService:

    @staticmethod
    def validar(lat, lng):
        lat = float(lat)
        lng = float(lng)

        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            raise ValueError("Coordenadas inválidas")

        return lat, lng

    @staticmethod
    def crear(descripcion, lat, lng, user_id):
        lat, lng = IncidenteService.validar(lat, lng)

        data = (
            descripcion,
            lat,
            lng,
            "Abierto",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id
        )

        IncidenteDAO.create(data)