{
    'name': "MEQ",
    'version': '17.0.0.1.0',
    'depends': [
        'base',
        'hr',
        'mail'
    ],
    'author': "Sqcccrc",
    'category': 'App',
    'application': True,
    'data': [
        # security
        'security/meq_security.xml',
        'security/ir.model.access.csv',

        # data
        'data/meq_sequence.xml',
        'data/currency_data.xml',

        # views     # order matters!!
        'views/meq.xml',
        'views/meq_menus.xml',
    ]
}