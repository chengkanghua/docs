# Generated by Django 3.2 on 2022-03-20 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_alter_student_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='age',
            field=models.IntegerField(default=20),
        ),
    ]
