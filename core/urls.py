from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core.views import ClientCreateView, ClientRetrieveView

urlpatterns = format_suffix_patterns([

    path('loan/', ClientCreateView.as_view(), name='client-create'),
    path('loan/<str:pk>/', ClientRetrieveView.as_view(), name='client-retrieve'),
])  