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
    date = models.DateTimeField()

    class Meta:
        abstract = True
        ordering = ['date']


income_status = [
    ('Calculated', 'Calculated'),
    ('Not calculated', 'Not calculated'),
]


class IncomeOfCourier(CommonInfo):
    income_of_travel = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=15, choices=income_status, default='Not calculated')

    def __str__(self):
        return f"{self.courier} {self.income_of_travel} {self.date.date()}"

    def save(self, *args, **kwargs):
        try:
            obj = DailySalary.objects.get(courier=self.courier, date=self.date.date())
        except Exception as e:
            obj = DailySalary.objects.create(courier=self.courier, date=self.date.date())

        obj.daily_salary += self.income_of_travel
        obj.status = 'Calculated'
        obj.save()
        super(IncomeOfCourier, self).save()


class IncreaseOfIncome(CommonInfo):
    increase_income = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=15, choices=income_status, default='Not calculated')

    def __str__(self):
        return f"{self.courier} {self.increase_income} {self.date.date()}"

    def save(self, *args, **kwargs):
        try:
            obj = DailySalary.objects.get(courier=self.courier, date=self.date.date())
        except Exception as e:
            obj = DailySalary.objects.create(courier=self.courier, date=self.date.date())

        obj.daily_salary += self.increase_income
        obj.status = 'Calculated'
        obj.save()
        super(IncreaseOfIncome, self).save()


class DecreaseOfIncome(CommonInfo):
    decrease_income = models.BigIntegerField(default=0)
    status = models.CharField(max_length=15, choices=income_status, default='Not calculated')

    def __str__(self):
        return f"{self.courier} {self.decrease_income} {self.date.date()}"

    def save(self, *args, **kwargs):
        try:
            obj = DailySalary.objects.get(courier=self.courier, date=self.date.date())
        except Exception as e:
            obj = DailySalary.objects.create(courier=self.courier, date=self.date.date())

        obj.daily_salary -= self.decrease_income
        obj.status = 'Calculated'
        obj.save()
        super(DecreaseOfIncome, self).save()


status_choices = [
    ('Updating', 'Updating'),
    ('Closed', 'Closed'),
]


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


class DailySalary(CommonInfo):
    status = models.CharField(max_length=10, choices=status_choices, default='Updating')
    daily_salary = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        saturday = calculate_saturday_of_week_that_courier_worked_in(obj=self)
        try:
            obj_weekly_salary = WeeklySalary.objects.get(courier=self.courier, date=saturday.date())
        except Exception as e:
            obj_weekly_salary = WeeklySalary.objects.create(courier=self.courier, date=saturday.date())

        daily_salary = DailySalary.objects.filter(courier__exact=self.courier, date__gte=saturday,
                                                  date__lte=saturday + timedelta(days=6))
        for salary in daily_salary:
            obj_weekly_salary.weekly_salary += salary.daily_salary

        obj_weekly_salary.save()

        super(DailySalary, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.courier}, {self.daily_salary}, {self.date.date()}"


class WeeklySalary(CommonInfo):
    weekly_salary = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.courier}, {self.weekly_salary}, {self.date.date()}"
