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
        'security/ir.model.access.csv',
        'security/meq_security.xml',

        # data
        'data/meq_sequence.xml',
        'data/currency_data.xml',

        # views     # order matters!!
        'views/meq.xml',
    ]
}