# Generated by Django 2.2.4 on 2019-10-31 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0013_delete_filteradapter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='repair',
            old_name='description',
            new_name='detail',
        ),
    ]