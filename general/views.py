from django.views.generic.base import TemplateView
from common.views import TitleMixin
from django.views.generic.list import ListView
from users.models import Employee
from vacations.models import Vacations
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Q


# Create your views here.
class IndexView(ListView):
    model = Employee
    template_name = 'general/homePage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        announcements = Vacations.objects.filter(
            Q(send_to_all=True),
            Q(date_of_begin__gte=now.date()) | Q(date_of_end__gte=now.date()),
            employee__isnull=False
        ).select_related('employee').order_by('-id')

        # Add the first and last name of the employee who requested the announcement to the context
        context['announcements'] = [
            {
                'employee': f"{announcement.employee.first_name} {announcement.employee.last_name}",
                'comments': announcement.comments,
                'request_date': announcement.requests_date,
                'start_date': announcement.date_of_begin,
                'end_date': announcement.date_of_end,
            }
            for announcement in announcements
        ]

        context['today'] = date.today()

        # Get all employees who have a birthday this month
        context['birthdays'] = Employee.objects.filter(birthday__month=context['today'].month)

        return context


class HowToUseView(TitleMixin, TemplateView):
    template_name = 'general/howToUse.html'
    title = 'Instructions'


class DocumentsView(TitleMixin, TemplateView):
    template_name = 'general/documents.html'
    title = 'Documents'




# class IndexView(TitleMixin, ListView):
#     model = Employee
#     template_name = 'general/homePage.html'
#     title = 'Home'
#     today = date.today()
#     month = today.month
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(IndexView, self).get_context_data()
#         context['birthdays'] = Employee.objects.filter(birthday__month=self.month)
#         context['announcements'] = Vacations.objects.filter(send_to_all=True).annotate(
#             first_name=F('employee__first_name'),
#             last_name=F('employee__last_name')
#         )
#         return context