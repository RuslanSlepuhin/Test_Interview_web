from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from distrib.views import MessagesViews, ClientViews, DistributionViews, SendToClient, MessagesWaitViews, StatisticViews

router = routers.DefaultRouter()
router.register(r'messages', MessagesViews, basename='Messages')
router.register(r'clients', ClientViews, basename='Clients')
router.register(r'distributions', DistributionViews, basename='Distribution')
router.register(r'messages-wait', MessagesWaitViews, basename='Wait')
router.register(r'statistic', StatisticViews, basename='statistic')

schema_view2 = get_swagger_view(title='EndPoints')

urlpatterns = [
    path('api/', include(router.urls)),
    path('send/', SendToClient.as_view()),
    path('docs/', schema_view2),
]
