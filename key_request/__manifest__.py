{
    'name': "key_request",
    'author': "SQCCCRC",

    'category': 'App',
    'application': True,

    'version': '17.0.0.1.0',
    'depends': ['base','hr','mail'],

    'data': [
        # security
        'security/key_request_security.xml',
        'security/ir.model.access.csv',

        # data
        # 'data/demo.xml',
        # 'data/key_request_demo.csv',
        # 'data/key_request_line_demo.csv',
        'data/key_request_sequence.xml',

        # views
        'views/key_request_form.xml',
        'views/key_request_menu.xml',
    ],
}