# -*- coding: utf-8 -*-
{
    'name': "Cloudalia Politicas ANS",

    'summary': """
        - Cambio política ANS -> acorde con el estado del ticket.
        - Asignado por defecto""",

    'description': """
        Varios cambios en la politica ANS
    """,

    'author': "Cloudalia Educacion",
    'website': "https://cloudaliaeducacion.com",
    'category': 'Uncategorized',
    'version': '0.1',

    'installable': True,
    'auto_install': False,
    'application': True,
    # any module necessary for this one to work correctly
    'depends': ['base','helpdesk'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/helpdesk_views.xml',
    ],
}