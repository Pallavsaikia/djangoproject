# Generated by Django 2.1.7 on 2019-11-26 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='replied_by',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='replied_to',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='query',
            name='asked_by',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
        migrations.DeleteModel(
            name='Query',
        ),
    ]
