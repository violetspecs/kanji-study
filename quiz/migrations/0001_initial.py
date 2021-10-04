# Generated by Django 3.1.1 on 2021-09-08 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kanji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kanji', models.CharField(max_length=20)),
                ('onyomi', models.CharField(max_length=100)),
                ('kunyomi', models.CharField(max_length=100)),
                ('english', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserKanji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times_correct', models.IntegerField()),
                ('times_answered', models.IntegerField()),
                ('kanji', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.kanji')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
