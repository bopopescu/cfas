# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='and_rule',
            old_name='policy_id',
            new_name='policy',
        ),
        migrations.RenameField(
            model_name='cloud_provider',
            old_name='cloud_platform_id',
            new_name='cloud_platform',
        ),
        migrations.RenameField(
            model_name='condition',
            old_name='attribute_type_id',
            new_name='attribute_type',
        ),
        migrations.RenameField(
            model_name='condition',
            old_name='operator_id',
            new_name='operator',
        ),
        migrations.RenameField(
            model_name='policy',
            old_name='cloud_provider_id',
            new_name='cloud_provider',
        ),
        migrations.RenameField(
            model_name='policy',
            old_name='external_policy_id',
            new_name='external_policy',
        ),
    ]
