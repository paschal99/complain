from django.shortcuts import redirect, render,get_object_or_404
from django.views.generic import CreateView
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import StudentSignUpForm, AccommodationSignUpForm, BuildingStateSignUpForm, LoginForm,ComplaintForm, FeedbackForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import *
from .sms import *

from django.shortcuts import render, get_object_or_404
from .models import Complaint


CREATE = "Create"
READ = "Read"
UPDATE = "Update"
DELETE = "Delete"
LOGIN = "Login"
LOGOUT = "Logout"
LOGIN_FAILED = "Login Failed"

# Statuses
SUCCESS = "Success"
FAILED = "Failed"


# Create your views here
def log_activity(actor, action_type, status, remarks, data=None):
    try:
        log_entry = ActivityLog.objects.create(
            actor=actor,
            action_type=action_type,
            status=status,
            remarks=remarks,
            data=data or {}
        )
        return log_entry
    except Exception as e:
        # Handle exceptions or log errors if necessary
        print(f"Error logging activity: {e}")

def admin_home(request):
    return render(request, 'core/admin_home.html')


@login_required(login_url='login/')  # Adjust login URL based on your setup
def student_home(request):
    # Assuming the logged-in user is a student, adjust this based on your authentication logic
    student = request.user.student

    # Retrieve all complaints submitted by this student
    total_complaints = Complaint.objects.filter(student=student)

    # Count the total number of complaints
    total_complaint_count = total_complaints.count()

    context = {
        'student': student,
        'total_complaint_count': total_complaint_count,
        'total_complaints': total_complaints  # You can pass this to display detailed complaints if needed
    }

    return render(request, 'student/student_home.html', context)

def accommodation_home(request):
    complaint = Complaint.objects.filter(location='None', status='Pending')
    new_complaints = Complaint.objects.filter(location='None', status='Pending')

    # Count the total number of new complaints
    total_new_complaints = new_complaints.count()

    return render(request, 'accomodation/accommodation_home.html', {'complaint':complaint, 'total_new_complaints':total_new_complaints })


@login_required(login_url='/login/')
def building_home(request):
    return render(request, 'building/building_home.html')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'student/student_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('student-home')


class BuildingSignUpView(CreateView):
    model = User
    form_class = BuildingStateSignUpForm
    template_name = 'building/building_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'building'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('building-home')


def delete_complaint_view(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)

    if request.method == 'POST':
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully.')

    return redirect('my_complaints')

class AccommodationSignUpView(CreateView):
    model = User
    form_class = AccommodationSignUpForm
    template_name = 'accomodation/accommodation_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'accommodation'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accommodation-home')

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'core/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_student:
                return reverse('student-home')
            elif user.is_accomodation:
                return reverse('accommodation-home')
            elif user.is_system_admin:
                return reverse('admin_home')
            elif user.is_building_estate:
                return reverse('building-home')
        else:
            #  messages.error(request, 'Incorrect username or password. Please try again.')
             return reverse('login')


def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user.student
            complaint.save()

            # Log activity for complaint creation
            log_activity(
                actor=request.user,  # The user initiating the action
                action_type=CREATE,  # Action type (using constant)
                status=SUCCESS,  # Status of the action (using constant)
                remarks="Complaint created",  # Remarks or description
                data={'complaint_id': complaint.id}  # Additional data if needed
            )

            # Redirect to a page indicating successful complaint submission
            messages.success(request, "Complaint has been sent.")
            return redirect('submit_complaint')
        else:
            # Handle form validation errors
            messages.error(request, "Error submitting complaint. Please check the form.")
    else:
        form = ComplaintForm()

    context = {'form': form}
    return render(request, 'student/submit_complaint.html', context)
def logout_view(request):
    logout(request)
    return redirect('login')




def complaint_details(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    log_activity(
        actor=request.user,  # The user initiating the action
        action_type=CREATE,  # Action type (using constant)
        status=SUCCESS,  # Status of the action (using constant)
        remarks="view-complain detail",  # Remarks or description
        data={'complaint_id': complaint.id}  # Additional data if needed
    )
    context = {'complaint': complaint}
    return render(request, 'core/complaint_details.html', context)






def pending_complaints(request):
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        complaint = Complaint.objects.get(pk=complaint_id)
        
        complaint.location = request.POST.get('location')
        complaint.save()
        log_activity(
            actor=request.user,  # The user initiating the action
            action_type=CREATE,  # Action type (using constant)
            status=SUCCESS,  # Status of the action (using constant)
            remarks="update complain location",  # Remarks or description
            data={'complaint_id': complaint.id}  # Additional data if needed
        )

        return redirect('building_complaints')
    else:
        # Get pending complaints with status 'Pending'
        pending_complaints = Complaint.objects.filter(location='None').order_by('-created_at')

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(pending_complaints, 2)  # 2 complaints per page
        try:
            pending_complaints = paginator.page(page)
        except PageNotAnInteger:
            pending_complaints = paginator.page(1)
        except EmptyPage:
            pending_complaints = paginator.page(paginator.num_pages)

        location_choices = Complaint.location_choices  # Get location choices

        return render(request, 'core/pending_complaints.html', {'pending_complaints': pending_complaints, 'location_choices': location_choices})



# def get_student_phone_number_from_complaint(complaint_id):
#     try:
#         complaint = Complaint.objects.get(pk=complaint_id)
#         student = complaint.student
#         formatted_phone = format_phone_number(student.phone_no)
#         return {
#             'name': f"{student.first_name} {student.last_name}",
#             'phone_no': formatted_phone
#         }
#     except Complaint.DoesNotExist:
#         return None
#
# def format_phone_number(phone_number):
#     # Function to format phone numbers to international format, assuming Tanzanian numbers
#     if phone_number.startswith('0'):
#         return '+255' + phone_number[1:]
#     elif phone_number.startswith('+'):
#         return phone_number
#     else:
#         return '+255' + phone_number
#
# def building_complaints(request):
#     if request.method == 'POST':
#         complaint_id = request.POST.get('complaint_id')
#         try:
#             complaint = Complaint.objects.get(pk=complaint_id)
#             complaint.status = request.POST.get('status')
#             complaint.feedback = request.POST.get('feedback')
#             complaint.location = request.POST.get('location')
#             complaint.save()
#
#             # Send SMS notification to the student who made the complaint
#             student_data = get_student_phone_number_from_complaint(complaint_id)
#             if student_data:
#                 message = f"Hello {student_data['name']}, thank you for your complaint. We are working on it."
#                 print(message)
#                 print(student_data)
#                 response = send_sms([student_data['phone_no']], message)
#                 # Optionally, print the response for debugging
#                 print('SMS Response:', response)
#                 # Check for errors in SMS response
#                 if response.get('code') != 200:
#                     print(f"Failed to send SMS: {response.get('message')}")
#             else:
#                 print(f'Unable to retrieve student information for complaint ID {complaint_id}')
#
#         except Complaint.DoesNotExist:
#             print(f'Complaint with ID {complaint_id} does not exist.')
#         except Exception as e:
#             print(f'An error occurred: {e}')
#
#         return redirect('building_complaints')
#
#     else:
#         pending_complaints = Complaint.objects.filter(status='Pending').order_by('-created_at')
#
#         # Pagination
#         page = request.GET.get('page', 1)
#         paginator = Paginator(pending_complaints, 2)  # 2 complaints per page
#         try:
#             pending_complaints = paginator.page(page)
#         except PageNotAnInteger:
#             pending_complaints = paginator.page(1)
#         except EmptyPage:
#             pending_complaints = paginator.page(paginator.num_pages)
#
#         location_choices = Complaint.location_choices  # Get location choices
#
#         return render(request, 'Building/building_complaints.html', {
#             'pending_complaints': pending_complaints,
#             'location_choices': location_choices
#         })
def my_complaints(request):
    if request.method == 'POST':
        # If POST request, it means delete action
        complaint_id = request.POST.get('complaint_id')
        complaint = get_object_or_404(Complaint, pk=complaint_id)
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully.')
        return redirect('my_complaints')

    else:
        # If GET request, render the complaints list
        complaints = Complaint.objects.all()
        total_complaints = complaints.count()
        context = {
            'complaints': complaints,
            'total_complaints': total_complaints
        }
        return render(request, 'student/my_complaints.html', context)



def register_complaint(request):
    if request.method == 'POST':
        title_complaint = request.POST.get('Title_complaint')
        user=request.user
        location = request.POST.get('location')
        budget = request.POST.get('budget')
        toolname = request.POST.get('toolname')

        # Save the complaint to the database
        ComplainReport.objects.create(
            Title_complaint=title_complaint,
            staff_name=user,
            location=location,
            budget=budget,
            toolname=toolname
        )
        return redirect('building-home')  # Redirect to a success page or another appropriate page

    return render(request, 'core/register_complaint.html')


def complaint_list(request):
    complaints = ComplainReport.objects.all()
    
    # Fetch login activity logs with content
    login_activity_logs = ActivityLog.objects.filter(action_type=LOGIN).select_related('content_object').order_by('-action_time')
    
    return render(request, 'accomodation/complaint_list.html', {'complaints': complaints, 'login_activity_logs': login_activity_logs})




def generate_pdf(request):
    # Fetch the complaint data
    complaints = ComplainReport.objects.all()

    # Prepare context data
    context = {'complaints': complaints}

    # Render the HTML template with context data
    template_path = 'accomodation/generate_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

    # Create a HttpResponse object and set content type to 'application/pdf'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="complaints.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check for errors
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

def get_student_phone_number_from_complaint(complaint_id):
    try:
        complaint = Complaint.objects.get(pk=complaint_id)
        student = complaint.student
        formatted_phone = format_phone_number(student.phone_no)
        return {
            'name': f"{student.first_name} {student.last_name}",
            'phone_no': formatted_phone
        }
    except Complaint.DoesNotExist:
        return None

def format_phone_number(phone_number):
    # Function to format phone numbers to international format, assuming Tanzanian numbers
    if phone_number.startswith('0'):
        return '+255' + phone_number[1:]
    elif phone_number.startswith('+'):
        return phone_number
    else:
        return '+255' + phone_number

def building_complaints(request):
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        try:
            complaint = Complaint.objects.get(pk=complaint_id)
            complaint.status = request.POST.get('status')
            complaint.feedback = request.POST.get('feedback')
            complaint.location = request.POST.get('location')
            complaint.save()

            # Send SMS notification to the student who made the complaint
            student_data = get_student_phone_number_from_complaint(complaint_id)
            if student_data:
                message = f"Hello {student_data['name']}, thank you for your complaint. We are working on it."
                response = send_sms([student_data['phone_no']], message)
                print('SMS Response:', response)  # Print or log full response for debugging
                # Check for errors in SMS response
                if response.get('code') != 100:
                    print(f"Failed to send SMS: {response.get('message')}")
                    # Log the failure details for further investigation
                    # You can also add logging to a file or external service for better tracking

        except Complaint.DoesNotExist:
            print(f'Complaint with ID {complaint_id} does not exist.')
        except Exception as e:
            print(f'An error occurred: {e}')

        return redirect('building_complaints')

    else:
        pending_complaints = Complaint.objects.filter(status='Pending').order_by('-created_at')

        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(pending_complaints, 2)  # 2 complaints per page
        try:
            pending_complaints = paginator.page(page)
        except PageNotAnInteger:
            pending_complaints = paginator.page(1)
        except EmptyPage:
            pending_complaints = paginator.page(paginator.num_pages)

        location_choices = Complaint.location_choices  # Get location choices

        return render(request, 'Building/building_complaints.html', {
            'pending_complaints': pending_complaints,
            'location_choices': location_choices
        })