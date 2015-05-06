# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0007_attribute_hierarchy'),
    ]

    operations = [
        migrations.CreateModel(
            name='And_rules',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute_categories',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conditions',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('attribute', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('attribute_category', models.ForeignKey(to='policies.Attribute_categories')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Policies',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('external_policy', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Cloud_provider',
            new_name='Cloud_providers',
        ),
        migrations.RenameModel(
            old_name='Operator',
            new_name='Operators',
        ),
        migrations.RemoveField(
            model_name='and_rule',
            name='conditions',
        ),
        migrations.RemoveField(
            model_name='and_rule',
            name='policy',
        ),
        migrations.DeleteModel(
            name='And_rule',
        ),
        migrations.RemoveField(
            model_name='condition',
            name='attribute_category',
        ),
        migrations.RemoveField(
            model_name='condition',
            name='operator',
        ),
        migrations.DeleteModel(
            name='Condition',
        ),
        migrations.RemoveField(
            model_name='policy',
            name='cloud_provider',
        ),
        migrations.DeleteModel(
            name='Policy',
        ),
        migrations.AddField(
            model_name='policies',
            name='cloud_provider',
            field=models.ForeignKey(to='policies.Cloud_providers'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conditions',
            name='operator',
            field=models.ForeignKey(to='policies.Operators'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='and_rules',
            name='conditions',
            field=models.ManyToManyField(to='policies.Conditions'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='and_rules',
            name='policy',
            field=models.ForeignKey(to='policies.Policies'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='cloud_platform',
            name='attribute_category',
        ),
        migrations.DeleteModel(
            name='Attribute_category',
        ),
        migrations.AddField(
            model_name='cloud_platform',
            name='attribute_categories',
            field=models.ManyToManyField(to='policies.Attribute_categories'),
            preserve_default=True,
        ),
    ]
