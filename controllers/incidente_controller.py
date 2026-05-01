from flask import Blueprint, request, redirect, session, render_template
from services.incidente_service import IncidenteService
from models.incidente_dao import IncidenteDAO

incidente_bp = Blueprint("incidente", __name__)

@incidente_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        try:
            IncidenteService.crear(
                request.form["descripcion"],
                request.form["latitud"],
                request.form["longitud"],
                session["user_id"]
            )
        except Exception as e:
            return f"Error: {e}"

        return redirect("/dashboard")

    data = IncidenteDAO.get_all()
    return render_template("dashboard.html", data=data, user=session)