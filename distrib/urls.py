from django.urls import path, include
from rest_framework import routers

from distrib.views import MessagesViews, ClientViews, DistributionViews, SendToClient

router_messages = routers.SimpleRouter()
router_messages.register(r'messages', MessagesViews)
router_clients = routers.SimpleRouter()
router_clients.register(r'clients', ClientViews)
router_distribution = routers.SimpleRouter()
router_distribution.register(r'distributions', DistributionViews)



urlpatterns = [
    path('api/', include(router_messages.urls)),
    path('api/', include(router_clients.urls)),
    path('api/', include(router_distribution.urls)),
    path('api/send/', SendToClient.as_view()),
]