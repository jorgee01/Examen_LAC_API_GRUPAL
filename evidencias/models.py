from django.db import models
from django.contrib.auth.models import User


class EvidenciaProyecto(models.Model):

    CATEGORIA_CHOICES = [
        ('codigo', 'Código'),
        ('diseno', 'Diseño'),
        ('documentacion', 'Documentación'),
        ('prueba', 'Prueba'),
        ('presentacion', 'Presentación'),
        ('otro', 'Otro'),
    ]

    TIPO_ARCHIVO_CHOICES = [
        ('pdf', 'PDF'),
        ('png', 'PNG'),
        ('jpeg', 'JPEG'),
    ]

    # Campos principales
    titulo = models.CharField(max_length=255)
    proyecto = models.CharField(max_length=255)
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='evidencias'
    )
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        default='otro'
    )
    descripcion = models.TextField(blank=True, default='')

    # Campos de archivo (Cloudinary)
    archivo_url = models.URLField(max_length=500, blank=True, default='')
    archivo_nombre_original = models.CharField(max_length=255, blank=True, default='')
    archivo_tipo = models.CharField(
        max_length=10,
        choices=TIPO_ARCHIVO_CHOICES,
        blank=True,
        default=''
    )
    archivo_tamano = models.PositiveIntegerField(
        help_text='Tamaño en bytes',
        default=0
    )

    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Evidencia de Proyecto'
        verbose_name_plural = 'Evidencias de Proyecto'

    def __str__(self):
        return f"{self.titulo} - {self.proyecto}"
