from flask import Blueprint, request, redirect, session, render_template
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # AuthService ahora retorna un UsuarioDTO o None
        usuario_dto = AuthService.login(
            request.form["correo"],
            request.form["password"]
        )

        if usuario_dto:
            # Se almacena el dict del DTO en sesión (sin password)
            session["user_id"] = usuario_dto.id
            session["nombre"] = usuario_dto.nombre
            session["rol"] = usuario_dto.rol
            return redirect("/dashboard")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
