# Generated by Django 4.0.4 on 2022-05-31 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courier_income', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courier',
            name='marriage_status',
        ),
        migrations.RemoveField(
            model_name='dailysalary',
            name='created',
        ),
        migrations.RemoveField(
            model_name='dailysalary',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='decreaseofincome',
            name='created',
        ),
        migrations.RemoveField(
            model_name='decreaseofincome',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='incomeofcourier',
            name='created',
        ),
        migrations.RemoveField(
            model_name='incomeofcourier',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='increaseofincome',
            name='created',
        ),
        migrations.RemoveField(
            model_name='increaseofincome',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='weeklysalary',
            name='created',
        ),
        migrations.RemoveField(
            model_name='weeklysalary',
            name='daily_salary',
        ),
        migrations.RemoveField(
            model_name='weeklysalary',
            name='updated',
        ),
    ]