from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AsistenteViewSet,
    ConferenciaViewSet,
    EventoViewSet,
    InscripcionViewSet,
    OrganizadorViewSet,
    PagoViewSet,
    PatrocinadorViewSet,
    SedeViewSet,
)


router = DefaultRouter()
router.register(r'sedes', SedeViewSet)
router.register(r'organizadores', OrganizadorViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'asistentes', AsistenteViewSet)
router.register(r'inscripciones', InscripcionViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'conferencias', ConferenciaViewSet)
router.register(r'patrocinadores', PatrocinadorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
