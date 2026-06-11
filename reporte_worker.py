"""
Worker de procesamiento de reportes (patrón Productor-Consumidor).

Cuando un usuario envía un reporte desde el formulario, en lugar de
guardarlo directamente y bloquear la petición HTTP, se encola y un
hilo trabajador en segundo plano se encarga de persistirlo
(incluyendo su ubicación lat/lng para el mapa de Bogotá).
"""

import threading
import queue
from datetime import datetime

from models.reporte_dao import ReporteDAO

# Cola compartida entre el hilo principal (Flask) y el worker
cola_reportes = queue.Queue()

_worker_iniciado = False
_lock_worker = threading.Lock()


def _procesar_reportes():
    """Consumidor: toma reportes de la cola y los guarda en la BD."""
    while True:
        item = cola_reportes.get()
        try:
            data = item["data"]
            print(f"[worker] Procesando reporte de {data[0]} ({data[1]})...")
            ReporteDAO.create(data)
            print(f"[worker] Reporte guardado en BD: {data[0]}")
        except Exception as e:
            print(f"[worker] ERROR al guardar reporte: {e}")
        finally:
            cola_reportes.task_done()


def iniciar_worker():
    """Arranca el hilo trabajador una sola vez (idempotente)."""
    global _worker_iniciado
    with _lock_worker:
        if not _worker_iniciado:
            hilo = threading.Thread(target=_procesar_reportes, daemon=True)
            hilo.start()
            _worker_iniciado = True
            print("[worker] Hilo de procesamiento de reportes iniciado.")


def encolar_reporte(nombre, cedula, direccion, descripcion, imagen_path,
                     latitud, longitud, usuario_id):
    """
    Productor: agrega un reporte (incluyendo coordenadas) a la cola
    para ser procesado/guardado de forma asíncrona por el worker.
    """
    iniciar_worker()

    data = (
        nombre,
        cedula,
        direccion,
        descripcion,
        imagen_path,
        latitud,
        longitud,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Pendiente",
        usuario_id
    )
    cola_reportes.put({"data": data})
    print(f"[worker] Reporte encolado: {nombre} - {cedula} - ({latitud}, {longitud})")