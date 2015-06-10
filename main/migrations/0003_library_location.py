# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_library'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='location',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
