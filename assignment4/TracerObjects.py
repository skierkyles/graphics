from Vectors import Vec3, dot, normal
from GraphicsUtils import *

from math import sqrt, pow, pi

class Sphere(object):
	def __init__(self, center, radius, color=None, name=None, is_mirror=False, is_light=False):
		self.center = center
		self.radius = float(radius)
		self.color = color

		self.is_mirror = is_mirror
		self.is_light = is_light

		if name == None:
			self.name = "A circle of size {0} at {1}".format(self.radius, self.center)
		else:
			self.name = name

	# Returns if it hit and the distance it hit at.
	def intersect(self, ray):
		a = dot(ray.destination, ray.destination)
		offset = ray.origin - self.center
		b = 2*dot(ray.destination, offset)
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

			t0, t1 = min(t0, t1), max(t0, t1)
			if t1 >= 0:
				return (True, t1) if t0 < 0 else (True, t0)

		return (False, None)

	def bounds(self):
		# @Override
		# public BoundingBox getBounds() {
		# 	return new BoundingBox(position.x - radius, position.x + radius,
		# 			position.y - radius, position.y + radius, position.z - radius,
		# 			position.z + radius);
		# }
		print "A bounds method here"

	def __str__(self):
		return "{0} - {1}".format(self.center, self.color)
