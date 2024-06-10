from odoo import models, fields, api


class curso(models.Model):
    _name = "administracion_academica.curso"
    _description = "Relacion de los cursos del colegio"

    nombre = fields.Char(string="Nombre del curso")
    # un curso puede darse varias materias (muchos a muchos)
    materias = fields.Many2many(
        "administracion_academica.materia", "curso_materia", "curso_id", "materia_id"
    )
    # un curso puede tener varios alumnos (muchos a muchos)
    alumnos = fields.Many2many(
        "administracion_academica.alumno", "inscripcion", "curso_id", "alumno_id"
    )

    @api.depends("nombre")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nombre}"
            )

    
