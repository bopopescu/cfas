# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0016_auto_20150605_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('attribute', models.CharField(max_length=255)),
                ('policy', models.ForeignKey(to='policies.Policy')),
            ],
        ),
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=255)),
                ('attribute', models.ForeignKey(to='policies.Attribute')),
            ],
        ),
        migrations.AddField(
            model_name='hierarchy',
            name='child',
            field=models.ForeignKey(to='policies.Value', related_name='child'),
        ),
        migrations.AddField(
            model_name='hierarchy',
            name='parent',
            field=models.ForeignKey(to='policies.Value', related_name='parent'),
        ),
    ]
