from odoo import api, fields, models, _
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError
import calendar
import maya
import logging
from profilehooks import profile
import requests
import json
import traceback
from ..controllers.auth import ShopifySession, XeroSession
import shopify
from .xero_sync_models import XeroContact, XeroProduct, XeroOrder
_logger = logging.getLogger(__name__)


class ShopifyStore(models.Model):
    _name = 'shopify.store'
    _description = 'Shopify Store'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'shopify_url'

    def _default_plan(self):
        return self.env['app.plan'].search([('cost', '=', 0)], limit=1).id

    shopify_token = fields.Char(string="Shopify Token", index=True)
    shopify_url = fields.Char(string="Shopify URL", index=True)
    xero_token = fields.Text(string="Xero Token")
    orders_synced = fields.Integer(string="Orders Synced This Month", default=0)
    charge_id = fields.Char(string="Shopify Charge ID")

    sale_account = fields.Char(string="Xero Sale Account")
    shipping_account = fields.Char(string="Xero Shipping Account")
    payment_account = fields.Char(string="Xero Payment Account")
    auto_sync = fields.Boolean(string='Automatically Sync', index=True)
    plan = fields.Many2one('app.plan',string='Current Plan', default=_default_plan)
    xero_session = None
    shopify_session = None

    def switch_status(self, status):
        switcher = {
            'pending': 'SUBMITTED',
            'authorized': 'AUTHORISED',
            'partially_paid': 'AUTHORISED',
            'paid': 'AUTHORISED',
            'partially_refunded': 'AUTHORISED',
            'refunded': 'AUTHORISED',
        }
        return switcher.get(status,"DELETED")

    def sync_to_xero_cron(self):
        _logger.info('Start Sync data to Xero')
        shops = self.search([('auto_sync', '=', True), ('xero_token','!=', False),('shopify_token','!=', False)])
        for shop in shops:
            shop._init_access()  # creat shopifysession xerosession
            shop.shopify_session.check_access(raise_exception_on_failure=True)
            last_sync = self.env['app.log'].sudo().search([('shopify_store', '=',shop.id),('execution_time', '!=', False)],order='execution_time desc', limit=1).execution_time
            if not last_sync:
                last_sync = datetime.now()
            interval_number = int(shop.plan.interval_number)
            next_call = (last_sync + timedelta(hours=interval_number)).strftime('%Y-%m-%d %H:%M:%S')
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if now >= next_call:
            # if now < next_call:  # for test
                log = {'shopify_store': shop.id,
                       'is_cron': True}
                try:
                    has_account = shop.check_account()
                    if not has_account:
                        raise Exception('Accounts is missing')
                    shop._init_access()  # creat shopifysession xerosession
                    shop.shopify_session.check_access(raise_exception_on_failure=True)
                    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    to_date = (last_sync + timedelta(days=1)).strftime('%Y-%m-%d')
                    from_date = last_sync.strftime('%Y-%m-%d')
                    shop.sync_data(from_date=from_date, to_date=to_date)
                    finish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log['execution_time'] = execution_time
                    log['finish_time'] = finish_time
                    log['status'] = "Success"
                    log['message'] = "Ok"
                    self.env['app.log'].sudo().create(log)
                    # shop.shopify_session.delete_session()
                except Exception as e:
                    log['status'] = "Failed"
                    log['message'] = "Error: "+ str(e)
                    log['stack_trace'] = traceback.format_exc()
                    self.env['app.log'].sudo().create(log)
                    # shop.shopify_session.delete_session()
        _logger.info('Stop Sync data to Xero')

    def sync_data(self, from_date, to_date):
        self.ensure_one()
        dict = {
            'updated_at_min': from_date,
            'updated_at_max': to_date
        }
        XeroContact().add_filter(dict)
        # XeroContact().sync()
        # XeroProduct().sync()
        XeroOrder().add_filter(dict)
        XeroOrder().sync()
        print('abc')
        # self.pass_contact_to_xero(from_date=from_date, to_date=to_date)
        # self.pass_product_to_xero(from_date=from_date, to_date=to_date)
        # self.pass_order_to_xero(from_date=from_date, to_date=to_date)

    def pass_contact_to_xero(self, from_date, to_date):
        customers = shopify.Customer.find(updated_at_min=from_date, updated_at_max=to_date)
        if customers:
            try:
                vals_list = self.customer_vals_list(customers)
                xero = XeroSession().get_xero_connector()
                xero.contacts.save(vals_list)
                return True
            except Exception as e:
                pass

    def customer_vals_list(self,customers):
        vals_list = []
        for customer in customers:
            vals = {
                "Name": '%s %s - Shopify (%s)' % (customer.first_name, customer.last_name, customer.id),
                "ContactNumber": customer.id,
                "IsSupplier": False,
                "IsCustomer": True,
                "FirstName": customer.first_name,
                "LastName": customer.last_name,
                "EmailAddress": customer.email,
                "ContactPersons": [
                    {
                        "FirstName": customer.first_name,
                        "LastName": customer.last_name,
                        "EmailAddress": customer.email,
                        "IncludeInEmails": True,
                    }
                ],
                "Phones": [
                    {
                        "PhoneType": "DEFAULT",
                        "PhoneNumber": customer.phone,
                    }, {
                        "PhoneType": "FAX"
                    }, {
                        "PhoneType": "MOBILE"
                    }, {
                        "PhoneType": "DDI"
                    }
                ],
            }
            vals_list.append(vals)
        if vals_list:
            return vals_list

    def pass_product_to_xero(self, from_date, to_date):
        products = shopify.Product.find(updated_at_min=from_date, updated_at_max=to_date)
        vals_list = []
        if products:
            sale_account = self.sale_account
            if sale_account:
                for product in products:
                    for variant in product.variants:
                        if variant.fulfillment_service == 'gift_card':
                            if not self.plan.sync_giftcard:
                                continue
                        vals = self.product_vals(product, variant, sale_account)
                        vals_list.append(vals)
                if vals_list:
                    try:
                        xero = XeroSession().get_xero_connector()
                        xero.items.save(vals_list)
                        return True
                    except Exception as e:
                        pass

    def product_vals(self,product, variant, sale_account):
        varitant_title = variant.title
        if varitant_title == 'Default Title':
            varitant_title = ''
        vals = {
            "Code": variant.id,
            "Name": product.title + ' ' + varitant_title.upper(),
            "Description": product.title + ' ' + varitant_title.upper(),
            "PurchaseDetails": {
                "COGSAccountCode": "300"
              },
            "SalesDetails": {
                "UnitPrice": int(variant.price),
                "AccountCode": sale_account,
            },
            "IsTrackedAsInventory": True,
            "InventoryAssetAccountCode": "630",
            "QuantityOnHand": variant.inventory_quantity,  # cant pass on hand ????
            "IsSold": True,
        }
        if vals:
            return vals

    def pass_order_to_xero(self, from_date, to_date):
        xero = XeroSession().get_xero_connector()
        if xero:
            if not self.orders_synced >= self.plan.order_number or self.plan.is_unlimited:
                orders = shopify.Order.find(updated_at_min=from_date, updated_at_max=to_date)
                while True:
                    vals_list = []
                    if orders:
                        for order in orders:
                            line_items_vals = []
                            vals = self.order_vals(order)
                            vals['Contact'] = self.add_contact_vals(order)
                            # ALl discount: free ship, fixed, perentage
                            if order.discount_applications:
                                line_items_vals = self.get_all_order_discount(order=order)
                            # Add shipping fee
                            if order.shipping_lines:
                                shipping_item_vals = self.add_shiping_item(order=order)
                                line_items_vals.append(shipping_item_vals)
                            # Add Tip item
                            if order.total_tip_received:
                                total_tip = int(float(order.total_tip_received))
                                if total_tip > 0:
                                    tip_vals = self.add_tip(total_tip)
                                    line_items_vals.append(tip_vals)
                            # order line vals
                            for line_item in order.line_items:
                                line_vals = self.order_line_vals(line_item)
                                if line_vals:
                                    line_items_vals.append(line_vals)
                            vals['LineItems'] = line_items_vals
                            vals_list.append(vals)
                        # Pass orders
                        invoices = ''
                        if vals_list:
                            successful_records = 0
                            try:
                                invoices = xero.invoices.save(vals_list)
                            except Exception as e:
                                try:
                                    if hasattr(e, 'response') and hasattr(e.response, 'text'):
                                        response = json.loads(e.response.text)
                                        if 'Elements' in response:
                                            failed_records = len(response['Elements'])
                                            requested_records = len(vals_list)
                                            successful_records = requested_records - failed_records
                                except Exception as e:
                                    _logger.error(_logger.error(traceback.format_exc()))
                            if successful_records > 0:
                                self.env['order.request.log'].sudo().create({
                                    'shopify_store': self.id,
                                    'order_count': successful_records
                                })
                                self.update_order_synced_number()
                        # pass payment or refund AFTER create Invoice, need InvoiceNumber
                        list_payment_vals = []
                        list_refund_vals = []
                        list_allocate_refund_vals = []
                        for order in orders:
                            invoice_number = "Shopify: " + str(order.id)
                            if order.financial_status in ['paid', 'refunded','partially_refunded']:
                                transactions = shopify.Transaction.find(order_id=order.id)
                                if transactions:
                                    payment_vals = self.get_payment_vals(invoice_number=invoice_number, transactions=transactions)
                                    if payment_vals:
                                        list_payment_vals.append(payment_vals)
                            if self.plan.sync_refund:
                                if order.financial_status in ['refunded', 'partially_refunded']: #  'partially_refunded'
                                    refund_vals = self.get_refund_vals(order=order, invoice_number=invoice_number)
                                    if refund_vals:
                                        list_refund_vals.append(refund_vals)
                                    payment_refund_vals = self.get_payment_refund_vals(order=order)
                                    if payment_refund_vals:
                                        list_allocate_refund_vals.append(payment_refund_vals)
                        if list_payment_vals:
                            try:
                                xero.payments.save(list_payment_vals)
                            except Exception as e:
                                pass
                        if list_refund_vals:
                            try:
                                xero.creditnotes.save(list_refund_vals)
                            except Exception as e:
                                pass
                        if list_allocate_refund_vals:
                            try:
                                xero.payments.save(list_allocate_refund_vals)
                            except Exception as e:
                                pass
                        if orders.has_next_page():
                            orders = orders.next_page()
                        else:
                            break
                        return True
                return True      # FINAL

    def get_all_order_discount(self, order):
        line_items_vals = []
        for discount_application in order.discount_applications:
            if order.discount_codes:
                for discount_code in order.discount_codes:
                    if discount_application.target_selection == 'all' or discount_application.target_selection == 'entitled':
                        if discount_code.type == 'shipping':
                            free_ship_item_vals = self.add_free_ship_item(order)
                            line_items_vals.append(free_ship_item_vals)
                        elif discount_code.type == 'fixed_amount':
                            fixed_amount_vals = self.add_discount_amount(order)
                            line_items_vals.append(fixed_amount_vals)
                        elif discount_code.type == 'percentage':
                            percentage_amount_vals = self.add_discount_percentage(order)
                            line_items_vals.append(percentage_amount_vals)
            else:
                if discount_application.type == 'automatic':
                    if discount_application.target_selection == 'all' or discount_application.target_selection == 'entitled':
                        if discount_application.allocation_method == 'across':  # differ with buy 1 get 1
                            if discount_application.value_type == 'fixed_amount':
                                auto_discount_fixed_vals = self.auto_discount_fixed(order)
                                line_items_vals.append(auto_discount_fixed_vals)
                            elif discount_application.value_type == 'percentage':
                                auto_discount_percentage_vals = self.auto_discount_percentage(order)
                                line_items_vals.append(auto_discount_percentage_vals)
        return line_items_vals

    def order_vals(self, order ,status=None):
        # get duedate
        duedate = maya.parse(order.updated_at).datetime()
        vals = {
            "Type": "ACCREC",
            "DateString": order.created_at,
            "DueDate": duedate,
            "InvoiceNumber": "Shopify: " + str(order.id),
            "Reference": order.name,
            # "CurrencyCode": order.presentment_currency,
            "LineAmountTypes": "Inclusive" if order.taxes_included else "Exclusive",
            "SubTotal": order.subtotal_price,
            "TotalTax": order.total_tax,
            "Total": order.total_price,
        }
        if not status:
            if order.financial_status:
                status = self.switch_status(order.financial_status)
                vals.update({'Status': status})
        if vals:
            return vals

    def add_contact_vals(self, order):
        contact_vals = {}
        if 'customer' in order.attributes:
            contact_vals = {
                "ContactNumber": order.customer.id,
            }
        else:
            contact_vals = {
                "ContactNumber": order.user_id,
                "Name": 'Shopify User: '+ str(order.user_id),
            }
        return contact_vals

    def add_free_ship_item(self, order, sale_account=None):
        if not sale_account:
            sale_account = self.sale_account
        free_ship_item_vals = {
            "Description": "Free Ship",
            "UnitAmount": str(-int(order.discount_codes[0].amount)),
            "Quantity": 1,
            "TaxType": "NONE",
            "AccountCode": sale_account,
        }
        if free_ship_item_vals:
            return free_ship_item_vals

    def add_discount_amount(self, order, sale_account=None):
        if not sale_account:
            sale_account = self.sale_account
        fixed_amount_vals = {
            "Description": "Discount Code: Fixed Amount",
            "UnitAmount": str(-int(order.discount_codes[0].amount)),
            "Quantity": 1,
            "TaxType": "NONE",
            "AccountCode": sale_account,
        }
        if fixed_amount_vals:
            return fixed_amount_vals

    def add_discount_percentage(self, order, sale_account=None):
        if not sale_account:
            sale_account = self.sale_account
        percentage_amount_vals = {
            "Description": "Discount Code: Percentage",
            "UnitAmount": str(-int(order.discount_codes[0].amount)),
            "Quantity": 1,
            "TaxType": "NONE",
            "AccountCode": sale_account,
        }
        if percentage_amount_vals:
            return percentage_amount_vals

    def auto_discount_fixed(self, order, sale_account=None):
        if not sale_account:
            sale_account = self.sale_account
        auto_discount_vals = {
            "Description": "Auto Discount Amount",
            "UnitAmount": str(-int(order.total_discounts)),
            "Quantity": 1,
            "TaxType": "NONE",
            "AccountCode": sale_account,
        }
        if auto_discount_vals:
            return auto_discount_vals

    def auto_discount_percentage(self, order, sale_account=None):
        if not sale_account:
            sale_account = self.sale_account
        auto_discount_vals = {
            "Description": "Auto Discount Pecentage",
            "UnitAmount": str(-int(order.total_discounts)),
            "Quantity": 1,
            "TaxType": "NONE",
            "AccountCode": sale_account,
        }
        if auto_discount_vals:
            return auto_discount_vals

    def add_shiping_item(self, order, shipping_account=None):
        if not shipping_account:
            shipping_account = self.shipping_account
        shipping_item_vals = {
            "Description": 'Shipping: ' + order.shipping_lines[0].title,
            "UnitAmount": order.shipping_lines[0].price,
            "Quantity": 1,
            "AccountCode": shipping_account,
        }
        tax_type = ''
        tax_amount = ''
        for shipping_line in order.shipping_lines:
            if not shipping_line.tax_lines:
                tax_type = 'NONE'
            else:
                for tax_line in shipping_line.tax_lines:
                    tax_amount += tax_line.price
        if tax_type:
            shipping_item_vals.update({
                "TaxType": tax_type,
            })
        else:
            if tax_amount:
                shipping_item_vals.update({
                    "TaxAmount": tax_amount,
                })
        return shipping_item_vals

    def add_tip(self, total_tip, sale_account=None):
        if not sale_account:
            sale_account = self.sale_account
        tip_vals = {
            "Description": 'Tip',
            "UnitAmount": total_tip,
            "Quantity": 1,
            "AccountCode": sale_account,
            "TaxType": "NONE",
        }
        return tip_vals

    def order_line_vals(self, line_item, sale_account=None):
        discount_amount = 0
        if line_item.total_discount:
            discount_amount = int(line_item.total_discount)
        if not sale_account:
            sale_account = self.sale_account
        tax_line_amount = 0
        if line_item.tax_lines:
            for tax_line in line_item.tax_lines:
                tax_line_amount += int(tax_line.price)
        line_vals = {}
        if line_item.variant_id:
            line_vals = {
                "Description": line_item.name,
                "UnitAmount": int(line_item.price),
                "ItemCode": line_item.variant_id,
                "Quantity": line_item.quantity,
                "TaxAmount": tax_line_amount,
                "AccountCode": sale_account,
            }
        if discount_amount > 0:
            line_vals.update({
                "DiscountAmount": discount_amount,
            })
        return line_vals

    def get_payment_vals(self, invoice_number, transactions, payment_account=None):
        if not payment_account:
            payment_account = self.payment_account
        transaction_amount = 0
        transaction_date = ''
        if transactions:
            for transaction in transactions:
                if transaction.kind in ['sale', 'capture'] and transaction.status == 'success':
                    transaction_amount += int(transaction.amount)
                    transaction_date = maya.parse(transaction.processed_at).datetime()
        payment_vals = {
            "Type": "ACCREC",
            "Invoice": {"InvoiceNumber": invoice_number, },
            "Account": {"Code": payment_account},
            # "Date": "2009-09-08",
            "Date": transaction_date,
            "Amount": str(transaction_amount),
        }
        # payments = xero.payments.save(payment_vals)
        if payment_vals:
            return payment_vals

    def check_account(self):
        if not self.sale_account or not self.payment_account or not self.shipping_account:
            return False
        else:
            return True

    def get_refund_vals(self, order, invoice_number):
        payment_account = self.payment_account
        created_at = ''
        total_amount = 0
        message = ''
        line_items_vals = []
        if order.refunds:
            for refund in order.refunds:
                created_at = maya.parse(refund.created_at).datetime()
                for transaction in refund.transactions:
                    total_amount += int(transaction.amount)
                    message = transaction.message
        line_vals = {
            'Description': '%s: %s' % (invoice_number,message),
            'Quantity': 1.0000,
            'UnitAmount': total_amount,
            'AccountCode': payment_account,
            'TaxType': 'NONE',
            'TaxAmount': 0
        }
        line_items_vals.append(line_vals)
        refund_vals = {
            'Type': 'ACCPAYCREDIT',
            'Status': 'AUTHORISED',
            # 'CurrencyCode': order.presentment_currency,
            'CreditNoteNumber': 'SC-%s'%(order.number),
            'Contact': {'ContactNumber': order.customer.id if 'customer' in order.attributes else order.user_id},
            'Date': created_at,
            'LineAmountTypes': 'Exclusive',
            'LineItems': line_items_vals,
        }
        if refund_vals:
            return refund_vals

    def get_payment_refund_vals(self, order):
        created_at = ''
        total_amount = 0
        if order.refunds:
            for refund in order.refunds:
                created_at = maya.parse(refund.created_at).datetime()
                for transaction in refund.transactions:
                    total_amount += int(transaction.amount)
        payment_refund_vals = {
            'Type': 'ARCREDITPAYMENT',
            'CreditNote': {
                'CreditNoteNumber': 'SC-%s'%(order.number),
            },
            'Account': {
                'Code': self.payment_account,
            },
            'Date': created_at,
            'Amount': total_amount,
            "CurrencyRate": 1,
        }
        if payment_refund_vals:
            return payment_refund_vals

    def check_shop_plan_cron(self):
        _logger.info('Start checking plan Xero Shopify')
        shops = self.search([('shopify_token', '!=', False), ('xero_token', '!=', False)])
        for shop in shops:
            log = {'shopify_store': shop.id,
                   'is_cron': True}
            try:
                shop._init_access() #creat shopifysession xerosession
                shop.shopify_session.check_access(raise_exception_on_failure=True)
                execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                shop.check_current_plan()
                finish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log['execution_time'] = execution_time
                log['finish_time'] = finish_time
                log['status'] = "Success"
                log['message'] = "Ok(1)"
                self.env['app.log'].sudo().create(log)
                shop.shopify_session.delete_session()
            except Exception as e:
                log['status'] = "Failed"
                log['message'] = "Error (1): " + str(e)
                log['stack_trace'] = traceback.format_exc()
                self.env['app.log'].sudo().create(log)
                shop.shopify_session.delete_session()
        _logger.info('Stop checking plan Xero Shopify')

    def check_current_plan(self):
        current_plan = shopify.RecurringApplicationCharge.current()
        if not current_plan:
            default_plan_id = self.env['app.plan'].sudo().search([], order='cost asc', limit=1).id
            self.plan = default_plan_id
            self.charge_id = None
            return
        else:
            if self.plan.cost != current_plan.price or not self.plan:
                plan_id = self.env['app.plan'].sudo().search([('cost', '=', current_plan.price)], limit=1).id
                self.plan = plan_id
                self.charge_id = current_plan.id
                return

    def update_order_synced_number(self):
        first_day, last_day = self.get_month_range()
        order_request_logs = self.env['order.request.log'].sudo().search([('shopify_store','=', self.id),
                                                                                ('sync_date', '>=' , first_day),
                                                                                ('sync_date', '<=' , last_day),])
        order_synced_number = 0
        if order_request_logs:
            for order_request_log in order_request_logs:
                order_synced_number += order_request_log.order_count
        if order_synced_number:
            self.orders_synced = order_synced_number

    def get_month_range(self):
        today = date.today()
        first_day = today.replace(day=1)
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        return first_day, last_day

    def clear_shopify_token(self):
        self.shopify_token = None

    def clear_xero_token(self):
        self.xero_token = None

    def _init_access(self):
        self._init_shopify_access()
        self._init_xero_access()

    def _init_shopify_access(self):
        if not self.shopify_token:
            raise Exception('Shopify Token is missing')
        self.shopify_session = ShopifySession(shop_url=self.shopify_url, token=self.shopify_token, env=self.env)

    def _init_xero_access(self):
        if not self.xero_token:
            raise Exception('Xero Token is missing')
        self.xero_session = XeroSession(token=self.xero_token, env=self.env)
