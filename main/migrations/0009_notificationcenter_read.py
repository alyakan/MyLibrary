# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_notificationcenter'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationcenter',
            name='read',
            field=models.IntegerField(default=0),
        ),
    ]
