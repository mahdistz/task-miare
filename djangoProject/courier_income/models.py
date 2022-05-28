from django.db import models

marriage_status_choices = [
    ('S', 'single'),
    ('M', 'married'),
]


# Create your models here.
class Courier(models.Model):
    first_name = models.CharField(max_length=100, )
    last_name = models.CharField(max_length=100, )
    age = models.IntegerField(null=True, blank=True)
    marriage_status = models.CharField(max_length=1, choices=marriage_status_choices, null=True, blank=True)


class IncomeOfEachCourier(models.Model):
    income_of_travel = models.PositiveBigIntegerField()
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, )

    class Meta:
        abstract = True


class IncreaseOrDecreaseOfIncome(IncomeOfEachCourier):
    increase_income = models.PositiveBigIntegerField(null=True, blank=True)
    decrease_income = models.PositiveBigIntegerField(null=True, blank=True)


class DailySalary(models.Model):
    pass


class WeeklySalary(models.Model):
    pass
