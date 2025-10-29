# AI Campus Admin Backend - Hugging Face Deployment Guide

## 🚀 Quick Deploy to Hugging Face Spaces

This guide will help you deploy the AI Campus Admin backend to Hugging Face Spaces using Docker.

## Prerequisites

1. **Hugging Face Account**: Create one at [huggingface.co](https://huggingface.co/)
2. **OpenAI API Key**: Get from [platform.openai.com](https://platform.openai.com/)
3. **MongoDB Database**: 
   - [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (recommended for production)
   - Or any MongoDB instance accessible via URL

## Step-by-Step Deployment

### 1. Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in the details:
   - **Name**: `ai-campus-admin-backend` (or your preferred name)
   - **License**: Choose appropriate license (e.g., MIT)
   - **Space SDK**: Select **Docker**
   - **Visibility**: Choose Public or Private
4. Click **"Create Space"**

### 2. Upload Files to Space

You need to upload these files from the `backend` folder:

#### Required Files:
```
backend/
├── Dockerfile                 ✅ (Created)
├── requirements.txt          ✅ (Created)
├── main.py                   ✅ (Existing)
├── settings.py               ✅ (Existing)
├── db.py                     ✅ (Existing)
├── schemas.py                ✅ (Existing)
├── __init__.py               ✅ (Existing)
├── models/                   ✅ (Folder)
│   ├── __init__.py
│   ├── student.py
│   └── user.py
├── routers/                  ✅ (Folder)
│   ├── __init__.py
│   ├── auth.py
│   ├── chat.py
│   ├── students.py
│   └── analytics.py
├── services/                 ✅ (Folder)
│   ├── __init__.py
│   ├── auth.py
│   ├── chat_history.py
│   ├── students.py
│   ├── users.py
│   └── voice.py
├── agent/                    ✅ (Folder)
│   ├── __init__.py
│   ├── graph.py
│   ├── ragagent.py
│   └── tools.py
└── uaf_data/                 ✅ (Folder - Optional)
    ├── ragagent.py
    └── uaf_scraped_data.json
```

#### Upload Methods:

**Option A: Git Upload (Recommended)**
```bash
# Clone your new space
git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-campus-admin-backend
cd ai-campus-admin-backend

# Copy all backend files
cp -r /path/to/your/backend/* .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

**Option B: Web Interface**
1. On your Space page, click **"Files"** tab
2. Click **"Add file"** → **"Upload files"**
3. Drag and drop all files/folders from backend directory
4. Click **"Commit changes to main"**

### 3. Configure Environment Variables (Secrets)

On your Space page:

1. Click **"Settings"** tab
2. Scroll to **"Repository secrets"**
3. Add the following secrets:

```env
# Required Secrets
OPENAI_API_KEY=sk-your-openai-api-key-here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
JWT_SECRET_KEY=your-super-secret-jwt-key-min-32-chars
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Optional Secrets (if using voice features)
ELEVENLABS_API_KEY=your-elevenlabs-api-key

# SMTP Configuration (if using email)
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Important**: 
- Click **"Add secret"** for each one
- Never commit actual secrets to the repository
- Use strong, unique values for JWT_SECRET_KEY

### 4. Create .env Template (Optional)

Create a `.env.example` in your Space (already exists in backend):

```env
# Copy this to repository secrets in Hugging Face Spaces

# AI Services
OPENAI_API_KEY=your-key-here
ELEVENLABS_API_KEY=your-key-here

# Database
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DB=ai_campus

# Security
JWT_SECRET_KEY=your-secret-key-min-32-characters
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (Update with your frontend URL)
ALLOW_ORIGINS=https://your-frontend-domain.com,http://localhost:5173

# Environment
ENVIRONMENT=production
```

### 5. Update CORS Settings

Before deploying, update `settings.py` to include your Hugging Face Space URL:

```python
# In settings.py, update allow_origins:
allow_origins: str = "https://your-space-name.hf.space,http://localhost:5173"
```

Or add it as a secret:
```
ALLOW_ORIGINS=https://your-space-name.hf.space,http://localhost:5173
```

### 6. Wait for Build

1. Hugging Face will automatically build your Docker image
2. Check the **"Logs"** tab to monitor progress
3. Build typically takes 5-10 minutes
4. Once complete, your API will be available at:
   ```
   https://YOUR_USERNAME-ai-campus-admin-backend.hf.space
   ```

### 7. Test Your Deployment

Test the health endpoint:
```bash
curl https://YOUR_USERNAME-ai-campus-admin-backend.hf.space/health
```

Expected response:
```json
{"status": "ok"}
```

Test the API documentation:
```
https://YOUR_USERNAME-ai-campus-admin-backend.hf.space/docs
```

## MongoDB Atlas Setup (Recommended)

### Why MongoDB Atlas?
- Free tier available (512MB storage)
- Cloud-hosted, no server management
- Automatic backups
- High availability

### Setup Steps:

1. **Create Account**: Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)

2. **Create Cluster**:
   - Choose **FREE** tier (M0)
   - Select a region close to your users
   - Click **"Create Cluster"**

3. **Database Access**:
   - Go to **"Database Access"**
   - Click **"Add New Database User"**
   - Create username and password
   - Grant **"Read and write to any database"**

4. **Network Access**:
   - Go to **"Network Access"**
   - Click **"Add IP Address"**
   - Add **"0.0.0.0/0"** (Allow from anywhere)
   - Or add Hugging Face IPs if known

5. **Get Connection String**:
   - Go to **"Database"** → **"Connect"**
   - Choose **"Connect your application"**
   - Copy the connection string
   - Replace `<password>` with your database password
   - Example: `mongodb+srv://user:pass@cluster.mongodb.net/`

6. **Create Database**:
   - Click **"Browse Collections"**
   - Click **"Add My Own Data"**
   - Database name: `ai_campus`
   - Collection name: `users`

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for AI features | `sk-...` |
| `MONGODB_URI` | ✅ Yes | MongoDB connection string | `mongodb+srv://...` |
| `MONGO_URI` | ✅ Yes | Alias for MONGODB_URI | `mongodb+srv://...` |
| `JWT_SECRET_KEY` | ✅ Yes | Secret key for JWT tokens (min 32 chars) | `your-secret-key-here` |
| `MONGODB_DB` | No | Database name (default: ai_campus) | `ai_campus` |
| `ENVIRONMENT` | No | Environment (default: development) | `production` |
| `ALLOW_ORIGINS` | No | CORS allowed origins | `https://frontend.com` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | No | Token expiry (default: 30) | `30` |
| `ELEVENLABS_API_KEY` | No | For voice features | `your-key` |
| `SMTP_USERNAME` | No | For email notifications | `email@gmail.com` |
| `SMTP_PASSWORD` | No | Email app password | `your-app-pass` |

## Troubleshooting

### Build Fails

**Check Logs**:
1. Go to **"Logs"** tab in your Space
2. Look for error messages
3. Common issues:
   - Missing dependencies in requirements.txt
   - Python version mismatch
   - File not found errors

**Solutions**:
- Ensure all files are uploaded
- Check Dockerfile syntax
- Verify requirements.txt has all dependencies

### Application Won't Start

**Check Environment Variables**:
- Ensure all required secrets are set
- Verify MongoDB connection string is correct
- Test MongoDB connection separately

**Check Logs**:
```
# Look for startup errors in Space logs
# Common issues:
- MongoDB connection timeout
- Missing OPENAI_API_KEY
- Invalid JWT_SECRET_KEY
```

### MongoDB Connection Issues

**Test Connection**:
```python
# Create a test script
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test():
    client = AsyncIOMotorClient("your-mongodb-uri")
    db = client.ai_campus
    result = await db.command("ping")
    print("Connected:", result)

asyncio.run(test())
```

**Common Fixes**:
- Check IP whitelist in MongoDB Atlas
- Verify username/password are correct
- Ensure connection string format is correct
- Check if database exists

### CORS Errors

**Update CORS Settings**:
Add your frontend URL to `ALLOW_ORIGINS` secret:
```
ALLOW_ORIGINS=https://your-frontend.com,https://another-domain.com
```

Or update `settings.py`:
```python
allow_origins: str = "https://your-frontend.com,*"
```

### API Endpoints Not Working

**Check**:
1. Health endpoint: `/health`
2. API docs: `/docs`
3. Verify all routers are included in `main.py`

## Updating Your Deployment

### Update Code:
```bash
# Make changes locally
# Then push to your Space
git add .
git commit -m "Update: description of changes"
git push
```

### Update Environment Variables:
1. Go to Space **"Settings"**
2. Update secrets
3. Space will automatically rebuild

## Production Checklist

Before going live:

- [ ] Set `ENVIRONMENT=production` in secrets
- [ ] Use strong JWT_SECRET_KEY (min 32 characters, random)
- [ ] Set up MongoDB Atlas (not local MongoDB)
- [ ] Configure proper CORS origins (not `*`)
- [ ] Enable MongoDB authentication
- [ ] Set up database backups
- [ ] Monitor API usage and logs
- [ ] Set up error alerting
- [ ] Document API endpoints
- [ ] Test all endpoints thoroughly
- [ ] Set up rate limiting (if needed)
- [ ] Configure proper logging level

## Cost Considerations

### Hugging Face Spaces
- **Free Tier**: Basic CPU instances
- **Upgraded**: GPU instances for faster AI processing
- **Pricing**: Check [huggingface.co/pricing](https://huggingface.co/pricing)

### MongoDB Atlas
- **Free Tier**: 512MB storage (suitable for testing)
- **Paid Plans**: Start at $9/month for more storage
- **Pricing**: Check [mongodb.com/pricing](https://www.mongodb.com/pricing)

### OpenAI API
- **Pay-per-use**: Charged based on tokens used
- **GPT-4o-mini**: ~$0.15 per 1M input tokens
- **Set Usage Limits**: In OpenAI dashboard to prevent overcharges

## Support & Resources

- **Hugging Face Docs**: [huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- **MongoDB Atlas Docs**: [docs.atlas.mongodb.com](https://docs.atlas.mongodb.com/)

## Next Steps

After successful deployment:

1. **Update Frontend**: Point your frontend `VITE_API_BASE_URL` to your Space URL
2. **Create Admin User**: Use the `/auth/signup` endpoint to create first admin
3. **Test All Features**: Verify chat, history, students, analytics work
4. **Monitor Performance**: Check logs for errors and slow requests
5. **Set Up Monitoring**: Consider application monitoring tools

## Example Frontend Configuration

Update your frontend `.env`:
```env
VITE_API_BASE_URL=https://YOUR_USERNAME-ai-campus-admin-backend.hf.space
```

---

**Deployment Complete! 🎉**

Your AI Campus Admin backend is now live on Hugging Face Spaces!

API URL: `https://YOUR_USERNAME-ai-campus-admin-backend.hf.space`  
API Docs: `https://YOUR_USERNAME-ai-campus-admin-backend.hf.space/docs`

