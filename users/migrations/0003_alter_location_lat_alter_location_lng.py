# Generated by Django 4.0.5 on 2022-07-03 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_location_options_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='lng',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
