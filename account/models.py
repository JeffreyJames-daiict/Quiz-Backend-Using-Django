from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,verbose_name='User Object')  #Define the relationship  
    # on-delete = models.CASCADE means when the record get delete all the related rows should also get deleted
    # on_delete = models.SET_NULL means when the recrd gets deleted then all the related rows get the null values
    #verbose_name 
    email_address = models.CharField(max_length=55,unique=True,null=True,verbose_name='Email')
    bio = models.TextField( blank=True,null=True)
    profile_image = models.ImageField(upload_to='profile_images',default='user.png',blank=True,null=True,verbose_name='Profile Pic')
    location = models.CharField(max_length=100,blank=True,null=True)
    GENDER = (
            ('Male','Male'),
            ('Female','Female'),
            ('Other','Other'),
    )
    gender = models.CharField(max_length=6,choices=GENDER,blank=True,null=True)

    def __str__(self):
        return self.user.username


    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
