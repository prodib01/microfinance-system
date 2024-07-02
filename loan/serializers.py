from rest_framework import serializers
from .models import Loan, LoanAmortization

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        
class LoanAmortizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanAmortization
        fields = '__all__'
