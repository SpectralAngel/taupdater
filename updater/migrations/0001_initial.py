# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bridge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankUpdateFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('archivo', models.FileField(upload_to=b'update//%Y/%m/%d')),
                ('fecha_de_cobro', models.DateField()),
                ('fecha_de_procesamiento', models.DateField()),
                ('procesado', models.BooleanField(default=False)),
                ('banco', models.ForeignKey(to='bridge.Banco')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
