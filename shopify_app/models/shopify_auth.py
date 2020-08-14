from odoo import api, fields, models, _
import shopify


class ShopifyConfig(object):

    BASE_URL = "https://odoo.website"
    CALLBACK_URL = "https://odoo.website/shopify/callback"
    SHOPIFY_SCOPE = [ "read_inventory","read_customers", "write_customers", "write_products", "read_products","write_price_rules"
        , "read_price_rules", "read_script_tags","read_discounts","write_discounts",
            "read_draft_orders" ,"write_script_tags", "read_orders", "read_checkouts",]
    SHOPIFY_API_KEY = 'd91f498b5330cd86191a94e2d161ef6c'
    SHOPIFY_SHARED_SECRET = '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'
    API_VERSION = '2020-04'

class ShopifyAuth(models.AbstractModel):
    _name = 'shopify.auth'
    _description = 'Shopify Authenticate'

    def get_shopify_session(self, shopify_url , shopify_token):
        shopify_config = ShopifyConfig()
        shopify.Session.setup(api_key=shopify_config.SHOPIFY_API_KEY, secret=shopify_config.SHOPIFY_SHARED_SECRET)
        session = shopify.Session(shopify_url, shopify_config.API_VERSION, shopify_token)
        shopify.ShopifyResource.activate_session(session)
        return shopify


