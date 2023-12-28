# Generated by Django 4.2.7 on 2024-01-11 01:44

import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Firstnames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'firstnames',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Lastnames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'lastnames',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Phones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('number', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'phones',
                'ordering': ['id'],
                'indexes': [django.contrib.postgres.indexes.HashIndex(fields=['number'], name='number_idx'), models.Index(fields=['number', 'code'], name='number_code_idx')],
            },
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('city_id', models.IntegerField(blank=True, null=True)),
                ('last_auth_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('firstname', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.firstnames')),
                ('lastname', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.lastnames')),
                ('phone', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='customers.phones')),
            ],
            options={
                'db_table': 'customers',
                'ordering': ['id'],
            },
        ),
    ]
