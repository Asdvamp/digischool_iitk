# Generated by Django 4.0.1 on 2022-03-29 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectureapp', '0003_remove_all_lectures_yt_link_unique_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_lectures',
            name='files',
            field=models.FileField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]