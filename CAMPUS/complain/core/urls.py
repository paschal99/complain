from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("student/", views.student_home, name="student-home"),
    path("system_admin/", views.admin_home, name="admin_home"),
    path("accommodation/", views.accommodation_home, name="accommodation-home"),
    path("building/", views.building_home, name="building-home"),
    path('delete_complaint/<int:complaint_id>/', views.delete_complaint_view, name='delete_complaint'),

    #These are Authentication urls
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout_view/", views.logout_view, name="logout"),
    path("signup/system_admin/", views.StudentSignUpView.as_view(), name="system_admin-signup"),
    path("signup/student/", views.StudentSignUpView.as_view(), name="student-signup"),
    path("signup/building/", views.BuildingSignUpView.as_view(), name="building-signup"),
    path("signup/accommodation/", views.AccommodationSignUpView.as_view(), name="accommodation-signup"),


    #These are urls pages handling complaints
    path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
    path('register_complaint/', views.register_complaint, name='register_complaint'),
    path('complaint_list/',views.complaint_list,name='complaint_list'),
    path('generate_pdf/',views.generate_pdf, name='generate_pdf'),
    # path('forward_complaint/<int:complaint_id>/', views.forward_complaint, name='forward_complaint'),
    # path('resolve_complaint/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),


    path('pending_complaints/', views.pending_complaints, name='pending_complaints'),
   
    path('building_complaints/', views.building_complaints, name='building_complaints'),
    
    path('my_complaints/', views.my_complaints, name='my_complaints'),

    # path('send-automated-sms/', views.send_automated_sms, name='send_automated_sms'),

    # These are the urls pages for password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)