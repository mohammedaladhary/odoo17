from datetime import datetime
from odoo import models, fields, api
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

    item_name = fields.Char('Item Name', required=True)
    item_code = fields.Char('Item Code', required=True)
    item_type = fields.Selection([('disposable', 'Disposable'), ('implantable', 'Implantable'), ('reusable', 'Reusable'),
                                  ('instrument', 'Instrument'), ('na', 'Not Applicable'), ('other', 'Others')],
                                 'Item Type', required=True)

    urgency = fields.Selection(AVAILABLE_PRIORITIES, string='Urgency', required=True)
    usage_location = fields.Char('Location of Usage', required=True)
    uom = fields.Selection([('PC', 'PC'), ('Pack', 'PACK'), ('Kit', 'KIT'), ('BOX', 'BOX')],
                           'Unit of Measure', required=True)
    reason = fields.Text('Reason for Request', required=True)

    equipment_month = fields.Float('Expected Monthly Equipments', required=True)
    quantity = fields.Float('Quantity Required', required=True)
    description = fields.Text('Item Description', required=True)
    cost = fields.Float('Estimated Cost per Unit', required=True)
    cost_subtotal = fields.Float('Total Cost', compute="compute_cost_subtotal", required=True)

    attachment = fields.Binary('Supplementary Document', required=True)
    name = fields.Char('Name')
    request_date = fields.Datetime('Date of Request', default=datetime.now(), readonly=True)
    req_by = fields.Many2one('res.users', 'Requested By', default=lambda self: self.env.user)
    contact = fields.Char('Contact No.', default=lambda self: self.env.user.phone, readonly=True)

    dept_id = fields.Many2one('hr.department', 'Department', compute='_compute_department',store=True, readonly=True)
    staff_id = fields.Char('Employee ID', compute="_compute_department", store=True)

    state = fields.Selection([('draft', 'Draft'), ('submit', 'Pending HOD Approval'),
                            ('committee_approve', 'Pending Equipment Committee Approval'),
                            ('store_approve', 'Pending Main Store Approval'), ('approve', 'Completed'),
                            ('cancel', 'Cancel'), ('reject', 'Rejected')],
                            string='Status', default='draft', tracking=True, copy=False)
    committee_comment = fields.Text('Committee Comment', readonly=False, copy=False)
    committee_status = fields.Selection([('review', 'Under Review. Requested More Info.')], 'Committee Status')

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

    hod_name = fields.Char("HOD Name")
    hod_signature = fields.Char("HOD Signature")
    hod_date = fields.Date("HOD Date")
    hod_comment = fields.Text('HOD Comment')
    submitted_to_committee = fields.Selection([('yes', 'Yes'),('no', 'No')], string="Submitted to Equipment Committee?")

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['name'] = _('New')
        return super(MeqRequest, self).create(vals_list)

    def action_submit(self):
        if self.req_by != self.env.user:
            raise UserError(_('only %s can submit this request') % self.req_by.name)
        self.state = 'submit'
        self.name = self.env['ir.sequence'].next_by_code('meq.request') or _('New')

    def reject(self):
        self.state = 'reject'

    def reset_to_draft(self):
        self.state = 'draft'

    def action_hod_approve(self):
        self.hod_date = fields.Date.today()
        self.state = 'committee_approve'

    def reset_to_hod(self):
        self.state = 'submit'

    def reset_to_committee(self):
        self.state = 'committee_approve'

    def cancel(self):
        self.state = 'cancel'

    def hod_approve(self):
        self.state = 'committee_approve'

    def committee_approve(self):
        self.state = 'store_approve'

    def store_approve(self):
        self.state = 'approve'

    @api.onchange('cost', 'quantity')
    def compute_cost_subtotal(self):
        for rec in self:
            rec.cost_subtotal = rec.cost * rec.quantity

    @api.depends('req_by')
    def _compute_department(self):
        for rec in self:
            employee = rec.req_by.employee_ids[:1]
            rec.dept_id = employee.department_id.id

    @api.constrains('equipment_month', 'quantity', 'cost', 'cost_subtotal')
    def _check_non_negative_fields(self):
        for rec in self:
            if (rec.equipment_month <= 0 or
                    rec.quantity <= 0 or
                    rec.cost <= 0 or
                    rec.cost_subtotal <= 0):

                raise ValidationError(
                    "Fields 'Expected Monthly Equipments', 'Quantity Required', "
                    "'Estimated Cost per Unit', and 'Total Cost' cannot be less than zero or zero.")

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super(MeqRequest, self).fields_get(allfields, attributes)
        user = self.env.user

        if not (user.has_group(
                'meq_requisition_form.group_meq_hod') and not user._is_admin()):
            for field in [
                'hod_name', 'hod_date', 'hod_signature', 'hod_comment']:
                if field in res:
                    res[field]['readonly'] = True

        if not (user.has_group(
                'meq_requisition_form.group_meq_committee') and not user._is_admin()):
            for field in [
                'submitted_to_committee', 'committee_status', 'committee_comment']:
                if field in res:
                    res[field]['readonly'] = True

        return res

    def equipment_xlsx_report(self):
        ids = ','.join(str(x.id) for x in self)
        return {
            'type': 'ir.actions.act_url',
            'url': f'/equipment/excel/report/{ids}',
            'target': 'new',
        }