# Generated by Django 3.0.3 on 2020-06-06 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0008_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_body',
            field=models.TextField(default='', null=True),
        ),
    ]
