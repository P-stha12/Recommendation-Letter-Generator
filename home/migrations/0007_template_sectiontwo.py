# Generated by Django 3.2.4 on 2023-08-14 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_template_sectionone'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='sectionTwo',
            field=models.TextField(default="<br />I recall {{firstname}} as a {{quality.quality}} student.{% if academics.tentative_ranking == 'Batch Topper' %} In fact, he was thetopper of his batch in {{student.std.program}} Engineering. {% else %}He maintained excellent academic performance throughout hisundergraduate ranking among the {{academics.tentative_ranking}}students of his batch. {% endif %} As an instructor and his supervisortoo I had enough opportunity is observe his capabilities closely."),
        ),
    ]