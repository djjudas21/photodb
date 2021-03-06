# Generated by Django 2.2.16 on 2020-10-21 14:38

from django.db import migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0091_auto_20201013_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='negative',
            name='location',
            field=geoposition.fields.GeopositionField(blank=True, help_text='Location where the picture was taken', max_length=42, null=True),
        ),
    ]
