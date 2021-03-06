# Generated by Django 2.2.14 on 2020-08-27 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0078_auto_20200825_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='cameramodel',
            name='fastest_shutter_speed',
            field=models.ForeignKey(blank=True, help_text='Fastest shutter speed available on this camera', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fastest_shutter_speed', to='schema.ShutterSpeed'),
        ),
        migrations.AddField(
            model_name='cameramodel',
            name='slowest_shutter_speed',
            field=models.ForeignKey(blank=True, help_text='Slowest shutter speed available on this camera', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slowest_shutter_speed', to='schema.ShutterSpeed'),
        ),
        migrations.AddField(
            model_name='historicalcameramodel',
            name='fastest_shutter_speed',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Fastest shutter speed available on this camera', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='schema.ShutterSpeed'),
        ),
        migrations.AddField(
            model_name='historicalcameramodel',
            name='slowest_shutter_speed',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Slowest shutter speed available on this camera', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='schema.ShutterSpeed'),
        ),
    ]
