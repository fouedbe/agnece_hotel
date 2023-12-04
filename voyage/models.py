from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Hotel(models.Model):
    name=models.CharField(max_length=40)
    hotel_image= models.ImageField(upload_to='hotel_image/',null=True,blank=True)
    prix = models.PositiveIntegerField()
    description=models.CharField(max_length=40)
    def __str__(self):
        return self.name
class Voiture(models.Model):
    name=models.CharField(max_length=40)
    voiture_image= models.CharField(max_length=40000)
    prix = models.PositiveIntegerField()
    description=models.CharField(max_length=40)
    def __str__(self):
        return self.name


class Orders(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed')
       
    )
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    hotel=models.ForeignKey('Hotel',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
