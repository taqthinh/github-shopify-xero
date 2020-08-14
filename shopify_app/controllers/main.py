from odoo import http
from odoo.http import request
import werkzeug
import requests
import json
import maya
from .shopify import ShopifyController
from .xero import XeroController
from ..models.xero_auth import XeroConfig, XeroAuth
from ..models.shopify_auth import ShopifyConfig, ShopifyAuth
from profilehooks import profile
from datetime import datetime, timedelta, date
import calendar
from urllib.parse import urlencode
import logging
import traceback
_logger = logging.getLogger(__name__)


class MainController(http.Controller):

    # @check_connect
    @http.route('/index', auth='public', type='http', csrf=False)
    def index(self, **kw):
        sale_accounts = []
        payment_accounts = []
        shipping_accounts = []
        shop_url = request.session['shop_url']
        if shop_url:
            request.session['shop_url'] = shop_url
            shopify_store = request.env['shopify.store'].sudo().search([('shopify_url', '=', shop_url)], limit=1)
            xero = shopify_store.get_xero_session()
            accounts = xero.accounts.filter(Status='ACTIVE')
            for account in accounts:
                if account['Type'] in ['SALES', 'REVENUE']:
                    sale_accounts.append({
                        'name': account['Code'] + ' - ' + account['Name'],
                        'code': account['Code'],
                    })
                    shipping_accounts.append({
                        'name': account['Code'] + ' - ' + account['Name'],
                        'code': account['Code'],
                    })
                if account['Type'] == 'BANK' or account['EnablePaymentsToAccount']:
                    payment_accounts.append({
                        'name': account['Code'] + ' - ' + account['Name'],
                        'code': account['Code'],
                    })

            plans = request.env['app.plan'].sudo().search([])
            logs = request.env['app.log'].sudo().search([('shopify_store', '=', shopify_store.id)], limit=10, order='create_date desc')
            organisation_name = ''
            if xero:
                organisation_name = xero.organisations.filter()[0]['Name']
            if shopify_store:
                context = {
                    'shop_url': shop_url,
                    'shopify_store': shopify_store,
                    # 'accounts': accounts,
                    'sale_accounts': sale_accounts,
                    'shipping_accounts': shipping_accounts,
                    'payment_accounts': payment_accounts,
                    'plans': plans,
                    'logs': logs,
                    'organisation_name': organisation_name,
                }
                return request.render('shopify_app.index', context)
        else:
            _logger.info('HAS NO SHOP_URL')

    @http.route('/save_settings', auth='public', type='http', csrf=False)
    def save_settings(self, **kw):
        shop_url = ShopifyController().get_shop_url()
        if shop_url:
            shopify_store = request.env['shopify.store'].sudo().search([('shopify_url', '=', shop_url)])
            if shopify_store:
                sale_account = shopify_store.sale_account
                if 'sale_account' in kw:
                    sale_account = kw['sale_account']
                shipping_account = shopify_store.shipping_account
                if 'shipping_account' in kw:
                    shipping_account = kw['shipping_account']
                payment_account = shopify_store.payment_account
                if 'payment_account' in kw:
                    payment_account = kw['payment_account']
                auto_sync = False
                cron_job = request.env.ref('shopify_app.sync_data_to_xero')
                if cron_job:
                    if 'auto_sync' in kw:
                        auto_sync = True
                    else:
                        auto_sync = False
                else:
                    _logger.error('These is no cron job.')
                vals = {
                    'sale_account': sale_account,
                    'shipping_account': shipping_account,
                    'payment_account': payment_account,
                    'auto_sync': auto_sync,
                }
                shopify_store.sudo().write(vals)
                return werkzeug.utils.redirect('/index?shop_url=%s' % shop_url)

    # @profile(immediate=True)
    @http.route('/sync_to_xero', auth='public', type='http', csrf=False)
    def sync_to_xero(self, **kw):
        # execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        shop_url = ShopifyController().get_shop_url()
        if shop_url:
            shopify_store = request.env['shopify.store'].sudo().search([('shopify_url', '=', shop_url)], limit=1)
            if shopify_store.xero_token:
                account = shopify_store.check_account()
                if not account:
                    return werkzeug.utils.redirect('/index?' + urlencode({'error_message': 'Please save your settings'}))
                from_date = ''
                to_date = ''
                if 'from_date' in kw:
                    from_date = kw['from_date']
                if 'to_date' in kw:
                    to_date = kw['to_date']
                date_valid = self.is_date_valid(from_date,to_date)
                if not date_valid:
                    return werkzeug.utils.redirect('/index?' + urlencode({'error_message': 'Error: Invalid date'}))
                else:
                    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log = {'shopify_store': shopify_store.id,}
                    try:
                        # massage = ''
                        from_date ,to_date = self.convert_date_format(from_date=from_date,to_date=to_date)
                        pass_contact = shopify_store.pass_contact_to_xero(from_date=from_date, to_date=to_date)
                        # if not pass_contact:
                        #     massage = massage + 'ERROR: SYNC CONTACT \n'
                        pass_product = shopify_store.pass_product_to_xero(from_date=from_date, to_date=to_date)
                        # if not pass_product:
                        #     massage = massage + 'ERROR: SYNC PRODUCT \n'
                        success = shopify_store.pass_order_to_xero(from_date=from_date, to_date=to_date)
                        # if not success:
                        #     massage = massage + 'ERROR: SYNC ORDER \n'
                        finish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        log['execution_time'] = execution_time
                        log['finish_time'] = finish_time
                        log['status'] = "Success"
                        log['message'] = "Ok"
                        request.env['app.log'].sudo().create(log)
                    except Exception as e:
                        log['status'] = "Failed"
                        log['message'] = "Error: " + str(e)
                        log['stack_trace'] = traceback.format_exc()
                        request.env['app.log'].sudo().create(log)
                    return werkzeug.utils.redirect('/index?shop_url=%s'%shop_url)
            else:
                _logger.error('HAS NO XERO TOKEN')
        else:
            _logger.error('HAS NO SHOP_URL')

    @http.route('/disconnect', auth='public', type='http', csrf=False)
    def disconnect_xero(self, **kw):
        shop_url = ShopifyController().get_shop_url()
        if shop_url:
            shopify_store = request.env['shopify.store'].sudo().search([('shopify_url', '=', shop_url)], limit=1)
            shopify_store.sudo().write({
                'auto_sync': False,
                'xero_token': None,
            })
            return werkzeug.utils.redirect('/index?shop_url=%s' % shop_url)

    @http.route('/sign_up/<int:plan_id>', auth='public', type='http', csrf=False)
    def sign_up_plan(self, plan_id, **kw):
        shop_url = ''
        if 'shop_url' in kw:
            shop_url = kw['shop_url']
        shopify_store = request.env['shopify.store'].sudo().search([('shopify_url', '=', shop_url)])
        shopify = shopify_store.get_shopify_session(shopify_url=shopify_store.shopify_url, shopify_token=shopify_store.shopify_token)
        plan = request.env['app.plan'].sudo().search([('id', '=', plan_id)])
        if plan:
            plan_data = {
                    "name": plan.name,
                    'price': plan.cost,
                    "return_url": ShopifyConfig.BASE_URL + '/approve',
                    "test": True
                }
            shop_new_plan = shopify.RecurringApplicationCharge.create(plan_data)
            return werkzeug.utils.redirect(shop_new_plan.confirmation_url)
        else:
            _logger.error("Sign Up: Invalid plan")

    @http.route('/approve', auth='public', type='http', csrf=False)
    def approve(self, **kw):
        shop_url = ShopifyController().get_shop_url()
        if shop_url:
            shopify_store = request.env['shopify.store'].sudo().search([('shopify_url', '=', shop_url)])
            shopify = shopify_store.get_shopify_session(shopify_url=shopify_store.shopify_url,
                                                        shopify_token=shopify_store.shopify_token)
            if shopify:
                charge = shopify.RecurringApplicationCharge.find(kw['charge_id'])
                shopify.RecurringApplicationCharge.activate(charge)
                plan_id = request.env['app.plan'].sudo().search([('name', 'like', charge.name),('cost', '=', charge.price)], limit=1).id
                if plan_id:
                    shopify_store.sudo().write({
                        'plan': plan_id,
                        'charge_id': charge.id,
                    })
                    URL = 'https://%s/admin/apps/%s' % (shop_url, shopify_store.api_key)
                    return werkzeug.utils.redirect(URL)
                else:
                    _logger.error("Approve Plan: Invalid plan")

    def is_date_valid(self,from_date,to_date):
        date_format = "%m/%d/%Y"
        a = datetime.strptime(from_date, date_format)
        b = datetime.strptime(to_date, date_format)
        delta = b - a
        if delta.days < 0:
            return False
        else:
            return True

    def convert_date_format(self, from_date, to_date):
        date_format = "%m/%d/%Y"
        from_date = datetime.strptime(from_date, date_format)
        from_date = from_date.strftime('%Y-%m-%d')
        to_date = datetime.strptime(to_date, date_format)
        # add 1 more day to to_date for call api
        to_date += timedelta(days=1)
        to_date = to_date.strftime('%Y-%m-%d')
        return from_date,to_date

