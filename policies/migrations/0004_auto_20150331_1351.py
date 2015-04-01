# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0003_auto_20150331_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='external_policy',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
