# Generated by Django 4.2 on 2023-05-30 00:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0017_cart_text_box_obs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='text_box_obs',
        ),
        migrations.CreateModel(
            name='CartObs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_box_obs', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
