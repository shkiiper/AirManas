from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from users.views import UserLoginView, UserProfileView, ChangeEmployee, AddNewEmployeeAPIView, DashboardView, EmployeeListView, EmployeeRetrieveAPIView, AddNewEmployeeView


app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('change_employee/', ChangeEmployee.as_view(), name='change_employee'),
    path('addemployee/', AddNewEmployeeAPIView.as_view(), name='addemployee'),
    path('add_employee/', AddNewEmployeeView.as_view(), name='add_employee'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:id>/', EmployeeRetrieveAPIView.as_view(), name='employee-detail'),
]
