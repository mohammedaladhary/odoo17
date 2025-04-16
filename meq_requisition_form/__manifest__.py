{
    'name': "MEQ",
    'version': '17.0.0.1.0',
    # any module necessary for this one to work correctly
    'depends': [
        'base',
    ],
    'author': "Sqcccrc",
    'category': 'App',
    'application': True,
    'data': [

        # security
        'security/ir.model.access.csv',

        # views     #order matter!!
        'views/meq.xml',
    ]
}

