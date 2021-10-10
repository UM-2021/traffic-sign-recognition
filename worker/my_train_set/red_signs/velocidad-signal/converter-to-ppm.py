import os
from PIL import Image


for filename in os.listdir():
	_filename = os.path.splitext(filename)
	if _filename[1] == '.jpeg' or _filename[1] == 'png':
		print(_filename[0])
		with Image.open(filename) as im:
			im.save(_filename[0] + ".ppm")
