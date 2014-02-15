#-*- coding: utf-8 -*-
from navigation.models import *
from django import forms
from django.forms.models import modelform_factory

# définition de tous les formulaires associés au modèle (un par classe)

PersonneForm = modelform_factory( Personne,  
  widgets={
    'nom': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nom', 'onblur' :'recupPersonneInfo()'}),
    'prenom': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Prénom', 'onblur' :'recupPersonneInfo()'}),
    'pseudonyme': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Pseudonyme'}),
    'uri_cesar': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Uri Cesar'}),
    'genre': forms.RadioSelect(attrs={'class' : 'radio inline'}),
    'nationalite': forms.Select(attrs={'class' : 'form-control'}),
    'titre': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre'}),
    'date_de_naissance': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dpersonne1' }),
    'date_de_deces': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dpersonne2'}),
    'plus_dinfo': forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : '...'})
    },
  labels={
    'prenom': 'Prénom',
    'date_de_deces': 'Décès',
    'date_de_naissance': 'Naissance',
  })
    
PieceForm = modelform_factory( Piece,  
  widgets={
    'titre': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre', 'onblur' :'recupPieceInfo()'}),
    'titre_brenner': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Titre Brenner'}),
    'uri_theaville': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Uri Theaville'}),
    'date_premiere': forms.TextInput(attrs={'class' : 'form-control', 'value':'1700-01-01', 'id' : 'dpiece1' }),
    'langue': forms.Select(attrs={'class' : 'form-control'}),
    'auteurs': forms.Select(attrs={'class' : 'form-control'}),
    'commentaire': forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : '...'})
    },
  labels={
    'date_premiere': 'Première',
    'titre_brenner': 'Titre Brenner',
    'uri_theaville': 'Uri Theaville'
  })   
    
SoireeForm = modelform_factory( Soiree,
  fields=('date', 'libelle_date_reg'),
	widgets={
		'date': forms.TextInput(attrs={'class' : 'form-control', 'value' : '1700-01-01', 'id' : 'dsoiree1' }),
		'libelle_date_reg': forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Date de la soiree(version originale)'}),
	},
  labels={
    'libelle_date_reg': 'Date Registre'
  }
)
  
BudgetSoireeForm = modelform_factory( BudgetSoiree,
  fields=('credit_final_reg', 'debit_initial_reg','montant_cachet','montant_cachet_auteur','nb_total_billets_vendus_reg','nombre_cachets','quart_pauvre_reg','credit_total_reg','debit_total_reg','reste_reg','total_depenses_reg','total_recettes_reg'),
	widgets={
		'credit_final_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Crédit final'}),
		'debit_initial_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Débit initial'}),
		'montant_cachet': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Montant cachet'}),
		'montant_cachet_auteur': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Montant cachet de l\'auteur'}),
		'nb_total_billets_vendus_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Nombre total de billets vendus'}),
		'nombre_cachets': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Nombre de cachets'}),
		'quart_pauvre_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Quart du pauvre'}),
		'credit_total_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Crédit total'}),
		'debit_total_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Débit total'}),
		'reste_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Reste'}),
		'total_depenses_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Total dépenses'}),
		'total_recettes_reg': forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Total recettes'}),
	},
	labels={
    'credit_final_reg':'Crédit Final', 
    'debit_initial_reg':'Débit Initial',
    'montant_cachet':'Montant Cachet',
    'montant_cachet_auteur':'Montant Cachet Auteur',
    'nb_total_billets_vendus_reg':'Total Billets Vendus',
    'nombre_cachets':'Nombre Cachets',
    'quart_pauvre_reg':'Quart Pauvre',
    'credit_total_reg':'Credit Total',
    'debit_total_reg':'Debit Total',
    'reste_reg':'Reste'
	}
)  



PageRegistreForm = modelform_factory(PageRegistre)
TransactionSoireeForm = modelform_factory(TransactionSoiree)
TransactionAbonnementForm = modelform_factory(TransactionAbonnement)
AbonnementForm = modelform_factory(Abonnement)
RecapitulatifForm = modelform_factory(Recapitulatif)
DebitRecapitulatifForm = modelform_factory(DebitRecapitulatif)
CreditRecapitulatifForm = modelform_factory(CreditRecapitulatif)
DebitForm = modelform_factory(Debit)
CreditForm = modelform_factory(Credit)
BilletterieForm = modelform_factory(Billetterie)
RepresentationForm = modelform_factory(Representation)
AnimationForm = modelform_factory(Animation)
RoleForm = modelform_factory(Role)