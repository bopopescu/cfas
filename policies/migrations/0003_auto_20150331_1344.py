# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0002_auto_20150331_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='external_policy_ref',
            field=models.CharField(max_length=255, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='policy',
            name='external_policy',
            field=models.BinaryField(),
            preserve_default=True,
        ),
    ]
