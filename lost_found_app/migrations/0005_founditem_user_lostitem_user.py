# Generated by Django 5.1.4 on 2025-01-21 01:01

import django.db.models.deletion
import lost_found_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lost_found_app', '0004_itemmatch'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='founditem',
            name='user',
            field=models.ForeignKey(default=lost_found_app.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lostitem',
            name='user',
            field=models.ForeignKey(default=lost_found_app.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
