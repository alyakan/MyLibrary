# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='actor',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
