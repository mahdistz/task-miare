from rest_framework import serializers
from .models import DailySalary, DecreaseOfIncome, IncreaseOfIncome, WeeklySalary, IncomeOfCourier, Courier, CommonInfo


class CourierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Courier
        fields = [
            'first_name', 'last_name', 'age',
        ]


class CommonInfoSerializer(serializers.HyperlinkedModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = CommonInfo
        fields = ['date', ]


class IncomeOfCourierSerializer(serializers.HyperlinkedModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)
    date = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = IncomeOfCourier
        fields = [
            'income_of_travel', 'status',
        ]


class IncreaseOfIncomeSerializer(serializers.HyperlinkedModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)
    date = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = IncreaseOfIncome
        fields = [
            'increase_income', 'status',
        ]


class DecreaseOfIncomeSerializer(serializers.HyperlinkedModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)
    date = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = DecreaseOfIncome
        fields = [
            'decrease_income', 'status',
        ]


class DailySalarySerializer(serializers.HyperlinkedModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)
    date = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = DailySalary
        fields = [
            'daily_salary', 'status',
        ]


class WeeklySalarySerializer(serializers.HyperlinkedModelSerializer):
    courier = serializers.StringRelatedField(read_only=True, required=False)
    date = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = WeeklySalary
        fields = [
            'weekly_salary',
        ]
