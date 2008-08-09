# -*- coding: utf-8 -*-

import unittest
from flahoo.photos.models import Flickr
from flahoo.photos.models import Yahoo

class PhotosTestCase(unittest.TestCase):

	def testTagr(self):
		"""Test la fonction make_tagr"""
		tags = (
			 	('bob', 'bo<strong>b</strong>'),
			 	('Jack', 'Jac<strong>k</strong>'),
			 	)
		
		f = Flickr()
		for tag, tagr in tags:
			result = f.make_tagr(tag)
			self.assertEqual(result, tagr)
			
	def testFiltrerTag(self):
		"""Test la fonction filtrer_tag"""
		tags = (
			 	('in,', 'in'),
			 	('casse-tete', 'casse-tete'),
			 	)
		
		f = Flickr()
		for tag, tag_filter in tags:
			result = f.filtrer_tag(tag)
			self.assertEqual(result, tag_filter)