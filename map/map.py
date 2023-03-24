#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker

from gradient import hsv2rgb # wymagane oba pliki w celu zaimportowania funkcji!

class Map:
	def __init__(self, file):
		self.data = []
		self.read_file(file)
		self.size = len(self.data)
		self.maxh = 0
		self.minh = 200
		self.maxdiff = 0
		self.find_values()
		# self.check_type()
		self.draw_map()


	def read_file(self, f) -> None:
		file = open(f, "r")
		for line in file:
			self.data.append([float(i) for i in line.split(" ")[:-1]])
		file.close()
		self.data = self.data[1:]


	def normalize_height(self, h):
		h -= self.minh
		h /= (self.maxh - self.minh)
		return h


	def simple_shading(self, point, next):
		if point < next:
			return -0.2
		return 0.2


	def shading(self, point, next):
		diff = abs(point - next)
		if diff < 0.00000005: # less value - more sensitivity
			return 0
		if point < next:
			return -0.9 * (diff / self.maxdiff)
		return 0.1 


	def find_values(self) -> None:
		for i in range(self.size):
			for j in range(self.size):
				if self.data[i][j] > self.maxh:
					self.maxh = self.data[i][j]
				if self.data[i][j] < self.minh:
					self.minh = self.data[i][j]
		for i in range(self.size):
			for j in range(self.size):
				if j < self.size-1:
					diff = abs(self.normalize_height(self.data[i][j]) - self.normalize_height(self.data[i][j + 1]))
					if diff > self.maxdiff:
						self.maxdiff = diff
		return


	def draw_map(self) -> None:
		plt.figure()
		for i in range(self.size):
			for j in range(self.size):
				h = self.normalize_height(self.data[i][j])
				if j < self.size-1:
					v = self.shading(h, self.normalize_height(self.data[i][j+1]))
				self.data[i][j] = hsv2rgb(1-(2/3 + 1/3*h), 1, 0.9 + v) # simple: 0.6 - 0.8 - 1.0
		plt.imshow(self.data)
		plt.savefig('mymap.pdf', bbox_inches='tight')
		plt.close()
	

	def check_type(self) -> None:
		for i in self.data:
			for j in i:
				if not isinstance(j, float):
					print("Bad data type")
					return 0


def main():
	mymap = Map("big.dem")

if __name__ == '__main__':
	main()