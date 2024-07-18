from django.urls import path
from .views import RegisterView, LoginView, TimesheetView, register_page, login_page, timesheet_page

urlpatterns = [
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('timesheet/', timesheet_page, name='timesheet_page'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/timesheet/', TimesheetView.as_view(), name='timesheet'),
]
