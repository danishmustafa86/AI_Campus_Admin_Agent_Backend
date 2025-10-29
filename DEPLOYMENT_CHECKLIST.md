# Hugging Face Spaces Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Files Ready
- [ ] `Dockerfile` created and tested
- [ ] `requirements.txt` with all dependencies
- [ ] `.dockerignore` to exclude unnecessary files
- [ ] All backend code files present
- [ ] `main.py` configured correctly

### 2. Environment Variables Prepared
- [ ] `OPENAI_API_KEY` - Get from OpenAI
- [ ] `MONGODB_URI` - Set up MongoDB Atlas
- [ ] `JWT_SECRET_KEY` - Generate strong secret (min 32 chars)
- [ ] `ALLOW_ORIGINS` - Add your frontend URL
- [ ] Optional: `ELEVENLABS_API_KEY` (if using voice)

### 3. MongoDB Atlas Setup
- [ ] Create MongoDB Atlas account
- [ ] Create free cluster (M0)
- [ ] Create database user with read/write access
- [ ] Add IP whitelist: `0.0.0.0/0` (allow from anywhere)
- [ ] Get connection string
- [ ] Create database: `ai_campus`
- [ ] Test connection locally

### 4. Hugging Face Space Created
- [ ] Create account on Hugging Face
- [ ] Create new Space (Docker SDK)
- [ ] Choose appropriate visibility (Public/Private)
- [ ] Note your Space URL

## 📤 Deployment Steps

### Step 1: Upload Files

#### Option A: Git (Recommended)
```bash
# Clone your Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
cd SPACE_NAME

# Copy backend files
cp -r /path/to/backend/* .

# Remove unnecessary files
rm -rf __pycache__ .env

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

#### Option B: Web Interface
1. Go to your Space page
2. Click "Files" tab
3. Upload all files from `backend/` folder
4. Commit changes

### Step 2: Configure Secrets

On your Space Settings page, add these secrets:

```
OPENAI_API_KEY=sk-your-key-here
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
JWT_SECRET_KEY=your-super-secret-key-min-32-characters
MONGODB_DB=ai_campus
ENVIRONMENT=production
ALLOW_ORIGINS=https://your-frontend-url.com
```

### Step 3: Wait for Build
- [ ] Check "Logs" tab for build progress
- [ ] Wait for "Build successful" message (5-10 minutes)
- [ ] Space automatically starts after build

### Step 4: Test Deployment

Test these endpoints:

```bash
# Health check
curl https://YOUR_USERNAME-SPACE_NAME.hf.space/health

# API docs (open in browser)
https://YOUR_USERNAME-SPACE_NAME.hf.space/docs

# Test signup
curl -X POST https://YOUR_USERNAME-SPACE_NAME.hf.space/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

### Step 5: Create Admin User

Use the `/auth/signup` endpoint to create your first admin user, then manually update the database to set `is_admin: true`.

## 🔍 Post-Deployment Verification

### API Endpoints Check
- [ ] GET `/health` returns `{"status": "ok"}`
- [ ] GET `/docs` shows Swagger UI
- [ ] POST `/auth/signup` creates user successfully
- [ ] POST `/auth/login` returns JWT token
- [ ] GET `/auth/me` returns user data (with token)
- [ ] POST `/chat/authenticated` returns AI response
- [ ] GET `/students/` lists students
- [ ] GET `/analytics/` returns analytics data

### Security Check
- [ ] CORS configured correctly (frontend can access)
- [ ] JWT tokens working
- [ ] Protected endpoints require authentication
- [ ] Passwords are hashed (not stored in plain text)
- [ ] API keys not exposed in logs

### Performance Check
- [ ] API responds within 3 seconds
- [ ] Chat streaming works smoothly
- [ ] Database queries are fast
- [ ] No memory leaks after sustained use

## 🛠️ Troubleshooting

### Build Fails
**Check:**
- All files uploaded correctly
- No syntax errors in Dockerfile
- All dependencies in requirements.txt
- Python version compatibility

**Fix:**
- Review build logs
- Test Dockerfile locally
- Verify file structure

### App Won't Start
**Check:**
- Environment variables set correctly
- MongoDB connection string valid
- OpenAI API key valid
- Port 7860 not hardcoded (should use from env)

**Fix:**
- Double-check all secrets
- Test MongoDB connection separately
- Review application logs

### MongoDB Connection Fails
**Check:**
- IP whitelist includes 0.0.0.0/0
- Database user has correct permissions
- Connection string format correct
- Network access configured

**Fix:**
- Update MongoDB Atlas network access
- Verify credentials
- Test connection with MongoDB Compass

### CORS Errors from Frontend
**Check:**
- ALLOW_ORIGINS includes your frontend URL
- Format: `https://domain.com` (no trailing slash)
- Multiple origins separated by commas

**Fix:**
- Update ALLOW_ORIGINS secret
- Rebuild Space
- Clear browser cache

### AI Chat Not Working
**Check:**
- OPENAI_API_KEY is valid
- OpenAI account has credits
- Request format is correct
- Rate limits not exceeded

**Fix:**
- Verify API key in OpenAI dashboard
- Check usage limits
- Review error messages in logs

## 📊 Monitoring

### Things to Monitor
- [ ] API response times
- [ ] Error rates
- [ ] MongoDB usage
- [ ] OpenAI API costs
- [ ] Storage usage
- [ ] Active users

### Tools
- Hugging Face Spaces logs (built-in)
- MongoDB Atlas monitoring
- OpenAI usage dashboard
- Custom logging in application

## 🔄 Updating Your Deployment

### To Update Code:
```bash
# Make changes locally
git add .
git commit -m "Description of changes"
git push
# Space automatically rebuilds
```

### To Update Secrets:
1. Go to Space Settings
2. Update secret value
3. Space automatically restarts

### To Roll Back:
```bash
git revert HEAD
git push
# Or use Hugging Face web interface to revert commit
```

## 📝 Important Notes

1. **Free Tier Limitations**:
   - CPU-only instances (slower AI responses)
   - May sleep after inactivity
   - Limited resources
   - Consider upgrading for production

2. **Security Best Practices**:
   - Never commit secrets to repository
   - Use strong, unique JWT_SECRET_KEY
   - Rotate API keys regularly
   - Monitor for unauthorized access
   - Keep dependencies updated

3. **Cost Management**:
   - Monitor OpenAI API usage
   - Set usage limits in OpenAI dashboard
   - Use MongoDB free tier initially
   - Upgrade only when necessary

4. **Performance Tips**:
   - Use MongoDB indexes for queries
   - Implement caching where possible
   - Optimize AI prompts for speed
   - Monitor response times

## ✨ Success Criteria

Your deployment is successful when:
- ✅ All API endpoints respond correctly
- ✅ Frontend can connect without CORS errors
- ✅ Users can sign up and login
- ✅ AI chat works and streams responses
- ✅ Student management CRUD operations work
- ✅ Chat history is saved and retrieved
- ✅ Analytics display correctly
- ✅ No critical errors in logs
- ✅ Response times are acceptable

## 🎉 Post-Deployment

After successful deployment:
1. Update frontend `.env` with Space URL
2. Test all features from frontend
3. Create documentation for users
4. Set up monitoring and alerts
5. Plan for scaling if needed
6. Celebrate! 🎊

---

**Need Help?**
- Hugging Face Community: [discuss.huggingface.co](https://discuss.huggingface.co/)
- FastAPI Discord: [discord.gg/fastapi](https://discord.gg/fastapi)
- Check logs for error messages
- Review documentation again

