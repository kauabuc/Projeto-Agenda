from django.contrib import admin

from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone',
                    'categoria', 'data_criação', 'mostrar')
    list_display_links = ('nome', 'sobrenome')
    # list_filter = ('nome', 'sobrenome')
    search_fields = ('nome', 'sobrenome', 'telefone')
    list_per_page = 10
    list_editable = ('telefone', 'mostrar')


admin.site.register(Contato, ContatoAdmin)
admin.site.register(Categoria)
