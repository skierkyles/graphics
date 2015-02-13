import numpy as np

from math import sqrt, pow, pi

class Vec3(object):
	def __init__(self, x, y, z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

	def __add__(self, b):
		return Vec3(self.x + b.x, self.y + b.y, self.z + b.z)

	def __sub__(self, b):
		return Vec3(self.x - b.x, self.y - b.y, self.z - b.z)

	def __rmul__(self, b):
		return self.__mul__(b)

	def __mul__(self, b):
		assert type(b) == float or type(b) == int
		return Vec3(self.x * b, self.y * b, self.z * b)

	def __div__(self, b):
		assert type(b) == float or type(b) == int
		return Vec3(self.x / b, self.y / b, self.z / b)

	def __str__(self):
		return "Vec3({0}, {1}, {2})".format(self.x, self.y, self.z)

	def normal(self):
		return normal(self)

	def magnitude(self):
		return magnitude(self)

def dot(a, b):
	return (a.x * b.x) + (a.y * b.y) + (a.z * b.z)

def magnitude(a):
	return sqrt(a.x**2 + a.y**2 + a.z**2)

def normal(a):
	m = magnitude(a)
	assert m != 0

	return Vec3(a.x/m, a.y/m, a.z/m)
