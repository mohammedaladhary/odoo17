from datetime import datetime
from email.policy import default

from odoo import models, fields, api, re
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High')]

class MeqRequest(models.Model):
    _name = 'meq.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Meq Request'

    name = fields.Char('Name')
    request_date = fields.Datetime('Date of Request', default=datetime.now(), readonly=True)
    req_by = fields.Many2one('res.users', 'Requested By', default=lambda self: self.env.user)
    contact = fields.Char('Contact No.', default=lambda self: self.env.user.phone)
    dept_id = fields.Many2one('hr.department', 'Department')
    staff_id = fields.Char('Employee ID', compute="_compute_department", store=True)
    product_name = fields.Char('Item Name')
    item_code = fields.Char('Item Code')
    item_type = fields.Selection(
        [('disposable', 'Disposable'), ('implantable', 'Implantable'), ('reusable', 'Reusable'),
         ('instrument', 'Instrument'), ('na', 'Not Applicable'), ('other', 'Others')], 'Item Type')
    urgency = fields.Selection(AVAILABLE_PRIORITIES, string='Urgency')
    Equipment_month = fields.Float('Expected Monthly Equipments')
    quantity = fields.Float('Quantity Required')
    cost = fields.Float('Estimated Cost per Unit')
    cost_subtotal = fields.Float('Total Cost', compute="compute_cost_subtotal")
    uom = fields.Selection([('PC', 'PC'), ('Pack', 'PACK'), ('Kit', 'KIT'), ('BOX', 'BOX')], 'Unit of Measure', )
    reason = fields.Text('Reason for Request')
    description = fields.Text('Item Description')
    attachment = fields.Binary('Supplementary Document')
    state = fields.Selection([('draft', 'Draft'), ('submit', 'Pending HOD Approval'),
                            ('committee_approve', 'Pending Equipment Committee Approval'),
                            ('store_approve', 'Pending Main Store Approval'), ('approve', 'Completed'),
                            ('cancel', 'Cancel'), ('reject', 'Rejected')],
                            string='Status', default='draft', tracking=True, copy=False)
    hod_comment = fields.Text('HOD Comment')
    committee_comment = fields.Text('Committee Comment', readonly=False, copy=False)
    committee_status = fields.Selection([('review', 'Under Review. Requested More Info.')], 'Committee Status')
    usage_location = fields.Char('Location of Usage')
    backup_available = fields.Selection([('yes', 'Yes'), ('no', 'No')],'Any similar/Back-up equipments available?')
    backup_details = fields.Text('Details of Back-up Equipment')
    replaces_existing = fields.Selection([('yes', 'Yes'), ('no', 'No')],'Does this replace any current existing MEQ?')
    replaces_details = fields.Text('Details of Replaced Equipment')
    additional_doc_attached = fields.Selection([('yes', 'Yes'), ('no', 'No')],'Any additional document attached?')
    additional_doc_details = fields.Text('Additional Document Details')
    urgency_justification = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Urgency and Justification?')
    urgency_details = fields.Text('Justification Details')
    manpower_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Manpower Requirement?')
    manpower_details = fields.Text('Details of Manpower Requirement')
    space_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Space Requirement?')
    space_details = fields.Text('Space Details')
    accessories_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Accessories / Software’s?')
    accessories_details = fields.Text('Accessories / Software’s Details')
    consumables_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Required Consumables?')
    consumables_details = fields.Text('Consumables Details')
    patient_usage = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Expected Patient Usage/Month?')
    usage_details = fields.Text('Expected Monthly Patient Usage')
    used_in_other_departments = fields.Selection([('yes', 'Yes'), ('no', 'No')],'Can this MEQ be used in other departments?')
    departments_details = fields.Text('Other Departments')
    other_factors = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Any other factors to be considered?')
    factors_details = fields.Text('Other Factors')
    eu_name = fields.Char("End User Name")
    eu_signature = fields.Char("End User Signature")
    eu_date = fields.Date("End User Date")
    eu_contact = fields.Char("End User Contact no.")
    eu_hod_name = fields.Char("HOD Name")
    eu_hod_signature = fields.Char("HOD Signature")
    eu_hod_date = fields.Date("HOD Date")
    submitted_to_committee = fields.Selection([('yes', 'Yes'),('no', 'No')], string="Submitted to Equipment Committee?")

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

    # @api.constrains('contact','eu_contact')
    # def _check_contact_number(self):
    #     for rec in self:
    #         if rec.contact:
    #             if not re.match(r'^[97]\d{7}$', rec.contact):
    #                 raise ValidationError(
    #                     "Contact number must start with 9 or 7 and be exactly 8 digits long (Contact Number).")
    #         if rec.eu_contact:
    #             if not re.match(r'^[97]\d{7}$', rec.eu_contact):
    #                 raise ValidationError(
    #                     "Contact number must start with 9 or 7 and be exactly 8 digits long (End User Contact).")

    @api.constrains('Equipment_month', 'quantity', 'cost', 'cost_subtotal')
    def _check_non_negative_fields(self):
        for rec in self:
            if rec.Equipment_month < 0 or rec.quantity < 0 or rec.cost < 0 or rec.cost_subtotal < 0:
                raise ValidationError(
                    "Fields 'Expected Monthly Equipments', 'Quantity Required', 'Estimated Cost per Unit', and 'Total Cost' cannot be less than zero.")

    def equipment_xlsx_report(self):
        ids = ','.join(str(x.id) for x in self)
        return {
            'type': 'ir.actions.act_url',
            'url': f'/equipment/excel/report/{ids}',
            'target': 'new',
        }
