# academic_management/controllers/auth_api.py
from odoo import http
from odoo.http import request
from odoo.tools import config
import json
import jwt
import datetime
import logging
from .decorators import token_required

_logger = logging.getLogger(__name__)

CORS = config.get("cors_domain", "*")


class AuthAPI(http.Controller):

    secret_key = "your_secret_key"

    @http.route("/api/auth/login", auth="public", type="json", methods=["POST"])
    def authenticate(self, **kwargs):
        try:
            params = json.loads(request.httprequest.data)
            username = params.get("username")
            password = params.get("password")

            # Autenticar el usuario con el nombre de la base de datos actual
            uid = request.session.authenticate(
                request.env.cr.dbname, username, password
            )
            if uid is not False:  # Verificar si la autenticación fue exitosa
                user = request.env["res.users"].browse(uid)

                # Verificar si el usuario es un apoderado
                apoderado = (
                    request.env["administracion_academica.apoderado"]
                    .sudo()
                    .search([("user_id", "=", user.id)], limit=1)
                )
                if not apoderado:
                    return {"error": "Acceso no autorizado", "success": False}

                payload = {
                    "user_id": user.id,
                    "exp": datetime.datetime.now()
                    + datetime.timedelta(hours=24),  # Token expira en 24 horas
                }
                token = jwt.encode(payload, self.secret_key, algorithm="HS256")
                # _logger.info("Token creado correctamente para el usuario %s", username)

                response_data = {
                    "success": True,
                    "message": "Usuario autenticado con éxito.",
                    "data": {
                        "user_id": user.id,
                        "user_name": user.name,
                        "user_email": user.email,
                        "token": token,
                    },
                }
                return response_data

            # _logger.error("Credenciales inválidas para el usuario %s", username)
            return {"error": "Credenciales no válidas", "success": False}
        except Exception as e:
            # _logger.exception("Error en el proceso de autenticación: %s", str(e))
            return {
                "error": "Error Interno del Servidor",
                "message": str(e),
                "success": False,
            }

    @http.route("/api/students", auth="public", methods=["GET"])
    @token_required
    def get_students(self):
        try:
            # Obtener la lista de estudiantes
            students = request.env["administracion_academica.alumno"].sudo().search([])
            student_data = []
            for student in students:
                apoderado = student.apoderado
                student_data.append(
                    {
                        "id": student.id,
                        "nombre": student.nombre,
                        "apellido_paterno": student.apellido_paterno,
                        "apellido_materno": student.apellido_materno,
                        "fecha_nacimiento": (
                            student.fecha_nacimiento.strftime("%Y-%m-%d")
                            if student.fecha_nacimiento
                            else None
                        ),
                        "direccion": student.direccion if student.direccion else None,
                        "foto": student.foto_url if student.foto_url else None,
                        "apoderado": (
                            {
                                "id": apoderado.id,
                                "nombre": apoderado.nombre,
                                "apellidos": apoderado.apellidos,
                                "carnet_identidad": apoderado.carnet_identidad,
                                "correo_electronico": apoderado.correo_electronico,
                                "telefono": (
                                    apoderado.telefono if apoderado.telefono else None
                                ),
                                "direccion": (
                                    apoderado.direccion if apoderado.direccion else None
                                ),
                            }
                            if apoderado
                            else None
                        ),
                    }
                )

            _logger.info("Datos de estudiantes obtenidos correctamente")
            response_data = {
                "success": True,
                "data": student_data,
            }
            response_data = json.dumps(response_data)
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            _logger.exception(
                "Error al obtener los datos de los estudiantes: %s", str(e)
            )
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )

    @http.route(
        "/api/apoderado/<int:user_id>/estudiantes", auth="public", methods=["GET"]
    )
    @token_required
    def get_estudiantes_apoderado(self, user_id, **kwargs):
        try:
            # Buscar el apoderado asociado al user_id
            apoderado = (
                request.env["administracion_academica.apoderado"]
                .sudo()
                .search([("user_id", "=", user_id)], limit=1)
            )
            if not apoderado:
                return {"error": "Apoderado no encontrado", "success": False}

            # Obtener los estudiantes asociados al apoderado
            estudiantes = (
                request.env["administracion_academica.alumno"]
                .sudo()
                .search([("apoderado", "=", apoderado.id)])
            )

            # Construir la respuesta con los datos de los estudiantes
            data = []
            for estudiante in estudiantes:
                data.append(
                    {
                        "id": estudiante.id,
                        "nombre": estudiante.nombre,
                        "apellido_paterno": estudiante.apellido_paterno,
                        "apellido_materno": estudiante.apellido_materno,
                        "fecha_nacimiento": (
                            estudiante.fecha_nacimiento.strftime("%Y-%m-%d")
                            if estudiante.fecha_nacimiento
                            else None
                        ),
                        "direccion": estudiante.direccion if estudiante.direccion else None,
                        "foto": estudiante.foto_url if estudiante.foto_url else None,
                    }
                )

            response_data = json.dumps({
                "success": True,
                "data": data,
            })
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
        except Exception as e:
            response_data = json.dumps(
                {
                    "error": "Error Interno del Servidor",
                    "message": str(e),
                    "success": False,
                }
            )
            return request.make_response(
                response_data,
                headers=[
                    ("Content-Type", "application/json"),
                    ("Access-Control-Allow-Origin", CORS),
                ],
            )
