import sys

from PIL import Image, ImageOps

class GraphicsClassLib:
	def invert_image(self, in_file, out_file):
		# print "Inverting {0} to {1}".format(in_file, out_file)
		image = Image.open(in_file)

		rgb_image = image.convert('RGB')

		width, height = rgb_image.size

		new_image = Image.new('RGB', (width, height))

		for x in range(0, width):
			for y in range(0, height):
				r, g, b = rgb_image.getpixel((x,y))
				new_rgb = (255-r, 255-g, 255-b)

				new_image.putpixel((x,y), new_rgb)


		new_image.save(out_file)

if __name__ == "__main__":
	cls = GraphicsClassLib()
	cls.invert_image(sys.argv[1], sys.argv[2])