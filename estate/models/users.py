import uuid

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = "res.users"
    auth_token = fields.Char(string="Authentication Token", copy=False)
    #added the column manually:
        # ALTER TABLE res_users ADD COLUMN auth_token VARCHAR(255);

    @api.model
    def create(self, vals):
        vals['auth_token'] = self._auth_token_generator()

        return super(ResUsers, self).create(vals)

    def generate_auth_token(self):
        for user in self:
            user.auth_token = self._auth_token_generator()

        return True

    def _auth_token_generator(self):
        return str(uuid.uuid4())