# -*- coding: utf-8 -*-

from django.db import models
from flahoo.lib.FlickrClient import FlickrClient
    
class Flickr(models.Model):
	def get_photos_by_tag(self, tag, total=10):
		import flahoo.settings
		client = FlickrClient(flahoo.settings.FLICKR_API_KEY)

		photos = client.flickr_photos_search(tags=tag, per_page=total)
		return photos;
	
	def get_photo_image(self, photo, size='small_square'):
		
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

class Yahoo(models.Model):
	
	from yahoo.search.web import *
	
	def search(self, query, total):
		y = self.WebSearch("YahooDemo")
		y.query = query
		y.results = total
		return y.parse_results().results