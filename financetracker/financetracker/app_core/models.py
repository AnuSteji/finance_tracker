from django.db import models


class District(models.Model):
    name=models.CharField(max_length=100)

class Location(models.Model):
    name = models.CharField(max_length=100)
    dis = models.ForeignKey(District, on_delete=models.CASCADE)

class Category(models.Model):
    name=models.CharField(max_length=20)
    description=models.CharField(max_length=100)
    img=models.ImageField(upload_to="media/",null=True,blank=True)

class Incomehead(models.Model):
   namefield=models.CharField(max_length=50) 

class Expensehead(models.Model):
   name=models.CharField(max_length=50)
   description=models.CharField(max_length=500)

   