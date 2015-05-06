# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0006_remove_policy_external_policy_ref'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute_hierarchy',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('superior', models.CharField(max_length=255)),
                ('subordinate', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
