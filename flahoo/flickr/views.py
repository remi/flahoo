# -*- coding: utf-8 -*-

from django.template import Context, loader
from django.http import HttpResponse
from flahoo.flickr.models import Flickr
from yahoo.search.web import *

def index(request):
    if (request.GET.has_key('s')) :
        return photos(request)
    else :
        t = loader.get_template('accueil.html')
        c = Context({})
        return HttpResponse(t.render(c))    

def photos(request):

	# Récupération des résultats sur Yahoo.com
	y = WebSearch("YahooDemo")
	y.query = request.GET['s']
	resultats = y.parse_results().results
	import random
	r = random.randrange(0, len(resultats)-1)
	resultat = resultats[r]
	
	mots = resultat.Summary
	mots_originaux = mots
	mots = mots.split(' ')
	tags = []

	def enleverpoints(x): return x != u'...'
	mots = filter(enleverpoints, mots)

	if (len(mots) < 6) :
		raise Exception('Pas assez de mots!')

	for i in range(3):
		tag = mots[random.randrange(0, len(mots))]
		tags.append(tag)
		mots.remove(tag)

	# Récupération des photos sur Flickr.com
	f = Flickr()
	output = []
	for tag in tags:
		photos = f.get_photos_by_tag(tag.encode('utf-8'))
		newphotos = []
		for photo in photos:
			p = {
	 		'title' : photo('title'),
	 		'image'   : f.get_photo_image(photo),
	 		'url' : f.get_photo_url(photo)
	 		}
			newphotos.append(p)
		output.append({'photos':newphotos, 'tag': tag})

	def highlight_tags(mot): 
		if (tags.count(mot)) :
			return '<strong>%s</strong>' % mot
		else :
			return mot

	mots_originaux = mots_originaux.split(' ')
	mots_originaux = map(highlight_tags, mots_originaux)
	mots_originaux = " ".join(mots_originaux)

	t = loader.get_template('photos.html')
	c = Context({
    	'tags': output,
    	'mots' : mots_originaux,
    	'source' : resultat.Url
	})
	
	return HttpResponse(t.render(c))