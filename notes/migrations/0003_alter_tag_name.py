# Generated by Django 5.1.2 on 2025-03-21 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
