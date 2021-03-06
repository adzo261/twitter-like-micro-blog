# Generated by Django 2.1.5 on 2019-07-13 22:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quack', '0015_auto_20190218_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2019, 7, 13, 22, 14, 30, 39170)),
        ),
        migrations.RemoveField(
            model_name='quack',
            name='tags',
        ),
        migrations.AddField(
            model_name='quack',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='quack.Tag'),
        ),
    ]
