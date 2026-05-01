from flask import Blueprint, request, redirect, session, render_template
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = AuthService.login(
            request.form["correo"],
            request.form["password"]
        )

        if user:
            session["user_id"] = user["id"]
            session["nombre"] = user["nombre"]
            session["rol"] = user["rol"]
            return redirect("/dashboard")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")