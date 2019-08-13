# Generated by Django 2.1.10 on 2019-08-13 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0007_auto_20190813_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='Name of this collection, e.g. Canon FD SLRs')),
            ],
        ),
        migrations.AddField(
            model_name='format',
            name='negative_size',
            field=models.ManyToManyField(to='schema.NegativeSize'),
        ),
        migrations.AddField(
            model_name='cameramodel',
            name='series',
            field=models.ManyToManyField(to='schema.Series'),
        ),
        migrations.AddField(
            model_name='lensmodel',
            name='series',
            field=models.ManyToManyField(to='schema.Series'),
        ),
    ]