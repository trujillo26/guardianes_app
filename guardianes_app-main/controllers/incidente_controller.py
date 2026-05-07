from flask import Blueprint, request, redirect, session, render_template
from models.publicacion_dao import PublicacionDAO

incidente_bp = Blueprint("incidente", __name__)

@incidente_bp.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    data = PublicacionDAO.get_all()
    return render_template("dashboard.html", data=data, user=session)

@incidente_bp.route("/")
def index():
    return redirect("/dashboard")
