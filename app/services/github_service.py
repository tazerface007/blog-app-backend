import requests
import base64

def upload_to_github(filename, content_json, token, repo):
    url = f'https://api.github.com/repos/{repo}/contents/blogs/{filename}.json'
    headers = {'Authorization': f'token {token}'}

    encoded_content = base64.b64encode(content_json.encode()).decode()

    data = {
        'message': f'Add blog: {filename}',
        'content': encoded_content
    }

    return requests.put(url=url, json=data, headers=headers)


