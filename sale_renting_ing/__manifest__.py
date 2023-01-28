{
    'name': 'Cambio en modulo alquiler',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': '',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'base', 'account', 'sale'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/financial_view.xml',
         'views/sale_order_view.xml',
        # 'views/res_partner_view.xml',
        'report/agreement_delivery.xml',
    ],

    'auto_install': False,
    'application': False,
    'assets': {

    }
}
