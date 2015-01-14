f = open('out.ppm', 'w')
f.write('P3\n')
f.write('512 512\n')
f.write('255\n')

color = 0

for y in range(0,512):
    # The gradient loop
    for x in range(0, 256):
        f.write('{0} {0} {0}\t'.format(color))
    # Increment the color value by one after writing this row.
    if (y%2 == 0):
        color+=1

    # The stripe loop
    for x in range(256, 512):
        # Alternate between white and black
        if (y%2 == 0):
            f.write('0 0 0\t')
        else:
            f.write('255 255 255\t')

    # New line in the file
    f.write('\n')
