from django.urls import path
from .views import weekly_salary

urlpatterns = [
    path('weekly_salary/', weekly_salary, name='weekly_salary'),
]
