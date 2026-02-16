# SBS Bot Render Deployment

## 🚀 How to Deploy on Render via GitHub

This project is set up to deploy your existing `app.py` bot to Render easily, with added API monitoring and stability.

### Step 1: Push to GitHub
1.  Initialize a git repository if you haven't already:
    ```bash
    git init
    git add .
    git commit -m "Initial commit for Render deployment"
    ```
2.  Create a new repository on GitHub.
3.  Push your code:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    git push -u origin master
    ```

### Step 2: Deploy on Render
1.  Go to [Render Dashboard](https://dashboard.render.com/).
2.  Click **"New +"** and select **"Web Service"**.
3.  Connect your GitHub repository.
4.  Render will automatically detect the settings from `render.yaml`.
5.  Click **"Create Web Service"**.

### 🎉 Done!
Your bot will be live. Render will give you a URL (e.g., `https://boom-bot-tele.onrender.com`).
- **Dashboard**: `https://boom-bot-tele.onrender.com`
- **Stats**: `https://boom-bot-tele.onrender.com/stats`
- **Health**: `https://boom-bot-tele.onrender.com/health`

### ⚠️ Important Note on Database
Render's filesystem is ephemeral (temporary). If the bot restarts, the `sbs_pro_database.json` file will reset to its initial state.
To persist data, you would normally need a persistent disk (paid feature) or an external database (MongoDB/PostgreSQL).
Since you requested **no code changes** to `app.py`, the bot will use the local file, which means **data will reset on each deployment/restart**.
