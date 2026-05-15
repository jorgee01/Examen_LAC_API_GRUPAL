from django.contrib import admin
from .models import EvidenciaProyecto

@admin.register(EvidenciaProyecto)
class EvidenciaProyectoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'autor', 'categoria', 'fecha_creacion']
    list_filter = ['categoria', 'archivo_tipo', 'fecha_creacion']
    search_fields = ['titulo', 'proyecto', 'autor__email']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
