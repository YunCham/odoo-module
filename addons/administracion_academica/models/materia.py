from odoo import models, fields, api


class Materia(models.Model):
    _name = "administracion_academica.materia"
    _description = "Relacion de las materias del colegio"

    nombre = fields.Char(string="Nombre", required=True)
    # muchas materias pueden tener varios profesores (muchos a muchos)
    profesores = fields.Many2many(
        "administracion_academica.profesor",
        "carga_horaria_rel",
        "materia_id",
        "profesor_id",
    )
    # muchas materias pueden tener varios cursos (muchos a muchos)
    cursos = fields.Many2many(
        "administracion_academica.curso", "curso_materia", "materia_id", "curso_id"
    )
    grado = fields.Selection(
        [
            ("primaria", "Primaria"),
            ("secundaria", "Secundaria"),
        ],
        string="Grado",
        default="primaria",
        required=True,
    )
    

    @api.depends("nombre")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nombre}"
            )

    

