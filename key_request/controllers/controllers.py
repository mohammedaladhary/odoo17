# -*- coding: utf-8 -*-
# from odoo import http


# class KeyRequest(http.Controller):
#     @http.route('/key_request/key_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/key_request/key_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('key_request.listing', {
#             'root': '/key_request/key_request',
#             'objects': http.request.env['key_request.key_request'].search([]),
#         })

#     @http.route('/key_request/key_request/objects/<model("key_request.key_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('key_request.object', {
#             'object': obj
#         })

