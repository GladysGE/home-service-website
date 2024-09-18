from django.db import models

# Create your models here.
class Add_Categorydb(models.Model):
    Category_Name=models.CharField(max_length=100,null=True,blank=True)
    Category_Image=models.ImageField(upload_to="Category Images",null=True,blank=True)
    Description=models.CharField(max_length=100,null=True,blank=True)
class Add_Servicedb(models.Model):
    Category=models.CharField(max_length=100,null=True,blank=True)
    Service_Name=models.CharField(max_length=100,null=True,blank=True)
    Price=models.IntegerField(null=True,blank=True)
    Discount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    Discount_Type=models.CharField(max_length=100,choices=[('fixed','Fixed'),('percent','Percent')],null=True)
    Description=models.CharField(max_length=100,null=True,blank=True)
    Service_Image=models.ImageField(upload_to="Service Images",null=True,blank=True)
    Included=models.CharField(max_length=100,null=True,blank=True)
    Excluded=models.CharField(max_length=100,null=True,blank=True)
class ServiceTypedb(models.Model):
    Service_Name=models.CharField(max_length=100,null=True,blank=True)
    Service_Type=models.CharField(max_length=100,null=True,blank=True)
    Price=models.IntegerField(null=True,blank=True)
class State(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
class City(models.Model):
    cname = models.CharField(max_length=100,null=True,blank=True)
    sname = models.CharField(max_length=100,null=True,blank=True)
class Service(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)


