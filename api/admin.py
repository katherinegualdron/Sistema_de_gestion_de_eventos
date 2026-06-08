from django.contrib import admin

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


class AuditoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_creacion', 'fecha_modificacion', 'creado_por', 'modificado_por')
    list_filter = ('activo', 'fecha_creacion', 'fecha_modificacion')
    ordering = ('-fecha_creacion',)

    def save_model(self, request, obj, form, change):
        if not change and not obj.creado_por:
            obj.creado_por = request.user
        obj.modificado_por = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.activo = False
        obj.modificado_por = request.user
        obj.save()

    def delete_queryset(self, request, queryset):
        queryset.update(activo=False, modificado_por=request.user)


@admin.register(Sede)
class SedeAdmin(AuditoriaAdmin):
    list_display = ('id_sede', 'nombre', 'ciudad', 'capacidad', 'activo', 'fecha_creacion')
    list_filter = AuditoriaAdmin.list_filter + ('ciudad',)
    search_fields = ('nombre', 'direccion', 'ciudad', 'email')


@admin.register(Organizador)
class OrganizadorAdmin(AuditoriaAdmin):
    list_display = ('id_organizador', 'nombre', 'apellido', 'email', 'empresa', 'activo')
    list_filter = AuditoriaAdmin.list_filter + ('empresa',)
    search_fields = ('nombre', 'apellido', 'email', 'empresa')


@admin.register(Evento)
class EventoAdmin(AuditoriaAdmin):
    list_display = ('id_evento', 'nombre', 'id_sede', 'id_organizador', 'fecha_inicio', 'activo')
    list_filter = AuditoriaAdmin.list_filter + ('id_sede', 'id_organizador', 'fecha_inicio')
    search_fields = ('nombre', 'descripcion', 'id_sede__nombre', 'id_organizador__nombre')


@admin.register(Asistente)
class AsistenteAdmin(AuditoriaAdmin):
    list_display = ('id_asistente', 'nombre', 'apellido', 'email', 'documento_identidad', 'activo')
    search_fields = ('nombre', 'apellido', 'email', 'documento_identidad')


@admin.register(Inscripcion)
class InscripcionAdmin(AuditoriaAdmin):
    list_display = ('id_inscripcion', 'id_evento', 'id_asistente', 'estado', 'activo', 'fecha_creacion')
    list_filter = AuditoriaAdmin.list_filter + ('estado', 'id_evento')
    search_fields = ('estado', 'id_evento__nombre', 'id_asistente__nombre', 'id_asistente__apellido')


@admin.register(Pago)
class PagoAdmin(AuditoriaAdmin):
    list_display = ('id_pago', 'id_inscripcion', 'monto', 'metodo_pago', 'estado', 'activo')
    list_filter = AuditoriaAdmin.list_filter + ('estado', 'metodo_pago')
    search_fields = ('estado', 'metodo_pago', 'referencia', 'id_inscripcion__id_asistente__nombre')


@admin.register(Conferencia)
class ConferenciaAdmin(AuditoriaAdmin):
    list_display = ('id_conferencia', 'titulo', 'ponente', 'sala', 'id_evento', 'activo')
    list_filter = AuditoriaAdmin.list_filter + ('sala', 'id_evento')
    search_fields = ('titulo', 'descripcion', 'ponente', 'sala', 'id_evento__nombre')


@admin.register(Patrocinador)
class PatrocinadorAdmin(AuditoriaAdmin):
    list_display = ('id_patrocinador', 'nombre', 'nivel', 'monto_aporte', 'id_evento', 'activo')
    list_filter = AuditoriaAdmin.list_filter + ('nivel', 'id_evento')
    search_fields = ('nombre', 'contacto', 'email_contacto', 'nivel', 'id_evento__nombre')
