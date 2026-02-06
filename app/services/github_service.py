import json
from flask import jsonify
import requests
import base64
import os


from app.db import db
from app.exceptions.missing_token_exception import MissingTokenException



def upload_to_github(filename, content_json, repo):
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    if GITHUB_TOKEN is None:
        raise MissingTokenException()
    url = f'https://api.github.com/repos/{repo}/contents/blogs/{filename}.json'
    headers = {'Authorization': f'Bearer {GITHUB_TOKEN}'}

    encoded_content = base64.b64encode(content_json.encode()).decode()

    data = {
        'message': f'Add blog: {filename}',
        'content': encoded_content
    }

    return requests.put(url=url, json=data, headers=headers)


def create_blog(filename, content_json, repo):
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    if GITHUB_TOKEN is None:
        raise MissingTokenException()
    URL = f'https://api.github.com/repos/{repo}/data/blogs/{filename}.json'
    
    json_string = json.dumps(content_json)

    encoded_content = base64.b64encode(json_string.encode()).decode()

    payload = {
        "message": f'Feat: create blog post {filename}.json',
        "content": encoded_content,
        "branch": "main"
    }

    headers = {'Authnorization': f'Bearer {GITHUB_TOKEN}', 'Accept': 'application/vnd.github.v3+json'}

    gh_response = requests.put(url=URL,json=payload, headers=headers)

    try:
        if gh_response.status_code not in [201, 200]:
            # db.session.delete(new_metadata) 
            db.session.commit()
            return jsonify({"error": "GitHub Upload Failed", "details": gh_response.json()}, 500)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f'{str(e)}'}), 500



def update_blog(filename, content_json, sha, repo):
    # 1. Token Check
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise MissingTokenException()

    # 2. URL Setup (Added /contents/ which is required by GitHub API)
    url = f'https://api.github.com/repos/{repo}/contents/data/blogs/{filename}.json'
    
    # 3. Encoding
    json_string = json.dumps(content_json)
    encoded_content = base64.b64encode(json_string.encode()).decode()

    # 4. Payload
    payload = {
        "message": f'Feat: Update blog post {filename}.json',
        "content": encoded_content,
        "sha": sha,
        "branch": "main"
    }

    # 5. Headers (Fixed Typo)
    headers = {
        'Authorization': f'Bearer {token}', 
        'Accept': 'application/vnd.github.v3+json'
    }

    # 6. Execution
    try:
        gh_response = requests.put(url=url, json=payload, headers=headers, timeout=10)
        
        # Check if it failed
        if gh_response.status_code not in [200, 201]:
            # Log the error for internal debugging
            print(f"GitHub Error: {gh_response.json()}")
            return False, gh_response.json()

        return True, gh_response.json()

    except requests.exceptions.RequestException as e:
        db.session.rollback()
        return False, str(e)
