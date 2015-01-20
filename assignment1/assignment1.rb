require 'RMagick'
include Magick

class GraphicsClassLibrary
	@image = nil

	def initialize(image_file)
		@image = Image.read(image_file).first
	end

	def save(out_file)
		@image.write(out_file)
	end

	def invert!
		@image = invert(@image)
	end

	def invert(img)
		new_pixels = []	

		img.each_pixel do |pixel, col, row|
			# The pixel.red is actually a very large number. So devide it by 257, 
			# then multiply it back. http://stackoverflow.com/questions/12651632/rmagick-pixel-color-value
			new_pixels.push((255-pixel.red/257)*257)
			new_pixels.push((255-pixel.green/257)*257)
			new_pixels.push((255-pixel.blue/257)*257)
		end

		image = Image.constitute(img.columns, img.rows, "RGB", new_pixels)
	end
end

img = GraphicsClassLibrary.new("image.jpg")
img.invert!
img.save("Outfile.jpg")