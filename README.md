# Evidencias API

API REST para gestión de evidencias de proyectos con autenticación Google OAuth + JWT y almacenamiento de archivos en Cloudinary.

## Stack
- Django + Django REST Framework
- SimpleJWT (autenticación)
- Cloudinary (archivos)
- drf-yasg (Swagger)
- SQLite (base de datos)

## Setup en Linux

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd proyecto

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales reales

# 5. Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# 6. Crear superusuario (opcional)
python manage.py createsuperuser

# 7. Correr el servidor
python manage.py runserver
```

## Endpoints

| Método | URL | Descripción | Auth |
|--------|-----|-------------|------|
| GET | `/health/` | Health check | No |
| POST | `/api/auth/google/` | Login con Google | No |
| POST | `/api/auth/token/refresh/` | Refrescar JWT | No |
| GET | `/api/evidencias/` | Listar evidencias | JWT |
| POST | `/api/evidencias/` | Crear evidencia | JWT |
| GET | `/api/evidencias/{id}/` | Ver evidencia | JWT |
| PUT | `/api/evidencias/{id}/` | Actualizar evidencia | JWT |
| DELETE | `/api/evidencias/{id}/` | Eliminar evidencia | JWT |
| GET | `/swagger/` | Documentación Swagger | No |

## Subir archivo (POST /api/evidencias/)

```
Content-Type: multipart/form-data
Authorization: Bearer <access_token>

titulo: "Mi evidencia"
proyecto: "Proyecto Final"
categoria: "codigo"
descripcion: "Descripción opcional"
archivo: <file.pdf | file.png | file.jpeg>
```

**Validaciones del archivo:**
- Tipos permitidos: PDF, PNG, JPEG
- Tamaño máximo: 5 MB

## Despliegue (Render / Railway)

1. Genera requirements: `pip freeze > requirements.txt`
2. Comando de inicio: `gunicorn config.wsgi:application`
3. Configura variables de entorno en el panel del servicio
