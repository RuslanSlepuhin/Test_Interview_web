import datetime
import threading
from datetime import timezone

import pytz
import requests
import schedule
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
import time
from distrib.models import Messages, Client, Distribution
from distrib.serializers import MessagesSerializer, ClientSerializer, DistributionSerializer, SendSerializer


class MessagesViews(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = [permissions.AllowAny]

class ClientViews(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]

class DistributionViews(viewsets.ModelViewSet):
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer
    permission_classes = [permissions.AllowAny]

class SendToClient(generics.GenericAPIView):
    queryset = Messages.objects.all()
    queryset_distribution = Distribution.objects.all()
    queryset_client = Client.objects.all()

    serializer_class = SendSerializer

    def post(self, request):


        serializer = SendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        distribution_queryset = Distribution.objects.filter(
            id_distribution=int(request.data['id_distribution'])
        ).values(
            "message_text",
            "id_distribution",
            "date_start",
            "date_end"
        )

        self.client_queryset = Client.objects.filter(
            tag=request.data['filter_tag'],
            code_phone=request.data['filter_phone_code']
        ).values(
            "phone_number",
            "id_client"
        )

        self.distribution_message = distribution_queryset[0]["message_text"]
        self.distibution_id = distribution_queryset[0]["id_distribution"]
        self.time_start = distribution_queryset[0]["date_start"]
        self.time_stop = distribution_queryset[0]["date_end"]
        self.client_id = self.client_queryset[0]["id_client"]


        self.start_schedule()
        queryset = Messages.objects.filter()
        return Response({'messages in session': MessagesSerializer(queryset, many=True).data})



    def start_schedule(self):
        self.tz = pytz.timezone('Europe/Moscow')
        print(datetime.datetime.now(pytz.utc).time())
        print(self.time_start.time())
        if datetime.datetime.now(pytz.utc).time() < self.time_start.time():
            print('datetime less than start_time')
            thread = threading.Thread(target=self.while_loop())
            thread.start()
        else:
            self.send_messages()


    def while_loop(self):
        while datetime.datetime.now(pytz.utc).time() < self.time_start.time():
            print('less')
            time.sleep(5)
        else:
            self.send_messages()

    def send_messages(self):

        __my_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTMwNDA5MDUsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IlJ1c2xhblNMUCJ9.WNKYtH7IEZ8QGvz9TKdSwHKWjxkmBLWhROyLXcF3zwg"

        self.count = 6
        for client in self.client_queryset:
            print(self.time_stop.time())
            if datetime.datetime.now(pytz.utc).time()<self.time_stop.time():
                self.phone = client["phone_number"]
                pass

                self.count += 1


                headers = {'Authorization': f'Bearer {__my_token}'}
                response = requests.post(f'https://probe.fbrq.cloud/docs/send/{self.count}/',
                                         data={"id": self.count, "phone": self.phone, "text": self.distribution_message},
                                         headers=headers)

                print(response.json)
                new_message = Messages.objects.create(
                    id_message=self.count,
                    status=str(response.status_code),
                    # id_distr = 455,
                    # id_client = 12
                )
            else:
                print('time_is_out')
                break

        # return Response({"id_client": self.client_id, "id_distribution": self.distibution_id, "id_message": self.count, "status": response.status_code})