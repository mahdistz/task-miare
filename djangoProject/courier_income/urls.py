from django.urls import path
from .views import weekly_salary, list_of_couriers, daily_salary

urlpatterns = [
    path('weekly_salaries/<str:from_date>/<str:to_date>/', weekly_salary, name='weekly_salary'),
    path('daily_salaries/', daily_salary, name='daily_salary'),
    path('couriers/', list_of_couriers, name='couriers'),
]
