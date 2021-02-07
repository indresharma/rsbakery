from PIL import Image
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


def crop_and_save(image_path, height, width):
    """image should be path"""
    img = Image.open(image_path)
    w, h = img.size

    if w == width and h == height:
        return img

    if width < w:
        ratio = h/w
        nw, nh = (width, width*ratio)
        if nh < height:
            nw, nh = (height/ratio, height)

        size = (nw, nh)
        img.thumbnail(size, Image.ANTIALIAS)
        w, h = img.size

    left = (w - width)/2
    right = (w + width)/2
    top = (h - height)/2
    bottom = (h + height)/2
    img = img.crop((left, top, right, bottom)) 
    return img


class CustomAuthMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = []

    
