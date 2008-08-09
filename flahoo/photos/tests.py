# -*- coding: utf-8 -*-

import unittest
from flahoo.photos.models import *

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
	
	def testHighlightMots(self):
		"""Test la fonction highlighter_mots"""
		y = Yahoo()
		mots = (
			('La pomme est un fruit alors que la poire, en est un aussi mais pas la Banane!', ['pomme', 'poire', 'banane'], 'la <strong>pomme</strong> est un fruit alors que la <strong>poire</strong> en est un aussi mais pas la <strong>banane</strong>'),
			)
		for (mot, tags, highlight) in mots:
			result = y.highliter_mots(mot, tags)
			self.assertEqual(result, highlight)
	
	def testGetMots(self):
		"""Test la fonction get_tags_from_mots"""
		mots = (
			 	(u'Mot ; mot2'),
			 	(u'Mot -'),
			 	)
		
		f = Flickr()
		for mot in mots:
			
			self.assertRaises(BadTagsError, f.get_tags_from_mots, mot.split(" "))