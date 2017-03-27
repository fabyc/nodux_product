import datetime

from trytond.pool import Pool, PoolMeta
from trytond.model import ModelSQL, fields
from trytond.pyson import Eval, Or
from decimal import Decimal
from trytond.config import config

__all__ = ['Product', 'Template']
__metaclass__ = PoolMeta

class Template:
    __name__ = 'product.template'

    code1 = fields.Char('Code')

    code2 = fields.Char('Code')

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()
        cls.name.size = 100

    @staticmethod
    def default_products():
        return []

    @staticmethod
    def default_salable():
        return True

    @staticmethod
    def default_purchasable():
        return True

    @fields.depends('name')
    def on_change_name(self):
        res = {}
        cont = 0
        if self.name:
            name = self.name.strip()
            name = name.replace("\n","")
            res['name'] = name
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        products = cls.search([
                ('code1',) + tuple(clause[1:]),
                ], limit=1)
        if products:
            return [('code1',) + tuple(clause[1:])]

        products2 = cls.search([
                ('code2',) + tuple(clause[1:]),
                ], limit=1)
        if products2:
            return [('code2',) + tuple(clause[1:])]

        return [('name',) + tuple(clause[1:])]

    @fields.depends('products')
    def on_change_products(self):
        res = {}
        cont = 0
        for product in self.products:
            if cont == 0:
                if product.code:
                    res['code1'] = product.code
            if cont == 1:
                if product.code:
                    res['code2'] = product.code
            cont += 1
        return res

    @fields.depends('taxes_category', 'category', 'list_price', 'cost_price',
        'taxes')
    def on_change_category(self):
        try:
            changes = super(Template, self).on_change_category()
        except AttributeError:
            changes = {}

        if self.category:
            changes['account_category'] = True
            changes['taxes_category'] = True

        if self.taxes_category:
            changes['list_price_with_tax'] = None
            changes['cost_price_with_tax'] = None
            if self.category:
                changes['list_price_with_tax'] = self.get_list_price_with_tax()
                changes['cost_price_with_tax'] = self.get_cost_price_with_tax()
                changes['account_category'] = True
                changes['taxes_category'] = True
        return changes

class Product:
    __name__ = 'product.product'

    @classmethod
    def __setup__(cls):
        super(Product, cls).__setup__()
        cls.code.size = 50

        cls._sql_constraints += [
            ('code', 'UNIQUE(code)',
                'CODE Product already exists'),
        ]

    @fields.depends('code')
    def on_change_code(self):
        res = {}
        cont = 0
        if self.code:
            code = self.code.strip()
            code = code.replace("\n","")
            res['code'] = code
        return res

    @fields.depends('description')
    def on_change_description(self):
        res = {}
        cont = 0
        if self.description:
            description = self.description.strip()
            res['description'] = description
        return res
