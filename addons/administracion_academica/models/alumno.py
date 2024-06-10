from odoo import models, fields, api
from ..utils.cloudinary_helper import CloudinaryHelper
from datetime import date


class alumno(models.Model):
    _name = "administracion_academica.alumno"
    _description = "Relacion de los alumnos del colegio"

    nombre = fields.Char(string="Nombre del alumno", required=True)
    apellido_paterno = fields.Char(string="Apellido paterno", required=True)
    apellido_materno = fields.Char(string="Apellido materno")
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento")
    direccion = fields.Char(string="Dirección")
    edad = fields.Integer(string="Edad", compute="_compute_edad", readonly=True)
    foto = fields.Image(string="Foto")
    foto_url = fields.Char(string="URL de la foto")
    genero = fields.Selection(
        [
            ("Masculino", "Masculino"),
            ("Femenino", "Femenino"),
            ("Otro", "Otro"),
        ],
        string="Sexo",
        required=True,
        default="Masculino",
    )
    # varios alumnos pertenecen a un alumno (muchos a uno)
    apoderado = fields.Many2one(
        "administracion_academica.apoderado", string="Nombre del apoderado"
    )
    # varios mensualidades pertenecen a un alumno (uno a muchos)
    mensualidades = fields.One2many(
        "administracion_academica.mensualidad",
        inverse_name="alumno",
        string="Mensualidad",
    )
    # un alumno puede inscribirse en varios cursos (muchos a muchos)
    cursos = fields.Many2many(
        "administracion_academica.curso", "inscripcion", "alumno_id", "curso_id"
    )
    # un alumno puede se relaciona con varios cursos_materias (muchos a muchos)
    cursos_materias = fields.Many2many(
        "administracion_academica.curso_materia",
        "calificacion",
        "alumno_id",
        "curso_materia_id",
    )

    @api.depends("fecha_nacimiento")
    def _compute_edad(self):
        today = date.today()
        for record in self:
            if record.fecha_nacimiento:
                birthdate = record.fecha_nacimiento
                age = (
                    today.year
                    - birthdate.year
                    - ((today.month, today.day) < (birthdate.month, birthdate.day))
                )
                record.edad = age
            else:
                record.edad = 0

    @api.model
    def create(self, vals):
        if vals.get("foto"):
            # Subir la imagen a Cloudinary
            vals["foto_url"] = CloudinaryHelper.upload_image(vals["foto"])
        return super(alumno, self).create(vals)

    def write(self, vals):
        if vals.get("foto"):
            if self.foto_url:
                # Eliminar la imagen de Cloudinary
                CloudinaryHelper.delete_image(self.foto_url)
            # Subir la imagen a Cloudinary
            vals["foto_url"] = CloudinaryHelper.upload_image(vals["foto"])
        elif "foto" in vals and not vals.get("foto"):
            if self.foto_url:
                # Eliminar la imagen de Cloudinary
                CloudinaryHelper.delete_image(self.foto_url)
            # Establecer foto_url en null
            vals["foto_url"] = None
        return super(alumno, self).write(vals)

    def unlink(self):
        for rec in self:
            # Eliminar la imagen de Cloudinary si existe
            if rec.foto_url:
                CloudinaryHelper.delete_image(rec.foto_url)
        return super(alumno, self).unlink()

    @api.depends("nombre", "apellido_paterno", "apellido_materno")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nombre} {rec.apellido_paterno} {rec.apellido_materno}"
            )
            
