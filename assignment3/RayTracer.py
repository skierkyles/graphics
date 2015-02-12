from Vectors import Vec3, dot, normal
from GraphicsUtils import *
from TracerObjects import Sphere

from PIL import Image
from math import sqrt, pow, pi


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
				y = -1 + 2*(j/((self.height)-1))
				z = -1

				ray = Vec3(x, y, z)

				# Add the min stuff here! Instead of the break
				hit_sphere = False
				hit_point = None
				sphere = None

				closest = float("inf")

				for obj in self.objects:
					hit, distance = obj.intersect(self.origin, ray)
					closer = distance < closest

					if hit and closer:
						closest = distance
						hit_sphere = True
						# print ray
						# print "The ray sent out is {0}".format(ray)
						hit_point = ray*distance
						# print "Hit Point is then {0}".format(hit_point)
						sphere = obj



				if hit_sphere:
					# y_normal_component = hit_point.normal().y
					# shader = max(0.0, -y_normal_component)
					# color = sphere.color * shader
					color = sphere.color

					# for secondary_obj in self.objects:
					# 	hit, distance = secondary_obj.intersect(hit_point, Vec3(0, -1, 0))
					#
					# 	not_self = secondary_obj != sphere
					# 	if hit and not_self:
					# 		# print "Starting from {0}, hp: {1}".format(sphere.name, hit_point)
					# 		# print "It hit {0}".format(secondary_obj.name)
					# 		color = RGBColor(0, 0, 0)

					# for shadow_obj in self.objects:
					# 	hit, distance = shadow_obj.intersect(hit_point, Vec3(0, 1, 0))
					#
					# 	not_self = shadow_obj != sphere
					# 	if hit:
					#
					# 		# print "Hit a circle"
					# 		# print shadow_obj.name
					# 		# print "Hit at {0} far away".format(distance)
					# 		# print distance
					# 		color = RGBColor(0, 0, 0)

					self.image.putpixel((i,j), color.get_256_tuple())

				else:
					r = 0
					g = 0.2*(1 + ray.y)
					b = 0.1

					# bg = RGBColor(r, g, b)
					bg = RGBColor(0, 0, 0)

					self.image.putpixel((i,j), bg.get_256_tuple())

	def add_objects(self):
		# center (0, 1, -3) radius 1   object_color = (1.0, 0.5, 0.5)
		# center (2, 1, -4) radius 1    object_color = (0.5, 1.0, 0.5)
		# center (-2, 1, -3) radius 1    object_color = (0.5, 0.5, 1.0)
		# center (0, -100, 0) radius 100    object_color = (1.0, 1.0, 1.0)

		sphere1_center = Vec3(0, 1, -3)
		circle1 = Sphere(sphere1_center, 1, RGBColor(1.0, 0.5, 0.5)) #Red
		self.objects.append(circle1)

		sphere2_center = Vec3(2, 1, -4)
		circle2 = Sphere(sphere2_center, 1, RGBColor(0.5, 1.0, 0.5)) #Green
		self.objects.append(circle2)

		sphere3_center = Vec3(-2, 1, -3)
		circle3 = Sphere(sphere3_center, 1, RGBColor(0.5, 0.5, 1.0)) #Blue
		self.objects.append(circle3)

		sphere4_center = Vec3(0, -100, 0)
		circle4 = Sphere(sphere4_center, 100, RGBColor(1.0, 1.0, 1.0), name="Monster")
		# self.objects.append(circle4)

	def export(self, file_name):
		self.image.save(file_name)

if __name__ == '__main__':
	tracer = RayTracer(100, 100, Vec3(0, 0, 0))
	tracer.add_objects()
	tracer.trace()
	tracer.export("out.png")
