# Generated by Django 5.1.3 on 2024-11-28 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursemanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='type',
            field=models.CharField(default='Lecture', max_length=666),
        ),
    ]
