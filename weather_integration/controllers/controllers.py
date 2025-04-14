# -*- coding: utf-8 -*-
# from odoo import http


# class WeatherIntegration(http.Controller):
#     @http.route('/weather_integration/weather_integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/weather_integration/weather_integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('weather_integration.listing', {
#             'root': '/weather_integration/weather_integration',
#             'objects': http.request.env['weather_integration.weather_integration'].search([]),
#         })

#     @http.route('/weather_integration/weather_integration/objects/<model("weather_integration.weather_integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('weather_integration.object', {
#             'object': obj
#         })

