# Generated by Django 4.0.4 on 2022-05-31 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courier_income', '0002_remove_courier_marriage_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomeofcourier',
            name='income_of_travel',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
