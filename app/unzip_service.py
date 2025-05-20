import os
import zipfile
import shutil
import io
import uuid
import logging
from datetime import datetime
from flask import current_app

logger = logging.getLogger(__name__)


def extract_zip(file_content, original_filename):
    """Extract ZIP file content to a temporary directory"""
    if not file_content:
        return None

    # Create unique folder for this extraction
    extract_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    extract_path = os.path.join(
        current_app.config['TEMP_FOLDER'],
        f"{timestamp}_{extract_id}"
    )

    try:
        os.makedirs(extract_path, exist_ok=True)

        # Store extraction metadata
        with open(os.path.join(extract_path, '.metadata'), 'w') as f:
            f.write(f"Original file: {original_filename}\n")
            f.write(f"Extracted at: {datetime.now().isoformat()}\n")

        # Extract the zip file
        with zipfile.ZipFile(io.BytesIO(file_content)) as zip_ref:
            zip_ref.extractall(extract_path)

        # Get list of extracted files
        files = []
        for root, dirs, filenames in os.walk(extract_path):
            if os.path.basename(root) == '__MACOSX':  # Skip macOS metadata
                continue
            for filename in filenames:
                if filename == '.metadata':
                    continue
                rel_path = os.path.relpath(os.path.join(root, filename), extract_path)
                files.append({
                    'name': os.path.basename(filename),
                    'path': rel_path,
                    'size': os.path.getsize(os.path.join(root, filename))
                })

        return {
            'extract_path': extract_path,
            'files': files
        }
    except Exception as e:
        logger.error(f"Error extracting ZIP file: {e}")
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)
        return None


def cleanup_old_extractions():
    """Remove old extracted files based on retention policy"""
    # Implementation omitted for brevity
    pass

