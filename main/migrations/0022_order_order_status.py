# Generated by Django 4.2 on 2023-06-10 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_remove_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]