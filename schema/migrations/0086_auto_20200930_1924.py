# Generated by Django 2.2.14 on 2020-09-30 19:24

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0085_auto_20200922_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmanufacturer',
            name='country',
            field=django_countries.fields.CountryField(blank=True, help_text='Country in which the manufacturer is based', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='country',
            field=django_countries.fields.CountryField(blank=True, help_text='Country in which the manufacturer is based', max_length=2, null=True),
        ),
    ]
