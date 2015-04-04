# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0005_auto_20150402_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='external_policy_ref',
        ),
    ]
