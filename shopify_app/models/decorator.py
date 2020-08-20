import json
import shopify
from odoo.http import request
from werkzeug.utils import redirect
from urllib.parse import urlencode
import werkzeug
from ..controllers.auth import ShopifySession

def check_shopify_login(func):

    def wrapper(*args, **kwargs):
        if not is_shop_login(check_access=True):
            if is_xero_login():
                request.session.pop('xero', None)
            return werkzeug.utils.redirect('/shopify/login?' + urlencode(request.params))
        return func(*args, **kwargs)
    return wrapper

def check_xero_login(func):

    def wrapper(*args, **kwargs):
        if not is_xero_login():
            try:
                shopify_session = ShopifySession()
                shop_url = shopify_session.get_shop_url()
                shopify_store = request.env['shopify.store'].sudo().search([('shopify_url', '=', shop_url)], limit=1)
                if shopify_store and shopify_store.xero_token:
                    token = json.loads(shopify_store.xero_token)
                    xero_session = XeroSession(token=token)
                    return func(*args, **kwargs)
            except Exception as e:
                pass
            return request.render('shopify_app.xero_connect')
        return func(*args, **kwargs)

    return wrapper


def is_shop_login(check_access=False):
    is_shop_login = 'shopify_xero' in request.session and 'token' in request.session['shopify_xero']
    if hasattr(request, 'params') and 'shop' in request.params:
        is_shop_login = is_shop_login and request.params['shop'] == request.session['shopify_xero']['shop_url']
    if is_shop_login and check_access:
        shopify_session = ShopifySession()
        is_shop_login = is_shop_login and shopify_session.check_access()
    return is_shop_login


def is_xero_login():
    return 'xero' in request.session and 'token' in request.session['xero']


def ensure_login():
    if not (is_shop_login() and is_xero_login()):
        raise Exception('Please login before using the app.')