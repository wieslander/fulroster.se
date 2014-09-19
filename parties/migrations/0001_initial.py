# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ElectionDistrict',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('county', models.ForeignKey(to='parties.County')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_votes', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('name', models.TextField(unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, blank=True)),
            ],
            options={
                'ordering': ['-views', 'total_votes', 'slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VoteEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('election_type', models.CharField(max_length=1, choices=[(b'R', b'Riksdag'), (b'L', b'Landsting'), (b'K', b'Kommun')])),
                ('vote_count', models.IntegerField()),
                ('election_district', models.ForeignKey(to='parties.ElectionDistrict')),
                ('party', models.ForeignKey(related_name=b'vote_entries', to='parties.Party')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='electiondistrict',
            name='municipality',
            field=models.ForeignKey(to='parties.Municipality'),
            preserve_default=True,
        ),
    ]
