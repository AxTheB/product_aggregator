# Generated by Django 3.0.1 on 2020-01-03 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_aggregator', '0003_auto_20191227_0454'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='blocker',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
