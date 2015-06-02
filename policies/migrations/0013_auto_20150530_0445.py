# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0012_remove_policy_external_policy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cloud_platform',
            name='attribute_categories',
        ),
        migrations.RemoveField(
            model_name='cloud_platform',
            name='operators',
        ),
        migrations.RemoveField(
            model_name='cloud_provider',
            name='cloud_platform',
        ),
        migrations.RemoveField(
            model_name='condition',
            name='attribute_category',
        ),
        migrations.RemoveField(
            model_name='policy',
            name='cloud_provider',
        ),
        migrations.AddField(
            model_name='condition',
            name='type',
            field=models.CharField(default='o', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='policy',
            name='type',
            field=models.CharField(default='o', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='condition',
            name='operator',
            field=models.CharField(max_length=1),
        ),
        migrations.DeleteModel(
            name='Attribute_category',
        ),
        migrations.DeleteModel(
            name='Cloud_platform',
        ),
        migrations.DeleteModel(
            name='Cloud_provider',
        ),
        migrations.DeleteModel(
            name='Operator',
        ),
    ]
