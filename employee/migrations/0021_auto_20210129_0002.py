# Generated by Django 3.1.4 on 2021-01-28 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0020_auto_20210129_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisal',
            name='dept_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.department'),
        ),
    ]
