from django.shortcuts import render, redirect
from .models import Userdet,TrainerSelection
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.http import JsonResponse


def home(request):
    error_message = None  # Initialize error_message variable
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        trainers = ['trainer1@gmail.com', 'trainer2@gmail.com', 'trainer3@gmail.com']

        if email in trainers and password == '123':
            return redirect('trainerdashboard')

        # Check if email or password is empty
        if not email or not password:
            error_message = "Both email and password are required."
            
            
        else:
            try:
                # Attempt to retrieve user details if fields are not empty
                log = Userdet.objects.get(email=email, password=password)
                request.session['fname'] = log.fname
                request.session['id'] = log.id
                return redirect('dashboard')

            except Userdet.DoesNotExist:
                error_message = "Email or password is incorrect."

    return render(request, 'home.html', {'error_message': error_message})


def registration(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')       
        contactno = request.POST.get('contactno')
        gender = request.POST.get('gender')
        
        if password != repassword:
            messages.error(request, "Passwords do not match")
            return redirect('registration')

        if Userdet.objects.filter(email=email).exists():
            messages.error(request, "Email id already exists")
            return redirect('registration')

        if Userdet.objects.filter(fname=fname).exists():
            messages.error(request, "A user with this name already exists")
            return redirect('registration')

        myuser = Userdet(
            fname=fname,
            lname=lname,
            email=email,
            password=password,
            gender=gender,
            contactno=contactno
        )
        myuser.save()
        request.session['id'] = myuser.id

        messages.success(request, "Your account has been created successfully!")
        return redirect("userdetails")

    return render(request, "registration.html")



def userdetails(request):
    # Fetch the user based on session ID
    user_id = request.session.get('id')
    
    if not user_id:
        return redirect('home')  # Redirect to home if user is not logged in

    user = Userdet.objects.get(id=user_id)  # Retrieve the user from the database
    
    if request.method == "POST":
        user.age = request.POST.get('age')
        user.height = request.POST.get('height')
        user.weight = request.POST.get('weight')
        user.medical_condition = request.POST.get('medical_condition')
        user.accidental_history = request.POST.get('accidental_history')
        user.save()  # Save the updated user details
        return redirect("goal")  # Redirect to the next page

    return render(request, "userdetails.html", {'userdet': user})





def goal(request):
    user_id = request.session.get('id')
    
    if not user_id:
        return redirect('home')  # Redirect if no user is logged in

    user = Userdet.objects.get(id=user_id)
    
    if request.method == "POST":
        user.goal = request.POST.get('goal')
        user.equipment = request.POST.get('equipment')
        user.otherequipment = request.POST.get('otherequipment')
        user.save()  # Save the updated user goal and equipment details
        return redirect("home")  # Redirect to home after saving

    return render(request, 'goal.html', {'userdet': user})

#@login_required


def dashboard(request):
    user_id = request.session.get('id')
 
    if not user_id:
        return redirect('home')

    userdet = Userdet.objects.get(id=user_id)

    # Retrieve the trainer selection for the user, if it exists
    trainer_selection = TrainerSelection.objects.filter(user=userdet).first()
    message_log = trainer_selection.message_log if trainer_selection else ""

    # Handle form submission for trainer selection, time, and messages
    if request.method == 'POST':
        trainer_name = request.POST.get('trainer_name')
        scheduled_time = request.POST.get('scheduled_time')  # Ensure this value is submitted
        message = request.POST.get('message')

        # Allow message sending without scheduled time
        if message:
            # Create or update TrainerSelection for the user
            trainer_selection, created = TrainerSelection.objects.get_or_create(user=userdet)

            if trainer_name:
                trainer_selection.trainer_name = trainer_name
            if scheduled_time:  # Only update if scheduled_time is provided
                trainer_selection.scheduled_time = scheduled_time
            if trainer_selection.message_log:
                trainer_selection.message_log += f"\n{message}"  # Append new message
            else:
                trainer_selection.message_log = message

            trainer_selection.save()

            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Message is required.'}, status=400)

    context = {
        'userdet': userdet,
        'message_log': message_log  # Pass the message log to the template
    }
    return render(request, 'dashboard.html', context)



def trainerdashboard2(request):
    return render(request,'trainerdashboard2.html')
def trainerdashboard3(request):
    return render(request,'trainerdashboard3.html')


# views.py



# views.py



def trainerdashboard(request):
    trainer_name = "Trainer 1" 
    
    # Get all users who have selected "Trainer 1"
    clients = Userdet.objects.filter(trainerselection__trainer_name=trainer_name)

    # Get messages for those clients
    messages = TrainerSelection.objects.filter(trainer_name=trainer_name)

    context = {
        'clients': clients,
        'messages': messages,
    }
    
    return render(request, 'trainerdashboard.html', context)


