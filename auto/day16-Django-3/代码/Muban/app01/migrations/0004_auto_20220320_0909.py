# Generated by Django 3.2 on 2022-03-20 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_student_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='isMarried',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='age',
            field=models.IntegerField(default=20, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
