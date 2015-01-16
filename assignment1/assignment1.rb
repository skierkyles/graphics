require 'RMagick'
include Magick

class GraphicsClassLibrary
	@image = nil

	def initialize(image_file)
		@image = ImageList.new(image_file)
		puts "Image #{@image}"
	end

	def save(out_file)
		puts "Saving #{out_file}"
	end

	def invert

	end
end

img = GraphicsClassLibrary.new("image.jpg")
img.save("Outfile.jpg")