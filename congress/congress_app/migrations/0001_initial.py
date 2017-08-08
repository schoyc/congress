# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 04:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('state', models.CharField(max_length=2)),
                ('bioguide_id', models.CharField(default='0000000000', max_length=10)),
                ('last_vote_time', models.DateTimeField()),
                ('district', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Senator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('state', models.CharField(max_length=2)),
                ('bioguide_id', models.CharField(default='0000000000', max_length=10)),
                ('last_vote_time', models.DateTimeField()),
                ('election_year', models.DateField()),
                ('stateRegionKey', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]