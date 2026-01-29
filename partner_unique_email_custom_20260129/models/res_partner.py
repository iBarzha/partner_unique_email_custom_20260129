from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """Extension of res.partner to enforce unique email addresses."""

    _inherit = 'res.partner'

    @api.constrains('email')
    def _check_unique_email(self):
        """Ensure email address is unique across all partners.

        Raises:
            ValidationError: If another partner with same email exists.
        """
        for partner in self:
            if partner.email:
                duplicate = self.search([
                    ('email', '=ilike', partner.email),
                    ('id', '!=', partner.id),
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        _('A partner with email "%(email)s" already exists: '
                          '%(partner)s',
                          email=partner.email,
                          partner=duplicate.display_name)
                    )
