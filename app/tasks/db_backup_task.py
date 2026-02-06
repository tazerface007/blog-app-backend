from app.utils.task_scheduler import scheduler
from app.db.models.blogmetadata import BlogMetadata 
import json
import os
from datetime import datetime

# Change 'hours=1' to 'seconds=5' for testing
@scheduler.task('interval', id='backup_jobs', seconds=5)
def backup_db_to_json():
    with scheduler.app.app_context():
        # Querying all data might be slow if the table is large
        data = BlogMetadata.query.all()
        serialized_data = [item.to_dict() for item in data]

        backup_path = '/data/blogs/fallback.json'
        
        try:
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)

            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(serialized_data, f, indent=4)
            
            print(f'Backup complete at {datetime.now()}')
        except Exception as e:
            print(e)