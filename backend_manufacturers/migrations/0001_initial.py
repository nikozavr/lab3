# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturers',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('established', models.IntegerField()),
                ('country', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
