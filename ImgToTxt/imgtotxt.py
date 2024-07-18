import argparse

from PIL import ImageGrab, Image
from pytesseract import image_to_string 

def process_to_string(img):
	txt = image_to_string(img)
	print(txt)

parser = argparse.ArgumentParser(
                    prog='ImgToTxt',
                    description='Converting image to text',
                    epilog='By default app process an image from clipboard or use <filename> param to load from a file')
           
parser.add_argument('filename', nargs='?', default="") 

args = parser.parse_args()

if args.filename == "":
	img = ImageGrab.grabclipboard()

	if img is None:
		print("<No image in the clipboard! Please note you can use <filename> param to load from a file>")
	else:
		img.save('image.png','PNG')
		process_to_string(img)
else:
	img = Image.open(args.filename)
	process_to_string(img)

