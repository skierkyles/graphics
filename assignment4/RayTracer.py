from Vectors import Vec3, dot, normal
from GraphicsUtils import *
from TracerObjects import Sphere

from PIL import Image
from math import sqrt, pow, pi

import random

MAX_DEPTH = 5
TINY = 0.00000001

class RayTracer(object):
	def __init__(self, height, width, origin):
		self.image = Image.new("RGB", (width, height))
		self.height = float(height)
		self.width = float(width)
		self.origin = origin
		self.objects = []


	def trace(self):
		for i in range(0, int(self.width)):
			for j in range(0, int(self.height)):
				x = -1 + 2*(i/((self.width)-1))
				y = 1 - 2*(j/((self.height)-1))
				z = -1

				ray = Ray(self.origin, Vec3(x, y, z))

				# Check this out for structure.
				# http://www.cs.jhu.edu/~cohen/RendTech99/Lectures/Ray_Tracing.bw.pdf
				color = self.ray_point_color(ray)
				self.image.putpixel((i,j), color.get_256_tuple())

	def backgroundColor(self, ray):
		r = 0
		g = 0.2*(1 - ray.destination.y)
		b = 0.1

		return RGBColor(r, g, b)

	def intersectedObject(self, ray):
		ray_hit_object = False
		hit_point = None
		hit_object = None
		distance_to_closest_hit = float("inf")

		# Check this out for structure.
		# http://www.cs.jhu.edu/~cohen/RendTech99/Lectures/Ray_Tracing.bw.pdf
		for obj in self.objects:
			hit, distance = obj.intersect(ray)
			closer = distance < distance_to_closest_hit

			if hit and closer:
				distance_to_closest_hit = distance

				ray_hit_object = True
				hit_point = ray.origin + ray.destination * distance #A scalar
				hit_object = obj

		if ray_hit_object:
			# (Hit object (bool), hp, ho)
			return (True, hit_point, hit_object)
		else:
			return (False, None, None)

	def ray_point_color(self, ray):
		ray_hit_object, hit_point, hit_object = self.intersectedObject(ray)

		if ray_hit_object:
			unit_normal = hit_point - hit_object.center
			normal_vector = unit_normal.normal()

			# Calculate shading
			# So take the point on the surface of the sphere
			# then, figure out the distance from it to the center.
			# Then take the normal of that.
			color = hit_object.color
			if hit_object.is_light is False and hit_object.is_mirror is False:
				shader = max(0.0, normal_vector.y)
				color = hit_object.colorAtPoint(hit_point) * shader

			if hit_object.is_mirror:
				color = self.recursiveReflections(hit_object, hit_point, ray, normal_vector)

			# Calculate shadows
			for shadow_obj in self.objects:
				# semi_rand = Vec3(-1+2*random.random(),2*random.random(),-1+2*random.random())
				shadow_ray = Ray(hit_point, Vec3(0, 1, 0))

				hit, distance = shadow_obj.intersect(shadow_ray)

				not_self = shadow_obj != hit_object
				is_not_a_light = shadow_obj.is_light == False

				if hit and not_self and is_not_a_light:
					color = RGBColor(0,0,0)

			return color

		else:
			return self.backgroundColor(ray)



	def recursiveReflections(self, obj, initial_hit, ray, normal, depth=0):
		# https://www.cs.unc.edu/~rademach/xroads-RT/RTarticle.html
		c1 = -dot(ray.destination, normal) #This is a integer!!
		reflection = ray.destination + (2 * normal * c1)

		# c = (2 * dot(ray.destination, normal) * normal)
		# reflection = (ray.destination - c).normal()

		reflection_ray = Ray(initial_hit + normal * TINY, reflection)
		return self.ray_point_color(reflection_ray)

		# print "Reflection of {0}".format(ray.destination)
		# print rl

		# if depth >= MAX_DEPTH:
		# 	return "Done!"
		#
		# else:
		# 	return self.recursiveReflections(obj, initial_hit, ray, normal, depth=depth+1)

	def add_objects(self):
		# Vec3(left right, up down, back forth)

		light_center = Vec3(0, 10, 0)
		light_sphere = Sphere(light_center, 1,
							color=RGBColor(1.0, 1.0, 1.0),
							is_light=True)
		self.objects.append(light_sphere)

		sphere1_center = Vec3(0, 0, -3)
		red_center = Sphere(sphere1_center, 1, color=RGBColor(1.0, 0.5, 0.5)) #Red
		self.objects.append(red_center)

		sphere2_center = Vec3(2, 0, -4)
		green_right = Sphere(sphere2_center, 1,
							color=RGBColor(0.5, 1.0, 0.5)) #Green
		self.objects.append(green_right)

		sphere3_center = Vec3(-2, 0, -3)
		blue_left = Sphere(sphere3_center, 1,
							color=RGBColor(0.5, 0.5, 1.0),
							is_mirror=True) #Blue
		self.objects.append(blue_left)

		sphere4_center = Vec3(0, -100, 0)
		circle4 = Sphere(sphere4_center, 98.5,
							color=RGBColor(1.0, 1.0, 1.0),
							name="Monster")
		self.objects.append(circle4)

	def export(self, file_name):
		self.image.save(file_name)

class Ray(object):
	def __init__(self, origin, destination):
		self.origin = origin
		self.destination = destination


if __name__ == '__main__':
	# Vec3(left right, up down, back forth)
	tracer = RayTracer(450, 450, Vec3(0, 0, 0))
	tracer.add_objects()
	tracer.trace()
	tracer.export("out.png")
