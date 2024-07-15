from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

# Create your models here.
CREATE, READ, UPDATE, DELETE = "Create", "Read", "Update", "Delete"
LOGIN, LOGOUT, LOGIN_FAILED = "Login", "Logout", "Login Failed"
ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]

SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_accomodation = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_building_estate = models.BooleanField(default=False)
    is_system_admin = models.BooleanField(default=False)

class ActivityLog(models.Model):
     actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
     action_type = models.CharField(choices=ACTION_TYPES, max_length=15)
     action_time = models.DateTimeField(auto_now_add=True)
     remarks = models.TextField(blank=True, null=True)
     status = models.CharField(choices=ACTION_STATUS, max_length=7, default=SUCCESS)
     data = models.JSONField(default=dict)

     def __str__(self):
        return f"{self.actor} - {self.action_type} - {self.action_time}"

SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]

class Content(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SystemAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='admin')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__ (self):
        return self.first_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    phone_no= models.CharField(max_length=15,default='None',null=True)

    def __str__ (self):
        return self.first_name


class BuildingEstateDepartment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='building')
    department_head = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    phone_no= models.CharField(max_length=15,default='None',null=True)

    def __str__ (self):
        return self.department_head


class AccommodationOfficeDepartment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='accommodation')
    department_head = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    phone_no= models.CharField(max_length=15, default='None',null=True)

    def __str__ (self):
        return self.department_head
   

class Complaint(models.Model):
    location_choices = (
        ('None', 'None'),
        ('accommodation', 'acommodation'),
        ('building', 'building'),
    )

    status_choices = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')
    feedback = models.CharField(max_length=100, null=True, default='None')
    location =  models.CharField(max_length=20, choices=location_choices, default='None', null=True)
    



class Feedback(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='feedbacks')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message = models.TextField()
    receiver= models.CharField(max_length=100)
    sender= models.CharField(max_length=100)

    def __str__(self):
        return self.sender


class ComplainReport(models.Model):
    Title_complaint= models.CharField(max_length=50)
    staff_name= models.CharField(max_length=100)
    location= models.CharField(max_length=100)
    budget= models.CharField(max_length=100)
    toolname= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.sender   


