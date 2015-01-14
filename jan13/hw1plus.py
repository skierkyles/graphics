f = open('outplus.ppm', 'w')
f.write('P3\n')
f.write('512 64\n')
f.write('255\n')

color = 0

ticker = 0

colors = ['255 0 0', '0 255 0', '0 0 255', '255 255 0', '255 165 0', '0 255 255', '128 0 128', '128 128 128']
color_index = -1
current_color = colors[color_index]

for x in range(0, 64):
    for y in range(0,512):
        if (y % 64 == 0):
            color_index += 1
        if color_index == len(colors):
            color_index = 0
        current_color = colors[color_index]
        f.write(current_color + '\t')

    f.write('\n')
