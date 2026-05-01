from werkzeug.security import generate_password_hash, check_password_hash
from models.user_dao import UserDAO

class AuthService:

    @staticmethod
    def register(nombre, correo, password):
        hashed = generate_password_hash(password)
        UserDAO.create(nombre, correo, hashed)

    @staticmethod
    def login(correo, password):
        user = UserDAO.find_by_email(correo)
        if user and check_password_hash(user["password"], password):
            return user
        return None