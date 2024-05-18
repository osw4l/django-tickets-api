from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TicketSerializer, TicketDetailSerializer, ImageUploadSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Ticket
from .filters import TicketFilter
from .pagination import TicketPagination


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    pagination_class = TicketPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketFilter
    lookup_field = 'uuid'
    serializer_class = TicketSerializer
    detail_serializer_class = TicketDetailSerializer
    queryset = Ticket.objects.all().prefetch_related('images').select_related('user')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    @action(
        detail=True, 
        methods=['POST'],
        parser_classes=[
            MultiPartParser,
            FormParser
        ],
        serializer_class=ImageUploadSerializer
    )
    def upload_image(self, request, uuid=None):
        ticket = self.get_object()
        if ticket.can_add_images():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            file = serializer.validated_data['image']
            ticket.add_image(file=file)
            return Response({
                'success': True
            })
        raise APIException("ticket doesn't allow more photos")