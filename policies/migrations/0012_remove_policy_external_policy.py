# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0011_auto_20150427_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='external_policy',
        ),
    ]
