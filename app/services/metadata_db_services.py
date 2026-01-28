from app.db import db

def create_metadata_entry(title:str, description:str, slug: str, github_path:str):
    from app.db.models.blogmetadata import BlogMetadata
    new_metadata = BlogMetadata(
        title=title,
        description=description,
        slug = slug,
        github_path=github_path,
        is_published=True
    )
    try:
        db.session.add(new_metadata)
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def update_metadata_entry(id, title:str=None, description:str = None ):
    # get blog entry
    from app.db.models.blogmetadata import BlogMetadata
    try:
        blog = BlogMetadata.query.get_or_404(id)
        if title !=None:
            blog.title = title
        elif description !=None:
            blog.description =description
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def delete_metadata_entry(id):
    # get blog entry
    from app.db.models.blogmetadata import BlogMetadata
    try:
        blog = BlogMetadata.query.get_or_404(id)
        db.session.delete(blog)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    
def get_all_metadata_entry():
    from app.db.models.blogmetadata import BlogMetadata
    try:
        blogs = BlogMetadata.query.all()
        return blogs
    except Exception as e:
        return None
    