from django.contrib.auth.models import User
from django.db import models


class Toronto311(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(blank=True, null=True, max_length=30)
    first_3_chars_of_postal_code = models.CharField(blank=True, null=True, max_length=30)
    intersection_street_1 = models.CharField(blank=True, null=True, max_length=50)
    intersection_street_2 = models.CharField(blank=True, null=True, max_length=50)
    ward = models.CharField(blank=True, null=True, max_length=50)
    service_request_type = models.CharField(blank=True, null=True, max_length=100)
    division = models.CharField(blank=True, null=True, max_length=100)
    section = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return self.service_request_type