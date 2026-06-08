import logging


operation_logger = logging.getLogger('api.operations')


class OperationLoggingMixin:
    action_names = {
        'list': 'LISTAR',
        'retrieve': 'CONSULTAR',
        'create': 'CREAR',
        'update': 'ACTUALIZAR',
        'partial_update': 'ACTUALIZAR_PARCIAL',
        'destroy': 'ELIMINAR',
    }

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        self.log_operation(request, response)
        return response

    def log_operation(self, request, response):
        user = getattr(request, 'user', None)
        username = user.username if user and user.is_authenticated else 'anonimo'
        action = self.action_names.get(
            getattr(self, 'action', None),
            request.method,
        )
        resource = self.get_queryset().model.__name__
        status_code = getattr(response, 'status_code', 'sin_estado')

        operation_logger.info(
            'usuario=%s accion=%s recurso=%s metodo=%s ruta=%s estado=%s',
            username,
            action,
            resource,
            request.method,
            request.get_full_path(),
            status_code,
        )
