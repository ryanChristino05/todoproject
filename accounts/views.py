from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .forms import CustomUserCreationForm

def login_user(request):#contenant l'url où on est en ce moment
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("tasks:task_list")
        else:
            messages.info(request,"Identifiant ou mot de passe incorrect")

    form = AuthenticationForm()
    # Modifier le formulaire ici
    form.fields['username'].label = "Nom d'utilisateur"
    form.fields['password'].label = "Mot de passe"
    
    return render(request,"accounts/login.html",{"form":form})        

def logout_user(request):
    logout(request)
    return redirect("accounts:login")

def register_user(request):
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("accounts:login")
        else:
            messages.error(request,"Erreur lors de l'inscritption !")
    form=CustomUserCreationForm()
    return render(request,"accounts/register.html",{"form":form})

