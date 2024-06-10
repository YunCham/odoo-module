import json
import jwt
from odoo.http import request
from odoo.tools import config
import logging

CORS = config.get("cors_domain", "*")

_logger = logging.getLogger(__name__)
_secret_key = "your_secret_key"


def token_required(f):
    def wrapper(*args, **kwargs):
        try:
            token = request.httprequest.headers.get("Authorization")

            if not token:
                _logger.error("Token faltante en la solicitud")
                response_data = json.dumps(
                    {
                        "error": "Token faltante",
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
            elif token.startswith("Bearer "):
                token = token.split(" ")[
                    1
                ]  # Obtener solo el token, sin el prefijo 'Bearer '

            _logger.info("Token recibido: %s", token)

            try:
                # Decodificar el token JWT
                payload = jwt.decode(token, _secret_key, algorithms=["HS256"])
                _logger.info("Token decodificado: %s", payload)

                user_id = payload["user_id"]
                _logger.info(
                    "Token decodificado correctamente para el usuario ID %s", user_id
                )
                user = request.env["res.users"].sudo().browse(user_id)
                if not user:
                    _logger.error("Token inválido para el usuario ID %s", user_id)
                    response_data = json.dumps(
                        {
                            "error": "Token inválido",
                            "message": "Usuario no encontrado",
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
            except jwt.ExpiredSignatureError:
                _logger.error("Token expirado")
                response_data = json.dumps(
                    {
                        "error": "Token expirado",
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
            except jwt.InvalidTokenError:
                _logger.error("Token inválido")
                response_data = json.dumps(
                    {
                        "error": "Token inválido",
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

            return f(*args, **kwargs)
        except Exception as e:
            _logger.exception(
                "Error en el proceso de verificación del token: %s", str(e)
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

    return wrapper
