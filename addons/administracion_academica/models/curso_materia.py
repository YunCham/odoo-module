from odoo import models, fields, api

#tabla intermedia entre curso y  materia 
class CursoMateria(models.Model):
    _name = 'administracion_academica.curso_materia'
    _description = 'Relación entre curso y materias'

    #relacion con curso
    curso_id = fields.Many2one('administracion_academica.curso', string="Curso", required=True)
    
    #relacion con materia
    materia_id = fields.Many2one('administracion_academica.materia', string="Materia", required=True)

    alumnos = fields.Many2many('administracion_academica.alumno', "calificacion", 'curso_materia_id','alumno_id') 
    # materia_id = fields.Many2one('administracion_academica.materia', ondelete="cascade", string='Materia', required=True)
    # profesor_id = fields.Many2one('administracion_academica.profesor',ondelete="cascade", string='Profesor', required=True)

