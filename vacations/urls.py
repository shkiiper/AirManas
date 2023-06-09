from django.urls import path
from vacations.views import TakeVacationView, VacationHistoryViewAPI, VacationInfoView, VacationCalendarView, \
    VacationHistoryView, VacationRequestsView, VacationCalendarAPIView, AcceptVacationView, DenyVacationView
from django.contrib.auth.decorators import login_required

app_name = 'vacations'

urlpatterns = [
    path('take_vacation/', login_required(TakeVacationView.as_view()), name='take_vacation'),
    path('calendar', VacationCalendarView.as_view(), name='calendar'),
    path('calendar/<int:user_id>/', VacationCalendarView.as_view(), name='calendar'),
    path('history', VacationHistoryView.as_view(), name='history'),
    path('history/<int:user_id>/', VacationHistoryView.as_view(), name='history'),
    path('info', VacationInfoView.as_view(), name='vacation_info'),
    path('requests_', VacationRequestsView.as_view(), name='vacation_requests'),
    path('history/<int:employee_id>/api/', VacationHistoryViewAPI.as_view(), name='history_api'),
    path('calendar/api/', VacationCalendarAPIView.as_view(), name='calendar_api'),
    path('calendar/<int:employee_id>/api/', VacationCalendarAPIView.as_view(), name='calendar-api'),
    path('<int:vacation_id>/accept/', AcceptVacationView.as_view(), name='accept_vacation'),
    path('<int:vacation_id>/deny/', DenyVacationView.as_view(), name='deny_vacation'),
]