from odoo import api, fields, models, _
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError
import calendar
import maya
import logging
from profilehooks import profile
import requests
import json
from .shopify_auth import ShopifyAuth
_logger = logging.getLogger(__name__)
import traceback

class ShopifyStore(models.Model):
    _name = 'shopify.store'
    _description = 'Shopify Store'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'shopify.auth', 'xero.auth']
    _rec_name = 'shopify_url'

    def _default_plan(self):
        return self.env['app.plan'].search([('cost', '=', 0)], limit=1).id

    # shop_name = fields.Char('Shop Name', index=True)
    shopify_token = fields.Char(string="Shopify Token", index=True)
    shopify_url = fields.Char(string="Shopify URL", index=True)
    api_key = fields.Char(string="Shopify API Key")
    xero_token = fields.Text(string="Xero Token")
    orders_synced = fields.Integer(string="Orders Synced This Month", default=0)
    charge_id = fields.Char(string="Shopify Charge ID")

    sale_account = fields.Char(string="Xero Sale Account")
    shipping_account = fields.Char(string="Xero Shipping Account")
    payment_account = fields.Char(string="Xero Payment Account")
    auto_sync = fields.Boolean(string='Automatically Sync', index=True)
    plan = fields.Many2one('app.plan',string='Current Plan', default=_default_plan)

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
        # execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        shops = self.search([('auto_sync', '=', True), ('xero_token','!=', False),('shopify_token','!=', False)])
        for shop in shops:
            last_sync = self.env['app.log'].sudo().search([('shopify_store', '=',shop.id),('execution_time', '!=', False)],order='execution_time desc', limit=1).execution_time
            interval_number = int(shop.plan.interval_number)
            next_call = (last_sync + timedelta(hours=interval_number)).strftime('%Y-%m-%d %H:%M:%S')
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if now >= next_call:
            # if now < next_call:  # for test
                log = {'shopify_store': shop.id}
                try:
                    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    to_date = (last_sync + timedelta(days=1)).strftime('%Y-%m-%d')
                    from_date = last_sync.strftime('%Y-%m-%d')
                    pass_contact = shop.pass_contact_to_xero(from_date=from_date, to_date=to_date)
                    # if not pass_contact:
                    #     massage = massage + 'ERROR: SYNC CONTACT \n'
                    # elif pass_contact != True:
                    #     _logger.info(pass_contact)
                    pass_product = shop.pass_product_to_xero(from_date=from_date, to_date=to_date)
                    # if not pass_product:
                    #     massage = massage + 'ERROR: SYNC PRODUCT \n'
                    # elif pass_product != True:
                    #     _logger.info(pass_product)
                    pass_order = shop.pass_order_to_xero(from_date=from_date, to_date=to_date)
                    # if not pass_order:
                    #     massage = massage + 'ERROR: SYNC ORDER \n'
                    finish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log['execution_time'] = execution_time
                    log['finish_time'] = finish_time
                    log['status'] = "Success"
                    log['message'] = "Ok"
                    self.env['app.log'].sudo().create(log)
                except Exception as e:
                    log['status'] = "Failed"
                    log['message'] = "Error: "+ str(e)
                    log['stack_trace'] = traceback.format_exc()
                    self.env['app.log'].sudo().create(log)

    def pass_contact_to_xero(self, from_date, to_date):
        shopify = self.get_shopify_session(shopify_url=self.shopify_url,shopify_token=self.shopify_token)
        vals_list = []
        if shopify:
            customers = shopify.Customer.find(updated_at_min=from_date, updated_at_max=to_date)
            if customers:
                try:
                    vals_list = self.customer_vals_list(customers)
                    xero = self.get_xero_session()
                    xero.contacts.save(vals_list)
                    _logger.info('PASS CONTACT SUCCESS')
                    return True
                except Exception as e:
                    _logger.error('ERROR PASS CONTACT: %s', e)
            else:
                _logger.info('NO CONTACT TO PASS')
                return True

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
                # "Phones": customer.phone,
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
        shopify = self.get_shopify_session(shopify_url=self.shopify_url, shopify_token=self.shopify_token)
        vals_list = []
        if shopify:
            products = shopify.Product.find(updated_at_min=from_date, updated_at_max=to_date)
            # get product sale_account
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
                    try:
                        xero = self.get_xero_session()
                        xero.items.save(vals_list)
                        _logger.info('PASS PRODUCT SUCCESS')
                        return True
                    except Exception as e:
                        _logger.error('ERROR PASS PRODUCT: %s', e)
                else:
                    _logger.error('HAVE NO SALE ACCOUNT')
            else:
                _logger.info('NO PRODUCT TO PASS')
                return True

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
        xero = self.get_xero_session()
        # vals_list = []
        if xero:
            if not self.orders_synced >= self.plan.order_number or self.plan.is_unlimited:
                shopify = self.get_shopify_session(shopify_url=self.shopify_url, shopify_token=self.shopify_token)
                # invoices = self.get_invoices(from_date=from_date, to_date=to_date, xero=xero)
                orders = shopify.Order.find(updated_at_min=from_date, updated_at_max=to_date)
                while True:
                    vals_list = []
                    if orders:
                        for order in orders:
                            status = ''
                            # invoice = [invoice for invoice in invoices if invoice["InvoiceNumber"] == "Shopify: " + str(order.id)]
                            # if invoice:
                                # invoice = invoice[0]
                                # if invoice['Status'] == 'PAID':
                                # continue
                            # order vals
                                # add contact
                            vals = self.order_vals(order, status=status)
                            contact_vals = self.add_contact_vals(order)
                            if contact_vals:
                                vals['Contact'] = contact_vals
                            else:
                                _logger.error('HAVE NO ORDER CONTACT')
                            # ALl discount: free ship, fixed, perentage
                            line_items_vals = []
                            if order.discount_applications:
                                line_items_vals = self.get_all_order_discount(order=order)
                            # Add shipping fee
                            if order.shipping_lines:
                                shipping_item_vals = self.add_shiping_item(order=order)
                                if shipping_item_vals:
                                    line_items_vals.append(shipping_item_vals)
                            # Add Tip item
                            if order.total_tip_received:
                                total_tip = int(float(order.total_tip_received))
                                if total_tip > 0:
                                    tip_vals = self.add_tip(total_tip)
                                    if tip_vals:
                                        line_items_vals.append(tip_vals)
                            # order line vals
                            for line_item in order.line_items:
                                discount_amount = 0
                                if line_item.total_discount:
                                    discount_amount = int(line_item.total_discount)
                                line_vals = self.order_line_vals(line_item, discount_amount)
                                if line_vals:
                                    line_items_vals.append(line_vals)
                            vals['LineItems'] = line_items_vals
                            vals_list.append(vals)
                        # Pass orders
                        invoices = ''
                        if vals_list:
                            try:
                                invoices = xero.invoices.save(vals_list)
                                # invoices_synced = self.get_invoices(from_date=first_day, to_date=last_day)
                                # self.sudo().write({'orders_synced': len(invoices)})
                                _logger.info('PASS ORDERS SUCCESS')
                            except Exception as e:
                                _logger.error('ERROR PASS ORDER: %s', e)
                        else:
                            _logger.error('NO ORDERS VALS TO PASS')
                        self.env['order.request.log'].sudo().create({
                            'shopify_store': self.id,
                            'order_count': len(vals_list)
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
                                _logger.info('CREATE PAYMENT SUCCESS')
                            except Exception as e:
                                _logger.error('ERROR CREATE PAYMENT: %s', e)
                        if list_refund_vals:
                            try:
                                xero.creditnotes.save(list_refund_vals)
                                _logger.info('CREATE REFUND SUCCESS')
                            except Exception as e:
                                _logger.error('ERROR CREATE REFUND: %s', e)
                        if list_allocate_refund_vals:
                            try:
                                xero.payments.save(list_allocate_refund_vals)
                                _logger.info('CREATE PAYMENT REFUND SUCCESS')
                            except Exception as e:
                                _logger.error('ERROR CREATE PAYMENT REFUND: %s', e)
                        if orders.has_next_page():
                            orders = orders.next_page()
                        else:
                            break
                    else:
                        _logger.info('NO ORDERS TO PASS')
                        return True
                return True      # FINAL
            else:
                _logger.error('THE ORDERS HAS REACHED THE LIMIT')

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

    # def get_month_day_range(self):
    #     today = date.today()
    #     first_day = today.replace(day=1)
    #     first_day = first_day.strftime('%Y,%m,%d')
    #     last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
    #     last_day = last_day.strftime('%Y,%m,%d')
    #     return first_day, last_day

    # def get_invoices(self, from_date, to_date, xero=None):
    #     format = ('%Y-%m-%d')
    #     check_fomat = False
    #     try:
    #         datetime.strptime(from_date, format)
    #         datetime.strptime(to_date, format)
    #         check_fomat = True
    #     except:
    #         check_fomat = False
    #     if check_fomat:
    #         from_date = datetime.strptime(from_date, format)
    #         from_date = from_date.strftime('%Y,%m,%d')
    #         to_date = datetime.strptime(to_date, format)
    #         to_date = to_date.strftime('%Y,%m,%d')
    #
    #     raw_query = 'Date >= DateTime(%s) && Date <= DateTime(%s)' % (from_date, to_date)
    #     raw_query = 'Status = "PAID"'
    #     if not xero:
    #         xero = self.get_xero_session()
    #     try:
    #         invoices = xero.invoices.filter(raw=raw_query, InvoiceNumber__startswith='Shopify: ' )
    #         # invoices = xero.invoices.filter(InvoiceNumber__startswith='Shopify: ')  # is not same update_at with shopify
    #         _logger.info('RETRIEVED INVOICES')
    #         return invoices
    #     except Exception as e:
    #         _logger.error('ERROR FETCHING INVOICES {}'.format(e))
    #         return False

    def order_vals(self, order ,status=None):
        # get duedate
        duedate = maya.parse(order.created_at).datetime()
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
        if contact_vals:
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
        if shipping_item_vals:
            return shipping_item_vals

    def add_tip(self, total_tip, sale_account=None):
        if not sale_account:
            sale_account = self.sale_account
        tip_vals ={}
        if total_tip and sale_account:
            tip_vals = {
                "Description": 'Tip',
                "UnitAmount": total_tip,
                "Quantity": 1,
                "AccountCode": sale_account,
                "TaxType": "NONE",
            }
        if tip_vals:
            return tip_vals

    def order_line_vals(self, line_item, discount_amount, sale_account=None):
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
        if discount_amount:
            line_vals.update({
                "DiscountAmount": discount_amount,
            })
        if line_vals:
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
            log = {'shopify_store': shop.id,}
            try:
                execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                shop.check_current_plan()
                finish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log['execution_time'] = execution_time
                log['finish_time'] = finish_time
                log['status'] = "Success"
                log['message'] = "Ok"
                self.env['app.log'].sudo().create(log)
            except Exception as e:
                log['status'] = "Failed"
                log['message'] = "Error (1): " + str(e)
                log['stack_trace'] = traceback.format_exc()
                self.env['app.log'].sudo().create(log)

        _logger.info('Stop checking plan Xero Shopify')

    def check_current_plan(self):
        shopify = self.get_shopify_session(shopify_url=self.shopify_url, shopify_token=self.shopify_token)
        if shopify:
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

    # def get_shopify_store(self):
    #     shop_url = ShopifyAuth().get_shop_url()
    #     if shop_url:
    #         shopify_store = request.env['shopify.store'].sudo().search([('shopify_url', '=', shop_url)], limit=1)
    #         if shopify_store:
    #             return shopify_store

# class XeroAccount(models.Model):
#     _name = 'xero.account'
#     _description = 'Xero Accounts'
#     # _inherit = ['mail.thread', 'mail.activity.mixin']
#     _order = 'code'
#
#     name = fields.Char('Account Name')
#     code = fields.Char('Account Code')
#     type = fields.Char('Account Type')
#     # active = fields.Boolean(default=True)
