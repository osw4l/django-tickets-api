from django.urls import path, include
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r'tickets', viewsets.TicketViewSet)

urlpatterns = [
    path('', include(router.urls))
]