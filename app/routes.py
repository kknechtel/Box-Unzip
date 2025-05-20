from flask import Blueprint, redirect, render_template, session, request, url_for, jsonify, send_file, abort
import os
import logging
from . import auth, box_service, unzip_service

bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


@bp.route('/')
def index():
    """Home page - redirects to login or file list"""
    if 'access_token' not in session:
        return render_template('login.html')
    return redirect(url_for('main.list_files'))


@bp.route('/login')
def login():
    """Initiate Box OAuth2 login flow"""
    auth_url = auth.get_authorization_url()
    return redirect(auth_url)


@bp.route('/callback')
def callback():
    """Handle Box OAuth2 callback"""
    # Verify state parameter to prevent CSRF
    if request.args.get('state') != session.get('oauth2_csrf_token'):
        abort(400, 'CSRF token mismatch')

    auth_code = request.args.get('code')
    if not auth_code:
        abort(400, 'Missing authorization code')

    auth.authenticate(auth_code)
    return redirect(url_for('main.list_files'))


@bp.route('/files')
def list_files():
    """List ZIP files from Box"""
    if 'access_token' not in session:
        return redirect(url_for('main.index'))

    zip_files = box_service.get_zip_files()
    if zip_files is None:
        # Error getting files, redirect to login
        session.clear()
        return redirect(url_for('main.index'))

    return render_template('files.html', files=zip_files)


@bp.route('/extract', methods=['POST'])
def extract_files():
    """Extract selected ZIP files"""
    if 'access_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    file_ids = request.json.get('file_ids', [])
    if not file_ids:
        return jsonify({'error': 'No files selected'}), 400

    results = []
    for file_id in file_ids:
        # Get file info first
        client = auth.get_client()
        try:
            file_info = client.file(file_id).get()
            file_name = file_info.name

            # Download and extract
            file_content = box_service.download_file(file_id)
            if not file_content:
                results.append({
                    'file_id': file_id,
                    'name': file_name,
                    'success': False,
                    'error': 'Failed to download file'
                })
                continue

            extraction = unzip_service.extract_zip(file_content, file_name)
            if not extraction:
                results.append({
                    'file_id': file_id,
                    'name': file_name,
                    'success': False,
                    'error': 'Failed to extract file'
                })
                continue

            results.append({
                'file_id': file_id,
                'name': file_name,
                'success': True,
                'extract_path': extraction['extract_path'],
                'files': extraction['files']
            })

        except Exception as e:
            logger.error(f"Error processing file {file_id}: {e}")
            results.append({
                'file_id': file_id,
                'success': False,
                'error': str(e)
            })

    return jsonify({'results': results})


@bp.route('/download/<path:extract_path>/<path:file_path>')
def download_file(extract_path, file_path):
    """Download extracted file"""
    if 'access_token' not in session:
        return redirect(url_for('main.index'))

    # Security check - ensure the path is within temp directory
    base_path = os.path.abspath(os.path.join(os.getcwd(), extract_path))
    requested_path = os.path.abspath(os.path.join(base_path, file_path))

    if not requested_path.startswith(base_path):
        abort(403, "Access denied")

    if not os.path.exists(requested_path):
        abort(404, "File not found")

    return send_file(requested_path, as_attachment=True)


@bp.route('/logout')
def logout():
    """Clear session and log out"""
    session.clear()
    return redirect(url_for('main.index'))

