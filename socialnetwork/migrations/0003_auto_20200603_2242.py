# Generated by Django 3.0.3 on 2020-06-03 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0002_auto_20200603_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(default='no', upload_to='post_imgs/'),
        ),
    ]
