from rest_framework.filters import BaseFilterBackend


class FieldFilterBackend(BaseFilterBackend):
    ignored_params = {'page', 'page_size', 'search', 'ordering', 'incluir_inactivos', 'format'}

    def filter_queryset(self, request, queryset, view):
        fields = {field.name: field for field in queryset.model._meta.fields}

        for field, value in request.query_params.items():
            if field in self.ignored_params:
                continue
            if field in fields:
                queryset = queryset.filter(**self.build_filter(field, fields[field], value))

        return queryset

    def build_filter(self, field_name, field, value):
        internal_type = field.get_internal_type()

        if internal_type in {'CharField', 'TextField'}:
            return {f'{field_name}__icontains': value}
        if internal_type == 'BooleanField':
            return {field_name: value.lower() in {'true', '1', 'si', 'sí'}}
        return {field_name: value}

    def get_schema_operation_parameters(self, view):
        model = view.get_queryset().model
        parameters = [
            {
                'name': 'incluir_inactivos',
                'required': False,
                'in': 'query',
                'description': 'Use true para incluir registros desactivados por soft delete.',
                'schema': {'type': 'boolean'},
            },
        ]

        for field in model._meta.fields:
            parameters.append(
                {
                    'name': field.name,
                    'required': False,
                    'in': 'query',
                    'description': self.get_description(field),
                    'schema': {'type': self.get_schema_type(field)},
                }
            )

        return parameters

    def to_html(self, request, queryset, view):
        fields = [
            field
            for field in queryset.model._meta.fields
            if field.name not in {'creado_por', 'modificado_por'}
        ]

        controls = []
        for field in fields:
            value = request.query_params.get(field.name, '')
            controls.append(
                '<div class="form-group">'
                f'<label for="filter-{field.name}">{field.name}</label>'
                f'<input class="form-control" id="filter-{field.name}" '
                f'name="{field.name}" type="text" value="{value}" />'
                '</div>'
            )

        incluir_inactivos = 'checked' if request.query_params.get('incluir_inactivos') == 'true' else ''
        controls.append(
            '<div class="checkbox">'
            '<label>'
            f'<input name="incluir_inactivos" type="checkbox" value="true" {incluir_inactivos} /> '
            'incluir_inactivos'
            '</label>'
            '</div>'
        )

        return (
            '<h4>Filtros de busqueda</h4>'
            '<form class="form" method="get">'
            + ''.join(controls)
            + '<button type="submit" class="btn btn-primary">Filtrar</button> '
            + f'<a class="btn btn-default" href="{request.path}">Limpiar</a>'
            + '</form>'
        )

    def get_schema_type(self, field):
        internal_type = field.get_internal_type()

        if internal_type in {'IntegerField', 'AutoField', 'BigAutoField'}:
            return 'integer'
        if internal_type in {'DecimalField', 'FloatField'}:
            return 'number'
        if internal_type == 'BooleanField':
            return 'boolean'
        return 'string'

    def get_description(self, field):
        if field.get_internal_type() in {'CharField', 'TextField'}:
            return f'Filtrar por coincidencia parcial en el campo {field.name}.'
        return f'Filtrar por coincidencia exacta en el campo {field.name}.'
