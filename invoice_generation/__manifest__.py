# -*- coding: utf-8 -*-
{
    'name': "Generación de facturas",

    'summary': """
        Genera facturas masivamente, convierte ordenes creadas
        en UF a CLP""",

    'description': """
        Generacion masiva de facturas
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_view.xml',
        'views/sale_order_views.xml',
        'wizard/invoice_gen_wzd.xml',
        'data/invoice_move_data.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
