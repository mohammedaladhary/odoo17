from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import datetime


class KeyRequest(models.Model):
    _name = 'key.request'
    _description = 'Key Request Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Request Reference", readonly=True, copy=False, tracking=True)
    request_date = fields.Datetime('Date of Request', default=fields.Datetime.now, readonly=True)

    request_type = fields.Selection([
        ('key_request', 'Key Request'),
        ('lost_key', 'Lost Key Request'),
        ('key_return', 'Key Return')
    ], string="Type of Request", required=True, tracking=True)

    req_by = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, readonly=True)
    staff_id = fields.Char(string="Staff ID No.", required=True)
    position = fields.Char(string="Position/Title")

    dept_id = fields.Many2one('hr.department', 'Department', compute='_compute_department',store=True, readonly=True)
    contact = fields.Char(string='Contact No.', default=lambda self: self.env.user.phone, readonly=True)
    key_line_ids = fields.One2many('key.request.line', 'request_id', string="Requested Keys")

    employee_signature = fields.Char(string="Employee Signature")
    hod_name = fields.Char(string="Head of Department")
    hod_signature = fields.Char(string="HOD Signature")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('key.request') or _('New')
        return super(KeyRequest, self).create(vals)

    def action_submit(self):
        for rec in self:
            if rec.req_by != self.env.user:
                raise UserError(_('Only the requester (%s) can submit this request.') % rec.req_by.name)
            rec.state = 'submit'
            rec.message_post(body=_("Key Request submitted."))

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'
            rec.message_post(body=_("Key Request approved."))

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'
            rec.message_post(body=_("Key Request rejected."))


class KeyRequestLine(models.Model):
    _name = 'key.request.line'
    _description = 'Key Request Line'

    request_id = fields.Many2one('key.request', string="Request", required=True, ondelete='cascade')
    level = fields.Char(string="Level")
    zone = fields.Char(string="Zone")
    room_no = fields.Char(string="Room no.")


