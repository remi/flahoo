# -*- coding: utf-8 -*-

from flahoo.lib.FlickrClient import FlickrClient
import random, re
import flahoo.settings

class FlickrError(Exception): pass
class BadTagsError(FlickrError): pass
class WordsError(FlickrError): pass

class Flickr:
	sort_methods = ('date-posted-asc',
					'date-posted-desc',
					'date-taken-asc',
					'date-taken-desc',
					'interestingness-desc',
					'interestingness-asc',
					'relevance')

	def get_tags_from_mots(self, mots):
		tags = []
		for i in range(flahoo.settings.FLAHOO_TOTAL_TAGS):
			if len(mots) == 0:
				raise BadTagsError
			tag = mots[random.randrange(0, len(mots))]
			mots.remove(tag)
			tag_original = tag
			tag = self.filtrer_tag(tag)
			if tag == u'':
				raise BadTagsError
			tags.append(tag.lower())
		return tags

	def filtrer_tag(self, tag):
		return re.sub(':|;|,|\.|\s|\(|\)|!', '', tag.lower())

	def get_photos_by_tag(self, tag, total=10):
		"""Retourne un objet contenant des photos et des informations relatives à un tag"""
		import flahoo.settings
		client = FlickrClient(flahoo.settings.FLAHOO_FLICKR_API_KEY)
		sort_method = random.choice(self.sort_methods)
		photos = client.flickr_photos_search(tags=tag, per_page=total, sort=sort_method)

		newphotos = []

		for photo in photos:
			p = {
	 		'title' : photo('title'),
	 		'image'   : self.get_photo_image(photo),
	 		'url' : self.get_photo_url(photo)
	 		}
			newphotos.append(p)

		tagr = self.make_tagr(tag)
		url = "/photos/%s" % tag.lower()
		obj = {
			'photos':newphotos,
			'tag': tag,
			'sort': sort_method,
			'tagr' : tagr,
			'url' : url
			}
		
		return obj
	
	def make_tagr(self, tag):
		return re.sub('^(.+)(.{1})$', '\\1<strong>\\2</strong>', tag)
	
	def get_photo_image(self, photo, size='small_square'):
		"""Retourne l'URL d'une photo selon un objet d'une photo et d'un format"""
		
		base_url = "http://static.flickr.com"
		size_char='s'  # default to small_square
		
		if size == 'small_square':
			size_char='_s'
		elif size == 'thumb':
			size_char='_t'
		elif size == 'small':
			size_char='_m'
		elif size == 'medium':
			size_char=''
		elif size == 'large':
			size_char='_b'
		elif size == 'original':
			size_char='_o'
		
		return "%s/%s/%s_%s%s.jpg" % (base_url, photo('server'), photo('id'), photo('secret'), size_char)
	
	def get_photo_url(self, photo):
		base_url = "http://flickr.com"
		return "%s/photos/%s/%s/" % (base_url, photo('owner'), photo('id'))

class Yahoo:
	
	from yahoo.search.web import *
	
	def search(self, query, total):
		"""Retourne des résultats de rechercher basés sur des mots-clés et un total"""
		
		y = self.WebSearch("YahooDemo")
		y.query = query
		y.results = total
		return y.parse_results().results
	
	def filtrer_mots(self, mots):
		def enleverpoints(x): return x != u'...' # on enlève les occurences de "..." dans les mots
		def tolower(x): return x.lower()
		mots = mots.encode('utf-8')
		mots = mots.split(" ")
		mots = filter(enleverpoints, mots)
		mots = map(tolower, mots)
		return mots
	
	def highliter_mots(self, mots, tags):
		f = Flickr()
		def highlight_tags(mot): 
			mot = f.filtrer_tag(mot.lower())
			if (tags.count(mot)) :
				return '<strong>%s</strong>' % mot
			else :
				return mot
		mots = mots.split(' ')
		mots = map(highlight_tags, mots)
		return " ".join(mots)
		
