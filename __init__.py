from trytond.pool import Pool
from .product import *

def register():
    Pool.register(
        Product,
        Template,
        module='nodux_product', type_='model')
