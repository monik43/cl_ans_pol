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
    'depends': ['base', 'helpdesk', 'mail'],

    'data': [
        'views/helpdesk_views.xml',
    ],
}
