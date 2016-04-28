# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 20:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0002_auto_20160426_0952'),
        ('updater', '0004_comparacionbanco_diferenciabanco'),
    ]

    operations = [
        migrations.CreateModel(
            name='BancoFaltante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('archivo', models.FileField(upload_to='complemento/%Y/%m/%d')),
                ('fecha_de_cobro', models.DateField()),
                ('cobrar_colegiacion', models.BooleanField(default=True)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bridge.Banco')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
