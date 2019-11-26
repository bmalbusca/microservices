# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 10:00:15 2014

@author: jnos
"""

class book:
	def __init__(self, author, title, year, b_id):
		self.author = author
		self.title = title
		self.year = year
		self.id = b_id
	def __str__(self):
		return "%d - %s - %s - %s" % (self.id, self.author, self.title, self.year) 
		
