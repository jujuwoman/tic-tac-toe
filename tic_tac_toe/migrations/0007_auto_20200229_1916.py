# Generated by Django 3.0.3 on 2020-02-29 19:16

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import tic_tac_toe.models


class Migration(migrations.Migration):

    dependencies = [
        ('tic_tac_toe', '0006_auto_20200229_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='players',
            name='cols',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=tic_tac_toe.models.get_default_array),
        ),
        migrations.AlterField(
            model_name='players',
            name='rows',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=tic_tac_toe.models.get_default_array),
        ),
    ]
