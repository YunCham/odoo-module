from odoo import models, fields, api


class calificacion(models.Model):
    _name = "administracion_academica.calificacion"
    _description = "notas de los alumnos"

    # relacion con alumnos (muchos a uno)
    alumno_id = fields.Many2one(
        "administracion_academica.alumno", string="Alumno", required=True
    )

    # relacion con curso_materia (muchos a uno)
    curso_materia_id = fields.Many2one(
        "administracion_academica.curso_materia", string="Curso Materia", required=True
    )
    descripcion = fields.Char("Descripción")
    nota = fields.Float("Nota", required=True)

    nombre_curso = fields.Char(string="Curso", compute="_compute_curso_materia")
    nombre_materia = fields.Char(string="Materia", compute="_compute_curso_materia")

    @api.depends("curso_materia_id")
    def _compute_curso_materia(self):
        for record in self:
            if record.curso_materia_id:
                record.nombre_curso = record.curso_materia_id.curso_id.nombre
                record.nombre_materia = record.curso_materia_id.materia_id.nombre
            else:
                record.nombre_curso = ""
                record.nombre_materia = ""
