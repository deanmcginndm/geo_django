# Generated by Django 3.0.4 on 2020-03-15 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0006_auto_20200315_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrydivision',
            name='engtype_2',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
