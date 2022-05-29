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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CommonInfo(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, )

    class Meta:
        abstract = True


class IncomeOfCourier(CommonInfo):
    income_of_travel = models.PositiveBigIntegerField()
    date_of_travel = models.DateField()

    class Meta:
        ordering = ['date_of_travel']

    def __str__(self):
        return f"{self.income_of_travel}, in {self.date_of_travel}"


class IncreaseOrDecreaseOfIncome(CommonInfo):
    increase_income = models.PositiveBigIntegerField(default=0)
    decrease_income = models.PositiveBigIntegerField(default=0)
    date = models.DateField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f" i:{self.increase_income},d:{self.decrease_income} in {self.date}"


class DailySalary(CommonInfo):
    income = models.ForeignKey(IncomeOfCourier, on_delete=models.CASCADE, )
    increase_decrease_of_income = models.ForeignKey(IncreaseOrDecreaseOfIncome, on_delete=models.CASCADE, )

    class Meta(IncomeOfCourier.Meta, IncreaseOrDecreaseOfIncome.Meta):
        pass

    def calculate_daily_salary(self):
        pass


class WeeklySalary(DailySalary):
    pass
