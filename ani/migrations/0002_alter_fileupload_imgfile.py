# Generated by Django 4.0.1 on 2022-04-16 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ani', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='imgfile',
            field=models.ImageField(blank=True, null=True, upload_to='ani_images'),
        ),
    ]