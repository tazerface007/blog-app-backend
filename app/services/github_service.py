import json
from flask import jsonify
import requests
import base64

from app.db import db

def upload_to_github(filename, content_json, token, repo):
    url = f'https://api.github.com/repos/{repo}/contents/blogs/{filename}.json'
    headers = {'Authorization': f'token {token}'}

    encoded_content = base64.b64encode(content_json.encode()).decode()

    data = {
        'message': f'Add blog: {filename}',
        'content': encoded_content
    }

    return requests.put(url=url, json=data, headers=headers)


def create_blog(filename, content_json, token, repo):
    URL = f'https://api.github.com/repos/{repo}/data/blogs/{filename}.json'
    
    json_string = json.dumps(content_json)

    encoded_content = base64.b64encode(json_string.encode()).decode()

    payload = {
        "message": f'Feat: create blog post {filename}.json',
        "content": encoded_content,
        "branch": "main"
    }

    headers = {'Authnorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

    gh_response = requests.put(url=URL,json=payload, headers=headers)

    try:
        if gh_response.status_code not in [201, 200]:
            db.session.delete(new_metadata) 
            db.session.commit()
            return jsonify({"error": "GitHub Upload Failed", "details": gh_response.json()}, 500)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f'{str(e)}'}), 500



