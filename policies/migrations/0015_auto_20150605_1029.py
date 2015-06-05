# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0014_remove_policy_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='operator',
            field=models.CharField(max_length=10),
        ),
    ]
