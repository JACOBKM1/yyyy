#from django.contrib import admin
#from .models import *  # Import the User model
#from django.contrib.auth.models import User

#admin.site.register(User)
from django.contrib import admin
from .models import * 
from .models import TrainerSelection

admin.site.register(Userdet)
admin.site.register(TrainerSelection)

