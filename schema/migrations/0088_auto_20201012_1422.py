# Generated by Django 2.2.16 on 2020-10-12 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0087_auto_20201002_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='condition_notes',
            field=models.TextField(blank=True, help_text='Description of condition', null=True),
        ),
        migrations.AlterField(
            model_name='camera',
            name='notes',
            field=models.TextField(blank=True, help_text='Freeform text field for extra notes', null=True),
        ),
        migrations.AlterField(
            model_name='cameramodel',
            name='notes',
            field=models.TextField(blank=True, help_text='Freeform text field for extra notes', null=True),
        ),
        migrations.AlterField(
            model_name='film',
            name='development_notes',
            field=models.TextField(blank=True, help_text='Extra freeform notes about the development process', null=True),
        ),
        migrations.AlterField(
            model_name='historicalcameramodel',
            name='notes',
            field=models.TextField(blank=True, help_text='Freeform text field for extra notes', null=True),
        ),
        migrations.AlterField(
            model_name='historicallensmodel',
            name='notes',
            field=models.TextField(blank=True, help_text='Freeform notes field', null=True),
        ),
        migrations.AlterField(
            model_name='historicalmount',
            name='notes',
            field=models.TextField(blank=True, help_text='Freeform notes field', null=True),
        ),
        migrations.AlterField(
            model_name='lens',
            name='condition_notes',
            field=models.TextField(blank=True, help_text='Description of condition', null=True),
        ),
        migrations.AlterField(
            model_name='lens',
            name='notes',
            field=models.TextField(blank=True, help_text='Freeform notes field', null=True),
        ),
        migrations.AlterField(
            model_name='lensmodel',
            name='notes',
            field=models.TextField(blank=True, help_text='Freeform notes field', null=True),
        ),
        migrations.AlterField(
            model_name='mount',
            name='notes',
            field=models.TextField(blank=True, help_text='Freeform notes field', null=True),
        ),
        migrations.AlterField(
            model_name='mountadapter',
            name='notes',
            field=models.TextField(blank=True, help_text='Freeform notes', null=True),
        ),
        migrations.AlterField(
            model_name='negative',
            name='notes',
            field=models.TextField(blank=True, help_text='Extra freeform notes about this exposure', null=True),
        ),
        migrations.AlterField(
            model_name='print',
            name='notes',
            field=models.TextField(blank=True, help_text='Freeform notes about this print, e.g. dodging, burning & complex toning', null=True),
        ),
    ]
