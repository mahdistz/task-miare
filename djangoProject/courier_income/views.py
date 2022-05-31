from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WeeklySalary, Courier, DailySalary
from .serializers import WeeklySalarySerializer, CourierSerializer, DailySalarySerializer
from datetime import datetime


# Create your views here.


@csrf_exempt
@api_view(["GET"])
def weekly_salary(request, from_date, to_date):
    if request.method == 'GET':
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
        weekly_salaries = WeeklySalary.objects.filter(date__gte=from_date, date__lte=to_date)
        serializer = WeeklySalarySerializer(weekly_salaries, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(["GET"])
def list_of_couriers(request):
    if request.method == 'GET':
        couriers = Courier.objects.all()
        serializer = CourierSerializer(couriers, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(["GET"])
def daily_salary(request):
    if request.method == 'GET':
        daily_salaries = DailySalary.objects.all()
        serializer = DailySalarySerializer(daily_salaries, many=True)
        return Response(serializer.data)
