from Vectors import Vec3, dot, normal
from GraphicsUtils import *

from math import sqrt, pow, pi

class Sphere(object):
	def __init__(self, center, radius, color, name=None):
		self.center = center
		self.radius = float(radius)
		self.color = color
		if name == None:
			self.name = "A {0} circle of size {1} at {2}".format(self.color, self.radius, self.center)
		else:
			self.name = name

	# Returns if it hit and the distance it hit at.
	def intersect(self, origin, direction):
		a = dot(direction, direction)
		offset = origin - self.center
		b = 2*dot(direction, offset)
		c = dot(offset, offset) - self.radius * self.radius
		disc = b * b - 4.0 * a * c

		if disc > 0:
			distSqrt = sqrt(disc)
			q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
			t0 = q / a
			if (q == 0.0):
				t1 = float('inf')
			else:
				t1 = c / q

			# TODO: INVESTIGATE IF IT"S RETURNING the proper one
			t0, t1 = min(t0, t1), max(t0, t1)
			if t1 >= 0:
				return (True, t1) if t0 < 0 else (True, t0)

		return (False, None)


	def __str__(self):
		return "{0} - {1}".format(self.center, self.color)
