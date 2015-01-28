from Vectors import Vec3, dot
from PIL import Image

class RayTracer(object):
	image = None
	width = None
	height = None
	origin = None

	def __init__(self, height, width, origin):
		self.image = Image.new("RGB", (width, height))
		self.height = float(height)
		self.width = float(width)
		self.origin = origin


	def trace(self):
		for i in range(0, int(self.width)):
			for j in range(0, int(self.height)):
				x = -1 + 2*(i/(self.width-1)) 
				y = -1 + 2*(j/(self.height-1))
				z = -1

				ray = Vec3(x, y, z)
				direction = Vec3(0, 0, -1)

				hit_sphere = False
				if hit_sphere:
					pass
				else:
					r = 0
					g = 0.2*(1 + ray.y)*256
					b = 0.1*256

					self.image.putpixel((i,j), (int(r),int(g),int(b)))

	def export(self, file_name):
		self.image.save(file_name)

class Ray(object):
	origin = None
	direction = None

	def __init__(self, origin, direction):
		self.origin = origin
		self.direction = direction

if __name__ == '__main__':
	tracer = RayTracer(256, 256, Vec3(0, 0, 0))
	tracer.trace()
	tracer.export("out.png")
