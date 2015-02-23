# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150218_0329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='member',
            name='thumb_link',
            field=models.ImageField(default='', max_length=256, upload_to=b''),
            preserve_default=False,
        ),
    ]
