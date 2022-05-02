# Generated by Django 4.0.4 on 2022-05-02 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('title', models.CharField(max_length=50)),
                ('model_name', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('file', models.FileField(blank=True, upload_to='')),
                ('user_id', models.ForeignKey(db_column='user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='member.user')),
            ],
        ),
    ]
