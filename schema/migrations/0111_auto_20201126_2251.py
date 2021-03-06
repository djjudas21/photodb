# Generated by Django 2.2.17 on 2020-11-26 22:51

import autosequence.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
import simple_history.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schema', '0110_auto_20201126_2236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teleconvertermodel',
            options={'ordering': ['manufacturer', 'model'], 'verbose_name_plural': 'teleconverter models'},
        ),
        migrations.RemoveField(
            model_name='teleconvertermodel',
            name='id_owner',
        ),
        migrations.RemoveField(
            model_name='teleconvertermodel',
            name='owner',
        ),
        migrations.AddField(
            model_name='teleconvertermodel',
            name='slug',
            field=models.SlugField(editable=False, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='teleconvertermodel',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='Teleconverter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_owner', autosequence.fields.AutoSequenceField(unique_with=('owner',), verbose_name='ID')),
                ('owner', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('teleconvertermodel', models.ForeignKey(help_text='Model of this teleconverter', on_delete=django.db.models.deletion.CASCADE, to='schema.TeleconverterModel')),
            ],
            options={
                'verbose_name_plural': 'teleconverters',
            },
        ),
        migrations.CreateModel(
            name='HistoricalTeleconverterModel',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('model', models.CharField(help_text='Model name of this teleconverter', max_length=45)),
                ('factor', models.DecimalField(blank=True, decimal_places=2, help_text='Magnification factor of this teleconverter (numerical part only, e.g. 1.4)', max_digits=4, null=True)),
                ('elements', models.PositiveIntegerField(blank=True, help_text='Number of optical elements used in this teleconverter', null=True)),
                ('groups', models.PositiveIntegerField(blank=True, help_text='Number of optical groups used in this teleconverter', null=True)),
                ('multicoated', models.BooleanField(blank=True, help_text='Whether this teleconverter is multi-coated', null=True)),
                ('slug', models.SlugField(editable=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('manufacturer', models.ForeignKey(blank=True, db_constraint=False, help_text='Manufacturer of this teleconverter', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='schema.Manufacturer')),
                ('mount', models.ForeignKey(blank=True, db_constraint=False, help_text='Lens mount used by this teleconverter', limit_choices_to={'purpose': 'Camera'}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='schema.Mount')),
            ],
            options={
                'verbose_name': 'historical teleconverter model',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
