from django.contrib import admin

from distrib.models import Messages
from distrib.models import Client
from distrib.models import Distribution

admin.site.register(Messages)
admin.site.register(Client)
admin.site.register(Distribution)
