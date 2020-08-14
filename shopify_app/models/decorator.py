import json
import shopify
from odoo.http import request
from werkzeug.utils import redirect
from urllib.parse import urlencode
import werkzeug

def check_shopify_login(func):

    def check_shopify(*args, **kwargs):
        if 'shop_url' in request.session:
            shop_url = request.session['shop_url']
        else:
            shop_url = None
        if shop_url:
            shopify_store = request.env['shopify.store'].sudo().search([('shopify_url', '=', shop_url)])
            if not shopify_store.shopify_token:
                return werkzeug.utils.redirect('/shopify/login?' + urlencode(request.params))
            return func(*args, **kwargs)
        return func(*args, **kwargs)
    return check_shopify

def check_xero_login(func):

    def check_xero(*args, **kwargs):
        if 'shop_url' in request.session:
            shop_url = request.session['shop_url']
        else:
            shop_url = None
        if shop_url:
            shopify_store = request.env['shopify.store'].sudo().search(
                [('shopify_url', '=', shop_url)])
            if not shopify_store.xero_token:
                return request.render('shopify_app.xero_connect')
            return func(*args, **kwargs)
        return func(*args, **kwargs)
    return check_xero