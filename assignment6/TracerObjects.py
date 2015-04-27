from PIL import Image

from math import sqrt, pow, pi, floor, acos

import random

from Vectors import Vec3, dot, normal, unit, cross
from GraphicsUtils import *

class Sphere(object):
	def __init__(self, center, radius, color=None, pattern="solid", name=None, is_mirror=False, is_light=False, casts_shadow=None, lambert=0.3, specular=0.0, diffuse=0.0, smudge=0.0):
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

		if self.is_light or self.is_mirror:
			self.diffuse = 0
		else:
			self.diffuse = diffuse

		if name == None:
			self.name = "A circle of size {0} at {1}".format(self.radius, self.center)
		else:
			self.name = name

		self.is_texture = False
		if pattern == "earth":
			self.is_texture = True
			self.texture = Image.open("texture/earth.jpg")

		if pattern == "camo":
			self.is_texture = True
			self.texture = Image.open("texture/camo.jpg")

		if pattern == "pool_1":
			self.is_texture = True
			self.texture = Image.open("texture/Ball1.jpg")

		if pattern == "pool_9":
			self.is_texture = True
			self.texture = Image.open("texture/Ball9.jpg")

		if self.is_texture:
			self.texture_width, self.texture_height = self.texture.size

	def colorAtPoint(self, point):

		if self.pattern == "related_abs":
			return RGBColor(self.color.r * abs(point.x)/4,
							self.color.g * abs(point.y)/4,
							self.color.b * abs(point.z)/4)
		elif self.pattern == "checkerboard":
			SCALE = 0.8
			OFFSET = 21423142

			x = floor((point.x + OFFSET) / SCALE) % 2 == 0
			y = floor((point.y + OFFSET) / SCALE) % 2 == 0
			z = floor((point.z + OFFSET) / SCALE) % 2 == 0

			if (x ^ y ^ z):
				return self.color
			else:
				return self.color.get_invert()
		elif self.is_texture:
			north_pole = self.center + self.radius * Vec3(1, 0, 0)
			north_pole = unit(north_pole)

			equator = self.center + self.radius * Vec3(1, 0, 0)
			equator = unit(equator)

			point = unit(self.center + point)

			# print "North Pole {0}".format(north_pole)
			# print "Equator {0}".format(equator)
			# print "HP {0}".format(point)

			phi = acos(-dot(north_pole, point))
			v = phi / pi

			theta = acos(dot(point,equator))
			if dot(cross(north_pole, equator), point) > 0:
				u = theta
			else:
				u = 1 - theta

			# u = min(0.999999999, u)
			# u = max(0, u)
			#
			# v = min(0.999999999, v)
			# v = max(0, v)

			# print "Width Point: {}".format(v * self.texture_width)
			# print "Height Point: {}".format(u * self.texture_height)

			cords = (int(v * self.texture_width), int(u * self.texture_height))
			c = self.texture.getpixel(cords)


			out_c = RGBColor(c[0]/255.0, c[1]/255.0, c[2]/255.0)
			return out_c

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
		return [[self.center.x - self.radius, self.center.x + self.radius],
				[self.center.y - self.radius, self.center.y + self.radius],
				[self.center.z - self.radius, self.center.z + self.radius]]

	def __str__(self):
		return "{0} - {1}".format(self.center, self.color)

class Plane(object):
	def __init__(self, center, normal, color=None, is_mirror=False, is_light=False, casts_shadow=None, lambert=0.3, specular=0.0, smudge=0.0):
		self.center = center
		self.normal = normal

		self.color = color
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

	def intersect(self, ray):
		denom = dot(ray.destination, self.normal)
		if abs(denom) < 1e-6:
			return (False, None)

		d = dot(self.center, self.normal) / denom
		if d < 0:
			return (False, None)

		return (True, d)

	def colorAtPoint(self, point):
		return self.color
