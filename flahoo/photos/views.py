# -*- coding: utf-8 -*-

from django.template import Context, loader
from django.http import HttpResponse
from flahoo.photos.models import * 
import re
import random
import flahoo.settings

def index(request):
	t = loader.get_template('accueil.html')
	c = Context({})
	return HttpResponse(t.render(c))    

def photos(request, search_tag):

	# Interaction avec Yahoo!
	y = Yahoo()
	resultats = y.search(search_tag, 30)
	
	if len(resultats) == 0 :
		return photos_vide(request, search_tag)
	
	resultat = random.choice(resultats)
	
	# Les mots
	mots = resultat.Summary.encode('utf-8')
	mots_originaux = mots
	mots = y.filtrer_mots(mots)

	# Les tags
	f = Flickr()
	tags = f.get_tags_from_mots(mots)

	# Interaction avec Flickr
	output = []
	for tag in tags:
		output.append(f.get_photos_by_tag(tag))

	# Highlight des tags dans les mots
	mots_originaux = y.highliter_mots(mots_originaux, tags)

	# Rendering de la template
	t = loader.get_template('photos.html')
	c = Context({
    	'tags': output,
    	'mots' : mots_originaux,
    	'source' : resultat.Url,
    	'input_value' : search_tag
	})
	
	return HttpResponse(t.render(c))

def photos_vide(request, search_tag):
	t = loader.get_template('photos_vide.html')
	c = Context({
    	'input_value' : search_tag
	})
	return HttpResponse(t.render(c))
