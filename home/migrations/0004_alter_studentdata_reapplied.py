# Generated by Django 3.2.4 on 2023-08-09 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_studentdata_reapplied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdata',
            name='reapplied',
            field=models.BooleanField(default=False),
        ),
    ]