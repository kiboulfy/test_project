from django.db import models
from django.conf import settings


# Create your models here.

class Ad(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    condition = models.ForeignKey('Condition', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name
    

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принят'),
        ('declined', 'Отклонён'),
    ]

    ad_sender = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='recieved_proposals')
    comment = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default='pending')
    created_at = created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ad_sender} exchange to {self.ad_receiver}, status: {self.status}'
 