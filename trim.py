from PIL import Image, ImageChops
import glob

for filename in ("report/page-3.png", "report/page-4.png", "report/page-5.png", "report/page-6.png"):
    im = Image.open(filename)
    bg = Image.new(im.mode, im.size, (255,255,255))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        im.crop(bbox).save(filename.replace('.png', '_crop.png'))
