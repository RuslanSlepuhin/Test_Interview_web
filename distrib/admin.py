from django.contrib import admin

from distrib.models import Messages, MessagesWait, Statistic, Send, Client, Distribution

admin.site.register(Messages)
admin.site.register(Client)
admin.site.register(Distribution)
admin.site.register(MessagesWait)
admin.site.register(Statistic)
admin.site.register(Send)
