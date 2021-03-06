# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-22 11:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('house_no', models.TextField()),
                ('locality', models.TextField()),
                ('city', models.TextField()),
                ('state', models.TextField()),
                ('pin_code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Civilian',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('isCriminal', models.IntegerField()),
                ('salary', models.IntegerField(default=0)),
                ('job', models.TextField(default='None')),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Criminal_Record',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('jail', models.IntegerField(default=0)),
                ('description', models.TextField()),
                ('section', models.TextField()),
                ('fine', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Police',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('salary', models.IntegerField()),
                ('description', models.TextField()),
                ('post', models.CharField(default='Inspector', max_length=30)),
                ('rank', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('date_posted', models.DateTimeField()),
                ('civilian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='police.Civilian')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('city', models.CharField(default='New Delhi', max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('locality', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='User_profile',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_no', models.CharField(max_length=12)),
                ('isPolice', models.IntegerField()),
                ('age', models.IntegerField()),
                ('gender', models.TextField(default='Male')),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='police.Station'),
        ),
        migrations.AddField(
            model_name='police',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='police.Station'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='police',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='police.Police'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
