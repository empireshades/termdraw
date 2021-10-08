from rich import print
import numpy as np
from PIL import Image
import os
import argparse

parser = argparse.ArgumentParser(description='Term Draw')
parser.add_argument('-f', '--file', help='image file path', required=True)
parser.add_argument('-t', '--text', help='text file to use for characters')
parser.add_argument('-m', '--multiplier', help='multiplier to correct image ratio. Default: 2.25', default=2.25)
args = parser.parse_args()
print(args)
imagepath = args.file

output = ''
termX, termY = os.get_terminal_size()
multiplier = args.multiplier

# Subtract 1 from terminal height
termY -= 1

with Image.open(imagepath) as im:
    imgX, imgY = im.size

    # PIL is 0 based indexing?
    #maprange = lambda z,termX,imgX: int(np.interp(z,[1,termX],[1,imgX]))
    maprange = lambda z,termX,imgX: int(np.interp(z,[1,termX],[0,imgX-1]))

    # Term is wide and image is tall
    if ((termX / multiplier) > termY) & (imgX < imgY):
        resizeY = termY
        # img is tall so need to widen the X to fit terminal char proportions
        resizeX = int(((imgX * termY) / imgY) * multiplier)

    # Term is tall and image is wide
    #elif (termX < (termY / multiplier)) & (imgX > imgY):
    elif (imgX > imgY):
        resizeX = termX
        # imt is wide so need to shorten the Y to fit terminal char proportions
        resizeY = int(((imgY * termX) / imgX) / multiplier)

    #print(f'im.size={im.size}, termX={termX}, termY={termY}, resizeX={resizeX}, resizeY={resizeY}')

    if args.text:
        with open(args.text) as f:
            text = f.read().replace('\n','')
    else:
        text = ['\u2584',]

    textindex = 0
    for line in range(1,resizeY+1):
        for pixel in range(1,resizeX+1):
            img_coords_top = (maprange(pixel,resizeX,imgX), maprange(line,resizeY,imgY))
            img_coords_bottom = (maprange(pixel,resizeX,imgX), maprange(line+0.5,resizeY,imgY))
            get_img_rgb = (im.getpixel(img_coords_top),im.getpixel(img_coords_bottom))
            get_img_rgb = [ str(i).replace(' ','') for i in get_img_rgb ]
            # \u2584 is bottom half block

            print(f'[rgb{get_img_rgb[1]} on rgb{get_img_rgb[0]}]{text[textindex]}',end='')
            if len(text) - 1 == textindex:
                textindex = 0
            else:
                textindex += 1

            #print(f'[rgb{get_img_rgb[1]} on rgb{get_img_rgb[0]}]\u2584',end='')
            #print(f'[rgb{get_img_rgb[1]} on rgb{get_img_rgb[0]}]@',end='')
        print()



