from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .responses import StandardResponseMixin


class StandardTokenObtainPairView(StandardResponseMixin, TokenObtainPairView):
    def get_success_message(self):
        return 'Token JWT generado correctamente.'


class StandardTokenRefreshView(StandardResponseMixin, TokenRefreshView):
    def get_success_message(self):
        return 'Token JWT actualizado correctamente.'
