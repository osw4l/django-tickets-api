import django_filters
from .constants import Status
from .models import Ticket


class TicketFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')
    status = django_filters.ChoiceFilter(field_name="status", choices=Status.choices)

    class Meta:
        model = Ticket
        fields = ('start_date', 'end_date', 'status', )