# -*- coding: utf-8 -*-

from django.template import Context, loader
from django.http import HttpResponse
from flahoo.photos.models import *

def index(request):
    if (request.GET.has_key('s')) :
        return photos(request)
    else :
        t = loader.get_template('accueil.html')
        c = Context({})
        return HttpResponse(t.render(c))    

def photos(request, tag):

	# Interaction avec Yahoo!
	y = Yahoo()
	resultats = y.search(tag, 30)
	
	# Sélection d'un résultat au hasard
	import random
	r = random.randrange(0, len(resultats)-1)
	resultat = resultats[r]

	# Les mots
	mots = resultat.Summary
	mots_originaux = mots
	def enleverpoints(x): return x != u'...' # on enlève les occurences de "..." dans les mots
	mots = filter(enleverpoints, mots.split(' '))
	if (len(mots) < 6) :
		raise Exception('Pas assez de mots!')

	# Les tags
	tags = []
	for i in range(3):
		tag = mots[random.randrange(0, len(mots))]
		tags.append(tag)
		mots.remove(tag)

	# Interaction avec Flickr
	f = Flickr()
	output = []
	for tag in tags:
		photos = f.get_photos_by_tag(tag.encode('utf-8'), 10)
		newphotos = []
		for photo in photos:
			p = {
	 		'title' : photo('title'),
	 		'image'   : f.get_photo_image(photo),
	 		'url' : f.get_photo_url(photo)
	 		}
			newphotos.append(p)
		output.append({'photos':newphotos, 'tag': tag})

	# Highlight des tags dans les mots
	def highlight_tags(mot): 
		if (tags.count(mot)) :
			return '<strong>%s</strong>' % mot
		else :
			return mot
	mots_originaux = mots_originaux.split(' ')
	mots_originaux = map(highlight_tags, mots_originaux)
	mots_originaux = " ".join(mots_originaux)

	# Rendering de la template
	t = loader.get_template('photos.html')
	c = Context({
    	'tags': output,
    	'mots' : mots_originaux,
    	'source' : resultat.Url
	})
	
	return HttpResponse(t.render(c))