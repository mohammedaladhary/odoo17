from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High')]

class MeqRequest(models.Model):
    _name = 'meq.request'
    _description = 'Meq Request'

    name = fields.Char('Name')
    request_date = fields.Datetime('Date of Request', default=datetime.now(), readonly=True)
    req_by = fields.Many2one('res.users', 'Requested By', default=lambda self: self.env.user)
    dept_id = fields.Many2one('hr.department', 'Department')
    contact = fields.Char('Contact Number')
    staff_id = fields.Char('Employee ID', compute="_compute_department", store=True)
    product_name = fields.Char('Item Name')
    item_code = fields.Char('Item Code')
    item_type = fields.Selection(
        [('disposable', 'Disposable'), ('implantable', 'Implantable'), ('reusable', 'Reusable'),
         ('instrument', 'Instrument'), ('na', 'Not Applicable'), ('other', 'Others')], 'Item Type')

    urgency = fields.Selection(AVAILABLE_PRIORITIES, string='Urgency')
    Equipment_month = fields.Float('Expected Monthly Equipments')
    quantity = fields.Float('Quantity Required')
    uom = fields.Selection([('PC', 'PC'), ('Pack', 'PACK'), ('Kit', 'KIT'), ('BOX', 'BOX')], 'Unit of Measure', )
    cost = fields.Float('Estimated Cost per Unit')
    cost_subtotal = fields.Float('Total Cost', compute="compute_cost_subtotal")
    reason = fields.Text('Reason for Request')
    description = fields.Html('Item Description')
    attachment = fields.Binary('Supplementary document')
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Pending HOD Approval'),
                            ('committee_approve', 'Pending Equipment Committee Approval'),
                            ('store_approve', 'Pending Main Store Approval'), ('approve', 'Completed'),
                            ('cancel', 'Cancel'), ('reject', 'Rejected')],
                            string='Status', default='draft', tracking=True, copy=False)

    hod_comment = fields.Text('HOD Comment')
    committee_comment = fields.Text('Committee Comment', readonly=False, copy=False)
    committee_status = fields.Selection([('review', 'Under Review. Requested More Info.')], 'Committee Status')

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['name'] = _('New')
        return super(MeqRequest, self).create(vals_list)

    def action_submit(self):
        if self.req_by != self.env.user:
            raise UserError(_('only %s can submit this request') % (self.req_by.name))
        self.state = 'submit'
        self.name = self.env['ir.sequence'].next_by_code('meq.request') or _('New')

    def reject(self):
        self.state = 'reject'

    def reset_to_hod(self):
        self.state = 'submit'

    def reset_to_committee(self):
        self.state = 'committee_approve'

    def cancel(self):
        self.state = 'reject'

    # Store Approve
    def approve(self):
        self.state = 'approve'

    def hod_reset_draft(self):
        self.state = 'draft'

    @api.onchange('cost', 'quantity')
    def compute_cost_subtotal(self):
        for rec in self:
            rec.cost_subtotal = rec.cost * rec.quantity