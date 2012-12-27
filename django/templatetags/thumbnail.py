"""
A simple drop-in image resizing templatetag.

* Only generates the resized image when first requested.
* Handles maintaining proportions when specifying only a width or a height.
* Makes use of PIL.ImageOps.fit for cropping without reinventing the wheel.

Usage:

Resize to 200px wide maintaining ratio: {% thumbnail path_to_image 200 0 %}
Resize to 200px high maintaining ratio: {% thumbnail path_to_image 0 200 %}
Resize and crop to 200x200px {% thumbnail path_to_image 200 200 %}

Credits:
--------

Stephen McDonald <steve@jupo.org>

License:
--------

Creative Commons Attribution-Share Alike 3.0 License
http://creativecommons.org/licenses/by-sa/3.0/

When attributing this work, you must maintain the Credits
paragraph above.
"""

import os

from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def thumbnail(image_url, width, height):
	"""
	Given the url to an image, resizes the image using the given width and 
	height on the first time it is requested, and returns the url to the new 
	resized image. If width or height are zero then the original ratio is 
	maintained.
	"""
	
	image_url = unicode(image_url)
	#image_path = os.path.join(os.path.normcase(settings.MEDIA_ROOT), os.path.normcase(image_url))
	image_path = os.path.normpath(os.path.normcase(settings.MEDIA_ROOT+image_url))	
	image_dir, image_name = os.path.split(image_path)
	thumb_name = "%s-%sx%s.jpg" % (os.path.splitext(image_name)[0], width, height)
	thumb_path = os.path.join(image_dir, thumb_name)
	thumb_url = "%s/%s" % (os.path.dirname(image_url), thumb_name)

	# abort if thumbnail exists, original image doesn't exist, invalid width or 
	# height are given, or PIL not installed
	if not image_url:
		return ""
	if os.path.exists(thumb_path):
		return thumb_url
	try:
		width = int(width)
		height = int(height)
	except ValueError:
		return image_url
	if not os.path.exists(image_path) or (width == 0 and height == 0):
		return image_url
	try:
		from PIL import Image, ImageOps
	except ImportError:
		return image_url

	# open image, determine ratio if required and resize/crop/save
	image = Image.open(image_path)
	if width == 0:
		width = image.size[0] * height / image.size[1]
	elif height == 0:
		height = image.size[1] * width / image.size[0]
	if image.mode not in ("L", "RGB"):
		image = image.convert("RGB")
	try:
		image = ImageOps.fit(image, (width, height), Image.ANTIALIAS).save(
			thumb_path, "JPEG", quality=100)
	except:
		return image_url
	return thumb_url