# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0009_auto_20150427_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='And_rule',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('attribute', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('external_policy', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Attribute_categories',
            new_name='Attribute_category',
        ),
        migrations.RenameModel(
            old_name='Cloud_platforms',
            new_name='Cloud_platform',
        ),
        migrations.RenameModel(
            old_name='Cloud_providers',
            new_name='Cloud_provider',
        ),
        migrations.RenameModel(
            old_name='Operators',
            new_name='Operator',
        ),
        migrations.RemoveField(
            model_name='and_rules',
            name='conditions',
        ),
        migrations.RemoveField(
            model_name='and_rules',
            name='policy',
        ),
        migrations.DeleteModel(
            name='And_rules',
        ),
        migrations.DeleteModel(
            name='Attribute_hierarchy',
        ),
        migrations.RemoveField(
            model_name='conditions',
            name='attribute_category',
        ),
        migrations.RemoveField(
            model_name='conditions',
            name='operator',
        ),
        migrations.DeleteModel(
            name='Conditions',
        ),
        migrations.RemoveField(
            model_name='policies',
            name='cloud_provider',
        ),
        migrations.DeleteModel(
            name='Policies',
        ),
        migrations.AddField(
            model_name='policy',
            name='cloud_provider',
            field=models.ForeignKey(to='policies.Cloud_provider'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='condition',
            name='attribute_category',
            field=models.ForeignKey(to='policies.Attribute_category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='condition',
            name='operator',
            field=models.ForeignKey(to='policies.Operator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='and_rule',
            name='conditions',
            field=models.ManyToManyField(to='policies.Condition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='and_rule',
            name='policy',
            field=models.ForeignKey(to='policies.Policy'),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='cloud_platform',
            old_name='attribute_categories',
            new_name='attribute_category',
        ),
    ]
