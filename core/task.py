# Create your tasks here
from __future__ import absolute_import, unicode_literals
import requests, io

from rest_framework.parsers import JSONParser
from celery import shared_task
from core.models import Client


class ValidateCredit:

    def get_interest_rate(self, score, parcela):
        interest_matrix = {
            (600, 6): 0.064, (600, 9): 0.066, (600, 12): 0.069,
            (700, 6): 0.055, (700, 9): 0.058, (700, 12): 0.061,
            (800, 6): 0.047, (800, 9): 0.050, (800, 12): 0.053,
            (900, 6): 0.039, (900, 9): 0.042, (900, 12): 0.045
        }
        return interest_matrix[score//100*100, parcela]

    def set_refused(self, client, refused):
        client.status = 'CP' #Complete
        client.result = 'RF' #Refused
        client.refused_policy = refused
        client.save()

    def set_approved(self, client, amount, terms):
        client.status = 'CP' #Complete
        client.result = 'AP' #Approved
        #client.amount_approved = amount
        client.amount_approved = client.amount_wanted
        client.terms_approved = terms
        client.save()

    def is_approved(self,client, parcela):
        while (parcela <= 12):
            #(1-compromentimento de renda)*renda mensal
            parcela_possivel = (1-self.get_commitment(client.cpf))*float(client.income)
            #Valor desejado
            pv = float(client.amount_wanted)
            #Calculo da taxa de Jurus
            i = self.get_interest_rate(self.get_score(client.cpf), parcela)
            #calculo da parcela
            aux = (1+i)**parcela
            pmt = pv*((aux*i)/(aux-1))

            if pmt <= parcela_possivel:
                self.set_approved(client, pmt, parcela)
                return True
            else:
                #tenta uma parcela menor
                parcela += 3

        return False
        
    def get_score(self, cpf, url='https://challenge.noverde.name/score'):
        '''
            Colocar validacao para caso o servico não estiver funcionando, ele tentar  rodar a task depois
        '''
        r = requests.post(url, headers={'x-api-key':'SnAB7jQEFs1Ai8XtZdssa14gORT3jWPI7TWdXN97'}, json={'cpf':cpf})
        if r.status_code == 200:
            stream = io.BytesIO(r.content)
            data = JSONParser().parse(stream)
            #return data['score']
            return 700

    def get_commitment(self, cpf, url='https://challenge.noverde.name/commitment'):
        '''
            Colocar validacao para caso o servico não estiver funcionando, ele tentar  rodar a task depois
        '''
        r = requests.post(url, headers={'x-api-key':'SnAB7jQEFs1Ai8XtZdssa14gORT3jWPI7TWdXN97'}, json={'cpf':cpf})
        if r.status_code == 200:
            stream = io.BytesIO(r.content)
            data = JSONParser().parse(stream)
            #return data['commitment']
            return 0.5

    #Log no shell celery
    def get_log_celery(self, client):
        return "Client %s: %s - %s" % (client.id, client.get_result_display(), client.get_refused_policy_display())


@shared_task
def credit_motor(pk):
    try:
        validate = ValidateCredit()
        client = Client.objects.get(pk=pk)

        #AGE POLITCY
        #Refused: older
        if client.get_age() <= 18:
            validate.set_refused(client, 'AG')
            return validate.get_log_celery(client)

        #SCORE POLICY
        # Refused: score < 600
        elif validate.get_score(client.cpf) < 600:
            validate.set_refused(client, 'SC')
            return validate.get_log_celery(client)


        elif validate.is_approved(client, client.terms_wanted):
            return validate.get_log_celery(client)
        else:
            #COMMITMENT POLICY
            # Refused: income < expenses        
            validate.set_refused(client, 'CM')
            return validate.get_log_celery(client)

    except client.DoesNotExist:
        pass

