# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0004_auto_20150331_1351'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Attribute_type',
            new_name='Attribute_category',
        ),
        migrations.RenameField(
            model_name='cloud_platform',
            old_name='attribute_types',
            new_name='attribute_category',
        ),
        migrations.RenameField(
            model_name='condition',
            old_name='attribute_type',
            new_name='attribute_category',
        ),
        migrations.RemoveField(
            model_name='condition',
            name='negated',
        ),
    ]
