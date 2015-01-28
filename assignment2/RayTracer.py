from Vectors import Vec3, dot

class RayTracer(object):
	def __init__(self):
		center = Vec3(0, 0, 0)
		print center

		a = Vec3(1, 3, -5)
		b = Vec3(4, -2, -1)

		print dot(a, b)

if __name__ == '__main__':
	tracer = RayTracer()
