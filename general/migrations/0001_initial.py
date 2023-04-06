# Generated by Django 4.1.7 on 2023-03-23 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('data_vidachi', models.DateField(auto_now_add=True)),
                ('document', models.FileField(upload_to='documents')),
                ('description', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trainings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_of_begin', models.DateField()),
                ('date_of_end', models.DateField(null=True)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
