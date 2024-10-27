from django.db import models
from django.contrib.auth.models import User
class Userdet(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)  # Ensure email is unique
    gender = models.CharField(max_length=10)
    contactno = models.CharField(max_length=15, default='')  # Default value set here
    password = models.CharField(max_length=20)
    age = models.CharField(max_length=20)
    height = models.CharField(max_length=20)
    weight = models.CharField(max_length=50)
    medical_condition = models.CharField(max_length=10)
    accidental_history = models.CharField(max_length=50)
    
    goal = models.CharField(max_length=30, choices=[
        ('weight_gain', 'Weight Gain'),
        ('weight_loss', 'Weight Loss'),
        ('strength_training', 'Strength Training')
    ], default='weight_loss')
    
    equipment = models.CharField(max_length=100, blank=True)  # User can enter multiple equipments
    otherequipment = models.CharField(max_length=100,blank=True)
    

    def __str__(self):
          return f"{self.fname} {self.lname}"


class TrainerSelection(models.Model):
    user = models.ForeignKey(Userdet, on_delete=models.CASCADE)  # Relates to the user who made the selection
    trainer_name = models.CharField(max_length=100)
    scheduled_time = models.TimeField(null=True,blank=True)
    message_log = models.TextField(blank=True,null=True)  # Stores chat messages as a text log
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamps when created

    def __str__(self):
        return f"{self.trainer_name} selected by {self.user.fname} {self.user.lname}"
