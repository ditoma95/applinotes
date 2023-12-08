from django import forms
from django.forms import ModelForm
from notes.models import Note, Eleve

class Formulaire(ModelForm):
    class Meta:
        #Pour utiliser le model de Note
        model = Note
        #création du champs valeurs
        fields = ['valeur']
        #Il s'agit du label et du placeholder
        labels = {"valeur" : "Note sur 20 "}

class EleveForm(ModelForm):
    class Meta:
        model = Eleve
        fields = '__all__'
        #exclure un champs pour qu'il ne soit pas affiché
        exclude = ["id"]

#fonction pour controller les entrées des users
    def clean_nom(self):
        nom = self.cleaned_data['nom']

        if any(char.isdigit() for char in nom):
            raise forms.ValidationError("Le chiffre n'est pas permis")
        return nom
    
    def clean_prenom(self):
        prenom = self.cleaned_data['prenom']

        if any(char.isdigit() for char in prenom):
            raise forms.ValidationError("Le chiffre n'est pas permis")
        return prenom


    
    
        