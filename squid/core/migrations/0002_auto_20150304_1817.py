# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberrsvp',
            name='worked_on',
            field=models.CharField(max_length=2048, null=True, blank=True),
            preserve_default=True,
        ),
    ]
