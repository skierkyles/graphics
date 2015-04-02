from Vectors import Vec3, dot, normal
from GraphicsUtils import *

from math import sqrt, pow, pi, floor

import random

class Sphere(object):
	def __init__(self, center, radius, color=None, pattern="solid", name=None, is_mirror=False, is_light=False, casts_shadow=None, lambert=0.3, specular=0.0, smudge=0.0):
		self.center = center
		self.radius = float(radius)
		self.color = color
		self.pattern = pattern

		self.is_mirror = is_mirror
		if is_mirror:
			self.specular = 1
		else:
			self.specular = specular

		self.is_light = is_light
		if casts_shadow == None:
			self.casts_shadow = False if self.is_light else True
		else:
			self.casts_shadow = casts_shadow

		if self.is_light:
			self.lambert = 1
		else:
			self.lambert = lambert

		self.smudge = smudge

		if name == None:
			self.name = "A circle of size {0} at {1}".format(self.radius, self.center)
		else:
			self.name = name

	def colorAtPoint(self, point):

		if self.pattern == "related_abs":
			return RGBColor(self.color.r * abs(point.x),
							self.color.g * abs(point.y),
							self.color.b * abs(point.z))
		elif self.pattern == "checkerboard":
			SCALE = .8
			OFFSET = 21423142

			x = floor((point.x + OFFSET) / SCALE) % 2 == 0
			y = floor((point.y + OFFSET) / SCALE) % 2 == 0
			z = floor((point.z + OFFSET) / SCALE) % 2 == 0

			if (x ^ y ^ z):
				return self.color
			else:
				return self.color.get_invert()
		else:
			return self.color



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

	def randomPointInSphere(self):
		b = self.bounds()

		while True:
			x = random.uniform(b[0][0], b[0][1])
			y = random.uniform(b[1][0], b[1][1])
			z = random.uniform(b[2][0], b[2][1])

			ran = Vec3(x, y, z)

			if self.pointInSphere(ran):
				return ran


	def pointInSphere(self, point):
		a = (self.center.x - point.x)**2 + (self.center.y - point.y)**2 + (self.center.z - point.z)**2
		return a <= self.radius**2

	def bounds(self):
		ext = self.radius/10

		return [[self.center.x - self.radius - ext, self.center.x + self.radius + ext],
				[self.center.y - self.radius - ext, self.center.y + self.radius + ext],
				[self.center.z - self.radius - ext, self.center.z + self.radius + ext]]

	def __str__(self):
		return "{0} - {1}".format(self.center, self.color)
