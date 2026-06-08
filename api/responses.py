from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler


class StandardResponseMixin:
    success_messages = {
        'list': 'Registros consultados correctamente.',
        'retrieve': 'Registro consultado correctamente.',
        'create': 'Registro creado correctamente.',
        'update': 'Registro actualizado correctamente.',
        'partial_update': 'Registro actualizado correctamente.',
        'destroy': 'Registro eliminado correctamente.',
    }

    error_messages = {
        400: 'Los datos enviados no son validos.',
        401: 'No se enviaron credenciales de autenticacion validas.',
        403: 'No tiene permisos para realizar esta accion.',
        404: 'El recurso solicitado no existe.',
        405: 'Metodo no permitido para este recurso.',
        500: 'Ocurrio un error interno en el servidor.',
    }

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        if not isinstance(response, Response):
            return response

        if self._is_standard_response(response.data):
            return response

        if response.status_code == status.HTTP_204_NO_CONTENT:
            response.status_code = status.HTTP_200_OK

        response.data = self.build_standard_response(response)
        return response

    def build_standard_response(self, response):
        is_success = 200 <= response.status_code < 400

        if is_success:
            return {
                'success': True,
                'message': self.get_success_message(),
                'data': response.data,
                'errors': None,
            }

        return {
            'success': False,
            'message': self.get_error_message(response.status_code),
            'data': None,
            'errors': response.data,
        }

    def get_success_message(self):
        return self.success_messages.get(
            getattr(self, 'action', None),
            'Solicitud procesada correctamente.',
        )

    def get_error_message(self, status_code):
        return self.error_messages.get(
            status_code,
            'La solicitud no pudo ser procesada.',
        )

    def _is_standard_response(self, data):
        if not isinstance(data, dict):
            return False

        return {'success', 'message', 'data', 'errors'}.issubset(data.keys())


def standard_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    standard_keys = {'success', 'message', 'data', 'errors'}
    if isinstance(response.data, dict) and standard_keys.issubset(response.data.keys()):
        return response

    error_messages = {
        400: 'Los datos enviados no son validos.',
        401: 'No se enviaron credenciales de autenticacion validas.',
        403: 'No tiene permisos para realizar esta accion.',
        404: 'El recurso solicitado no existe.',
        405: 'Metodo no permitido para este recurso.',
        500: 'Ocurrio un error interno en el servidor.',
    }

    response.data = {
        'success': False,
        'message': error_messages.get(
            response.status_code,
            'La solicitud no pudo ser procesada.',
        ),
        'data': None,
        'errors': response.data,
    }
    return response
