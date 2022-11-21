{
    'name': 'Herencia modulo de reparacion de autos',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': '',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'bi_car_repair_management', 'account', 'sale', 'sale_management', 'maintenance', 'web', 'base'
    ],
    'data': [
        "security/ir.model.access.csv",
<<<<<<< HEAD
        'views/car_management_view.xml',
        'views/sale_order_view.xml',
        'views/maintenance_view.xml',
        'report/car_diagnosys.xml',
=======
        #'views/car_management_view.xml',
        'views/sale_order_view.xml',
        'views/maintenance_view.xml',
        'report/car_diagnosys.xml',
        #'report/sale_order.xml'
>>>>>>> origin/klug
    ],
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}