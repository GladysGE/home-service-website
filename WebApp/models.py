from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class ContactDb(models.Model):
    FullName=models.CharField(max_length=100,null=True,blank=True)
    Email=models.EmailField(max_length=100,null=True,blank=True)
    Subject=models.CharField(max_length=100,null=True,blank=True)
    Message=models.CharField(max_length=100,null=True,blank=True)
class RegisterDb(models.Model):
    Username=models.CharField(max_length=100,null=True,blank=True)
    Email=models.EmailField(max_length=100,null=True,blank=True)
    Password=models.CharField(max_length=100,null=True,blank=True)
    Confirm_Password=models.CharField(max_length=100,null=True,blank=True)

class CartDb(models.Model):
    Username=models.CharField(max_length=100,null=True,blank=True)
    Service_Name=models.CharField(max_length=100,null=True,blank=True)
    Discount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    Discount_Type = models.CharField(max_length=10, choices=[('fixed', 'Fixed'), ('percent', 'Percent')],default='fixed')
    Total_Price=models.FloatField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if CartDb.objects.filter(Username=self.Username).exists() and not self.pk:
            raise ValidationError("Only one service can be added to the cart.")
        super().save(*args, **kwargs)
class BookingDb(models.Model):
    Name=models.CharField(max_length=100,null=True,blank=True)
    Email = models.EmailField(max_length=100, null=True, blank=True)
    Phone=models.IntegerField(null=True,blank=True)
    Date=models.DateField()
    Time=models.TimeField()
    Address=models.CharField(max_length=100,null=True,blank=True)
    Complaint_image=models.ImageField(upload_to="complaint_images",null=True,blank=True)
    Description=models.CharField(max_length=100,null=True,blank=True)
    Total_Price=models.FloatField(null=True,blank=True)


    def __str__(self):
        return f"Booking on {self.date} at {self.time}"

    def save(self, *args, **kwargs):
        # Additional logic can be added here before saving, if needed
        super().save(*args, **kwargs)