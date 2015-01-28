class Vec3(object):
	x = None
	y = None
	z = None

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return "({0}, {1}, {2})".format(self.x, self.y, self.z)

def dot(a, b):
	return (a.x*b.x) + (a.y*b.y) + (a.z*b.z)
