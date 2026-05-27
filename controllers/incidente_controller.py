from flask import Blueprint, request, redirect, session, render_template
from models.incidente_dao import IncidenteDAO 

incidente_bp = Blueprint("incidente", __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if"user_id" not in session: 
            return redirect("/login")
        if session.get("rol") != "admin":
            return redirect("/dashboard")
        return f(*args, **kwargs)
    return decorated

@incidente_bp.route("/")
def index():
    return redirect("/dashboard")

@incidente_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    reportes_aprobados = IncidenteDAO.get_reportes_aprobados()
    return render_template("dashboard.html", reportes_aprobados=reportes_aprobados, session=session)

@incidente_bp.route("/reportar", methods=["POST"])
@admin_required
def admin(): 
    filtro = request.args.get("estado", "todos")
    reportes = IncidenteDAO.get_reportes(filtro)
    conteo = IncidenteDAO.contar_por_estado()
    return render_template("admin.html", reportes=reportes, filtro=filtro, total=conteo["total"], aprobados=conteo["Aprobados"], rechazados=conteo["Rechazados"], pendiente=conteo["Pendiente"], session=session)

@incidente_bp.route("/admin/aprobar/<int:reporte_id>", methods=["POST"])
@admin_required
def aprobar(reporte_id):
    IncidenteDAO.aprobar_reporte(reporte_id, "Aprobado")
    return redirect(request.referrer or "/admin")

@incidente_bp.route("/admin/rechazar/<int:reporte_id>", methods=["POST"])
@admin_required
def rechazar(reporte_id):
    IncidenteDAO.aprobar_reporte(reporte_id, "Rechazado")
    return redirect(request.referrer or "/admin")