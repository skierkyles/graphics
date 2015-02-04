
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