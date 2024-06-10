# -*- coding: utf-8 -*-
{
    'name': "Administracion_academica",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
    Long description of module's purpose
    """,

    'author': "Carlos Vargas",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administración',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','hr','hr_attendance'],

    # always loaded

    'data': [
        'security/ir.model.access.csv',
        'views/greet_dashboard.xml',
        'views/record_profesores.xml',
        'views/record_materia.xml',
        'views/record_carga_horaria.xml',
        'views/record_curso.xml',
        'views/record_apoderado.xml',
        'views/record_alumno.xml',
        'views/record_inscripcion.xml',
        'views/record_gestion.xml',
        'views/record_periodo.xml',
        'views/record_tipo_periodo.xml',
        'views/record_calificacion.xml',
        'views/record_mensualidad.xml',
        'views/record_costo_mensualidad.xml',

        'views/menu_dashboard.xml',

        #'views/RRHH/record_alumno.xml',
        #'views/RRHH/menu_rrhh.xml',


    ],
    'installable': True,
    'application': True,
    'auto_install': False,  
    'assets':{
        'web.assets_backend':[
            'administracion_academica/static/src/components/**/*.js',
            'administracion_academica/static/src/components/**/*.xml',
        ],
    },
    #'qweb':['static/src/xml/dashboard.xml'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

