from django.db import models

class Distribution(models.Model):
    id_distribution = models.IntegerField(unique=True)
    date_start = models.DateTimeField()
    message_text = models.CharField(max_length=2000)
    filter_phone_code = models.CharField(max_length=20)
    filter_tag = models.CharField(max_length=30)
    date_end = models.DateTimeField()

    def __str__(self):
        return str(self.id_distribution)

class Client(models.Model):
    id_client = models.IntegerField(unique=True, blank=False)
    phone_number = models.PositiveBigIntegerField(null=False, blank=False)
    code_phone = models.IntegerField(blank=False)
    tag = models.CharField(max_length=30, blank=True, null=True)
    timezone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return str(self.phone_number)

class Messages(models.Model):
    id_message = models.IntegerField(unique=True, blank=False)
    date_send = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    id_distr = models.ForeignKey("Distribution", on_delete=models.CASCADE)
    id_client = models.ForeignKey("Client", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_message)

class MessagesWait(models.Model):
    id_message = models.IntegerField(unique=False, blank=False)
    date_send = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    id_distr = models.ForeignKey("Distribution", on_delete=models.CASCADE)
    id_client = models.ForeignKey("Client", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_message)

class Statistic(models.Model):
    id_message = models.IntegerField(unique=False, blank=False)
    date_send = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    attempt = models.IntegerField()
    id_distr = models.ForeignKey("Distribution", on_delete=models.CASCADE)
    id_client = models.ForeignKey("Client", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_message)

class Send(models.Model):
    id_distribution = models.IntegerField(unique=True, blank=False, null=False)
    filter_phone_code = models.CharField(max_length=5, blank=False, null=False)
    filter_tag = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return str(self.id_distribution)
