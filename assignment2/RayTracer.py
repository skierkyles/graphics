from Vectors import Vec3, dot, normal

from PIL import Image
from math import sqrt, pow, pi


class RayTracer(object):
	def __init__(self, height, width, origin):
		self.image = Image.new("RGB", (width, height))
		self.height = height
		self.width = width
		self.origin = origin


	def trace(self):
		sphere_center = Vec3(0, 0, -3)
		circle = Sphere(sphere_center, 2)

		for i in range(0, self.width):
			for j in range(0, self.height):
				x = -1 + 2*(i/(float(self.width)-1)) 
				y = -1 + 2*(j/(float(self.height)-1))
				z = -1

				ray = Vec3(x, y, z)

				hit_sphere = circle.intersect(self.origin, ray)

				if hit_sphere:
					nr = ray - sphere_center
					norm = nr.normal()		

					r = ((norm.x + 1)/2)*256
					g = ((norm.y + 1)/2)*256
					b = ((norm.z + 1)/2)*256

					self.image.putpixel((i,j), (int(r),int(g),int(b)))
				
				else:
					r = 0
					g = 0.2*(1 + ray.y)*256
					b = 0.1*256

					self.image.putpixel((i,j), (int(r),int(g),int(b)))

	def export(self, file_name):
		self.image.save(file_name)

class Sphere(object):
	def __init__(self, center, radius):
		self.center = center
		self.radius = radius 

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

			return True
		
		return False

if __name__ == '__main__':
	tracer = RayTracer(256, 256, Vec3(0, 0, 0))
	tracer.trace()
	tracer.export("out.png")
