# Generated by Django 2.0.7 on 2018-08-09 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stocks',
            fields=[
                ('ticker', models.TextField(primary_key=True, serialize=False, unique=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('momentum', models.FloatField(blank=True, null=True)),
                ('selected', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'stocks',
                'db_table': 'stocks',
                'managed': True,
            },
        ),
    ]
