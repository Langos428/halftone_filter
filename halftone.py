from PIL import Image, ImageDraw, ImageOps
from math import sqrt

SCALE = 5         # velkosť štvorčeka v gride, ovplyvňuje downscaling
MULTIPLY = 2      # faktor, koľkokrát väčší bude výstup oproti vstupu

filename = "grayscale-rose.jpg"

original = Image.open(filename)

def getluminance(x: int, y: int, px) -> float:
    red, green, blue = px[x, y]
    return (red + green + blue)/256/3


def halftonify(img: Image, scale, multiply, color1: str = "#FFFFFF", color2: str = "#000000"):

    downscaled = ImageOps.scale(img, 1/scale, Image.Resampling.BOX)

    factor = multiply*10
    new_width, new_heigth = int(img.size[0]*factor), int(img.size[1]*factor)
    new = Image.new("RGB", (new_width, new_heigth), color1)

    d = ImageDraw.Draw(new)
    px = downscaled.load()

    for x in range(downscaled.size[0]):
        for y in range(downscaled.size[1]):

            lum = getluminance(x, y, px)
            side = scale*factor     # strana štvorca jedného pixelu

            radius = side*sqrt(2)*(1-lum)*0.5
            pos_x = (x+0.5)*side
            pos_y = (y+0.5)*side

            d.circle((pos_x, pos_y), radius, color2)

    return ImageOps.scale(new, 1/(factor/multiply), Image.Resampling.LANCZOS)


name, format = filename.split(".")

halftonify(original, SCALE, MULTIPLY, "#FDF1D3", "#280306").save(f"{name}_dotted.{format}")

