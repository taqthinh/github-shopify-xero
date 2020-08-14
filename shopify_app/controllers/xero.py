from odoo import http
from odoo.http import request, Response
import base64
import werkzeug
import requests
import json
from ..models.xero_auth import XeroConfig
from xero.auth import OAuth2Credentials
from requests_oauthlib import OAuth2
from xero import Xero
import time
# from .shopify import ShopifyController

class XeroController(http.Controller):

    @http.route('/xero_connect', auth='public', type='http')
    def xero_connect(self, *ar, **kw):
        xero_config = XeroConfig()
        callback_uri = xero_config.CALLBACK_URL
        credentials = OAuth2Credentials(xero_config.CLIENT_ID, xero_config.CLIENT_SECRET, callback_uri=callback_uri, scope=xero_config.XERO_SCOPE)
        url = credentials.generate_url()
        return werkzeug.utils.redirect(url)

    @http.route('/xero/callback', auth='public', type='http')
    def xero_callback(self, *ar, **kw):
        xero_config = XeroConfig()
        if 'code' in kw:
            code = kw['code']
            token = self.token_fetch(code=code)
            if token:
                token["expires_at"] = time.time() + token['expires_in']
                credentials = OAuth2Credentials(xero_config.CLIENT_ID, xero_config.CLIENT_SECRET, token=token, scope=xero_config.XERO_SCOPE)
                if credentials.expired():
                    credentials.refresh()
                    # save token
                shop_url = ''
                if credentials.token:
                    token = json.dumps(credentials.token)
                    if 'shop_url' in request.session:
                        shop_url = request.session.get('shop_url')
                shopify_store = request.env['shopify.store'].sudo().search([('shopify_url','=',shop_url)],limit=1)
                if shopify_store.xero_token != token:
                    shopify_store.sudo().write({'xero_token':token})

                credentials.set_default_tenant()
                # xero = Xero(credentials)
                # accounts = xero.accounts.filter(Status='ACTIVE')
                # if accounts:
                #     self.fetch_accounts(accounts)
                if shopify_store.api_key:
                    URL = 'https://%s/admin/apps/%s' % (shop_url, shopify_store.api_key)
                    return werkzeug.utils.redirect(URL)

    def token_fetch(self,code):
        xero_config = XeroConfig()
        url = xero_config.XERO_OAUTH2_TOKEN_URL
        b64_id_secret = base64.b64encode(bytes(xero_config.CLIENT_ID + ':' + xero_config.CLIENT_SECRET, 'utf-8')).decode('utf-8')
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "authorization": "Basic " + b64_id_secret,
        }
        redirect_uri = xero_config.CALLBACK_URL
        data = {
            'grant_type':'authorization_code',
            'code':code,
            'redirect_uri': redirect_uri,
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        content = response.json()
        return content

    # def get_xero(self):
    #     xero_config = XeroConfig()
    #     shop_url = ''
    #     if 'shop_url' in request.session:
    #         shop_url = request.session.get('shop_url')
    #     xero_app = request.env['shopify.store'].sudo().search([('shopify_url', '=', shop_url)], limit=1)
    #     if xero_app.xero_token:
    #         token = json.loads(xero_app.xero_token)
    #         credentials = OAuth2Credentials(xero_config.CLIENT_ID, xero_config.CLIENT_SECRET, token=token,
    #                                         scope=token['scope'])
    #         if credentials.expired():
    #             credentials.refresh()
    #         if credentials.token:
    #             token = json.dumps(credentials.token)
    #             if xero_app.xero_token != token:
    #                 xero_app.sudo().write({'xero_token': token})
    #         credentials.set_default_tenant()
    #         xero = Xero(credentials)
    #         return xero
    #     else:
    #         return False

    # def fetch_accounts(self, accounts):
    #     for account in accounts:
    #         if account['Type'] in ['SALES', 'REVENUE', 'BANK', 'CURRLIAB', 'EQUITY']:
    #             if account['Type'] in ['BANK', 'CURRLIAB', 'EQUITY'] and account['EnablePaymentsToAccount'] != True:
    #                 continue
    #             vals = {
    #                 'name': account['Code'] + ' - ' + account['Name'],
    #                 'code': account['Code'],
    #                 'type': account['Type'],
    #             }
    #             account_existed = request.env['xero.account'].sudo().search([('code', '=', account['Code'])])
    #             if not account_existed:
    #                 request.env['xero.account'].sudo().create(vals)
    #             else:
    #                 request.env['xero.account'].sudo().write(vals)
