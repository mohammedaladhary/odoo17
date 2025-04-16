from odoo import http


class MeqRequisitionForm(http.Controller):
    @http.route('/meq_requisition_form/meq_requisition_form', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/meq_requisition_form/meq_requisition_form/objects', auth='public')
    def list(self, **kw):
        return http.request.render('meq_requisition_form.listing', {
            'root': '/meq_requisition_form/meq_requisition_form',
            'objects': http.request.env['meq_requisition_form.meq_requisition_form'].search([]),
        })

    @http.route('/meq_requisition_form/meq_requisition_form/objects/<model("meq_requisition_form.meq_requisition_form"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('meq_requisition_form.object', {
            'object': obj
        })

