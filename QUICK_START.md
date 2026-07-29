# 🚀 Quick Start Guide - AI Interview Platform

## Current Status
✅ **Backend Running:** http://127.0.0.1:5000  
✅ **Frontend Running:** http://localhost:3001  
✅ **All APIs Connected**  
✅ **Zero TypeScript Errors**  
✅ **CORS Configured**

---

## 📱 Access the Application

### Frontend
Open your browser and go to:
```
http://localhost:3001
```

### Backend API Documentation
```
http://127.0.0.1:5000/docs
```

---

## 🎯 Quick Test Flow

### 1. Register & Login
1. Click **"Register"** at http://localhost:3001/register
2. Fill in:
   - Name: `John Doe`
   - Email: `john@example.com`
   - Password: `password123`
3. Click **"Register"**
4. You'll be redirected to login
5. Login with your credentials

### 2. Upload Resume
1. Go to **"Resume"** page (sidebar)
2. Click **"Upload Resume"**
3. Select a PDF file
4. Click **"Analyze with AI"** to get resume analysis

### 3. Technical Interview
1. From Resume page, click **"Generate Interview"**
2. Select:
   - Role: `Software Engineer`
   - Difficulty: `Medium`
   - Questions: `5`
3. Click **"Generate"**
4. Click **"Start Interview"**
5. Answer questions one by one
6. View feedback after each answer
7. Click **"Finish"** when done
8. View your detailed report

### 4. Coding Interview
1. Go to **"Coding Interview"** page
2. Click **"New Coding Interview"**
3. Select:
   - Role: `Software Engineer`
   - Company: `Google`
   - Language: `Python` (or your preferred language)
   - Difficulty: `Medium`
   - Questions: `3`
4. Click **"Create"**
5. Start solving problems in Monaco editor
6. Submit each solution
7. See test results immediately
8. Finish and view AI-generated report

### 5. View Dashboard
1. Go to **"Dashboard"** (home icon in sidebar)
2. See your statistics:
   - Total interviews
   - Coding sessions
   - Average score
   - Highest score
3. View performance chart
4. Check topic analysis

### 6. Generate Learning Roadmap
1. Go to **"Dashboard"**
2. Click **"Skill Analysis"** tab
3. Click **"Generate Skill Report"** (requires completed interviews)
4. Click **"Generate Roadmap"**
5. View your personalized learning plan

### 7. Check History & Leaderboard
1. Go to **"History"** page to see all interviews
2. Go to **"Leaderboard"** to see rankings
3. Filter by date, type, score, etc.

### 8. AI Chat
1. Go to **"Chat"** page
2. Click **"New Chat"**
3. Ask questions about interview preparation
4. Get AI-powered advice

---

## 🛠️ If You Need to Restart

### Restart Backend
```bash
cd /home/chirag/Desktop/ai-interview-platform/Backend
docker compose restart
```

### Restart Frontend
```bash
cd /home/chirag/Desktop/ai-interview-platform/frontend
# Stop current dev server: Ctrl+C
npm run dev
```

---

## 📊 Check Backend Health

### Quick Health Check
```bash
curl http://127.0.0.1:5000/health
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected",
  "redis": "connected"
}
```

### View Docker Containers
```bash
docker ps
```

You should see:
- `ai-interview-api` (Backend)
- `ai-interview-postgres` (Database)
- `ai-interview-redis` (Cache)

---

## 🐛 Troubleshooting

### Frontend Issues

**Issue: "Cannot GET /"**
- **Solution:** Frontend dev server not running
- **Fix:** `cd frontend && npm run dev`

**Issue: "Network Error" when calling APIs**
- **Solution:** Backend not running or CORS issue
- **Fix:** Check backend is at http://127.0.0.1:5000

**Issue: "401 Unauthorized" on every request**
- **Solution:** JWT token expired or invalid
- **Fix:** Logout and login again

### Backend Issues

**Issue: Backend not responding**
- **Solution:** Docker containers not running
- **Fix:** `cd Backend && docker compose up -d`

**Issue: Database connection error**
- **Solution:** PostgreSQL container not ready
- **Fix:** `docker compose restart postgres`

**Issue: "ModuleNotFoundError" in logs**
- **Solution:** Python dependencies missing in container
- **Fix:** Rebuild container: `docker compose up -d --build`

---

## 📝 Default Credentials

### Test User (if pre-seeded)
```
Email: admin@example.com
Password: admin123
```

If not seeded, register a new user as shown above.

---

## 🔍 View Backend Logs

```bash
cd /home/chirag/Desktop/ai-interview-platform/Backend
docker compose logs -f api
```

Press `Ctrl+C` to stop viewing logs.

---

## 📂 Important Files

### Frontend
- **Environment:** `frontend/.env`
- **Config:** `frontend/vite.config.ts`
- **Styles:** `frontend/src/index.css`
- **API Client:** `frontend/src/api/client.ts`

### Backend
- **Main App:** `Backend/app/main.py`
- **Environment:** `Backend/.env`
- **Docker:** `Backend/docker-compose.yml`
- **Database:** PostgreSQL in Docker

---

## 🎨 UI Features to Try

### Dark Theme
- Default theme is dark
- Professional colors inspired by LeetCode
- No bright "LGBT+ colors" as requested

### Animations
- Page transitions (Framer Motion)
- Button hover effects
- Card animations
- Loading spinners
- Toast notifications

### Responsive Design
- Try resizing browser window
- Works on mobile, tablet, desktop

---

## 📚 Additional Documentation

1. **API Endpoints:** See `API_ENDPOINTS_VERIFICATION.md`
2. **Complete Setup:** See `FRONTEND_SETUP_COMPLETE.md`
3. **Backend API Docs:** http://127.0.0.1:5000/docs

---

## ✅ Verification Checklist

Before testing, verify:
- [ ] Backend running at http://127.0.0.1:5000
- [ ] Frontend running at http://localhost:3001
- [ ] Docker containers healthy: `docker ps`
- [ ] `.env` file exists in `frontend/` directory
- [ ] No console errors in browser DevTools
- [ ] Backend health check passes

---

## 🎯 Feature Highlights

### What Makes This Platform Special

1. **AI-Powered Everything**
   - Resume analysis
   - Interview question generation
   - Real-time answer evaluation
   - Skill gap analysis
   - Learning roadmap creation

2. **Complete Interview Suite**
   - Behavioral/technical questions
   - Coding challenges with live editor
   - Multiple languages supported
   - Instant feedback

3. **Comprehensive Analytics**
   - Performance tracking
   - Topic-wise analysis
   - Progress visualization
   - Historical data

4. **Professional Design**
   - Clean, modern UI
   - Dark theme
   - Smooth animations
   - Responsive layout

---

## 🚀 Ready to Go!

Everything is set up and ready. Just open:

```
http://localhost:3001
```

And start your interview preparation journey! 🎉

---

## 💡 Tips

1. **Complete at least one interview** before generating skill report
2. **Upload a detailed resume** for better question generation
3. **Answer thoroughly** to get better AI feedback
4. **Check the dashboard regularly** to track progress
5. **Use the chat feature** for quick interview tips

---

## 📞 Need Help?

If you encounter any issues:
1. Check the troubleshooting section above
2. View backend logs: `docker compose logs -f api`
3. Check browser console for errors (F12)
4. Verify all services are running: `docker ps`

---

**Happy interviewing! 🚀**
