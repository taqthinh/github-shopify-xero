from odoo import api, fields, models, _


class OrderRequestLog(models.Model):
    _name = 'order.request.log'
    _description = 'Order Request Logs'
    _order = 'sync_date desc'
    _rec_name = 'shopify_store'

    shopify_store = fields.Many2one('shopify.store', string='Shopify Store', index=True)
    order_count = fields.Integer('Orders Synced Number', default=0)
    sync_date = fields.Date('Sync Time', index=True, default=fields.Date.context_today)

class AppLog(models.Model):
    _name = 'app.log'
    _description = 'Application Logs'
    _order = 'create_date desc'
    _rec_name = 'shopify_store'

    shopify_store = fields.Many2one('shopify.store', string='Shopify Store' , index=True)
    # shopify_url = fields.Many2one(string='Shopify URL')
    execution_time = fields.Datetime(string='Execution Time')
    finish_time = fields.Datetime(string='Finish Time')
    status = fields.Char(string='Status')
    message = fields.Char(string='Message')
    stack_trace = fields.Char('Stack Trace')

class RequestLog(models.Model):
    _name = 'request.log'
    _description = 'Shopify Xero Request Logs'
    _order = 'create_date desc'
    _rec_name = 'shopify_store'

    shopify_store = fields.Many2one('shopify.store', string='Shopify Store', index=True)
    request_url = fields.Char('Request URL')
    request_headers = fields.Char('Request Headers')
    request_body = fields.Char('Request Body')
    request_params = fields.Char('Request Params')
    response_code = fields.Char('Response Code')
    response_body = fields.Char('Response Body')