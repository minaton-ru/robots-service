from django.db import models


class Customer(models.Model):
    email = models.EmailField(max_length=255, blank=False, null=False)

    def __str__(self) -> str:
        return self.email
