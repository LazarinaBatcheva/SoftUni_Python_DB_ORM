import os

import django
from django.db.models import Sum, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct


def product_quantity_ordered() -> str:
    ordered_products_quantity_info = []

    ordered_products = (Product.objects
                        .annotate(total_quantity_ordered=Sum("orderproduct__quantity"))
                        .exclude(total_quantity_ordered=None)
                        .order_by("-total_quantity_ordered"))

    for product in ordered_products:
        ordered_products_quantity_info.append(
            f"Quantity ordered of {product.name}: {product.total_quantity_ordered}"
        )

    return "\n".join(ordered_products_quantity_info)


def ordered_products_per_customer() -> str:
    orders = Order.objects.prefetch_related("orderproduct_set__product__category").order_by("id")

    orders_info = []
    for o in orders:
        orders_info.append(f"Order ID: {o.id}, Customer: {o.customer.username}")
        for order_product in o.orderproduct_set.all():
            orders_info.append(f"- Product: {order_product.product.name}, "
                               f"Category: {order_product.product.category.name}")

    return "\n".join(orders_info)


def filter_products() -> str:
    available_products = (Product.objects.available_products()
                          .filter(price__gt=3.00)
                          .order_by("-price", "name"))

    # available_products = (Product.objects
    #                       .filter(Q(is_available=True) & Q(price__gt=3.00))
    #                       .order_by("-price", "name"))

    available_products_info = []
    for p in available_products:
        available_products_info.append(f"{p.name}: {p.price}lv.")

    return "\n".join(available_products_info)


def give_discount() -> str:
    # gets and updates price of available products with price > 3.00
    Product.objects.available_products().filter(price__gt=3.00).update(price=F("price") * 0.7)
    
    # arrangement of products with updated prices
    discounted_products = Product.objects.available_products().order_by("-price", "name")

    available_products_info = []
    for p in discounted_products:
        available_products_info.append(f"{p.name}: {p.price}lv.")

    return "\n".join(available_products_info)








