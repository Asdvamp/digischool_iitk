# Generated by Django 3.1.5 on 2022-03-24 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0002_user_profile_database_edit_once_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile_database',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
