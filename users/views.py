from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone

from general.models import Trainings
from users.models import Employee
from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, AddNewEmployeeForm
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import filters
from rest_framework import generics
from .serializers import EmployeeSerializer, AddNewEmployeeSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.status import HTTP_201_CREATED

from django.views.generic.base import TemplateView


# Create your views here.
class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Authorization'


class UserProfileView(TitleMixin, UpdateView):
    model = Employee
    form_class = UserProfileForm
    template_name = 'users/profilePage.html'
    success_url = reverse_lazy('users:profile')
    title = 'Profile'

    # def get_object(self, queryset=None):
    #     return get_object_or_404(Employee, id=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            training = Trainings.objects.get(date_of_begin__gte=timezone.now())
            delta = training.date_of_begin - timezone.now().date()
            context['countdown'] = delta.days
        except Trainings.DoesNotExist:
            context['countdown'] = None
        return context

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class DashboardView(TitleMixin, ListView):
    model = Employee
    template_name = 'users/dashboard.html'
    context_object_name = 'employees'
    title = 'Dashboard'

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_id = self.kwargs.get('employee_id')
        return queryset.filter(employee_id=employee_id) if employee_id else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = Employee.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            query = request.GET.get('q', '')
            status_filter = request.GET.get('status', '')
            object_list = self.get_queryset()
            if query:
                object_list = object_list.filter(
                    Q(id__icontains=query) |
                    Q(name__icontains=query) |
                    Q(email__icontains=query) |
                    Q(available_vacation__icontains=query)
                )
            if status_filter:
                object_list = object_list.filter(status=status_filter)
            data = []
            for obj in object_list:
                item = {
                    'id': obj.id,
                    'name': obj.name,
                    'email': obj.email,
                    'available_vacation': obj.available_vacation,
                    'status': obj.status
                }
                data.append(item)
            return JsonResponse({'data': data})
        return super().get(request, *args, **kwargs)


class AddNewEmployeeView(TitleMixin, CreateView):
    model = Employee
    form_class = AddNewEmployeeForm
    template_name = 'users/addNewEmployer.html'
    success_url = reverse_lazy('users:dashboard')
    title = 'New employee'


class AddNewEmployeeAPIView(generics.CreateAPIView):
    serializer_class = AddNewEmployeeSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class ChangeEmployee(TitleMixin, TemplateView):
    template_name = 'users/changeEmployer.html'
    title = 'Update employee'


class EmployeeListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['birthday', 'status', 'doljnost']


from django.views.generic import TemplateView


class EmployeeRetrieveAPIView(TitleMixin, TemplateView):
    template_name = 'users/profilePage.html'
    title = 'Profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = Employee.objects.get(id=self.kwargs['id'])
        context['form'] = UserProfileForm(instance=context['employee'])
        return context

    def post(self, request, *args, **kwargs):
        employee = Employee.objects.get(id=self.kwargs['id'])
        form = UserProfileForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.kwargs['id'],))
