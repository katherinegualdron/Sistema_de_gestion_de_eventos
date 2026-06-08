from django.conf import settings
from django.db import models


class AuditoriaMixin(models.Model):
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_creados',
    )
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_modificados',
    )

    class Meta:
        abstract = True


# Modelo tabla Sede
class Sede(AuditoriaMixin):
    id_sede = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    ciudad = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'sedes'


# Modelo tabla Organizador
class Organizador(AuditoriaMixin):
    id_organizador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    empresa = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = 'organizadores'


# Modelo tabla Evento
class Evento(AuditoriaMixin):
    id_evento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=300)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    capacidad_maxima = models.IntegerField()
    id_sede = models.ForeignKey(
        Sede,
        on_delete=models.RESTRICT,
        db_column='id_sede'
    )
    id_organizador = models.ForeignKey(
        Organizador,
        on_delete=models.RESTRICT,
        db_column='id_organizador'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'eventos'


# Modelo tabla Asistente
class Asistente(AuditoriaMixin):
    id_asistente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    documento_identidad = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = 'asistentes'


# Modelo tabla Inscripcion
class Inscripcion(AuditoriaMixin):
    id_inscripcion = models.AutoField(primary_key=True)
    id_evento = models.ForeignKey(
        Evento,
        on_delete=models.RESTRICT,
        db_column='id_evento'
    )
    id_asistente = models.ForeignKey(
        Asistente,
        on_delete=models.RESTRICT,
        db_column='id_asistente'
    )
    estado = models.CharField(max_length=20, default='Pendiente')

    def __str__(self):
        return f"Inscripcion {self.id_inscripcion}"

    class Meta:
        db_table = 'inscripciones'


# Modelo tabla Pago
class Pago(AuditoriaMixin):
    id_pago = models.AutoField(primary_key=True)
    id_inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.RESTRICT,
        db_column='id_inscripcion'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=20, default='Pendiente')
    referencia = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Pago {self.id_pago}"

    class Meta:
        db_table = 'pagos'


# Modelo tabla Conferencia
class Conferencia(AuditoriaMixin):
    id_conferencia = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField(null=True, blank=True)
    ponente = models.CharField(max_length=200, null=True, blank=True)
    sala = models.CharField(max_length=100, null=True, blank=True)
    fecha_hora_inicio = models.DateTimeField(null=True, blank=True)
    duracion_minutos = models.IntegerField(null=True, blank=True)
    id_evento = models.ForeignKey(
        Evento,
        on_delete=models.RESTRICT,
        db_column='id_evento'
    )

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'conferencias'


# Modelo tabla Patrocinador
class Patrocinador(AuditoriaMixin):
    id_patrocinador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    logo = models.CharField(max_length=255, null=True, blank=True)
    sitio_web = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.CharField(max_length=200, null=True, blank=True)
    email_contacto = models.CharField(max_length=150, null=True, blank=True)
    nivel = models.CharField(max_length=20, null=True, blank=True)
    monto_aporte = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    id_evento = models.ForeignKey(
        Evento,
        on_delete=models.RESTRICT,
        db_column='id_evento'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'patrocinadores'
