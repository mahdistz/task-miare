from rest_framework import serializers
from .models import DailySalary, DecreaseOfIncome, IncreaseOfIncome, WeeklySalary, IncomeOfCourier, Courier


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = [
            'first_name', 'last_name', 'age',
        ]


class IncomeOfCourierSerializer(serializers.ModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)
    date = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = IncomeOfCourier
        fields = [
            'income_of_travel', 'courier', 'date',
        ]


class IncreaseOfIncomeSerializer(serializers.ModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)
    date = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = IncreaseOfIncome
        fields = [
            'increase_income', 'courier', 'date',
        ]


class DecreaseOfIncomeSerializer(serializers.ModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)
    date = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = DecreaseOfIncome
        fields = [
            'decrease_income', 'courier', 'date',
        ]


class DailySalarySerializer(serializers.ModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)
    date = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = DailySalary
        fields = [
            'daily_salary', 'courier', 'date',
        ]


class WeeklySalarySerializer(serializers.ModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)
    date = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = WeeklySalary
        fields = [
            'weekly_salary', 'courier', 'date',
        ]
