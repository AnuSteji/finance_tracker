from django.db import models

from app_core.models import Expensehead, Incomehead
from financetracker.users.models import User


# Create your models here.
class IncomeDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    incomehead=models.ForeignKey(Incomehead,on_delete=models.CASCADE)
    date=models.DateField()
    create_date=models.DateField(auto_now_add=True)
    amount=models.TextField()

class ExpenseDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    expensehead=models.ForeignKey(Expensehead,on_delete=models.CASCADE)
    description=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateField()
    create_date=models.DateField(auto_now_add=True)
    amount=models.TextField()

class BudgetDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    expensehead=models.ForeignKey(Expensehead,on_delete=models.CASCADE)
    month=models.CharField(max_length=20)
    create_date=models.DateField(auto_now_add=True)
    amount=models.TextField()
