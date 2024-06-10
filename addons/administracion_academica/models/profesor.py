from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Profesor(models.Model):
    _name = "administracion_academica.profesor"
    _description = "Relacion de los profesores del colegio"

    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    telefono = fields.Char(string="Telefono")
    direccion = fields.Char(string="Dirección")
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    foto = fields.Image(string="Foto")
    # muchos profesores pueden dar varias materias
    materias = fields.Many2many(
        "administracion_academica.materia",
        "carga_horaria_rel",
        "profesor_id",
        "materia_id",
    )
    correo_electronico = fields.Char(string="Email")
    # relacion con el modelo empleado del modulo de Odoo (Recursos Humanos)
    employee_id = fields.Many2one("hr.employee", string="Empleado", ondelete="cascade")

    _sql_constraints = [
        (
            "correo_electronico_uniq",
            "unique(correo_electronico)",
            "El correo electrónico debe ser único.",
        ),
    ]

    @api.constrains("nombre", "apellidos")
    def _check_names(self):
        for record in self:
            if not record.nombre:
                raise ValidationError("El nombre es requerido")
            if not record.apellidos:
                raise ValidationError("El apellido es requerido")
            
    @api.model
    def create(self, vals):
        # Crear empleado de Odoo
        full_name = f"{vals.get('nombre')} {vals.get('apellidos')}"
        employee_vals = {
            'name': full_name,
            'job_title': 'Profesor',
            'work_phone': vals.get('telefono'),
            'work_email': vals.get('correo_electronico'),
            'image_1920': vals.get('foto'),
            'private_street': vals.get('direccion'),
            "birthday": vals.get('fecha_nacimiento'),
            'resource_id': self.env['resource.resource'].create({'name': full_name}).id,
        }
        employee = self.env['hr.employee'].sudo().create(employee_vals)
        # Asignar el empleado creado al profesor
        vals['employee_id'] = employee.id
        return super(Profesor, self).create(vals)
    
    def write(self, vals):
        # Actualizar empleado relacionado
        res = super(Profesor, self).write(vals)
        for record in self:
            employee_vals = {}
            if 'nombre' in vals or 'apellidos' in vals:
                employee_vals['name'] = f"{record.nombre} {record.apellidos}"
            if 'telefono' in vals:
                employee_vals['work_phone'] = vals['telefono']
            if 'correo_electronico' in vals:
                employee_vals['work_email'] = vals['correo_electronico']
            if 'direccion' in vals:
                employee_vals['private_street'] = vals['direccion']
            if 'foto' in vals:
                employee_vals['image_1920'] = vals['foto']
            if 'fecha_nacimiento' in vals:
                employee_vals['birthday'] = vals['fecha_nacimiento']
            if employee_vals:
                record.employee_id.resource_id.name = f"{record.nombre} {record.apellidos}"
                record.employee_id.sudo().write(employee_vals)
        return res
    
    def unlink(self):
        # Primero eliminamos el empleado asociado si existe
        for record in self:
            if record.employee_id:
                record.employee_id.sudo().unlink()
        return super(Profesor, self).unlink()


    @api.depends("nombre", "apellidos")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.nombre} {rec.apellidos}"
