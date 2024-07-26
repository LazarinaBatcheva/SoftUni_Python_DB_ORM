import os
import django
from django.db.models import Q, Count, F, Case, When, Value, BooleanField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Order, Product


def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ''

    # query_name = Q(full_name__icontains=search_string)
    # query_email = Q(email__icontains=search_string)
    # query_phone_num = Q(phone_number__icontains=search_string)
    #
    # profiles = Profile.objects.filter(
    #     query_name | query_email | query_phone_num
    # ).order_by('full_name')

    query = (
        Q(full_name__icontains=search_string)
        |
        Q(email__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    )

    profiles = Profile.objects.filter(query).order_by('full_name')

    if not profiles.exists():
        return ''

    return '\n'.join(
        f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, '
        f'orders: {p.profile_orders.count()}'
        for p in profiles
    )


def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    if not profiles.exists():
        return ''

    return '\n'.join(
        f'Profile: {p.full_name}, orders: {p.profile_orders.count()}'
        for p in profiles
    )


def get_last_sold_products() -> str:
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ''

    product_names = ', '.join(last_order.products.order_by('name').values_list('name', flat=True))

    return f'Last sold products: {product_names}'


def get_top_products() -> str:
    top_products = Product.objects\
        .prefetch_related('products_orders')\
        .annotate(
            orders_count=Count('products_orders')
        ).filter(
            orders_count__gt=0
        ).order_by(
                '-orders_count',
                'name'
        )[:5]

    if not top_products.exists():
        return ''

    top_products_info = ['Top products:']

    product_names = '\n'.join(
        f'{p.name}, sold {p.orders_count} times'
        for p in top_products
    )

    top_products_info.append(product_names)

    return '\n'.join(top_products_info)


def apply_discounts() -> str:
    updated_products_price_count = Order.objects\
        .prefetch_related('products')\
        .annotate(
            products_count=Count('products')
        )\
        .filter(
            products_count__gt=2,
            is_completed=False,
        )\
        .update(
            total_price=F('total_price') * 0.90
        )

    return f'Discount applied to {updated_products_price_count} orders.'


def complete_order() -> str:
    first_not_completed_order = Order.objects\
        .filter(
            is_completed=False
        )\
        .order_by(
            'creation_date'
        )\
        .first()

    if first_not_completed_order is None:
        return ''

    first_not_completed_order.products.update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available'),
            output_field=BooleanField()
        )
    )

    first_not_completed_order.is_completed = True
    first_not_completed_order.save()

    return 'Order has been completed!'
