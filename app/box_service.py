import logging
from .auth import get_client

logger = logging.getLogger(__name__)


def get_zip_files(folder_id='0'):
    """Get all ZIP files from the specified Box folder"""
    client = get_client()
    if not client:
        return None

    try:
        items = client.folder(folder_id=folder_id).get_items()
        zip_files = [
            {
                'id': item.id,
                'name': item.name,
                'size': item.size,
                'modified_at': item.modified_at
            }
            for item in items if item.name.lower().endswith('.zip')
        ]
        return zip_files
    except Exception as e:
        logger.error(f"Error getting ZIP files: {e}")
        return None


def download_file(file_id):
    """Download file content from Box"""
    client = get_client()
    if not client:
        return None

    try:
        return client.file(file_id).content()
    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {e}")
        return None

