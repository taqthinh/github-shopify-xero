from odoo import api, fields, models, _
from xero.auth import OAuth2Credentials
from xero import Xero
import json

class XeroConfig(object):

    BASE_URL = "https://odoo.website"
    CALLBACK_URL = "https://odoo.website/xero/callback"
    XERO_URL = "https://login.xero.com"
    XERO_OAUTH2_TOKEN_URL = "https://identity.xero.com/connect/token"
    XERO_SCOPE = "offline_access openid profile email accounting.transactions accounting.contacts accounting.settings"
    # XERO_SCOPE = "accounting.contacts.read offline_access accounting.transactions.read"

    CLIENT_ID = "03CBCCCF06BD427D8D85B2F71EA075D3"
    CLIENT_SECRET = "vkosbjeHMfQ7Wa38JCUVzTyadlMIw7Pzr1WnW6m0FE0hViLy"

class XeroAuth(models.AbstractModel):
    _name = 'xero.auth'
    _description = 'Xero Authenticate'

    def get_xero_session(self):
        xero_config = XeroConfig()
        token = json.loads(self.xero_token)
        credentials = OAuth2Credentials(xero_config.CLIENT_ID, xero_config.CLIENT_SECRET, token=token,
                                    scope=token['scope'])
        if credentials.expired():
            credentials.refresh()
        if credentials.token:
            token = json.dumps(credentials.token)
            if self.xero_token != token:
                self.sudo().write({'xero_token': token})
        credentials.set_default_tenant()
        xero = Xero(credentials)
        return xero