# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0015_auto_20150605_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='operator',
            field=models.CharField(max_length=50),
        ),
    ]
