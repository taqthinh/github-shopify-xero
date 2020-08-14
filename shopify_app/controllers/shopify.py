from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import shopify
import werkzeug
import requests
import json
# from .shopify_config import ShopifyConfig
from urllib.parse import urlparse, parse_qs
from .xero import XeroController
from ..models.decorator import check_xero_login, check_shopify_login
from ..models.shopify_auth import ShopifyConfig

class ShopifyController(http.Controller):

    @http.route('/shopify', type='http', auth="public")
    def index(self):
        @check_shopify_login
        @check_xero_login
        def view():
            return werkzeug.utils.redirect('/index')
        return view()

    @http.route('/shopify/login', auth='public', type='http')
    def shopify_login(self,**kw):
        # self.check_login()
        shop_url = kw['shop']
        shopify_config = ShopifyConfig()
        shopify.Session.setup(api_key=shopify_config.SHOPIFY_API_KEY, secret=shopify_config.SHOPIFY_SHARED_SECRET)
        session = shopify.Session(shop_url, shopify_config.API_VERSION)
        redirect_uri = shopify_config.CALLBACK_URL
        permission_url = session.create_permission_url(redirect_uri=redirect_uri, scope=shopify_config.SHOPIFY_SCOPE)
        return werkzeug.utils.redirect(permission_url)

    @http.route('/shopify/callback', auth='public', type='http')
    def shopify_callback(self, **kw):
        shop_url = kw['shop']
        shopify_config = ShopifyConfig()
        shopify.Session.setup(api_key=shopify_config.SHOPIFY_API_KEY, secret=shopify_config.SHOPIFY_SHARED_SECRET)
        session = shopify.Session(shop_url, shopify_config.API_VERSION)
        token = session.request_token(kw)
        if token:
            shopify.ShopifyResource.activate_session(session)
            store_vals = {
                'shopify_token': token,
                'shopify_url': shop_url,
                'api_key': shopify_config.SHOPIFY_API_KEY,
            }
            shopify_store = request.env['shopify.store'].sudo().search([('shopify_url','=',shop_url)],limit=1)
            if not shopify_store:
                shopify_store = request.env['shopify.store'].sudo().create(store_vals)
            else:
                shopify_store.sudo().write(store_vals)
            URL = 'https://%s/admin/apps/%s' % (shop_url, shopify_store.api_key)
            return werkzeug.utils.redirect(URL)

    def get_shop_url(self):
        shop_url = ''
        if 'shop_url' in request.session:
            shop_url = request.session['shop_url']
        else:
            shop_url = None
        return shop_url

# class ShopifyAuth(object):
#
#
#     def get_shop_url(self):
#         shop_url = ''
#         if 'shop_url' in request.session:
#             shop_url = request.session['shop_url']
#         else:
#             shop_url = None
#         return shop_url



