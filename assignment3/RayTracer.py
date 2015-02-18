from Vectors import Vec3, dot, normal
from GraphicsUtils import *
from TracerObjects import Sphere

from PIL import Image
from math import sqrt, pow, pi

import random

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

				ray = Vec3(x, y, z)

				ray_hit_object = False
				hit_point = None
				hit_object = None
				distance_to_closest_hit = float("inf")


				for obj in self.objects:
					hit, distance = obj.intersect(self.origin, ray)
					closer = distance < distance_to_closest_hit

					if hit and closer:
						distance_to_closest_hit = distance

						ray_hit_object = True
						hit_point = self.origin + ray * distance #A scalar
						hit_object = obj

				if hit_object:
					# Calculate shading
					# So take the point on the surface of the sphere
					# then, figure out the distance from it to the center.
					# Then take the normal of that.
					unit_normal = hit_point - hit_object.center
					normal_vector = unit_normal.normal()

					shader = max(0.0, normal_vector.y)
					color = hit_object.color * shader

					# Calculate shadows
					for shadow_obj in self.objects:
						# semi_rand = Vec3(-1+2*random.random(),2*random.random(),-1+2*random.random())
						up = Vec3(0, 1, 0)
						hit, distance = shadow_obj.intersect(hit_point, up)

						not_self = shadow_obj != hit_object

						if hit and not_self:
							color = RGBColor(0,0,0)


					self.image.putpixel((i,j), color.get_256_tuple())

				else:
					r = 0
					g = 0.2*(1 - ray.y)
					b = 0.1

					bg = RGBColor(r, g, b)

					self.image.putpixel((i,j), bg.get_256_tuple())

	def add_objects(self):
		sphere1_center = Vec3(0, 0, -3)
		circle1 = Sphere(sphere1_center, 1, RGBColor(1.0, 0.5, 0.5)) #Red
		self.objects.append(circle1)

		sphere2_center = Vec3(2, 0, -4)
		circle2 = Sphere(sphere2_center, 1, RGBColor(0.5, 1.0, 0.5)) #Green
		self.objects.append(circle2)

		sphere3_center = Vec3(-2, 0, -3)
		circle3 = Sphere(sphere3_center, 1, RGBColor(0.5, 0.5, 1.0)) #Blue
		self.objects.append(circle3)

		sphere4_center = Vec3(0, -100, 0)
		circle4 = Sphere(sphere4_center, 98.5, RGBColor(1.0, 1.0, 1.0), name="Monster")
		self.objects.append(circle4)

	def export(self, file_name):
		self.image.save(file_name)

if __name__ == '__main__':
	tracer = RayTracer(5000, 5000, Vec3(0, 0, 0))
	tracer.add_objects()
	tracer.trace()
	tracer.export("out.png")
