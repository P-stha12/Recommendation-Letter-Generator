# Generated by Django 3.2.4 on 2023-08-14 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20230814_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]