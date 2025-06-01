{
    'name': "key_request",
    'author': "SQCCCRC",

    'category': 'App',
    'application': True,

    'version': '17.0.0.1.0',
    'depends': ['base','hr','mail'],

    'data': [
        # security
        'security/ir.model.access.csv',

        # data
        'data/key_request_sequence.xml',
        # views
        'views/key_request_form.xml',
        'views/key_request_menu.xml',
    ],
}