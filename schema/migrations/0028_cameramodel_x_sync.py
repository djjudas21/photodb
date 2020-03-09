# Generated by Django 2.2 on 2020-03-09 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0027_auto_20200306_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='cameramodel',
            name='x_sync',
            field=models.ForeignKey(blank=True, help_text='Flash X-sync speed', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='x_sync', to='schema.ShutterSpeed'),
        ),
    ]
