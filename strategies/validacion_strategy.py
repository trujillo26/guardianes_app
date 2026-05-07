from abc import ABC, abstractmethod

class ValidacionStrategy(ABC):
    """
    Interfaz base del patrón Strategy para validación de datos.
    Cada subclase implementa una estrategia de validación concreta.
    """

    @abstractmethod
    def validar(self, dto):
        """
        Valida el DTO recibido.
        Lanza ValueError con mensaje descriptivo si la validación falla.
        """
        pass


# ─── Estrategias concretas ────────────────────────────────────────────────────

class ValidacionPublicacion(ValidacionStrategy):
    """Valida que una publicación tenga descripción no vacía."""

    def validar(self, dto):
        if not dto.descripcion:
            raise ValueError("La descripción no puede estar vacía.")


class ValidacionReporte(ValidacionStrategy):
    """Valida que todos los campos obligatorios del reporte estén completos."""

    CAMPOS = ["nombre", "cedula", "direccion", "descripcion"]

    def validar(self, dto):
        for campo in self.CAMPOS:
            if not getattr(dto, campo, ""):
                raise ValueError(f"El campo '{campo}' es obligatorio.")


class ValidacionCedula(ValidacionStrategy):
    """Valida que la cédula contenga solo dígitos y tenga entre 6 y 10 caracteres."""

    def validar(self, dto):
        cedula = getattr(dto, "cedula", "")
        if not cedula.isdigit():
            raise ValueError("La cédula debe contener solo dígitos.")
        if not (6 <= len(cedula) <= 10):
            raise ValueError("La cédula debe tener entre 6 y 10 dígitos.")


class ValidacionImagen(ValidacionStrategy):
    """Valida el formato del archivo de imagen si se adjunta uno."""

    EXTENSIONES_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "webp"}

    def validar(self, dto):
        imagen = getattr(dto, "imagen_file", None)
        if imagen and imagen.filename:
            ext = imagen.filename.rsplit(".", 1)[-1].lower()
            if ext not in self.EXTENSIONES_PERMITIDAS:
                raise ValueError(
                    f"Formato de imagen '{ext}' no permitido. "
                    f"Use: {', '.join(self.EXTENSIONES_PERMITIDAS)}."
                )


# ─── Validador compuesto ──────────────────────────────────────────────────────

class ValidadorCompuesto:
    """
    Ejecuta una lista de estrategias de validación en orden.
    Permite combinar múltiples estrategias para un mismo caso de uso.
    """

    def __init__(self, estrategias: list):
        self._estrategias = estrategias

    def validar(self, dto):
        for estrategia in self._estrategias:
            estrategia.validar(dto)
