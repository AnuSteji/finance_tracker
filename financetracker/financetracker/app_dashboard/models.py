from django.db import models

from app_core.models import Location
from financetracker.users.models import User


# Create your models here.
class UserRegistration(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    contact=models.CharField(max_length=10)
    img=models.ImageField(upload_to='images/')
    address=models.TextField(max_length=100)
    location=models.ForeignKey(Location, on_delete=models.CASCADE)



