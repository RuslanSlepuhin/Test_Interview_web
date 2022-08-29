from rest_framework import serializers

from distrib.models import Messages, Client, Distribution, Send, Statistic, MessagesWait

class MessagesSerializer(serializers.ModelSerializer):


    class Meta:
        model = Messages
        fields = '__all__'

class MessagesWaitSerializer(serializers.ModelSerializer):


    class Meta:
        model = MessagesWait
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):


    class Meta:
        model = Client
        fields = '__all__'

class DistributionSerializer(serializers.ModelSerializer):


    class Meta:
        model = Distribution
        fields = '__all__'

class SendSerializer(serializers.ModelSerializer):


    class Meta:
        model = Send
        fields = ['id_distribution', 'filter_phone_code', 'filter_tag']

class StatisticSerializer(serializers.ModelSerializer):


    class Meta:
        model = Statistic
        fields = '__all__'
