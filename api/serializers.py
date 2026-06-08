from rest_framework import serializers

from .models import (
    Sede,
    Organizador,
    Evento,
    Asistente,
    Inscripcion,
    Pago,
    Conferencia,
    Patrocinador,
)


# Serializador para Sede
class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'creado_por', 'modificado_por')


# Serializador para Organizador
class OrganizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizador
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'creado_por', 'modificado_por')


# Serializador para Evento
class EventoSerializer(serializers.ModelSerializer):
    # Para escritura (POST/PUT)
    id_sede_id = serializers.PrimaryKeyRelatedField(
        queryset=Sede.objects.all(), source='id_sede', write_only=True
    )
    id_organizador_id = serializers.PrimaryKeyRelatedField(
        queryset=Organizador.objects.all(), source='id_organizador', write_only=True
    )
    # Para lectura (GET)
    id_sede = SedeSerializer(read_only=True)
    id_organizador = OrganizadorSerializer(read_only=True)

    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'creado_por', 'modificado_por')


# Serializador para Asistente
class AsistenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistente
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'creado_por', 'modificado_por')


# Serializador para Inscripcion
class InscripcionSerializer(serializers.ModelSerializer):
    # Para escritura (POST/PUT)
    id_evento_id = serializers.PrimaryKeyRelatedField(
        queryset=Evento.objects.all(), source='id_evento', write_only=True
    )
    id_asistente_id = serializers.PrimaryKeyRelatedField(
        queryset=Asistente.objects.all(), source='id_asistente', write_only=True
    )
    # Para lectura (GET)
    id_evento = EventoSerializer(read_only=True)
    id_asistente = AsistenteSerializer(read_only=True)

    class Meta:
        model = Inscripcion
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'creado_por', 'modificado_por')


# Serializador para Pago
class PagoSerializer(serializers.ModelSerializer):
    # Para escritura (POST/PUT)
    id_inscripcion_id = serializers.PrimaryKeyRelatedField(
        queryset=Inscripcion.objects.all(), source='id_inscripcion', write_only=True
    )
    # Para lectura (GET)
    id_inscripcion = InscripcionSerializer(read_only=True)

    class Meta:
        model = Pago
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'creado_por', 'modificado_por')


# Serializador para Conferencia
class ConferenciaSerializer(serializers.ModelSerializer):
    # Para escritura (POST/PUT)
    id_evento_id = serializers.PrimaryKeyRelatedField(
        queryset=Evento.objects.all(), source='id_evento', write_only=True
    )
    # Para lectura (GET)
    id_evento = EventoSerializer(read_only=True)

    class Meta:
        model = Conferencia
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'creado_por', 'modificado_por')


# Serializador para Patrocinador
class PatrocinadorSerializer(serializers.ModelSerializer):
    # Para escritura (POST/PUT)
    id_evento_id = serializers.PrimaryKeyRelatedField(
        queryset=Evento.objects.all(), source='id_evento', write_only=True
    )
    # Para lectura (GET)
    id_evento = EventoSerializer(read_only=True)

    class Meta:
        model = Patrocinador
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'creado_por', 'modificado_por')
