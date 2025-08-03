from django.db import models

# Create your models here.

class Student(models.Model):

    # id = models.AutoField()    Django Automatically adds this field 
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(null=True , blank=True)
    photo = models.ImageField()
    address = models.TextField()
    files = models.FileField()


class Car(models.Model):
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    color = models.CharField(max_length=20)