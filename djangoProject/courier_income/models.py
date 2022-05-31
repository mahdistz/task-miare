from datetime import timedelta
from django.db import models


# Create your models here.
class Courier(models.Model):
    first_name = models.CharField(max_length=100, )
    last_name = models.CharField(max_length=100, )
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        """Returns the person's full name."""
        return '%s %s' % (self.first_name, self.last_name)


class CommonInfo(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, )
    date = models.DateField()

    class Meta:
        abstract = True
        ordering = ['date']


income_status = [
    ('Calculated', 'Calculated'),
    ('Not calculated', 'Not calculated'),
]


class IncomeOfCourier(CommonInfo):
    income_of_travel = models.PositiveBigIntegerField()
    status = models.CharField(max_length=15, choices=income_status, default='Not calculated')

    def __str__(self):
        return f"{self.courier} ,{self.income_of_travel}, {self.date}"

    def save(self, *args, **kwargs):
        try:
            obj = DailySalary.objects.get(courier=self.courier, date=self.date)
        except Exception as e:
            obj = DailySalary.objects.create(courier=self.courier, date=self.date)

        obj.daily_salary += self.income_of_travel
        obj.status = 'Calculated'
        obj.save()
        super(IncomeOfCourier, self).save()


class IncreaseOfIncome(CommonInfo):
    increase_income = models.PositiveBigIntegerField()
    status = models.CharField(max_length=15, choices=income_status, default='Not calculated')

    def __str__(self):
        return f"{self.courier}, {self.increase_income}, {self.date}"

    def save(self, *args, **kwargs):
        try:
            obj = DailySalary.objects.get(courier=self.courier, date=self.date)
        except Exception as e:
            obj = DailySalary.objects.create(courier=self.courier, date=self.date)

        obj.daily_salary += self.increase_income
        obj.status = 'Calculated'
        obj.save()
        super(IncreaseOfIncome, self).save()


class DecreaseOfIncome(CommonInfo):
    decrease_income = models.BigIntegerField()
    status = models.CharField(max_length=15, choices=income_status, default='Not calculated')

    def __str__(self):
        return f"{self.courier}, {self.decrease_income} ,{self.date}"

    def save(self, *args, **kwargs):
        try:
            obj = DailySalary.objects.get(courier=self.courier, date=self.date)
        except Exception as e:
            obj = DailySalary.objects.create(courier=self.courier, date=self.date)

        obj.daily_salary -= self.decrease_income
        obj.status = 'Calculated'
        obj.save()
        super(DecreaseOfIncome, self).save()


def calculate_saturday_of_week_that_courier_worked_in(obj):
    """
    :param: obj: one object from DailySalary Model
    :return: saturday: {date} field
    """
    weekday = obj.date.weekday()
    "weekday() : Return day of the week, where Monday == 0 ... Sunday == 6."
    if weekday == 5:
        "saturday's weekday=5"
        saturday = obj.date
    elif weekday == 6:
        "sunday's weekday=6"
        saturday = obj.date - timedelta(days=1)
    elif 0 <= weekday <= 4:
        "monday=0 ,tuesday=1,wednesday=2,thursday=3,friday=4"
        saturday = obj.date - timedelta(days=weekday + 2)

    return saturday


salary_status = [('C', 'c'),
                 ('N', 'n')]


class DailySalary(CommonInfo):
    status_for_weekly = models.CharField(max_length=1, choices=salary_status, default='n')
    daily_salary = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        saturday = calculate_saturday_of_week_that_courier_worked_in(obj=self)
        try:
            obj_weekly_salary = WeeklySalary.objects.get(courier=self.courier, date=saturday)
        except Exception:
            obj_weekly_salary = WeeklySalary.objects.create(courier=self.courier, date=saturday, )

        obj_weekly_salary.save()

        super(DailySalary, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.courier}, {self.daily_salary}, {self.date}"


class WeeklySalary(CommonInfo):
    weekly_salary = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.courier}, {self.weekly_salary}, {self.date}"

    def save(self, *args, **kwargs):
        saturday = calculate_saturday_of_week_that_courier_worked_in(obj=self)
        daily_salary = DailySalary.objects.filter(courier__exact=self.courier, date__gte=saturday,
                                                  date__lte=saturday + timedelta(days=6), status_for_weekly='n')
        for obj in daily_salary:
            self.weekly_salary += obj.daily_salary
            obj.status = 'c'

        super(WeeklySalary, self).save(*args, **kwargs)
