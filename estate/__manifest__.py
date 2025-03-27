{
    'name': "Estate",
    'version': '17.0.0.1.0',
    'depends': ['base'],
    'author': "Mohammed Abdullah",
    'category': 'App',
    'application': True,
    'data': [

        # security
        'security/ir.model.access.csv',

        # templates
        # 'data/templates/example_email_template.xml',

        # views     #order matter!!
        'views/estate_property.xml',
        'views/estate_property_type.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_tag.xml',
        'views/users.xml',
        'views/menu.xml',

        # Load initial Data
        'data/estate.property.csv',

        # schedulers
        'views/schedulers/estate_property_scheduler.xml',

        # Reports
        'reports/output_pdf/estate_property.xml',

    ]
}