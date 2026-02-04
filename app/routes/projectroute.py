import base64
from flask import Blueprint, request, jsonify
import requests
import json
import os


project_bp = Blueprint('project',__name__, url_prefix='/project')


@project_bp.get('/getall')
def get_projects():
    API_URL = 'https://api.github.com/repos/tazerface007/portfolio/contents/data/project/projectData.json?ref=main'
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"
    }
    response = requests.get(API_URL, headers=headers)
    data = response.json()

    decoded = base64.b64decode(data["content"]).decode("utf-8")
    parsed = json.loads(decoded)
    return jsonify(parsed)

    