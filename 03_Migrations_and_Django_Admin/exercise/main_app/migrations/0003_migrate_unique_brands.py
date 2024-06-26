# Generated by Django 5.0.4 on 2024-06-25 14:57

from django.db import migrations


def create_unique_brands(apps, schema_editor):
    shoe_model = apps.get_model('main_app', 'Shoe')
    unique_brands_model = apps.get_model('main_app', 'UniqueBrands')

    unique_brands_names = shoe_model.objects.values_list('brand', flat=True).distinct()

    unique_brands_model.objects.bulk_create(
        [unique_brands_model(brand=brand_name) for brand_name in unique_brands_names]
    )


def reverse_unique_brands(apps, schema_editor):
    unique_brands_model = apps.get_model('main_app', 'UniqueBrands')
    unique_brands_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_uniquebrands'),
    ]

    operations = [
        migrations.RunPython(create_unique_brands, reverse_unique_brands)
    ]
