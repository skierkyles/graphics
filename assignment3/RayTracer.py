from Vectors import Vec3, dot, normal
from GraphicsUtils import *

from PIL import Image
from math import sqrt, pow, pi


class RayTracer(object):
	def __init__(self, height, width, origin):
		self.image = Image.new("RGB", (width, height))
		self.height = height
		self.width = width
		self.origin = origin
		self.objects = []


	def trace(self):
		for i in range(0, self.width):
			for j in range(0, self.height):
				x = -1 + 2*(i/(float(self.width)-1)) 
				y = -1 + 2*(j/(float(self.height)-1))
				z = -1

				ray = Vec3(x, y, z)

				# Add the min stuff here! Instead of the break
				hit_sphere = False
				sphere = None

				closest = float("inf")

				for obj in self.objects:
					hit, distance = obj.intersect(self.origin, ray)
					# closer = distance < closest
					closer = True

					if hit:
						hit_sphere = True
						sphere = obj
						


				if hit_sphere:
					nr = ray - obj.center

					self.image.putpixel((i,j), to_int_rgb(obj.color))
				
				else:
					r = 0
					g = 0.2*(1 + ray.y)*256
					b = 0.1*256

					self.image.putpixel((i,j), (int(r),int(g),int(b)))

	def add_objects(self):
		# center (0, 1, -3) radius 1   object_color = (1.0, 0.5, 0.5)
		# center (2, 1, -4) radius 1    object_color = (0.5, 1.0, 0.5)
		# center (-2, 1, -3) radius 1    object_color = (0.5, 0.5, 1.0)
		# center (0, -100, 0) radius 100    object_color = (1.0, 1.0, 1.0)

		sphere1_center = Vec3(0, 1, -3)
		circle1 = Sphere(sphere1_center, 1, to_256_rgb((1.0, 0.5, 0.5)))
		self.objects.append(circle1)

		sphere2_center = Vec3(2, 1, -4)
		circle2 = Sphere(sphere2_center, 1, to_256_rgb((0.5, 1.0, 0.5)))
		self.objects.append(circle2)

		sphere3_center = Vec3(-2, 1, -3)
		circle3 = Sphere(sphere3_center, 1, to_256_rgb((0.5, 0.5, 1.0)))
		self.objects.append(circle3)

		# sphere4_center = Vec3(0, -100, 0)
		# circle4 = Sphere(sphere4_center, 100, to_256_colors((1.0, 1.0, 1.0)))
		# self.objects.append(circle4)

	def export(self, file_name):
		self.image.save(file_name)

class Sphere(object):
	def __init__(self, center, radius, color):
		self.center = center
		self.radius = radius 
		self.color = color

	# Returns if it hit and the distance it hit at. 
	def intersect(self, origin, direction):
		temp = self.center - origin
		a = dot(direction, direction)
		b = 2.0 * dot(temp, direction)
		c = dot(temp, temp) - self.radius * self.radius
		disc = b * b - 4.0 * a * c


		if (disc > 0.0):
			e = sqrt(disc)
			denominator = 2.0 * a

			# epsilon = 1.0e-7

			# t = (-b - e) / denominator
			# if (t > epsilon):
			# 	n = (temp + (t * direction)) / self.radius
			# 	hp = origin + t * direction
				
			# 	return True

			# t = (-b + e) / denominator
			# if (t > epsilon):
			# 	n = (temp + (t * direction)) / self.radius
			# 	hp = origin + t * direction

			return (True, disc)
		
		return (False, None)

if __name__ == '__main__':
	tracer = RayTracer(256, 256, Vec3(0, 0, 0))
	tracer.add_objects()
	tracer.trace()
	tracer.export("out.png")
