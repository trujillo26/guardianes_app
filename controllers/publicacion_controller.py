from flask import Blueprint, request, redirect, session, render_template
from services.publicacion_service import PublicacionService
from services.reporte_service import ReporteService
from models.publicacion_dao import PublicacionDAO
from dto.publicacion_dto import PublicacionDTO
from dto.reporte_dto import ReporteDTO

publicacion_bp = Blueprint("publicacion", __name__)


@publicacion_bp.route("/publicacion", methods=["POST"])
def crear_publicacion():
    """Recibe el POST del dashboard, construye el DTO y llama al servicio."""
    if "user_id" not in session:
        return redirect("/login")

    try:
        dto = PublicacionDTO.from_form(request.form, session["user_id"])
        PublicacionService.crear(dto)
    except Exception as e:
        return f"Error: {e}"

    return redirect("/formulario")


@publicacion_bp.route("/formulario", methods=["GET"])
def ver_formulario():
    """Muestra el formulario detallado."""
    if "user_id" not in session:
        return redirect("/login")
    return render_template("formulario.html", user=session, mensaje=None, error=None)


@publicacion_bp.route("/formulario", methods=["POST"])
def enviar_formulario():
    """Construye el ReporteDTO y llama al servicio."""
    if "user_id" not in session:
        return redirect("/login")

    try:
        dto = ReporteDTO.from_form(request.form, request.files, session["user_id"])
        ReporteService.crear(dto)
        return render_template(
            "formulario.html",
            user=session,
            mensaje="¡Reporte enviado exitosamente!",
            error=None
        )
    except ValueError as e:
        return render_template(
            "formulario.html",
            user=session,
            mensaje=None,
            error=str(e)
        )
