# Generated by Django 3.1.1 on 2021-09-21 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kanji',
            name='english',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='kanji',
            name='kunyomi',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='kanji',
            name='onyomi',
            field=models.CharField(max_length=200),
        ),
    ]
