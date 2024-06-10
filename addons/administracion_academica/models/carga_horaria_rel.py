from odoo import models, fields, api


# tabla intermedia entre materia y profesor
class CargaHorariaRel(models.Model):
    _name = "administracion_academica.carga_horaria_rel"
    _description = "Relación entre profesores y materias"

    # relacion con materia
    materia_id = fields.Many2one(
        "administracion_academica.materia", string="Materia", required=True
    )

    # relacion con profesor
    profesor_id = fields.Many2one(
        "administracion_academica.profesor", string="Profesor", required=True
    )
