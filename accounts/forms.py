from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    fields=('username','email','password1','password2')

    class Meta:
        model=User
        fields=('username','email','password1','password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Modifier les labels
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer le mot de passe"
        self.fields['email'].label = "Adresse email"
        
        # Modifier les messages d'aide
        self.fields['username'].help_text = "Lettres, chiffres et @/./+/-/_ uniquement."
        self.fields['password1'].help_text = "Votre mot de passe doit contenir au moins 8 caractères."
        self.fields['password2'].help_text = "Entrez le même mot de passe pour vérification."
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé")
        return email
