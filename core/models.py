import uuid
from datetime import date
from django.db import models
from noverdechallenge import settings

class Client(models.Model):

    SITUATION_CHOICES = [
        ('status', (
                ('CP', 'Completed'),
                ('PS', 'Processing'),
            )
        ),
        ('result', (
                ('AP', 'Approved'),
                ('RF', 'Refused'),
            )
        ),
        ('refused', (
                ('AG', 'Age'),
                ('SC', 'Score'),
                ('CM', 'Commitment'),
            )

        ),
        ('unknown', 'Unknown'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    cpf = models.CharField(max_length=11)
    birthdate = models.DateField()
    #Valor desejado
    amount_wanted = models.DecimalField(max_digits=6, decimal_places=2)
    #Parcelas desejadas
    terms_wanted = models.IntegerField()
    #renda mensal do cliente
    income = models.DecimalField(max_digits=8, decimal_places=2)
    #options: rocessing, completed
    status = models.CharField(max_length=10,choices=SITUATION_CHOICES,default='PS')
    #options: approved, refused
    result = models.CharField(max_length=10, choices=SITUATION_CHOICES, blank=True, null=True)
    #options: age, score, commitment
    refused_policy = models.CharField(max_length=10, choices=SITUATION_CHOICES, blank=True, null=True)
    #montante liberado em caso de aprovado
    amount_approved = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    #Quantidade de parcelas aprovadas
    terms_approved = models.PositiveSmallIntegerField(blank=True, null=True)

    def get_age(self):
        born = self.birthdate
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def __str__(self):
        return self.pk




