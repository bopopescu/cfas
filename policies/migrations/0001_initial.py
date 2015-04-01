# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='And_rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute_type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cloud_platform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('accept_negated_conditions', models.BooleanField(default=False)),
                ('attribute_types', models.ManyToManyField(to='policies.Attribute_type')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cloud_provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('cloud_platform_id', models.ForeignKey(to='policies.Cloud_platform')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('negated', models.BooleanField(default=False)),
                ('attribute', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('attribute_type_id', models.ForeignKey(to='policies.Attribute_type')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('external_policy_id', models.CharField(max_length=255)),
                ('cloud_provider_id', models.ForeignKey(to='policies.Cloud_provider')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='condition',
            name='operator_id',
            field=models.ForeignKey(to='policies.Operator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cloud_platform',
            name='operators',
            field=models.ManyToManyField(to='policies.Operator'),
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
            name='policy_id',
            field=models.ForeignKey(to='policies.Policy'),
            preserve_default=True,
        ),
    ]
