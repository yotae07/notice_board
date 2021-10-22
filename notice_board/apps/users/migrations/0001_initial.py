# Generated by Django 3.2.8 on 2021-10-22 07:52

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='id')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('role', models.CharField(choices=[('admin', 'admin'), ('general', 'general'), ('manager', 'manager')], default='general', max_length=10, verbose_name='authority')),
                ('phone', models.CharField(db_index=True, max_length=20, verbose_name='phone')),
                ('email', models.EmailField(db_index=True, max_length=100, verbose_name='email')),
            ],
            options={
                'verbose_name': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
