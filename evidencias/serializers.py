from rest_framework import serializers
from .models import EvidenciaProyecto

MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_TYPES = ['application/pdf', 'image/png', 'image/jpeg']
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']


class EvidenciaProyectoSerializer(serializers.ModelSerializer):
    archivo = serializers.FileField(write_only=True, required=False)
    autor_email = serializers.CharField(source='autor.email', read_only=True)

    class Meta:
        model = EvidenciaProyecto
        fields = [
            'id', 'titulo', 'proyecto', 'autor', 'autor_email',
            'categoria', 'descripcion', 'archivo', 'archivo_url',
            'archivo_nombre_original', 'archivo_tipo', 'archivo_tamano',
            'fecha_creacion', 'fecha_actualizacion',
        ]
        read_only_fields = [
            'id', 'autor', 'autor_email', 'archivo_url',
            'archivo_nombre_original', 'archivo_tipo', 'archivo_tamano',
            'fecha_creacion', 'fecha_actualizacion',
        ]

    def validate_titulo(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío.")
        return value.strip()

    def validate_proyecto(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del proyecto no puede estar vacío.")
        return value.strip()

    def validate_categoria(self, value):
        categorias_validas = ['documento', 'imagen', 'captura', 'informe', 'presentacion', 'otro']
        if value not in categorias_validas:
            raise serializers.ValidationError(
                f"Categoría inválida. Valores permitidos: {', '.join(categorias_validas)}"
            )
        return value

    def validate_descripcion(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("La descripción no puede superar los 500 caracteres.")
        return value

    def validate_archivo(self, file):
        if file is None:
            return file
        if file.size > MAX_FILE_SIZE:
            raise serializers.ValidationError(
                f"El archivo no puede superar 5 MB. Tamaño recibido: {file.size / (1024*1024):.2f} MB."
            )
        content_type = getattr(file, 'content_type', '')
        if content_type not in ALLOWED_TYPES:
            extension = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
            if extension not in ALLOWED_EXTENSIONS:
                raise serializers.ValidationError("Solo se permiten archivos PDF, PNG o JPEG.")
        return file