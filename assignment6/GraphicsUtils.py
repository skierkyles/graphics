class RGBColor(object):
	def __init__(self, r, g, b):
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)

	def __add__(self, b):
		return RGBColor(self.r + b.r, self.g + b.g, self.b + b.b)

	def __rmul__(self, b):
		return self.__mul__(b)

	def __mul__(self, b):
		assert type(b) == float or type(b) == int
		return RGBColor(self.r * b, self.g * b, self.b * b)

	def get_invert(self):
		return invert(self)

	def get_tuple(self):
		return (self.r, self.g, self.b)

	def get_256_tuple(self):
		r, g, b = self.get_tuple()

		return to_int256_rgb((max(0, r), max(0, g), max(0, b)))

	def get_darker(self, amt=0.01):
		return RGBColor(self.r - amt, self.g - amt, self.b - amt)

	def get_brighter(self, amt=0.01):
		return RGBColor(self.r + amt, self.g + amt, self.b + amt)

	def __str__(self):
		return "RGBColor({0}, {1}, {2})".format(self.r, self.g, self.b)

def invert(color):
	return RGBColor(1 - color.r, 1 - color.g, 1 - color.b)

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
