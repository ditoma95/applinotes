from django.contrib import admin
from notes.models import  Eleve, Enseignant, Matiere, Niveau, Note
from notes.forms import EleveForm
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

#ce morceau de code nous permet d'exporter les donnée
#Ici c'est pour exporter les donnée de la classe Eleve
#En precisant quelle seront les les colonnes 
class EleveResource(resources.ModelResource):
    class Meta:
        model = Eleve
        fields = ('nom', 'prenom', 'sexe','date_naissance')
        export_order = ('i', 'nom',  'prenom', 'sexe', 'date_naissance')



class EleveAdmin(ImportExportModelAdmin):
    list_display = ('nom', 'prenom', 'sexe','date_naissance')
    search_fields = ['nom']
    show_full_result_count = False 

    form = EleveForm
    
    #resource est utilisé pour fixer EleveResource
    resources_class = [EleveResource]

#Pouur exporter on peut également au lieu de créer des resources, ajouter tout simplement l'extention des importations.
# C'est ce que je viens de faire au niveau de Enseignant admin
class AdminEnseignant(ImportExportModelAdmin):
    list_display = ('nom', 'prenom', 'sexe','date_naissance')

# class AdminNiveau(admin.ModelAdmin):
#     list_display = ('niveau')


# class AdminMatiere(admin.ModelAdmin):
#     list_display = ('nom')

# class AdminNote(admin.ModelAdmin):
#     list_display = ('valeur')

admin.site.register(Niveau)
admin.site.register(Eleve, EleveAdmin)
admin.site.register(Enseignant, AdminEnseignant)
admin.site.register(Matiere)
admin.site.register(Note)

