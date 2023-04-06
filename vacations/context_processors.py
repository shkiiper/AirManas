from vacations.models import Vacations


def vacation_requests(request):
    return {'vacation_requests': Vacations.objects.all(),
            'not_accepted_requests': Vacations.objects.filter(accepted=False)
           }
