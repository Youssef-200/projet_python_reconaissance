from django.shortcuts import render,redirect

from django.http import HttpResponse

from authentification.views import login

from .classe_user import recuperation

# Create your views here.

def recherche(request):
      
      import sqlite3

      recherche=request.POST['search']

      conn = sqlite3.connect('db.sqlite3')

      cur=conn.cursor()

      search=recherche.split()

      req="SELECT * FROM patient,consultation where nom='{}' AND prenom='{}' AND id_patient=patient_consulte ".format(search[0],search[1])

      resultat=cur.execute(req)

      result = cur.fetchone()

      nom=result[0]
      
      return render(request, 'resultat_recherche.html', {'nom': result[1], 'prenom': result[2] , 'cin': result[3], 'naissance':result[4], 'tel': result[5] })


def recherche_detect(request):
    
    import sqlite3

    conn = sqlite3.connect('db.sqlite3')

    cur=conn.cursor()
                    
    requezte="insert into consultation(patient_consulte) values (?)"

    ress=cur.execute(requezte,(request.session['id'],))

    conn.commit()
    
    s=request.session['id']

    requete="select * from patient,consultation where id_patient ='{}' AND id_patient=patient_consulte".format(s)

    res=cur.execute(requete)

    result = cur.fetchone()

      #del request.session['id']

    return render(request, 'affichage.html', {'nom': result[1], 'prenom': result[2] , 'cin': result[3], 'naissance':result[4], 'tel': result[5],'date_consult':result[9], 'maladie': result[10],'taritement': result[11],'diagnostic': result[12] })
