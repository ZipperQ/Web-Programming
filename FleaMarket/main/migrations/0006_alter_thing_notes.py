# Generated by Django 4.2.16 on 2024-10-20 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_thing_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='notes',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
