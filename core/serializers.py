from rest_framework import serializers
from noverdechallenge import settings

from  core.models import Client


class ClientSerializer(serializers.ModelSerializer):
    birthdate = serializers.DateField(input_formats=settings.DATE_INPUT_FORMAT)
    amount_wanted = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=1000, max_value=4000)
    cpf = serializers.CharField(max_length=11, min_length=11)
    terms_wanted = serializers.ChoiceField(choices=[(6,6), (9,9), (12,12)])

    class Meta:
        model = Client
        fields = ['pk','name', 'cpf', 'birthdate',  'amount_wanted', 'terms_wanted', 'income',
            'status', 'result', 'refused_policy', 'amount_approved', 'terms_approved']

        read_only_fields = ['pk','status', 'result', 'refused_policy', 'amount_approved', 'terms_approved']