from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Personne(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=100, choices=(('M', 'Masculin'),('F', 'Feminin'))) 
    date_naissance = models.DateField()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True


class Niveau(models.Model):
    nom = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.nom
    


class Enseignant(Personne):
    def __str__(self):
        daten = str(self.date_naissance)
        return self.nom + " " + self.prenom +" "+ self.sexe + " " + daten


class Matiere(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    niveaus = models.ManyToManyField(Niveau)

    class Meta:
        verbose_name_plural = 'Matière'
        ordering = ['-nom']
    def __str__(self):
        return self.nom 

  
        


class Eleve(Personne):
    id=models.CharField(max_length=50, primary_key=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    #matieres = models.ManyToManyField(Matiere)

    def save(self, *args, **kwargs):
        self.id = self.nom[0:2] + self.prenom[0:2] + self.sexe + str(datetime.datetime.today())                                           
        super(Eleve, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Élève'
        ordering = ['-nom']
        
    def __str__(self):
        return self.nom + " : " + self.prenom


class Note(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    #valeur = models.FloatField(max_length=30, null=True)
    
    valeur = models.FloatField(
        validators=[
            MinValueValidator(0, message="La note doit être superieur ou égale a 0 "),
            MaxValueValidator(20, message="La note doit être inferieur ou égale à 20")
        ]
    )
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.valeur)
    
