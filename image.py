from PIL import Image,ImageDraw
import numpy as np
import math
import sys

def hexagon_corners(center,size):    
    x = center[0]
    y = center[1]

    w = math.sqrt(3) * size
    h = 2 * size

    return [ 
        (x - w / 2, y - h / 4),
        (x, y - h /2),
        (x + w/2, y - h / 4),
        (x + w/2, y + h/4),
        (x, y + h/2),
        (x - w / 2, y + h/4)
    ]

def rectangle_corners(center, w, h):
    x = center[0]
    y = center[1]

    return [
        (x - w/2, y - h/2),
        (x + w/2 , y - h/2),
        (x +w/2, y + h/2),
        (x -w /2, y + h/2)
    ]


def hexagonify(path, hexagon_size):
    im = Image.open(path)
    I = np.asarray(im)
    draw = ImageDraw.Draw(im)
    
    w = math.sqrt(3) * hexagon_size
    h = 2 * hexagon_size

    #numer of hexagons horizontally and vertically
    num_hor = int(im.size[0] / w) + 2
    num_ver = int(im.size[1] / h * 4 / 3) + 2

    for i in range(0,num_hor*num_ver): 
        column = i % num_hor
        row = i // num_hor
        even = row % 2  # the even rows of hexagons has w/2 offset on the x-axis compared to odd rows.    
        
        p = hexagon_corners((column*w + even * w/2,row*h * 3/4), hexagon_size)

        # compute the average color of the hexagon, use a rectangle approximation.
        raw = rectangle_corners((column*w + even * w/2, row*h * 3/4), w, h)
        r = []
        for points in raw:
            np0 = int(np.clip(points[0], 0, im.size[0]))
            np1 = int(np.clip(points[1], 0, im.size[1]))
            r.append((np0,np1))    
        
        color = np.average(I[r[0][1]:r[3][1],r[0][0]:r[1][0]], axis=(0,1))    
        color = tuple(color.astype(int))    

        draw.polygon(p, fill=color)
    return im


if __name__ == "__main__":
    im = hexagonify(sys.argv[1], int(sys.argv[2]))
    im.show()


