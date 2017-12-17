"""Generate URLs for images on Wikimedia Commons."""
import hashlib


# TODO: Move to configuration file
# this can be changed to allow for the image files to be stored locally
URL_BASE_IMAGES = "https://upload.wikimedia.org/wikipedia/commons/"


def generate_thumbnail_url(filename, size):
    return "{base:s}thumb/{hash:s}{filename:s}" \
           "/{size:d}px-{filename:s}".format(base=URL_BASE_IMAGES,
                                             hash=generate_hash(filename),
                                             filename=normalize(filename),
                                             size=size)


def generate_image_file_url(filename):
    return "{base:s}{hash:s}{filename:s}".format(base=URL_BASE_IMAGES,
                                                 hash=generate_hash(filename),
                                                 filename=normalize(filename))


def generate_image_info_url(filename):
    return "https://commons.wikimedia.org/wiki/File:{:s}".format(
        normalize(filename))


def fetch_licensing_info(filename):
    # waiting for Structured Data on Commons
    raise NotImplementedError


def normalize(filename):
    return filename.replace(" ", "_").capitalize()


def generate_hash(filename):
    md5sum = hashlib.md5(normalize(filename).encode('utf-8')).hexdigest()
    return "{:s}/{:s}/".format(md5sum[0], md5sum[:2])


