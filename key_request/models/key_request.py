from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _


class KeyRequest(models.Model):
    _name = 'key.request'
    _description = 'Key Request Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    request_date = fields.Datetime('Date of Request', default=fields.Datetime.now, readonly=True)
    name = fields.Char('Name')
    form_type = fields.Selection([
        ('master', 'Master Key(s)'),
        ('locker', 'Locker Key(s)'),
        ('door', 'Door Key(s)')
    ], string="Form Type", required=True)

    req_by = fields.Many2one('res.users', string='Requested By:', default=lambda self: self.env.user, readonly=True)
    staff_id = fields.Char(string="Staff ID no.:", compute='_compute_staff_id', store=True, readonly=True)
    position = fields.Many2one('hr.job',string="Position/Title:", compute='_compute_position', store=True, readonly=True)
    dept_id = fields.Many2one('hr.department', string='Department:', compute='_compute_department', store=True, readonly=True)
    contact = fields.Char(string='Contact No.:', default=lambda self: self.env.user.phone, readonly=True)

    key_line_ids = fields.One2many('key.request.line', 'request_id', string="Requested Keys:")

    state = fields.Selection(
        [('draft', 'Draft'),
        ('submit', 'Pending HOD Approval'),
        ('maintenance_approve', 'Pending Maintenance Approval'),
        ('approve', 'Completed'),('reject', 'Rejected'),('cancel', 'Cancel')],
        string='Status:', default='draft', tracking=True, copy=False)

    eng_rev_by = fields.Many2one('hr.employee',string="Reviewed by Engineer:", required=True)
    eng_signature = fields.Char(string="Engineer Signature:")
    hod_signature = fields.Char(string="HOD Signature:")

    payment_approved_stamped_by = fields.Char(string="Payment Approved and Stamped by (Only for Lost Key Request):")
    request_type = fields.Selection([
        ('key_request', 'Key Request'),
        ('lost_key', 'Lost Key Request'),
        ('key_return', 'Key Return')
    ], string="Type of Request", required=True)

    @api.onchange('request_type')
    def _onchange_request_type(self):
        if self.request_type != 'lost_key':
            self.payment_approved_stamped_by = False

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['name'] = _('New')
        return super(KeyRequest, self).create(vals)

    def submit(self):
            if self.req_by != self.env.user:
                raise UserError(_('only %s can submit this request') % self.req_by.name)
            self.state = 'submit'
            self.name = self.env['ir.sequence'].next_by_code('key.request') or _('New')

    def hod_approve(self):
        self.state = 'maintenance_approve'

    def maintenance_approve(self):
        self.state = 'approve'

    def reset_to_hod(self):
        self.state = 'submit'

    def reset_to_draft(self):
        self.state = 'draft'

    def reject(self):
        self.state = 'reject'

    def cancel(self):
        self.state = 'cancel'

    @api.depends('req_by')
    def _compute_staff_id(self):
        for rec in self:
            employee = rec.req_by.employee_ids[:1]
            rec.staff_id = employee.barcode

    @api.depends('req_by')
    def _compute_position(self):
        for rec in self:
            employee = rec.req_by.employee_ids[:1]
            rec.position = employee.job_id

    @api.depends('req_by')
    def _compute_department(self):
        for rec in self:
            employee = rec.req_by.employee_ids[:1]
            rec.dept_id = employee.department_id

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super(KeyRequest, self).fields_get(allfields, attributes)
        user = self.env.user

        if user._is_admin():
            return res

        if not (user.has_group('key_request.group_key_hod') or
                user.has_group('key_request.group_key_maintenance')):

            readonly_fields = ['hod_signature', 'payment_approved_stamped_by']
        else:
            readonly_fields = ['eng_rev_by', 'eng_signature']

        for field in readonly_fields:
            if field in res:
                res[field]['readonly'] = True

        return res

class KeyRequestLine(models.Model):
    _name = 'key.request.line'
    _description = 'Key Request Line'

    request_id = fields.Many2one('key.request', string="Request", required=True, ondelete='cascade')
    level = fields.Char(string="Level")
    zone = fields.Char(string="Zone")
    room_no = fields.Char(string="Room no.")
    state = fields.Selection(related='request_id.state', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        return super(KeyRequestLine, self).create(vals_list)