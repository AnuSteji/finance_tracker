from django.db import models

from app_core.models import Expensehead, Incomehead
from financetracker.users.models import User


# Create your models here.
class IncomeDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    incomehead=models.ForeignKey(Incomehead,on_delete=models.CASCADE)
    date=models.DateField()
    create_date=models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class ExpenseDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    expensehead=models.ForeignKey(Expensehead,on_delete=models.CASCADE)
    description=models.CharField(max_length=1000,null=True,blank=True)
    date=models.DateField()
    create_date=models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class BudgetDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    expensehead=models.ForeignKey(Expensehead,on_delete=models.CASCADE)
    month=models.CharField(max_length=10)
    create_date=models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
