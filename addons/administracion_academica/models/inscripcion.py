from odoo import models, fields, api
from datetime import datetime


# tabla intermedia entre curso y alumno
class Inscripcion(models.Model):
    _name = "administracion_academica.inscripcion"
    _description = "Inscripciones de los estudiantes"

    curso_id = fields.Many2one(
        "administracion_academica.curso", string="Curso", required=True
    )
    alumno_id = fields.Many2one(
        "administracion_academica.alumno", string="Alumno", required=True
    )
    fecha = fields.Datetime(string="Fecha Actual", default=datetime.now())

    # muchas inscripciones pueden darse en una gestion (muchos a uno)
    gestion = fields.Many2one("administracion_academica.gestion", string="Gestión")
    
    
    @api.depends("fecha")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"Inscripción {self.id} - {rec.fecha}"
            )
