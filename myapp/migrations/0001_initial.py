# Generated by Django 4.1.4 on 2022-12-19 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Immobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('type_item', models.CharField(choices=[('01', 'APARTAMENTO'), ('02', 'KITNET'), ('03', 'CASA')], max_length=100)),
                ('address', models.TextField()),
                ('price', models.DecimalField(decimal_places=3, max_digits=10)),
            ],
            options={
                'verbose_name': 'Imóvel',
                'verbose_name_plural': 'Imóveis',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RegisterLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_start', models.DateTimeField(verbose_name='Inicio')),
                ('dt_end', models.DateTimeField(verbose_name='Fim')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.client')),
                ('immobile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.immobile')),
            ],
            options={
                'verbose_name': 'Registrar Locação',
                'verbose_name_plural': 'Registrar Locação',
                'ordering': ['-id'],
            },
        ),
    ]