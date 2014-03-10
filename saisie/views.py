 #-*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from navigation.models import Personne,Piece,Soiree,BudgetSoiree
from saisie.forms import *

	
@login_required(login_url='/login/')
def saisie(request, active_tab='Soiree', alert='off', alert_type='success', alert_message="unknown", previous_values = {}):

    personneForm = render_to_string(
        'form.html' , 
        {'action' : '/saisie/new/personne/', 'formset_list' : [PersonneForm()],'date_picker_id_list' : ['dpersonne1','dpersonne2'], 
        'previous_values' : previous_values, 'specific_function' : getPersonneJs(), 
				'alertZoneId':'azpersonne'},
        context_instance=RequestContext(request)) + render_to_string(
        'modal.html' , 
        {'modalId' : 'personneModal', 'modalTitle' : 'Recherche sur Cesar'},
        context_instance=RequestContext(request))
    
    pieceForm = render_to_string(
        'form.html' , 
        {'action' : '/saisie/new/piece/', 'formset_list' : [PieceForm()], 'date_picker_id_list' : ['dpiece1'],
        'previous_values' : previous_values, 'specific_function' : getPieceJs(),
				'alertZoneId':'azpiece'},
        context_instance=RequestContext(request)) + render_to_string(
        'modal.html' , 
        {'modalId' : 'pieceModal', 'modalTitle' : 'Recherche sur Theaville'},
        context_instance=RequestContext(request))
        
    soireeForm = render_to_string(
        'form.html' , 
        {'action' : '/saisie/new/soiree/', 'formset_list' : [SoireeForm(), BudgetSoireeForm()], 'formitems' : {'debit':DebitForm(),'credit':CreditForm(),'billetterie':BilletterieForm()}, 
        'previous_values' : previous_values, 'date_picker_id_list' : ['dsoiree1']},
        context_instance=RequestContext(request))
        
    return render_to_response('tab_page.html', 
        {"title":"Saisie", "active":"saisie", "tab_list" : 
        {"Personne" : personneForm, "Soiree":soireeForm, "Piece":pieceForm}, "active_tab":active_tab,  
        'alert' : alert, 'alert_type' : alert_type, 'alert_message' : alert_message}, 
        context_instance=RequestContext(request))

@login_required(login_url='/login/')
def creerPersonne(request):
    if request.POST:
        nom = request.POST.get('nom', 'none')
        prenom = request.POST.get('prenom', 'none')
        pseudonyme = request.POST.get('pseudonyme', 'none')
        uri_cesar = request.POST.get('uri_cesar', 'none')
        genre = request.POST.get('genre', 'none')
        nationalite = request.POST.get('nationalite', 'none')
        titre = request.POST.get('titre_personne', 'none')
        date_de_naissance = request.POST.get('date_de_naissance', 'none')
        date_de_deces = request.POST.get('date_de_deces', 'none')
        plus_dinfo = request.POST.get('plus_dinfo', 'none')
        personne = Personne(nom=nom, prenom=prenom, pseudonyme=pseudonyme, uri_cesar=uri_cesar, genre=genre, 
            nationalite=nationalite, titre_personne=titre, date_de_naissance=date_de_naissance, 
            date_de_deces=date_de_deces, plus_dinfo=plus_dinfo)
        try:
          personne.save()
          message = u"<b>" + prenom + " " + nom + u"</b> a bien été ajouté dans la base"
          return saisie(request, active_tab='Personne',alert='on',alert_type='success',alert_message=message)
        except ValidationError as e:
          message = ' '.join(e.messages)
          return saisie(request, active_tab='Personne',alert='on',alert_type='danger',alert_message=message, 
            previous_values = {'nom':nom,
                      'prenom':prenom,
                      'pseudonyme':pseudonyme,
                      'uri_cesar':uri_cesar,
                      'genre':genre,
                      'nationalite':nationalite,
                      'titre_personne':titre,
                      'date_de_naissance':date_de_naissance,
                      'date_de_deces':date_de_deces,
                      'plus_dinfo' : plus_dinfo})
        except IntegrityError as e:
          message = 'Cette Personne existe déja dans la base'
          return saisie(request, active_tab='Personne',alert='on',alert_type='danger',alert_message=message, 
            previous_values = {'nom':nom,
                      'prenom':prenom,
                      'pseudonyme':pseudonyme,
                      'uri_cesar':uri_cesar,
                      'genre':genre,
                      'nationalite':nationalite,
                      'titre_personne':titre,
                      'date_de_naissance':date_de_naissance,
                      'date_de_deces':date_de_deces,
                      'plus_dinfo' : plus_dinfo}) 
                      
@login_required(login_url='/login/')
def creerPiece(request):
    if request.POST:
        titre = request.POST.get('titre', 'none')
        titre_brenner = request.POST.get('titre_brenner', 'none')
        uri_theaville = request.POST.get('uri_theaville', 'none')
        date_premiere = request.POST.get('date_premiere', 'none')
        langue = request.POST.get('langue', 'none')
        auteurs = request.POST.get('auteurs', 'none')
        commentaire = request.POST.get('commentaire', 'none')
        
        piece = Piece(titre=titre, titre_brenner=titre_brenner, uri_theaville=uri_theaville, date_premiere=date_premiere, langue=langue, commentaire=commentaire)
        
        try:
          piece.save()
          piece.auteurs.add(auteurs)
          message = u"<b>" + titre + u"</b> a bien été ajouté dans la base"
          return saisie(request, active_tab='Piece',alert='on',alert_type='success',alert_message=message)
        except ValidationError as e:
          message = ' '.join(e.messages)
          return saisie(request, active_tab='Piece',alert='on',alert_type='danger',alert_message=message, 
            previous_values = {'titre':titre,
                      'titre_brenner':titre_brenner,
                      'date_premiere':date_premiere,
                      'uri_theaville':uri_theaville,
                      'langue':langue,
                      'auteurs':auteurs,
                      'commentaire':commentaire})
        except IntegrityError as e:
          message = 'Cette Piece existe déja dans la base'
          return saisie(request, active_tab='Piece',alert='on',alert_type='danger',alert_message=message, 
            previous_values = {'titre':titre,
                      'titre_brenner':titre_brenner,
                      'date_premiere':date_premiere,
                      'uri_theaville':uri_theaville,
                      'langue':langue,
                      'auteurs':auteurs,
                      'commentaire':commentaire})
        

@login_required(login_url='/login/')
def creerSoiree(request):
	if request.POST:
		try:
			ref_registre = request.POST.get('ref_registre', 'none')
			num_page_pdf = request.POST.get('num_page_pdf', 'none')
			redacteur = request.POST.get('redacteur', 'none')
			page_registre = PageRegistre(ref_registre=ref_registre, num_page_pdf=num_page_pdf)
			page_registre.save()

			total_depenses_reg = request.POST.get('total_depenses_reg', 'none')
			nb_total_billets_vendus_reg = request.POST.get('nb_total_billets_vendus_reg', 'none')
			total_recettes_reg = request.POST.get('total_recettes_reg', 'none')
			debit_derniere_soiree_reg = request.POST.get('debit_derniere_soiree_reg', 'none')
			total_depenses_corrige_reg = request.POST.get('total_depenses_corrige_reg', 'none')
			quart_pauvre_reg = request.POST.get('quart_pauvre_reg', 'none')
			debit_initial_reg = request.POST.get('debit_initial_reg', 'none')
			reste_reg = request.POST.get('reste_reg', 'none')
			debit_total_reg = request.POST.get('debit_total_reg', 'none')
			credit_total_reg = request.POST.get('credit_total_reg', 'none')
			nombre_cachets = request.POST.get('nombre_cachets', 'none')
			montant_cachet = request.POST.get('montant_cachet', 'none')
			montant_cachet_auteur = request.POST.get('montant_cachet_auteur', 'none')
			credit_final_reg = request.POST.get('credit_final_reg', 'none')
			budgetSoiree = BudgetSoiree(total_depenses_reg=total_depenses_reg, nb_total_billets_vendus_reg=nb_total_billets_vendus_reg, total_recettes_reg=total_recettes_reg, debit_derniere_soiree_reg=debit_derniere_soiree_reg, total_depenses_corrige_reg=total_depenses_corrige_reg, quart_pauvre_reg=quart_pauvre_reg, debit_initial_reg=debit_initial_reg, reste_reg=reste_reg, debit_total_reg=debit_total_reg, credit_total_reg=credit_total_reg, nombre_cachets=nombre_cachets, montant_cachet=montant_cachet, montant_cachet_auteur=montant_cachet_auteur, credit_final_reg=credit_final_reg)
			budgetSoiree.save()

			nb_debit = 0
			montant = request.POST.get('debit'+str(nb_debit)+'montant', 'none')
			while montant != 'none' :
				libelle = request.POST.get('debit'+str(nb_debit)+'libelle', 'none')
				type_depense = request.POST.get('debit'+str(nb_debit)+'type_depense', 'none')
				traduction = request.POST.get('debit'+str(nb_debit)+'traduction', 'none')
				mots_clefs = request.POST.get('debit'+str(nb_debit)+'mots_clefs', 'none')
				nb_debit += 1
				debit = Debit(montant=montant, libelle=libelle, type_depense=type_depense, traduction=traduction, mots_clefs=mots_clefs, budget=budgetSoiree)
				debit.save()
				montant = request.POST.get('credit'+str(nb_credit)+'montant', 'none')

			nb_credit = 0
			montant = request.POST.get('credit'+str(nb_credit)+'montant', 'none')
			while montant != 'none' :
				libelle = request.POST.get('credit'+str(nb_credit)+'libelle', 'none')
				nb_credit += 1
				credit = Credit(montant=montant, libelle=libelle, budget=budgetSoiree)
				credit.save()
				montant = request.POST.get('credit'+str(nb_credit)+'montant', 'none')

			nb_billetterie = 0
			montant = request.POST.get('billetterie'+str(nb_credit)+'montant', 'none')
			while montant != 'none' :
				libelle = request.POST.get('billetterie'+str(nb_credit)+'libelle_debit', 'none')
				nombre_billets_vendu = request.POST.get('billetterie'+str(nb_credit)+'nombre_billets_vendu', 'none')
				type_billet = request.POST.get('billetterie'+str(nb_credit)+'type_billet', 'none')
				commentaire = request.POST.get('billetterie'+str(nb_credit)+'commentaire', 'none')
				nb_billetterie += 1
				billetterie = Billetterie(montant=montant, libelle=libelle, budget=budgetSoiree, nombre_billets_vendu=nombre_billets_vendu, type_billet=type_billet, commentaire=commentaire)
				billetterie.save()
				montant = request.POST.get('billetterie'+str(nb_credit)+'montant', 'none')

			date = request.POST.get('date', 'none')
			libelle_date_reg = request.POST.get('libelle_date_reg', 'none')
			ligne_src = request.POST.get('ligne_src', 'none') 
			soiree = Soiree(date=sate, libelle_date_reg=libelle_date_reg, budget=budgetSoiree, ligne_src=ligne_src)
			soiree.save()

			message = u"La soirée du<b>" + date + u"</b> a bien été ajouté dans la base"
			return saisie(request, active_tab='Soiree',alert='on',alert_type='success',alert_message=message)
		except ValidationError as e:
			message = ' '.join(e.messages)
			return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message)
		except IntegrityError as e:
			message = 'Cette Soirée existe déja dans la base'
			return saisie(request, active_tab='Soiree',alert='on',alert_type='danger',alert_message=message)
  
def getPersonneJs():
  return '''
function recupPersonneInfo() { 
  var nom = document.getElementsByName("nom")[0].value;
  var prenom = document.getElementsByName("prenom")[0].value;
	 $.get( "/saisie/info/personne/"+nom+"/"+prenom, function( data ) 
        {
					if(data.indexOf("Aucune Personne ne correspond") == -1) {
          	addTopersonneModal("La personne que vous etes en train d\'enter correspond-t-elle à l\'une de ces personnes ? Si oui, cliquer sur le lien correpondant : <br/><br/>" + data);
						document.getElementById("azpersonne").innerHTML="<div class='alert alert-info'>Nous avons trouvé des personnes similaires sur Cesar.org.uk <button class='btn btn-info' onclick='lauchPersonneModal();'>Voir</button></div>";
					}
        });    
}

function lauchPersonneModal() {
	tooglepersonneModal();
	document.getElementById('azpersonne').innerHTML='';
}

function parsePersonneInfo(id) {
  $.get( "/saisie/info/personne/"+id, function( data ) 
  {
      var values = data.split(';');                   
      setValue('titre_personne',values[1]);                                      
      setValue('prenom',values[2]);                                                        
      setValue('nom',values[4]);                                     
      //setValue('date_de_naissance',values[5]);                                     
      //setValue('date_de_deces',values[6]);                                               
      setValue('pseudonyme',values[7]);
      if(values[8] == 'male') setValue('genre','M');
      else if(values[8] == 'female') setValue('genre','F'); 
      if(values[9] == 'French') setValue('nationalite', 'fr');
      else if(values[9] == 'Italian') setValue('nationalite', 'it');
      else if(values[9] == 'Deutsch') setValue('nationalite', 'de');
      else if(values[9] == 'English') setValue('nationalite', 'en');
      else setValue('nationalite', '-');
      if (values[10] != 'undefined') setValue('plus_dinfo', values[10]);
      setValue('uri_cesar','http://cesar.org.uk/cesar2/people/people.php?fct=edit&person_UOID='+id);
  });
  tooglepersonneModal();
}'''

def getPieceJs():
  return '''
function recupPieceInfo() { 
  var titre = document.getElementsByName("titre")[0].value;
  //var prenom = document.getElementsByName("auteur")[0].value; 
  if (titre != "") { 
    $.get( "../saisie/info/piece/"+titre, function( data ) 
        {
					if(data.indexOf("Aucune Piece ne correspond") == -1) {
          	addTopieceModal("La piece que vous etes en train d\'enter correspond-t-elle à l\'une de ces pieces ? Si oui, cliquer sur le lien correpondant : <br/><br/>" + data);
						document.getElementById("azpiece").innerHTML="<div class='alert alert-info'>Nous avons trouvé des pieces similaires sur Theaville.org <button class='btn btn-info' onclick='lauchPieceModal();''>Voir</button></div>";
					}
        });
     }
}         

function lauchPieceModal() {
	tooglepieceModal();
	document.getElementById('azpiece').innerHTML='';
}

function parsePieceInfo(id) {
  $.get( "../saisie/info/piece/"+id, function( data ) 
  {
			var values = data.split(';');                   
      setValue('titre',values[1]);                                      
      setValue('titre_brenner',values[2]);                                                        
      setValue('nom',values[4]);                                     
      //setValue('date_de_naissance',values[5]);                                     
      //setValue('date_de_deces',values[6]);                                               
      setValue('pseudonyme',values[7]);
      if(values[8] == 'male') setValue('genre','M');
      else if(values[8] == 'female') setValue('genre','F'); 
      if(values[9] == 'French') setValue('nationalite', 'fr');
      else if(values[9] == 'Italian') setValue('nationalite', 'it');
      else if(values[9] == 'Deutsch') setValue('nationalite', 'de');
      else if(values[9] == 'English') setValue('nationalite', 'en');
      else setValue('nationalite', '-');
      if (values[10] /= 'undefined') setValue('plus_dinfo', values[10]);
      setValue('uri_theaville','http://cesar.org.uk/cesar2/people/people.php?fct=edit&person_UOID='+id);
  });
  tooglepersonneModal();
}'''