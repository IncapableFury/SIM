# Generated by Django 3.2.3 on 2021-05-25 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
