import csv

from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.db import models
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action

from .filters import FieldFilterBackend
from .logging_mixins import OperationLoggingMixin
from .models import (
    Asistente,
    Conferencia,
    Evento,
    Inscripcion,
    Organizador,
    Pago,
    Patrocinador,
    Sede,
)
from .pagination import ApiPagination
from .responses import StandardResponseMixin
from .serializers import (
    AsistenteSerializer,
    ConferenciaSerializer,
    EventoSerializer,
    InscripcionSerializer,
    OrganizadorSerializer,
    PagoSerializer,
    PatrocinadorSerializer,
    SedeSerializer,
)


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return [
            field.name
            for field in view.get_queryset().model._meta.fields
            if isinstance(field, (models.CharField, models.TextField))
        ]


class IsEditorRole(permissions.BasePermission):
    message = 'Debe ser usuario staff o pertenecer al grupo Administrador o Editor.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        return request.user.groups.filter(name__in=['Administrador', 'Editor']).exists()


class IsAdminRole(permissions.BasePermission):
    message = 'Debe ser usuario staff o pertenecer al grupo Administrador.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        return request.user.groups.filter(name='Administrador').exists()


class BaseApiViewSet(OperationLoggingMixin, StandardResponseMixin, viewsets.ModelViewSet):
    filter_backends = [DynamicSearchFilter, filters.OrderingFilter, FieldFilterBackend]
    pagination_class = ApiPagination
    ordering_fields = '__all__'
    ordering = ['-fecha_creacion']
    export_filename = 'exportacion.csv'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('incluir_inactivos') == 'true':
            return queryset
        if hasattr(queryset.model, 'activo'):
            return queryset.filter(activo=True)
        return queryset

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        if getattr(self, 'action', None) == 'destroy':
            return [IsAdminRole()]
        return [IsEditorRole()]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(creado_por=user, modificado_por=user)

    def perform_update(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(modificado_por=user)

    def perform_destroy(self, instance):
        instance.activo = False
        if self.request.user.is_authenticated:
            instance.modificado_por = self.request.user
        instance.save()

    @action(detail=False, methods=['get'], url_path='exportar-csv')
    def exportar_csv(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        rows = serializer.data

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{self.export_filename}"'

        writer = csv.writer(response)
        if not rows:
            writer.writerow(['sin_registros'])
            return response

        headers = rows[0].keys()
        writer.writerow(headers)
        for row in rows:
            writer.writerow([row.get(header, '') for header in headers])
        return response


class SedeViewSet(BaseApiViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer
    export_filename = 'sedes.csv'


class OrganizadorViewSet(BaseApiViewSet):
    queryset = Organizador.objects.all()
    serializer_class = OrganizadorSerializer
    export_filename = 'organizadores.csv'


class EventoViewSet(BaseApiViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    export_filename = 'eventos.csv'


class AsistenteViewSet(BaseApiViewSet):
    queryset = Asistente.objects.all()
    serializer_class = AsistenteSerializer
    export_filename = 'asistentes.csv'


class InscripcionViewSet(BaseApiViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    export_filename = 'inscripciones.csv'


class PagoViewSet(BaseApiViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    export_filename = 'pagos.csv'


class ConferenciaViewSet(BaseApiViewSet):
    queryset = Conferencia.objects.all()
    serializer_class = ConferenciaSerializer
    export_filename = 'conferencias.csv'


class PatrocinadorViewSet(BaseApiViewSet):
    queryset = Patrocinador.objects.all()
    serializer_class = PatrocinadorSerializer
    export_filename = 'patrocinadores.csv'
    
    
