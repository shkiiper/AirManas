# Generated by Django 4.1.7 on 2023-03-02 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacations',
            name='employee',
        ),
    ]