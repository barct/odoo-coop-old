# -*- coding: utf-8 -*-
import sqlite3
import math
import os 


class Parser():

	def __init__(self):
		self.con = sqlite3.connect(os.path.join(os.path.dirname(__file__), './common_names.sqlite3'))
		self.cursor = self.con.cursor()

		self.cursor.execute("SELECT sum(frecuency) FROM last_names")
		self.sum_last_names = self.cursor.fetchone()[0]
		self.cursor.execute("SELECT sum(frecuency) FROM first_names")
		self.sum_first_names = self.cursor.fetchone()[0]

	def desaggregate_names(self, names):
		start = 0
		end = len(names)
		while start>=0:
			start = names.find(" ", start+1, end)
			if start > 0:
				yield names[:start], names[start+1:]


	def parse_lastnames_firstnames(self, names):	
		best = (names, None, 0)
		for last_names, first_names in self.desaggregate_names(names):
			p = 0 
			for name in last_names.split():
				self.cursor.execute("SELECT frecuency from last_names where names = ? COLLATE NOCASE LIMIT 1" , (name,))
				row = self.cursor.fetchone()
				if row:
					p=p+float(row[0])/self.sum_last_names
			
			last_names_rate=p
			p=0
				
			for name in first_names.split():
				self.cursor.execute("SELECT frecuency from first_names where names = ? COLLATE NOCASE LIMIT 1" , (name,))
				row = self.cursor.fetchone()
				if row:
					p=p+float(row[0])/self.sum_first_names
			
			first_names_rate = p
			rate = last_names_rate+first_names_rate
			if rate > best[2]:
				best = last_names,first_names,rate
		return best[0],best[1]

