from werkzeug.security import generate_password_hash, check_password_hash
from models.user_dao import UserDAO
from dto.usuario_dto import UsuarioDTO

class AuthService:

    @staticmethod
    def register(nombre, correo, password):
        hashed = generate_password_hash(password)
        UserDAO.create(nombre, correo, hashed)

    @staticmethod
    def login(correo, password):
        """
        Autentica al usuario y retorna un UsuarioDTO (sin password).
        Retorna None si las credenciales son inválidas.
        """
        row = UserDAO.find_by_email(correo)
        if row and check_password_hash(row["password"], password):
            return UsuarioDTO.from_row(row)
        return None
