from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from common.views import TitleMixin
from django.views.generic.base import TemplateView
from users.models import Employee
from vacations.forms import TakeVacationForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from datetime import datetime
import json
from django.utils import timezone
from .models import Vacations
from datetime import timedelta


class TakeVacationView(TitleMixin, CreateView):
    model = Vacations
    form_class = TakeVacationForm
    template_name = 'vacations/takeVacation.html'
    success_url = reverse_lazy('index')
    title = 'Take vacation'

    def form_valid(self, form):
        employee = Employee.objects.get(username=self.request.user.username)
        date_of_begin = form.cleaned_data['date_of_begin']
        date_of_end = form.cleaned_data['date_of_end']
        dif = (date_of_end - date_of_begin) / (1000 * 3600 * 24)
        available_vacation = ((dif.days / 365) * 28) - 28

        # if available_vacation < dif.days:
        #     form.add_error(None, 'Недостаточно доступных дней отпуска')
        #     return self.form_invalid(form)
        # else:
        employee.available_vacation = available_vacation
        employee.status = 'on vacation'
        employee.save()
        vacation = form.save(commit=False)
        vacation.employee = employee

        if date_of_begin <= timezone.now().date():
            vacation.status = 'now'
        else:
            vacation.status = 'planed'

        vacation.save()

        return super().form_valid(form)


# class VacationCalendarView(TitleMixin, ListView):
#     template_name = 'vacations/vacationCalendar.html'
#     model = Vacations
#     context_object_name = 'vacations'
#     title = 'Calendar of vacations'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         today = timezone.now().date()
#         # filter vacations that are either ongoing or haven't started yet
#
#         vacations = self.model.objects.filter(date_of_end__gte=today)
#         vacations_data = [
#             {
#                 'start': vacation['date_of_begin'].isoformat(),
#                 'end': vacation['date_of_end'].isoformat(),
#                 'range_of_dates': [i for i in range(vacation["date_of_begin"].day, vacation["date_of_end"].day + 1)],
#                 'employee': f"{vacation['employee__first_name']} {vacation['employee__last_name']}",
#                 'status': vacation['status']
#             }
#             for vacation in
#             vacations.values('date_of_begin', 'date_of_end', 'employee__first_name', 'employee__last_name', 'status')
#         ]
#         context['vacations_data'] = json.dumps(vacations_data)
#         return context

class VacationCalendarView(TitleMixin, ListView):
    template_name = 'vacations/vacationCalendar.html'
    model = Vacations
    context_object_name = 'vacations'
    title = 'Calendar of vacations'

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_id = self.kwargs.get('employee_id')
        return queryset.filter(employee_id=employee_id) if employee_id else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        # filter vacations that have already ended
        past_vacations = self.model.objects.filter(date_of_end__lt=today, status='past').order_by('-date_of_end')

        # filter vacations that are currently ongoing
        now_vacations = self.model.objects.filter(date_of_begin__lte=today, date_of_end__gte=today, status='now').order_by('date_of_begin')


        # filter vacations that haven't started yet
        upcoming_vacations = self.model.objects.filter(date_of_end__gt=today, status='planned').order_by('date_of_begin')

        # format past vacations data
        past_vacations_data = [{
            'start': vacation.date_of_begin.strftime('%Y-%m-%d'),
            'end': vacation.date_of_end.strftime('%Y-%m-%d'),
            'range_of_dates': [vacation.date_of_begin + timedelta(days=x) for x in
                               range((vacation.date_of_end - vacation.date_of_begin).days + 1)],
            'employee': f"{vacation.employee.first_name} {vacation.employee.last_name}",
            'status': vacation.status
        } for vacation in past_vacations]

        # format now vacations data
        now_vacations_data = [{
            'start': vacation.date_of_begin.strftime('%Y-%m-%d'),
            'end': vacation.date_of_end.strftime('%Y-%m-%d'),
            'range_of_dates': [vacation.date_of_begin + timedelta(days=x) for x in
                               range((vacation.date_of_end - vacation.date_of_begin).days + 1)],
            'employee': f"{vacation.employee.first_name} {vacation.employee.last_name}",
            'status': vacation.status
        } for vacation in now_vacations]

        # format upcoming vacations data
        upcoming_vacations_data = [{
            'start': vacation.date_of_begin.strftime('%Y-%m-%d'),
            'end': vacation.date_of_end.strftime('%Y-%m-%d'),
            'range_of_dates': [vacation.date_of_begin + timedelta(days=x) for x in
                               range((vacation.date_of_end - vacation.date_of_begin).days + 1)],
            'employee': f"{vacation.employee.first_name} {vacation.employee.last_name}",
            'status': vacation.status
        } for vacation in upcoming_vacations]

        context['past_vacations_data'] = past_vacations_data
        context['now_vacations_data'] = now_vacations_data
        context['upcoming_vacations_data'] = upcoming_vacations_data
        return context



# class VacationCalendarView(TitleMixin, ListView):
#     template_name = 'vacations/vacationCalendar.html'
#     model = Vacations
#     context_object_name = 'vacations'
#     title = 'Calendar of vacations'
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         employee_id = self.kwargs.get('employee_id')
#         return queryset.filter(employee_id=employee_id) if employee_id else queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         today = timezone.now().date()
#
#         # filter vacations that have already ended
#         past_vacations = self.model.objects.filter(date_of_end__lt=today, status='past').order_by('-date_of_end')
#
#         # filter vacations that are currently ongoing or haven't started yet
#         upcoming_vacations = self.model.objects.filter(date_of_end__gte=today, status='planned').order_by('date_of_begin')
#
#         # format past vacations data
#         past_vacations_data = [{
#             'start': vacation.date_of_begin.strftime('%Y-%m-%d'),
#             'end': vacation.date_of_end.strftime('%Y-%m-%d'),
#             'range_of_dates': [vacation.date_of_begin + timedelta(days=x) for x in
#                                range((vacation.date_of_end - vacation.date_of_begin).days + 1)],
#             'employee': f"{vacation.employee.first_name} {vacation.employee.last_name}",
#             'status': vacation.status
#         } for vacation in past_vacations]
#
#         # format upcoming vacations data
#         upcoming_vacations_data = [{
#             'start': vacation.date_of_begin.strftime('%Y-%m-%d'),
#             'end': vacation.date_of_end.strftime('%Y-%m-%d'),
#             'range_of_dates': [vacation.date_of_begin + timedelta(days=x) for x in
#                                range((vacation.date_of_end - vacation.date_of_begin).days + 1)],
#             'employee': f"{vacation.employee.first_name} {vacation.employee.last_name}",
#             'status': vacation.status
#         } for vacation in upcoming_vacations]
#
#         context['past_vacations_data'] = past_vacations_data
#         context['upcoming_vacations_data'] = upcoming_vacations_data
#         return context



class VacationHistoryView(TitleMixin, TemplateView):
    template_name = 'vacations/vacationHistory.html'
    title = 'History of vacations'

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_id = self.kwargs.get('employee_id')
        return queryset.filter(employee_id=employee_id) if employee_id else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        past_vacations = Vacations.objects.filter(date_of_end__lt=datetime.now())
        for vacation in past_vacations:
            vacation.dates_between = [vacation.date_of_begin + timedelta(days=x) for x in range((vacation.date_of_end - vacation.date_of_begin).days + 1)]
        context['past_vacations'] = past_vacations
        return context


class VacationInfoView(TitleMixin, TemplateView):
    model = Employee
    template_name = 'vacations/vacationInfo.html'
    title = 'Info about vacation'
    success_url = reverse_lazy('users:profile')
    title = 'Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class VacationRequestsView(TitleMixin, ListView):
    model = Vacations
    template_name = 'vacations/vacationRequests.html'
    title = 'Vacation requests'

    def get_queryset(self):
        queryset = super(VacationRequestsView, self).get_queryset()
        employee_id = self.kwargs.get('employee_id')
        return queryset.filter(employee_id=employee_id) if employee_id else queryset
