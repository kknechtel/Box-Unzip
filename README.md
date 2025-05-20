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


## Deployment with AWS Amplify

This project can be deployed using the Amplify Console's container support. Ensure you have the Amplify CLI installed:

```bash
npm install -g @aws-amplify/cli
```

Initialize Amplify in the project directory and publish:

```bash
amplify init
amplify add hosting
amplify publish
```

Amplify will build the Docker image using the provided `Dockerfile` and host it automatically.

## Running with Docker Locally

You can also run the app using Docker:

```bash
docker build -t box-unzipper .
docker run -p 8000:8000 --env-file .env box-unzipper
```

Then visit `http://localhost:8000/` in your browser.
