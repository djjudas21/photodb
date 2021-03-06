# Generated by Django 2.2.12 on 2020-05-27 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0059_auto_20200521_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='cameramodel',
            name='zoom_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, help_text='Ratio between minimum and maximum focal lengths', max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='lensmodel',
            name='zoom_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, help_text='Ratio between minimum and maximum focal lengths', max_digits=4, null=True),
        ),
    ]
