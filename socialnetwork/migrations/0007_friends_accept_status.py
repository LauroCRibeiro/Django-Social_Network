# Generated by Django 3.0.3 on 2020-06-05 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0006_auto_20200605_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='accept_status',
            field=models.BooleanField(default=False),
        ),
    ]
