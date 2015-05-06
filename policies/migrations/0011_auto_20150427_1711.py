# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0010_auto_20150427_1625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cloud_platform',
            old_name='attribute_category',
            new_name='attribute_categories',
        ),
    ]
