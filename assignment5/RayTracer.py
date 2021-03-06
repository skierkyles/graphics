from Vectors import Vec3, Ray, dot, normal, unit
from GraphicsUtils import *
from TracerObjects import Sphere

from PIL import Image
from math import sqrt, pow, pi

import random

from multiprocessing import Pool

MAX_DEPTH = 5
TINY = 0.00000001

height = float(1000)
width = float(1000)
origin = Vec3(0, 0, 0)

objects = []
lights = []

def multi_thread_trace():
	p = Pool(7)

	params = []
	for i in range(int(width)):
		for j in range(int(height)):
			params.append((i,j))

	return p.map(evaluate_ray, params, 1000)

# def trace():
# 	for i in range(0, int(width)):
# 		for j in range(0, int(height)):
# 			x = -1 + 2*(i/((width)-1))
# 			y = 1 - 2*(j/((height)-1))
# 			z = -1
#
# 			ray = Ray(origin, Vec3(x, y, z))
#
# 			# Check this out for structure.
# 			# http://www.cs.jhu.edu/~cohen/RendTech99/Lectures/Ray_Tracing.bw.pdf
# 			color = ray_point_color(ray)
# 			image.putpixel((i,j), color.get_256_tuple())

def evaluate_ray(pt):
	(i, j) = pt

	x = -1 + 2*(i/((width)-1))
	y = 1 - 2*(j/((height)-1))
	z = -1

	ray = Ray(origin, Vec3(x, y, z))

	return ray_point_color(ray)


def backgroundColor(ray):
	r = 0
	g = 0.2*(1 - ray.destination.y)
	b = 0.1

	return RGBColor(r, g, b)

def intersectedObject(ray):
	ray_hit_object = False
	hit_point = None
	hit_object = None
	distance_to_closest_hit = float("inf")

	# Check this out for structure.
	# http://www.cs.jhu.edu/~cohen/RendTech99/Lectures/Ray_Tracing.bw.pdf
	for obj in objects:
		hit, distance = obj.intersect(ray)
		closer = distance < distance_to_closest_hit

		if hit and closer:
			distance_to_closest_hit = distance

			ray_hit_object = True
			hit_point = ray.origin + ray.destination * distance #A scalar
			hit_object = obj

	if ray_hit_object:
		# (Hit object (bool), hp, ho)
		return (True, hit_point, hit_object, distance_to_closest_hit)
	else:
		return (False, None, None, None)

def ray_point_color(ray, depth=0):
	if depth == MAX_DEPTH:
		return RGBColor(0, 0, 0)

	ray_hit_object, hit_point, hit_object, hit_distance = intersectedObject(ray)

	if ray_hit_object:
		unit_normal = hit_point - hit_object.center
		normal_vector = unit_normal.normal()

		# Calculate shading
		# So take the point on the surface of the sphere
		# then, figure out the distance from it to the center.
		# Then take the normal of that.
		color = hit_object.color
		if hit_object.is_light is False and hit_object.is_mirror is False:
			color = shade(color, hit_object, hit_point, normal_vector)

		if hit_object.specular > 0:
			color = reflect(color, hit_object, hit_point, ray, normal_vector, depth)

		# Calculate shadows
		if hit_object.casts_shadow:
			color = shadow(color, hit_object, hit_point, normal_vector)

		return color

	else:
		return backgroundColor(ray)

def shade(color, hit_object, hit_point, normal):
	lambert_amt = 0
	for light in lights:
		if is_visible(hit_object, light) == False:
			contrib = dot(unit(light.center - hit_point), normal)

			if (contrib > 0):
				lambert_amt += contrib

	lambert_amt = min(1, lambert_amt)

	return color * (lambert_amt * hit_object.lambert)


def shadow(color, hit_object, hit_point, normal):
	SAMPLES = 2000

	sum_r = color.r
	sum_g = color.g
	sum_b = color.b

	for light in lights:
		for _ in range(0, SAMPLES):
			ray = Ray(hit_point + normal * TINY, light.randomPointInSphere())

			ray_hit_object, hp, ho, dis = intersectedObject(ray)

			if ray_hit_object and ho.casts_shadow and ho is not hit_object:
				sum_r += 0
				sum_g += 0
				sum_b += 0
			else:
				sum_r += color.r
				sum_g += color.g
				sum_b += color.b

	return RGBColor(sum_r/SAMPLES, sum_g/SAMPLES, sum_b/SAMPLES)
	# return RGBColor(0, 0, 0)


def reflect(color, obj, initial_hit, ray, normal, depth):
	# https://www.cs.unc.edu/~rademach/xroads-RT/RTarticle.html
	c1 = -dot(ray.destination, normal) #This is a integer!!
	reflection = ray.destination + (2 * normal * c1)

	# c = (2 * dot(ray.destination, normal) * normal)
	# reflection = (ray.destination - c).normal()

	# Like Marbels
	# rand_reflect = Vec3(reflection.x + random.uniform(-1, 1), reflection.y + random.uniform(-1, 1), reflection.z + random.uniform(-1, 1))


	# We only need to do multiple samples if the smudge is high.
	if obj.smudge > 0:
		SAMPLES = 35
	else:
		SAMPLES = 1

	sum_r = 0
	sum_g = 0
	sum_b = 0

	for _ in range(0, SAMPLES):
		dist = obj.smudge

		rand_reflect = Vec3(reflection.x + random.uniform(-dist, dist), reflection.y + random.uniform(-dist, dist), reflection.z + random.uniform(-dist, dist))

		reflection_ray = Ray(initial_hit + normal * TINY, rand_reflect)

		c = ray_point_color(reflection_ray, depth + 1)
		sum_r += c.r
		sum_g += c.g
		sum_b += c.b


	reflect_color = RGBColor(sum_r/SAMPLES, sum_g/SAMPLES, sum_b/SAMPLES)

	if obj.is_mirror:
		return reflect_color
	else:
		return color + (reflect_color * obj.specular)


def is_visible(src, dest):
	hit, pt, obj, dis = intersectedObject(Ray(src.center, unit(dest.center)))

	if hit and obj != src:
		return dis > -0.005
	else:
		return False

def add_objects():
	# Vec3(left right, up down, back forth)

	light_center = Vec3(0, 10, 0)
	light_sphere = Sphere(light_center, 1.3,
						color=RGBColor(1.0, 1.0, 1.0),
						is_light=True)
	objects.append(light_sphere)

	light_center2 = Vec3(-10, 10, 10)
	light_sphere2 = Sphere(light_center2, 1,
						color=RGBColor(1.0, 1.0, 1.0),
						is_light=True)
	# objects.append(light_sphere2)

	sphere1_center = Vec3(0, 0, -3)
	red_center = Sphere(sphere1_center, 1,
						color=RGBColor(1.0, 0.5, 0.5),
						lambert=1) #Red
	objects.append(red_center)

	sphere2_center = Vec3(2, 0, -4)
	green_right = Sphere(sphere2_center, 1,
						color=RGBColor(0.5, 1.0, 0.5),
						lambert=0.8,
						specular=0.5,
						smudge=0.1) #Green
	objects.append(green_right)

	sphere3_center = Vec3(-2, 0, -3)
	blue_left = Sphere(sphere3_center, 1,
						color=RGBColor(1.0, 1.0, 1.0),
						is_mirror=True) #Blue
	objects.append(blue_left)

	sphere4_center = Vec3(0, -100, 0)
	circle4 = Sphere(sphere4_center, 98.5,
						color=RGBColor(1.0, 1.0, 1.0),
						name="Monster",
						lambert=1)
	objects.append(circle4)


	for obj in objects:
		if obj.is_light:
			lights.append(obj)

	print "Objects added"

# def export(file_name):
	# image.save(file_name)


if __name__ == '__main__':
	# Vec3(left right, up down, back forth)


	# tracer = RayTracer(width, height, Vec3(0, 0, 0))
	add_objects()
	colors = multi_thread_trace()

	image = Image.new("RGB", (int(width), int(height)))


	pixels = []
	for _i in range(int(width)):
		for _j in range(int(height)):
			pixels.append((_i, _j))

	for _i in range(len(colors)):
		image.putpixel(pixels[_i], colors[_i].get_256_tuple())

	image.save('out.png')

	# tracer.export("out.png")
