# Generated by Django 3.1.4 on 2021-01-24 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_auto_20210125_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='dept_name',
            field=models.CharField(default='Engineering', max_length=50, unique=True, verbose_name='Department'),
        ),
    ]