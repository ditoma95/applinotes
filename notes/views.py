import os
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.urls import reverse
from notes.forms import Formulaire
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required, permission_required

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

from notes.models import Eleve, Matiere, Niveau, Note
def index(request):
   return render(request, "notes/index.html")
# Create your views here.
@login_required
@permission_required("notes.view_eleve", raise_exception=True)
def eleves(request):
    lesEleves = Eleve.objects.all()
    item_name = request.GET.get('item-name')
    if (item_name != '' and  item_name is not None):
        lesEleves = Eleve.objects.filter(nom__icontains=item_name)
    return render(request, "eleves/index.html", {'lesEleves' : lesEleves})


@login_required
def eleve(request, id):
    try:
        unEleve = Eleve.objects.get(id=id)
        #matier = Matiere.objects.filter(eleve=unEleve)
        #nbre_matiere = matier.count()
        listmatires = unEleve.niveau.matiere_set.all()

        # toutmatierne = Matiere.objects.filter(n)

        tab_moyenne = []
        
        for maits in listmatires:
            recupnotes = maits.note_set.all()
            moyenne = recupnotes.aggregate(Avg('valeur', default=0))['valeur__avg']
            tab_moyenne.append(moyenne)

        moyenne_generale = sum(tab_moyenne)/len(tab_moyenne)
        

        return render(request, "eleves/show.html", {'unEleve': unEleve, 'listmatires' : zip(listmatires, tab_moyenne), 'moyenne_generale': moyenne_generale})
    except Eleve.DoesNotExist:
        raise Http404("Model eleve n'existe pas ")


    
@login_required
@permission_required("notes.view_matieres", raise_exception=True)
def matieres(request):
    lesmatiers = Matiere.objects.all()
    item_name = request.GET.get('item-name')
    if (item_name != '' and  item_name is not None):
        lesmatiers = Matiere.objects.filter(nom__icontains=item_name)
    return render(request, "matieres/index.html", {'lesmatiers' : lesmatiers})


@login_required
def matiere(request, id):
    try:
        uneMatiere = Matiere.objects.get(id=id)
        return render(request, "matieres/show.html", {'uneMatiere': uneMatiere})
    except Matiere.DoesNotExist:
        raise Http404("Model Matiere n'existe pas ")
    

    
@login_required
def niveau(request, id):
    try:
        unNiveau = Matiere.objects.get(id=id)
        return render(request, "matieres/show.html", {'unNiveau': unNiveau})
    except Niveau.DoesNotExist:
        raise Http404("Model Matiere n'existe pas ")

    
@login_required
def add_notes(request, eleve_id, matiere_id):

    recup_eleve = get_object_or_404(Eleve, id=eleve_id)
    recup_matiere = get_object_or_404(Matiere, id=matiere_id)

    # if request.method == "POST":
    #     newNote = request.POST["note"]

    #     instance_note = Note.objects.create(
    #         eleve=recup_eleve,
    #         matiere=recup_matiere,
    #         valeur = newNote
    #     )
    
    # #return redirect("notes:eleves")
    #return render(request, "ajouternotes/add_notes.html")

    if request.method == "POST":
        #Pour recuperer les valeurs entrées par l'utilisateur
        form = Formulaire(request.POST)
        #si ses champs sont valide alors
        if form.is_valid():
            try:
                #On fait une sauvegarde partielle 
                #puisqu'on n'a pas encore l'id matiere et l'id eleve pour créer un objet complet 
                #donc on utilise commit=false pour une sauvegarde partielle
                saveNote = form.save(commit=False)
                #Maintenant qu'on recuperer les valeurs entréer par l'utilisateurs
                #on stock sa dans saveNote. Sur cet objet partielles on ajoute automatiquement l'id eleve et l'id matiere
                saveNote.eleve = recup_eleve
                saveNote.matiere = recup_matiere
                #Maitenant que l'objet et complet alors on peut donc créer l'objet
                saveNote.save()
                # pour retourner sur eleves il utiliser reverse
                return redirect(reverse("notes:eleves"))
            except:
                pass
    else:
        #on recupere le formualaire vide 
        form = Formulaire()
        # On retourne a l'utilisateur de reénvoyer les valeurs
        return render(request, "ajouternotes/add_notes.html", {'form':form})



def listEleves(request):
    paths = '/home/dimitri/Documents/L3/ProjetDjango/ifntidjango/pdf/fichier.pdf'
    if os.path.exists(paths):
        with open(paths, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="fichier.pdf"'
            return response
    else:
        return HttpResponse("Le fichier PDF n'a pas été trouvé.", status=404)