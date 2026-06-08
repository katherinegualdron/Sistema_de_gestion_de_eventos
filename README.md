# Sistema de Gestion de Eventos

## Informacion general

- **Nombre del proyecto:** Sistema de Gestion de Eventos
- **Autor:** Wendy Katherine Gualdron Marquez
- **Repositorio:** https://github.com/katherinegualdron/Sistema_de_gestion_de_eventos.git
- **Version:** 1.0.0

## Descripcion

Este proyecto es una API REST para la gestion integral de eventos. Permite administrar asistentes, eventos, sedes, organizadores, inscripciones, pagos, conferencias y patrocinadores.

La solucion esta desarrollada con Django y Django REST Framework, usando PostgreSQL como motor de base de datos. Incluye autenticacion JWT, control de permisos, filtros avanzados, paginacion, exportacion CSV, soft delete y documentacion Swagger.

## Tecnologias utilizadas

- Python 3.14
- Django 6.0.6
- Django REST Framework
- PostgreSQL
- drf-yasg (Swagger)
- djangorestframework-simplejwt
- django-filter
- django-cors-headers
- openpyxl
- python-decouple

## Instalacion

### Requisitos previos

- Python 3.10 o superior
- PostgreSQL instalado y en ejecucion
- Git instalado

### 1. Clonar el repositorio

```bash
git clone https://github.com/katherinegualdron/Sistema_de_gestion_de_eventos.git
cd Sistema-Gestion-De-Eventos
git checkout feature_katherine_final
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
```

En Windows:

```bash
venv\Scripts\activate
```

En Linux o macOS:

```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Variables de entorno

Copia el archivo de ejemplo y configura tus datos:

```bash
cp .envEjemplo .env
```

Edita el archivo `.env` y define tus credenciales:

```text
API_PORT=9000
DEBUG=True
DB_NAME=nombre_de_la_base
DB_USER=usuario_de_la_base
DB_PASSWORD=contrasena_de_la_base
DB_HOST=127.0.0.1
DB_PORT=5432
DB_SCHEMA=nombre_del_schema
```

## Configuracion de base de datos

Asegurate de que el esquema de PostgreSQL exista antes de ejecutar las migraciones:

```sql
CREATE SCHEMA IF NOT EXISTS nombre_del_schema;
```

## Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## Crear superusuario

```bash
python manage.py createsuperuser
```

## Ejecucion

```bash
python manage.py runserver
```

- API disponible en: `http://127.0.0.1:8000`
- Documentacion Swagger: `http://127.0.0.1:8000/swagger/`
- Panel de administracion Django: `http://127.0.0.1:8000/admin/`

## Autenticacion

La API utiliza JSON Web Tokens (JWT).

### Obtener token de acceso

- Metodo: `POST`
- Ruta: `/api/token/`

Cuerpo de la peticion:

```json
{
  "username": "usuario",
  "password": "contrasena"
}
```

Respuesta de ejemplo:

```json
{
  "success": true,
  "message": "Token JWT generado correctamente.",
  "data": {
    "refresh": "token_refresh",
    "access": "token_access"
  },
  "errors": null
}
```

### Renovar token

- Metodo: `POST`
- Ruta: `/api/token/refresh/`

### Uso del token en cabecera

```http
Authorization: Bearer <token_access>
```

## Roles y permisos

- `GET` (consultar): Sin autenticacion requerida
- `POST`, `PUT`, `PATCH`: Rol Editor o Administrador
- `DELETE`: Rol Administrador

## Endpoints principales

Base URL: `http://127.0.0.1:8000/api/v1/`

### Autenticacion

- `POST /api/token/` - Obtener token JWT
- `POST /api/token/refresh/` - Renovar token JWT

### Sedes

- `GET /api/v1/sedes/` - Listar sedes activas
- `POST /api/v1/sedes/` - Crear sede
- `GET /api/v1/sedes/{id}/` - Consultar sede
- `PUT /api/v1/sedes/{id}/` - Actualizar sede
- `PATCH /api/v1/sedes/{id}/` - Actualizar parcialmente
- `DELETE /api/v1/sedes/{id}/` - Eliminacion logica
- `GET /api/v1/sedes/exportar-csv/` - Exportar registros a CSV

### Organizadores

- `GET /api/v1/organizadores/`
- `POST /api/v1/organizadores/`
- `GET /api/v1/organizadores/{id}/`
- `PUT /api/v1/organizadores/{id}/`
- `PATCH /api/v1/organizadores/{id}/`
- `DELETE /api/v1/organizadores/{id}/`
- `GET /api/v1/organizadores/exportar-csv/`

### Eventos

- `GET /api/v1/eventos/`
- `POST /api/v1/eventos/`
- `GET /api/v1/eventos/{id}/`
- `PUT /api/v1/eventos/{id}/`
- `PATCH /api/v1/eventos/{id}/`
- `DELETE /api/v1/eventos/{id}/`
- `GET /api/v1/eventos/exportar-csv/`

### Asistentes

- `GET /api/v1/asistentes/`
- `POST /api/v1/asistentes/`
- `GET /api/v1/asistentes/{id}/`
- `PUT /api/v1/asistentes/{id}/`
- `PATCH /api/v1/asistentes/{id}/`
- `DELETE /api/v1/asistentes/{id}/`
- `GET /api/v1/asistentes/exportar-csv/`

### Inscripciones

- `GET /api/v1/inscripciones/`
- `POST /api/v1/inscripciones/`
- `GET /api/v1/inscripciones/{id}/`
- `PUT /api/v1/inscripciones/{id}/`
- `PATCH /api/v1/inscripciones/{id}/`
- `DELETE /api/v1/inscripciones/{id}/`
- `GET /api/v1/inscripciones/exportar-csv/`

### Pagos

- `GET /api/v1/pagos/`
- `POST /api/v1/pagos/`
- `GET /api/v1/pagos/{id}/`
- `PUT /api/v1/pagos/{id}/`
- `PATCH /api/v1/pagos/{id}/`
- `DELETE /api/v1/pagos/{id}/`
- `GET /api/v1/pagos/exportar-csv/`

### Conferencias

- `GET /api/v1/conferencias/`
- `POST /api/v1/conferencias/`
- `GET /api/v1/conferencias/{id}/`
- `PUT /api/v1/conferencias/{id}/`
- `PATCH /api/v1/conferencias/{id}/`
- `DELETE /api/v1/conferencias/{id}/`
- `GET /api/v1/conferencias/exportar-csv/`

### Patrocinadores

- `GET /api/v1/patrocinadores/`
- `POST /api/v1/patrocinadores/`
- `GET /api/v1/patrocinadores/{id}/`
- `PUT /api/v1/patrocinadores/{id}/`
- `PATCH /api/v1/patrocinadores/{id}/`
- `DELETE /api/v1/patrocinadores/{id}/`
- `GET /api/v1/patrocinadores/exportar-csv/`

## Filtros, busqueda y ordenamiento

Todos los endpoints soportan los siguientes parametros de consulta:

- Filtrar por campo especifico:
  - `/api/v1/sedes/?ciudad=Bogota`
  - `/api/v1/asistentes/?nombre=Angel`
  - `/api/v1/pagos/?estado=Aprobado`
- Busqueda de texto en campos de texto:
  - `/api/v1/sedes/?search=bogota`
- Ordenamiento ascendente o descendente:
  - `/api/v1/eventos/?ordering=-fecha_creacion`
  - `/api/v1/sedes/?ordering=nombre`
- Incluir registros con soft delete:
  - `/api/v1/sedes/?incluir_inactivos=true`
- Paginacion:
  - `/api/v1/sedes/?page=1&page_size=10`

## Estructura del proyecto

```text
Sistema-Gestion-De-Eventos/
+-- api/
|   +-- admin.py
|   +-- apps.py
|   +-- auth_views.py
|   +-- filters.py
|   +-- logging_mixins.py
|   +-- migrations/
|   +-- models.py
|   +-- pagination.py
|   +-- responses.py
|   +-- serializers.py
|   +-- tests.py
|   +-- urls.py
|   +-- views.py
+-- backend/
|   +-- asgi.py
|   +-- settings.py
|   +-- urls.py
|   +-- wsgi.py
+-- logs/
|   +-- operations.log
+-- .env
+-- .envEjemplo
+-- .gitignore
+-- manage.py
+-- README.md
+-- requirements.txt
+-- run.py
```

## Caracteristicas implementadas

| # | Caracteristica | Estado |
|---|----------------|--------|
| 1 | Swagger para documentacion | Implementado |
| 2 | Versionado de API | Implementado |
| 3 | Respuestas JSON estandarizadas | Implementado |
| 4 | Paginacion | Implementado |
| 5 | Filtros por campo | Implementado |
| 6 | Ordenamiento | Implementado |
| 7 | Soft Delete | Implementado |
| 8 | Auditoria de registros | Implementado |
| 9 | Autenticacion JWT | Implementado |
| 10 | Roles y permisos | Implementado |
| 11 | Relaciones anidadas (Nested Serializers) | Implementado |
| 12 | Exportacion CSV | Implementado |
| 13 | Logging de operaciones | Implementado |

## Notas adicionales

- Manten el archivo `.env` fuera del control de versiones.
- Usa el panel de administracion Django para revisar usuarios, permisos y datos administrativos.
- La documentacion Swagger facilita la prueba de los endpoints y la inspeccion de esquemas de datos.
