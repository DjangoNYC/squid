# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_event_meetup_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='meetup_id',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='meetup_id',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='memberrsvp',
            name='meetup_id',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='venue',
            name='meetup_id',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
    ]
