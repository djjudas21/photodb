# Generated by Django 2.2.12 on 2020-05-15 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0056_auto_20200514_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='display_lens',
        ),
    ]
