# Box Unzipper

This application allows you to authenticate with Box.com, select multiple ZIP files and extract them directly in the browser. It is built with Flask and the Box SDK.

## Setup

1. Create a `.env` file with your Box credentials:
   ```
   BOX_CLIENT_ID=your_client_id
   BOX_CLIENT_SECRET=your_client_secret
   BOX_REDIRECT_URI=http://localhost:5000/callback
   SECRET_KEY=change-this-secret
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python run.py
   ```

