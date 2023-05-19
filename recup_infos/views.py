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

    return redirect('./liste_attente')


def liste_attente(request):
      
      """
      request.session['prenom']=[]
    
      request.session['nom']=[]

      request.session['cin']=[]

      request.session['tel']=[]

      request.session['adresse']=[]
      """
      
      import sqlite3

      conn = sqlite3.connect('db.sqlite3')

      cur=conn.cursor()

      request.session['idd']=request.session['idd']+1

      requete="select nom,prenom,tel,adresse from patient,consultation where diagnostic is NULL AND patient_consulte = {} AND id_patient=patient_consulte ".format(request.session['id'])

      res=cur.execute(requete)

      result = cur.fetchall()

      if result is not None:
        
        for j in result:
            
            request.session['nom'].append(j[0])

            request.session['prenom'].append(j[1])

            #request.session['cin'].append(j[3])

            request.session['tel'].append(j[2])

            request.session['adresse'].append(j[3])
           

            """
            del request.session['prenom']

            del request.session['nom']
            del request.session['cin']
            del request.session['tel']
            del request.session['adresse']

            
            del request.session['id']
            del request.session['i']
            """
            return render(request, 'python.html', {'nom': request.session['nom'], 'prenom': request.session['prenom'],'tel': request.session['tel'],'adresse': request.session['adresse'],})
    
      else:

        return render(request, 'python.html',{'nom': [], 'prenom': [], 'cin': [], 'tel': [],'adresse': [],})
    
    
