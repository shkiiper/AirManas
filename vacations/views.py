from django.urls import reverse, reverse_lazy
from common.views import TitleMixin
from django.views.generic.base import TemplateView
from users.models import Employee
from vacations.forms import TakeVacationForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from datetime import datetime
from django.utils import timezone
from .models import Vacations
from datetime import timedelta
from .serializers import VacationsSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View


class TakeVacationView(TitleMixin, CreateView):
    model = Vacations
    form_class = TakeVacationForm
    template_name = 'vacations/takeVacation.html'
    success_url = reverse_lazy('index')
    title = 'Take vacation'

    # old var

    def form_valid(self, form):
        employee = Employee.objects.get(username=self.request.user.username)
        date_of_begin = form.cleaned_data['date_of_begin']
        date_of_end = form.cleaned_data['date_of_end']
        dif = (date_of_begin - date_of_end).days
        available_vacation = ((dif / 365) * 28) - 28

        # if available_vacation < dif:
        #     form.add_error(None, 'Недостаточно доступных дней отпуска')
        #     return self.form_invalid(form)

        now = timezone.now().date()
        vacations = Vacations.objects.filter(employee=employee)

        for vacation in vacations:
            if date_of_begin <= vacation.date_of_end and vacation.date_of_begin <= date_of_end:
                form.add_error(None, 'Отпуск уже запланирован на эти даты')
                return self.form_invalid(form)

        employee.available_vacation = available_vacation
        employee.status = 'on vacation' if date_of_begin <= now <= date_of_end else 'working'
        employee.save()
        vacation = form.save(commit=False)
        vacation.employee = employee

        if date_of_end < now:
            vacation.status = 'past'
        elif date_of_begin > now:
            vacation.status = 'planed'
        else:
            vacation.status = 'now'

        vacation.status = 'pending'
        vacation.save()

        return super().form_valid(form)

    # new var
    # def form_valid(self, form):
    #     employee = Employee.objects.get(username=self.request.user.username)
    #     date_of_begin = form.cleaned_data['date_of_begin']
    #     date_of_end = form.cleaned_data['date_of_end']
    #     dif = (date_of_end - date_of_begin).days
    #     available_vacation = ((timezone.now().date() - employee.date_joined).days / 365 * 28)
    #     available_vacation = available_vacation - dif
    #     if available_vacation < dif:
    #         form.add_error(None, 'Недостаточно доступных дней отпуска')
    #         return self.form_invalid(form)
    #
    #     now = timezone.now().date()
    #     vacations = Vacations.objects.filter(employee=employee)
    #
    #     for vacation in vacations:
    #         if date_of_begin <= vacation.date_of_end and vacation.date_of_begin <= date_of_end:
    #             form.add_error(None, 'Отпуск уже запланирован на эти даты')
    #             return self.form_invalid(form)
    #
    #     employee.status = 'on vacation' if date_of_begin <= now <= date_of_end else 'working'
    #     employee.save()
    #     vacation = form.save(commit=False)
    #     vacation.employee = employee
    #     vacation.days_used = dif
    #
    #     if date_of_end < now:
    #         vacation.status = 'past'
    #     elif date_of_begin > now:
    #         vacation.status = 'planed'
    #     else:
    #         vacation.status = 'now'
    #
    #     vacation.save()
    #
    #     return super().form_valid(form)


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

        past_vacations = self.model.objects.filter(date_of_end__lt=today, status='past').order_by('-date_of_end')

        now_vacations = self.model.objects.filter(date_of_begin__lte=today, date_of_end__gte=today,
                                                  status='now').order_by('date_of_begin')

        upcoming_vacations = self.model.objects.filter(date_of_end__gt=today, status='planned').order_by(
            'date_of_begin')

        past_vacations_data = [{
            'start': vacation.date_of_begin.strftime('%Y-%m-%d'),
            'end': vacation.date_of_end.strftime('%Y-%m-%d'),
            'range_of_dates': [vacation.date_of_begin + timedelta(days=x) for x in
                               range((vacation.date_of_end - vacation.date_of_begin).days + 1)],
            'employee': f"{vacation.employee.first_name} {vacation.employee.last_name}",
            'status': vacation.status
        } for vacation in past_vacations]

        now_vacations_data = [{
            'start': vacation.date_of_begin.strftime('%Y-%m-%d'),
            'end': vacation.date_of_end.strftime('%Y-%m-%d'),
            'range_of_dates': [vacation.date_of_begin + timedelta(days=x) for x in
                               range((vacation.date_of_end - vacation.date_of_begin).days + 1)],
            'employee': f"{vacation.employee.first_name} {vacation.employee.last_name}",
            'status': vacation.status
        } for vacation in now_vacations]

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


class VacationCalendarAPIView(ListView):

    def get(self, request, *args, **kwargs):
        employee_id = self.kwargs.get('employee_id')
        vacations = Vacations.objects.filter(employee_id=employee_id)

        today = timezone.now().date()

        past_vacations = vacations.filter(date_of_end__lt=today, status='past').order_by('-date_of_end')

        now_vacations = vacations.filter(date_of_begin__lte=today, date_of_end__gte=today,
                                         status='now').order_by('date_of_begin')

        upcoming_vacations = vacations.filter(date_of_end__gt=today, status='planed').order_by(
            'date_of_begin')

        past_vacations_data = [{
            'start': vacation.date_of_begin.strftime('%Y-%m-%d'),
            'end': vacation.date_of_end.strftime('%Y-%m-%d'),
            'range_of_dates': [vacation.date_of_begin + timedelta(days=x) for x in
                               range((vacation.date_of_end - vacation.date_of_begin).days + 1)],
            'employee': f"{vacation.employee.first_name} {vacation.employee.last_name}",
            'status': vacation.status
        } for vacation in past_vacations]

        now_vacations_data = [
            {'start': vacation.date_of_begin.strftime('%Y-%m-%d'), 'end': vacation.date_of_end.strftime('%Y-%m-%d'),
             'range_of_dates': [vacation.date_of_begin + timedelta(days=x) for x in
                                range((vacation.date_of_end - vacation.date_of_begin).days + 1)],
             'employee': f"{vacation.employee.first_name} {vacation.employee.last_name}",
             'status': vacation.status
             } for vacation in now_vacations]

        upcoming_vacations_data = [
            {'start': vacation.date_of_begin.strftime('%Y-%m-%d'), 'end': vacation.date_of_end.strftime('%Y-%m-%d'),
             'range_of_dates': [vacation.date_of_begin + timedelta(days=x) for x in
                                range((vacation.date_of_end - vacation.date_of_begin).days + 1)],
             'employee': f"{vacation.employee.first_name} {vacation.employee.last_name}",
             'status': vacation.status
             } for vacation in upcoming_vacations]

        response_data = {
            'past_vacations_data': past_vacations_data,
            'now_vacations_data': now_vacations_data,
            'upcoming_vacations_data': upcoming_vacations_data,
        }

        return JsonResponse(response_data)


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
            vacation.dates_between = [vacation.date_of_begin + timedelta(days=x) for x in
                                      range((vacation.date_of_end - vacation.date_of_begin).days + 1)]
        context['past_vacations'] = past_vacations
        return context


class VacationHistoryViewAPI(ListView):
    def get(self, request, *args, **kwargs):
        employee_id = kwargs.get('employee_id')
        past_vacations = Vacations.objects.filter(employee_id=employee_id, date_of_end__lt=timezone.now())

        for vacation in past_vacations:
            vacation.dates_between = [vacation.date_of_begin + timedelta(days=x) for x in
                                      range((vacation.date_of_end - vacation.date_of_begin).days + 1)]

        serializer = VacationsSerializer(past_vacations, many=True)
        return JsonResponse(serializer.data, safe=False)


class VacationInfoView(TitleMixin, TemplateView):
    model = Employee
    template_name = 'vacations/vacationInfo.html'
    title = 'Info about vacation'
    success_url = reverse_lazy('users:profile')
    title = 'Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class AcceptVacationView(View):
    def post(self, request, vacation_id):
        vacation = get_object_or_404(Vacations, id=vacation_id)
        vacation.status = 'accepted'
        vacation.save()
        return redirect('vacation_info', pk=vacation.employee.id)


class DenyVacationView(View):
    def post(self, request, vacation_id):
        vacation = get_object_or_404(Vacations, id=vacation_id)
        vacation.status = 'denied'
        vacation.save()
        return redirect('vacation_info', pk=vacation.employee.id)


class VacationRequestsView(TitleMixin, ListView):
    model = Vacations
    template_name = 'vacations/vacationRequests.html'
    title = 'Vacation requests'

    def get_queryset(self):
        queryset = super(VacationRequestsView, self).get_queryset()
        employee_id = self.kwargs.get('employee_id')
        return queryset.filter(employee_id=employee_id) if employee_id else queryset
