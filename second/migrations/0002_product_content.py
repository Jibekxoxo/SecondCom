# Generated by Django 4.2.2 on 2023-07-04 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('second', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
