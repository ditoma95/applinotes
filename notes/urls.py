from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "notes"
urlpatterns = [
    path('', views.index, name='index'),

    path("eleves/", views.eleves, name='eleves'),
    path("eleve/<str:id>/", views.eleve,  name='eleve'),

    path("matiers/", views.matieres, name='matieres'),
    path("matiere/<int:id>/", views.matiere, name='matiere'),

    path("niveau/<int:id>/", views.niveau, name='niveau'),

    path("add_notes/<str:eleve_id>/<int:matiere_id>", views.add_notes, name='add_notes'),

    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html")),

    path("pdf/", views.listEleves, name="pdf"),

    path("pdf_niveau/<int:id>/", views.liste_niveauElv, name="pdf_niveau"),
    path("notesEleves/<int:id>/", views.notesEleves, name="notesEleves"),
    path("notesSynthese/<str:id>/", views.notesSynthese, name="notesSynthese"),

    

]
