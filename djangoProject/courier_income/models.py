from datetime import timedelta
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

    def full_name(self):
        """Returns the person's full name."""
        return '%s %s' % (self.first_name, self.last_name)


class CommonInfo(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, )
    date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
        return f"income:{self.income_of_travel}, in {self.date}"


class IncreaseOfIncome(CommonInfo):
    increase_income = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=15, choices=income_status, default='Not calculated')

    def __str__(self):
        return f"increase:{self.increase_income}, in {self.date}"


class DecreaseOfIncome(CommonInfo):
    decrease_income = models.BigIntegerField(default=0)
    status = models.CharField(max_length=15, choices=income_status, default='Not calculated')

    def __str__(self):
        return f"decrease:{self.decrease_income}, in {self.date}"


status_choices = [
    ('Updating', 'Updating'),
    ('Closed', 'Closed'),
]


class DailySalary(CommonInfo):
    status = models.CharField(max_length=10, choices=status_choices, default='Updating')
    daily_salary = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        incomes = IncomeOfCourier.objects.filter(courier__exact=self.courier, date__exact=self.date)
        increases = IncreaseOfIncome.objects.filter(courier__exact=self.courier, date__exact=self.date)
        decreases = DecreaseOfIncome.objects.filter(courier__exact=self.courier, date__exact=self.date)

        for income in incomes:
            if income.status != 'Calculated':
                self.daily_salary += income.income_of_travel
                income.status = 'Calculated'
                income.save(update_fields=['status'])

        for inc in increases:
            if inc.status != 'Calculated':
                self.daily_salary += inc.increase_income
                inc.status = 'Calculated'
                inc.save(update_fields=['status'])

        for dec in decreases:
            if dec.status != 'Calculated':
                self.daily_salary -= dec.decrease_income
                dec.status = 'Calculated'
                dec.save(update_fields=['status'])

        self.daily_salary.save()
        super(DailySalary, self).save(*args, **kwargs)


class WeeklySalary(CommonInfo):
    daily_salary = models.ForeignKey(DailySalary, on_delete=models.CASCADE, )
    weekly_salary = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        couriers = Courier.objects.all()
        for courier in couriers:
            first_date_of_income = DailySalary.objects.filter(courier__exact=courier).order_by('date').first()
            weekday = first_date_of_income.date.weekday()
            """weekday() : Return day of the week, where Monday == 0 ... Sunday == 6."""
            if weekday == 5:
                "saturday's weekday=5"
                saturday = first_date_of_income.date
            elif weekday == 6:
                "sunday's weekday=6"
                saturday = first_date_of_income.date - timedelta(days=1)
            elif 0 <= weekday <= 4:
                saturday = first_date_of_income.date - timedelta(days=weekday + 2)
            self.date = saturday

            daily_salary = DailySalary.objects.filter(courier__exact=courier, date__gte=saturday,
                                                      date__lte=saturday + timedelta(days=6))
            for salary in daily_salary:
                self.weekly_salary += salary.daily_salary

        self.weekly_salary.save()
        super(WeeklySalary, self).save(*args, **kwargs)
