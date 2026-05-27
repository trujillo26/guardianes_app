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

        
        return render_template(
            "login.html",
            error_login="Correo o contraseña incorrectos.",
            tab_activo="login"
        )
 
    return render_template("login.html", tab_activo="login")
 
 
@auth_bp.route("/registro", methods=["POST"])
def registro():
    nombre   = request.form.get("nombre", "").strip()
    correo   = request.form.get("correo", "").strip()
    password = request.form.get("password", "")
 
    if not all([nombre, correo, password]):
        return render_template(
            "login.html",
            error_registro="Todos los campos son obligatorios.",
            tab_activo="registro"
        )
 
    if len(password) < 6:
        return render_template(
            "login.html",
            error_registro="La contraseña debe tener mínimo 6 caracteres.",
            tab_activo="registro"
        )
 
    try:
        AuthService.register(nombre, correo, password)
        return render_template(
            "login.html",
            ok_registro="¡Cuenta creada exitosamente! Ya puedes ingresar.",
            tab_activo="registro"
        )
    except Exception:
        return render_template(
            "login.html",
            error_registro="Ese correo ya está registrado.",
            tab_activo="registro"
        )
 
 
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
