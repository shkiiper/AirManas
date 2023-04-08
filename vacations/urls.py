from django.urls import path
from vacations.views import TakeVacationView, VacationHistoryViewAPI, VacationInfoView, VacationCalendarView, \
    VacationHistoryView, VacationRequestsView, VacationCalendarAPIView
from django.contrib.auth.decorators import login_required

app_name = 'vacations'

urlpatterns = [
    path('take_vacation/', login_required(TakeVacationView.as_view()), name='take_vacation'),
    path('calendar', VacationCalendarView.as_view(), name='calendar'),
    path('history', VacationHistoryView.as_view(), name='history'),
    path('history/<int:user_id>/', VacationHistoryView.as_view(), name='history'),
    path('info', VacationInfoView.as_view(), name='vacation_info'),
    path('requests_', VacationRequestsView.as_view(), name='vacation_requests'),
    path('api_history/<int:employee_id>/', VacationHistoryView.as_view(), name='api_history'),
    path('api_history/<int:employee_id>/api/', VacationHistoryViewAPI.as_view(), name='api_history'),
    path('api_calendar/', VacationCalendarAPIView.as_view(), name='api_calendar'),
    path('api_calendar/<int:employee_id>/', VacationCalendarAPIView.as_view(), name='api_calendar'),
]