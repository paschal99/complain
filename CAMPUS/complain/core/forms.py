from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import User, Student, BuildingEstateDepartment, AccommodationOfficeDepartment, Complaint, Feedback, SystemAdmin
from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class SystemAdminSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    phone = forms.CharField(widget=forms.TextInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_system_admin = True
        if commit:
            user.save()
        student = SystemAdmin.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'), phone=self.cleaned_data.get('phone'))
        return user



class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    course = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    reg_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    room_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if phone_no.isdigit():
            # Ensure the phone number starts with +255
            phone_no = '+255' + phone_no
        else:
            raise forms.ValidationError("Phone number must start with a number.")
        return phone_no


    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        student = Student.objects.create(
            user=user,
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            course=self.cleaned_data.get('course'),
            reg_no=self.cleaned_data.get('reg_no'),
            room_name=self.cleaned_data.get('room_name'),
            phone_no=self.cleaned_data.get('phone_no')  # Ensure phone_no is saved in the correct format
        )
        return user


class BuildingStateSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    department_head = forms.CharField(widget=forms.TextInput())
    department_name = forms.CharField(widget=forms.TextInput())
    phone_no= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_building_estate = True
        if commit:
            user.save()
        build = BuildingEstateDepartment.objects.create(user=user, department_head=self.cleaned_data.get('department_head'), department_name=self.cleaned_data.get('department_name'))
        return user


class AccommodationSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    department_head = forms.CharField(widget=forms.TextInput())
    department_name = forms.CharField(widget=forms.TextInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_accomodation = True
        if commit:
            user.save()
        accommodation = AccommodationOfficeDepartment.objects.create(user=user, department_head=self.cleaned_data.get('department_head'), department_name=self.cleaned_data.get('department_name'))
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your complaint'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
