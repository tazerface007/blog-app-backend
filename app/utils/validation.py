# Author: Deepak Suryawanshi

import os

import requests


def trigger_revalidate(slug):
    token = os.getenv("REVALIDATE_SECRET")
    website_url = os.getenv("REVALIDATE_SECRET")
    url = f'https://{website_url}/api/revalidate?path=/blog/{slug}&secret={token}'
    requests.post(url)