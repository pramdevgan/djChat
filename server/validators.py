import os.path

from PIL import Image
from django.core.exceptions import ValidationError


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 90 or img.height > 90:
                raise ValidationError(
                    f"The maximum allowed dimensions for the image are 90x90 - size of the image you uploaded: {img.size}"
                )


def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpeg", ".png", ".jpg", ".gif"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension")
