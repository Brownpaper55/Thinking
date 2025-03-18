from django.shortcuts import render, redirect
from .models import Profile, Thoughts
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ThoughtForm, SignUpForm, Profile_picForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        thoughts= Thoughts.objects.all().order_by('-created_at')
        form = ThoughtForm(request.POST or None)
        if request.method == 'POST':
            thought = form.save(commit=False)
            thought.user = request.user
            thought.save()
            messages.success(request, 'Thoughts shared!')
            return redirect('home')
        return render(request, 'home.html', {'thoughts':thoughts, 'form':form})
    return render(request, 'home.html')

def profile_list(request):
    if request.user.is_authenticated:
        profile = Profile.objects.exclude(user = request.user)
        return render(request, 'profile_list.html', {'profile':profile})
    else:
        return redirect('home')
    
def profile(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        thoughts = Thoughts.objects.filter(user_id = pk)
        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request,'profile.html', {'profile':profile,'thoughts':thoughts})
    else:
        return redirect('home')


def login_user(request):
    if request.method== 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username = username,password= password)
        if user is not None:
            login(request, user)
            messages.success(request,'Login succesful')
            return redirect('home')
        else:
            messages.error(request,'user doesnt exist')
            return redirect('login')

    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password2 = form.cleaned_data['password2']
            user = authenticate(username=username, password=password2)
            login(request, user)
            messages.success(request,'login successful!')
            return redirect('home')
    return render(request, 'register.html', {'form':form})
   

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id= request.user.id)
        image_user = Profile.objects.get(user_id = request.user.id)
        print(request.user.id)
        form = SignUpForm(request.POST or None, request.FILES or None, instance= current_user)
        P_image = Profile_picForm(request.POST or None, request.FILES or None, instance = image_user)
        if form.is_valid() and P_image.is_valid():
            form.save()
            P_image.save()
            login(request, current_user)
            messages.success(request, 'Your info has been updated!')
            return redirect('home')
        return render(request, 'update_user.html', {'form':form, 'image':P_image})
    else:
        messages.success(request,'You must be logged in to access this page.')
        return redirect('home')