# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0008_auto_20150427_1553'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cloud_platform',
            new_name='Cloud_platforms',
        ),
    ]
