from django.contrib import admin
from .models import DailySalary, DecreaseOfIncome, IncreaseOfIncome, WeeklySalary, IncomeOfCourier, Courier

# Register your models here.

admin.site.register(Courier)
admin.site.register(IncomeOfCourier)
admin.site.register(IncreaseOfIncome)
admin.site.register(DecreaseOfIncome)
admin.site.register(DailySalary)
admin.site.register(WeeklySalary)
