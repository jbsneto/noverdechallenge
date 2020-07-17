from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response

from core.serializers import ClientSerializer
from core.models import Client
from core.task import credit_motor


class ClientCreateView(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        credit_motor.delay(serializer.data['pk'])
        return Response({'id': serializer.data['pk'],}, headers=headers)

class ClientRetrieveView(RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if(serializer.data['status'] == 'PS'):
            return Response({'status': instance.get_status_display()})
        else:
            return Response({
                'status': instance.get_status_display(), 
                'result': instance.get_result_display(),
                'refused_policy': instance.get_refused_policy_display(),
            })

