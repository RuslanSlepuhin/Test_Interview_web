import datetime
import random
import threading
import pytz
import requests
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
import time
from distrib.models import Messages, Client, Distribution, MessagesWait, Statistic
from distrib.serializers import MessagesSerializer, ClientSerializer, DistributionSerializer, SendSerializer, \
    StatisticSerializer, MessagesWaitSerializer


class MessagesViews(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = [permissions.AllowAny]

class MessagesWaitViews(viewsets.ModelViewSet):
    queryset = MessagesWait.objects.all()
    serializer_class = MessagesWaitSerializer
    permission_classes = [permissions.AllowAny]

class ClientViews(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]

class DistributionViews(viewsets.ModelViewSet):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer
    permission_classes = [permissions.AllowAny]

class StatisticViews(viewsets.ModelViewSet):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
    permission_classes = [permissions.AllowAny]

class SendToClient(generics.GenericAPIView):
    queryset = Messages.objects.all()
    queryset_distribution = Distribution.objects.all()
    queryset_client = Client.objects.all()

    serializer_class = SendSerializer


    def post(self, request):

        serializer = SendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.reqest = request

        self.client_queryset_object = Client.objects.filter(
            tag=request.data['filter_tag'],
            code_phone=request.data['filter_phone_code']
        )

        self.distribution_queryset_object = Distribution.objects.get(
            id_distribution=int(request.data['id_distribution'])
        )

        self.distribution_message = self.distribution_queryset_object.message_text
        self.distibution_id = self.distribution_queryset_object.id_distribution
        self.time_start = self.distribution_queryset_object.date_start
        self.time_stop = self.distribution_queryset_object.date_end

        self.start_schedule()

        return Response(self.response)


    def start_schedule(self):

        if datetime.datetime.now(pytz.utc).time() <= self.time_start.time():
            thread = threading.Thread(target=self.while_loop())
            thread.start()
        elif datetime.datetime.now(pytz.utc).time() >= self.time_stop.time():
            self.response = {"message": "distribution's time is out"}
        else:
            self.send_messages()


    def while_loop(self):
        while datetime.datetime.now(pytz.utc).time() < self.time_start.time():
            time.sleep(5)
        else:
            self.send_messages()

    def send_messages(self):

        self.__my_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTMwNDA5MDUsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IlJ1c2xhblNMUCJ9.WNKYtH7IEZ8QGvz9TKdSwHKWjxkmBLWhROyLXcF3zwg"
        headers = {'Authorization': f'Bearer {self.__my_token}'}

        self.count = int(datetime.datetime.now().strftime("%H%M"))+random.randrange(1, 20)
        self.parameter_for_output_statistic = datetime.datetime.now(pytz.utc)

        count_client = 1
        for client in self.client_queryset_object:

            self.client_id = client.id_client

            self.phone = client.phone_number
            self.count += 1
            status_code = None
            data = {"id": self.count, "phone": self.phone, "text": self.distribution_message}

            attempt = 1

            if datetime.datetime.now(pytz.utc).time()<self.time_stop.time():

                while status_code != 200 and datetime.datetime.now(pytz.utc).time()<self.time_stop.time() and attempt<=3:
                    response = requests.post(
                        url=f'https://probe.fbrq.cloud/send/{self.count}/',
                        data=data,
                        headers=headers
                    )

                    status_code = response.status_code
                    attempt += 1

                    if status_code != 200:
                        time.sleep(1)

                Statistic.objects.create(
                    id_message=self.count,
                    status=status_code,
                    attempt=attempt-1,
                    id_distr=self.distribution_queryset_object,
                    id_client=client)

                if attempt<3:
                    Messages.objects.create(
                        id_message=self.count,
                        status=str(status_code),
                        id_distr=self.distribution_queryset_object,
                        id_client=client)
                else:
                    MessagesWait.objects.create(
                        id_message=self.count,
                        status=str(status_code),
                        id_distr=self.distribution_queryset_object,
                        id_client=client)

            else:
                MessagesWait.objects.create(
                    id_message=self.count,
                    status=str(status_code),
                    id_distr=self.distribution_queryset_object,
                    id_client=client)

                Statistic.objects.create(
                    id_message=self.count,
                    status='time is out',
                    attempt=0,
                    id_distr=self.distribution_queryset_object,
                    id_client=client)

        queryset = Statistic.objects.filter(date_send__gte=self.parameter_for_output_statistic)
        self.response = {'Statistic': StatisticSerializer(queryset, many=True).data}

