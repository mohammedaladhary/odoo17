from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class KeyRequest(models.Model):
    _name = 'key.request'
    _description = 'Key Request Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    request_date = fields.Datetime('Date of Request', default=fields.Datetime.now, readonly=True)
    request_type = fields.Selection([
        ('key_request', 'Key Request'),
        ('lost_key', 'Lost Key Request'),
        ('key_return', 'Key Return')
    ], string="Type of Request", required=True, tracking=True)
    name = fields.Char('Name')

    req_by = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, readonly=True)
    staff_id = fields.Char(string="Staff ID no.", compute='_compute_staff_id', store=True, readonly=True)
    position = fields.Many2one('hr.job',string="Position/Title", compute='_compute_position', store=True, readonly=True)
    dept_id = fields.Many2one('hr.department', string='Department', compute='_compute_department', store=True, readonly=True)
    contact = fields.Char(string='Contact No.', default=lambda self: self.env.user.phone, readonly=True)

    key_line_ids = fields.One2many('key.request.line', 'request_id', string="Requested Keys")

    employee_signature = fields.Char(string="Employee Signature")
    hod_name = fields.Char(string="Head of Department")
    hod_signature = fields.Char(string="HOD Signature")

    state = fields.Selection(
        [('draft', 'Draft'),
        ('submit', 'Pending HOD Approval'),
        ('maintenance_approve', 'Pending Maintenance Approval'),
        ('approve', 'Completed'),('reject', 'Rejected'),('cancel', 'Cancel')],
        string='Status', default='draft', tracking=True, copy=False)

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

from odoo import models, fields, api

class KeyRequestLine(models.Model):
    _name = 'key.request.line'
    _description = 'Key Request Line'
    _order = 'sequence'

    sequence = fields.Integer(string="#", readonly=True)
    request_id = fields.Many2one('key.request', string="Request", required=True, ondelete='cascade')
    level = fields.Char(string="Level")
    zone = fields.Char(string="Zone")
    room_no = fields.Char(string="Room no.")

    @api.onchange('request_id')
    def _onchange_request_id(self):
        if self.request_id:
            existing_lines = self.request_id.key_line_ids
            self.sequence = len(existing_lines)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('sequence') and vals.get('request_id'):
                last_line = self.search(
                    [('request_id', '=', vals['request_id'])],
                    order='sequence desc', limit=1
                )
                vals['sequence'] = last_line.sequence + 1 if last_line else 1
        return super().create(vals_list)
