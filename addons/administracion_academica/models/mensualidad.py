from odoo import models, fields, api


class mensualidad(models.Model):
    _name = "administracion_academica.mensualidad"
    _description = "Relacion de los mensualidades de los alumnos"

    monto = fields.Float(string="Monto")
    cantidad_meses = fields.Integer(string="Cantidad de meses")
    # mes = fields.Char(string= "Mes")
    # estado = fields.Selection(
    #     [
    #          ("pagado", "Pagado"),
    #          ("pendiente", "Pendiente"),
    #     ],
    #     string ="Estado",
    #     default="pendiente",
    #     required= True,
    # )
    # muchas mensualidades pueden ser pagadas por un apoderado ( muchos a uno)
    apoderado = fields.Many2one(
        "administracion_academica.apoderado", string="Nombre del apoderado"
    )
    # muchas mensualidades le pertencen a un alumno( muchos a uno)
    alumno = fields.Many2one(
        "administracion_academica.alumno", string="Nombre del alumno"
    )
    # muchas mensualidades puede tener una gestion ( muchos a uno)
    gestion = fields.Many2one("administracion_academica.gestion", string="Gestión")
    costo_mensualidad = fields.Many2one(
        "administracion_academica.costo_mensualidad", string="Costo de la mensualidad"
    )

    # carga el nombre del apoderado al seleccionar al alumno
    @api.onchange("alumno")
    def _onchange_alumno(self):
        if self.alumno:
            self.apoderado = self.alumno.apoderado

    # calcula la cantidad total a pagar segun los meses que paga
    @api.onchange("cantidad_meses", "costo_mensualidad")
    def _onchange_cantidad_meses(self):
        if self.cantidad_meses and self.costo_mensualidad:
            self.monto = float(self.cantidad_meses) * float(
                self.costo_mensualidad.monto
            )
