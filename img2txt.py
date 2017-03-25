from PIL import Image


def generate_grayscale_for_image(pixels, width, height, bgcolor):

    # grayscale
    color = "MNHQ$OC?7>!:-;. "

    string = ""
    # first go through the height,  otherwise will rotate
    for h in range(height):
        for w in range(width):

            rgba = pixels[w, h]

            # If partial transparency and we have a bgcolor, combine with bg
            # color
            if rgba[3] != 255 and bgcolor is not None:
                rgba = alpha_blend(rgba, bgcolor)

            # Throw away any alpha (either because bgcolor was partially
            # transparent or had no bg color)
            # Could make a case to choose character to draw based on alpha but
            # not going to do that now...
            rgb = rgba[:3]

            string += color[int(sum(rgb) / 3.0 / 256.0 * 16)]

        string += "\n"

    return string


def load_and_resize_image(img, antialias, maxLen, aspectRatio):

    if aspectRatio is None:
        aspectRatio = 1.0

    img = Image.open(img)

    # force image to RGBA - deals with palettized images (e.g. gif) etc.
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # need to change the size of the image?
    if maxLen is not None or aspectRatio != 1.0:

        native_width, native_height = img.size

        new_width = native_width
        new_height = native_height

        # First apply aspect ratio change (if any) - just need to adjust one axis
        # so we'll do the height.
        if aspectRatio != 1.0:
            new_height = int(float(aspectRatio) * new_height)

        # Now isotropically resize up or down (preserving aspect ratio) such that
        # longer side of image is maxLen
        if maxLen is not None:
            rate = float(maxLen) / max(new_width, new_height)
            new_width = int(rate * new_width)
            new_height = int(rate * new_height)

        if native_width != new_width or native_height != new_height:
            img = img.resize((new_width, new_height), Image.ANTIALIAS if antialias else Image.NEAREST)

    return img


def alpha_blend(src, dst):
    # Does not assume that dst is fully opaque
    # See https://en.wikipedia.org/wiki/Alpha_compositing - section on "Alpha Blending"
    src_multiplier = (src[3] / 255.0)
    dst_multiplier = (dst[3] / 255.0) * (1 - src_multiplier)
    result_alpha = src_multiplier + dst_multiplier
    if result_alpha == 0:       # special case to prevent div by zero below
        return (0, 0, 0, 0)
    else:
        return (
            int(((src[0] * src_multiplier) + (dst[0] * dst_multiplier)) / result_alpha),
            int(((src[1] * src_multiplier) + (dst[1] * dst_multiplier)) / result_alpha),
            int(((src[2] * src_multiplier) + (dst[2] * dst_multiplier)) / result_alpha),
            int(result_alpha * 255)
        )


def process_image(image, antialias, maxLen, aspectRatio):
    image = load_and_resize_image(image, antialias, maxLen, aspectRatio)
    pixel = image.load()
    width, height = image.size
    bgcolor = None
    string = generate_grayscale_for_image(pixel, width, height, bgcolor)
    return string
