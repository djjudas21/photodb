# Generated by Django 2.2.4 on 2019-09-05 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0018_auto_20190905_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='dissolved',
            field=models.IntegerField(blank=True, help_text='Year in which the manufacturer was dissolved', null=True),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='founded',
            field=models.IntegerField(blank=True, help_text='Year in which the manufacturer was founded', null=True),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(blank=True, help_text='Name of the manufacturer', max_length=45, unique=True),
        ),
        migrations.AlterField(
            model_name='mount',
            name='digital_only',
            field=models.BooleanField(blank=True, default=0, help_text='Whether this mount is intended only for digital cameras', null=True),
        ),
        migrations.AlterField(
            model_name='mount',
            name='purpose',
            field=models.CharField(blank=True, choices=[('Camera', 'Camera'), ('Enlarger', 'Enlarger'), ('Projector', 'Projector'), ('Telescope', 'Telescope'), ('Microscope', 'Microscope')], help_text='The intended purpose of this lens mount', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='mount',
            name='shutter_in_lens',
            field=models.BooleanField(blank=True, default=0, help_text='Whether this lens mount system incorporates the shutter into the lens', null=True),
        ),
        migrations.AlterField(
            model_name='mount',
            name='type',
            field=models.CharField(blank=True, choices=[('Bayonet', 'Bayonet'), ('Breech lock', 'Breech lock'), ('Screw', 'Screw'), ('Friction', 'Friction fit'), ('Lens board', 'Lens board')], help_text='The physical mount type of this lens mount', max_length=15, null=True),
        ),
    ]