# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0013_auto_20150530_0445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='type',
        ),
    ]
