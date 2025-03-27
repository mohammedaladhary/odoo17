# -*- coding: utf-8 -*-
# from odoo import http


# class ScaffoldTry(http.Controller):
#     @http.route('/scaffold_try/scaffold_try', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/scaffold_try/scaffold_try/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('scaffold_try.listing', {
#             'root': '/scaffold_try/scaffold_try',
#             'objects': http.request.env['scaffold_try.scaffold_try'].search([]),
#         })

#     @http.route('/scaffold_try/scaffold_try/objects/<model("scaffold_try.scaffold_try"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('scaffold_try.object', {
#             'object': obj
#         })

