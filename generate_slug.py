import unicodedata
import re


def generate_slug(long_string):
    slug = unicodedata.normalize("NFKD", long_string)
    slug = re.sub(r"[^\w]+", " ", slug)
    slug = "-".join(slug.lower().strip().split())
    slug = slug.encode("ascii", "ignore").decode("ascii")
    return slug

