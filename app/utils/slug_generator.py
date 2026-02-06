import re
import secrets
import string


def generate_slug(title: str, length=6):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]','',slug)

    slug = re.sub('r[\s-]+','-',slug).strip('-')

    stop_words = {'a', 'an', 'the', 'and', 'in', 'of', 'for', 'with', 'on', 'oh', 'at'}

    slug = '-'.join([w for w in slug.split('-') if w not in stop_words])
    suffix = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(length))
    return f'{slug}-{suffix}'