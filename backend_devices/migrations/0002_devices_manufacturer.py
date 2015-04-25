# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend_manufacturers', '0001_initial'),
        ('backend_devices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='manufacturer',
            field=models.ForeignKey(default=0, to='backend_manufacturers.Manufacturers'),
            preserve_default=False,
        ),
    ]
