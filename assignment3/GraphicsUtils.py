class RGBColor(object):
	def __init__(self, r, g, b):
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)

	def __rmul__(self, b):
		return self.__mul__(b)

	def __mul__(self, b):
		assert type(b) == float or type(b) == int
		return RGBColor(self.r * b, self.g * b, self.b * b)

	def get_tuple(self):
		return (self.r, self.g, self.b)

	def get_256_tuple(self):
		return to_int256_rgb((self.r, self.g, self.b))

	def __str__(self):
		return "RGBColor({0}, {1}, {2})".format(self.r, self.g, self.b)

def to_256_rgb(rgb):
	r = rgb[0] * 256
	g = rgb[1] * 256
	b = rgb[2] * 256

	return (r, g, b)

def to_int_rgb(rgb):
	r = int(rgb[0])
	g = int(rgb[1])
	b = int(rgb[2])

	return (r, g, b)

def to_int256_rgb(rgb):
	return to_int_rgb(to_256_rgb(rgb))
