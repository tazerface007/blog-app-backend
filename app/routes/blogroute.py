import base64
import json
import os
from flask import Blueprint, request, jsonify
import requests

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

blog_admin_bp = Blueprint('admin_blog', __name__, url_prefix='/admin/blog')

GITHUB_API_URL_BLOG = "https://api.github.com/repos/tazerface007/portfolio/contents/data/blogs/{slug}.json"

@blog_bp.route('/', methods=['GET'])
def blog_home():
    return jsonify({"message": "Welcome to the Blog Route!"})


@blog_admin_bp.route('/create', methods=['POST', 'OPTIONS'])
def create_blog():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.json
    title = data.get('title')
    description = data.get('description')
    content_blocks = data.get('content')
    from app.utils.slug_generator import generate_slug
    slug = generate_slug(title)

    # 1. Update the SQLite Metadata
    from app.db.models.blogmetadata import BlogMetadata
    new_metadata = BlogMetadata(
        title=title,
        description=description,
        slug=slug,
        github_path=f'/data/blogs/{slug}.json',
        is_published=True
    )
    from app.db import db
    try:
        db.session.add(new_metadata)
        db.session.commit()


        repo = os.getenv("GITHUB_REPO")
        url = GITHUB_API_URL_BLOG.format(repo=repo, slug=slug)

        # GitHub requires Base64 encoded data
        import json
        json_string = json.dumps(content_blocks)
        encoded_content = base64.b64encode(json_string.encode()).decode()

        payload = {
            "message": f'Feat: create blog post {slug}',
            "content": encoded_content,
            "branch": "main"
        }

        headers = {
            "Authorization": f'Bearer {os.getenv('GITHUB_TOKEN')}',
            "Accept": "application/vnd.github.v3+json"
        }

        gh_response = requests.put(url, json=payload, headers=headers)

        if gh_response.status_code not in [201, 200]:
            db.session.delete(new_metadata) 
            db.session.commit()
            return jsonify({"error": "GitHub Upload Failed", "details": gh_response.json()}, 500)
        
        return jsonify({
            "status": "success",
            "message": f"Blog '{title}' created and synced to GitHub",
            "slug": slug
        }), 201
    

    except Exception as e:
        db.session.rollback()
        print("!!! PYTHON ERROR !!!:", str(e)) # LOOK AT YOUR TERMINAL FOR THIS
        import traceback
        traceback.print_exc()
        return jsonify({"error": f'{str(e)}'}), 500
    

@blog_admin_bp.route('/update/<int:id>', methods=['PUT'])
def update_blog(id):
    from app.db.models.blogmetadata import BlogMetadata
    blog = BlogMetadata.query.get_or_404(id)
    data = request.json

    new_content = data.get('content')
    new_title = data.get('title', blog.title)

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO")
    url = f'https://api.github.com/repos/{repo}/contents/{blog.github_path}'
    headers = {"Authorization": f'token {token}'}

    try:
        # 1. GET the current 
        get_res = requests.get(url, headers=headers)

        if get_res.status_code != 200:
            return jsonify({"error": "Could not find file on GitHub"}), 404
        
        current_sha = get_res.json().get('sha')

        # 2. Prepare the Update Payload
        import json

        json_string = json.dumps(new_content)
        encoded_content = base64.b64encode(json_string.encode()).decode()

        payload = {
            "message": f'Update blog: {blog.slug}',
            "content": encoded_content,
            "sha": current_sha,
            "branch": "main"
        }


        # 3. PUT the updates to GitHub

        put_res = requests.put(url, json=payload, headers=headers)

        if put_res.status_code == 200:
            blog.title = new_title
            # db.session.commit() #TODO
        from app.utils.validation import trigger_revalidate
        trigger_revalidate(f'/blog/{blog.slug}')
        return jsonify({"message": "Updated successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": f'{str(e)}'}), 500

@blog_bp.route('/getall', methods=['GET'])
def get_blogs():
    from app.db import db
    from app.db.models.blogmetadata import BlogMetadata
    try:
        blogs = BlogMetadata.query.all()
        output = []
        for blog in blogs:
            output.append({
                "id": blog.id,
                "title": blog.title,
                "description":blog.description,
                "slug": blog.slug
            })
        print(output)
        return jsonify(output)
    except Exception as e:
        print('Error', e)
        return jsonify({"error": "error occured"}), 500

@blog_bp.route('/get/<string:slug>', methods=['GET'])
def get_blog(slug):
    API_ROUTE = f"https://api.github.com/repos/tazerface007/portfolio/contents/data/blogs/{slug}.json?ref=main"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"
    }

    response = requests.get(API_ROUTE, headers=headers)

    if response.status_code != 200:
        return jsonify({
            "error": "Failed to fetch blog",
            "status": response.status_code,
            "details": response.json()
        }), response.status_code

    data = response.json()

    decoded = base64.b64decode(data["content"]).decode("utf-8")
    parsed = json.loads(decoded)

    return jsonify({
        "slug": slug,
        "content": parsed
    })

