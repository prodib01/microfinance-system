from django.db import models
from django.core.exceptions import ValidationError
from utilities.choices import type_choices


class Account(models.Model):

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    account_type = models.CharField(
        max_length=10, choices=type_choices, default='ASSET')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateTimeField()
    amount = models.IntegerField()
    title = models.CharField(max_length=255)
    note = models.TextField(null=True, blank=True)
    is_debit = models.BooleanField()

    def clean(self):
        if self.account.children.exists():
            raise ValidationError(
                'You cannot post a transaction to a parent account')

    def __str__(self):
        return self.title + ' - ' + self.account.name + ' - ' + str(self.amount) + ' - ' + str(self.date)
