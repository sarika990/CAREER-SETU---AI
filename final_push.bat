@echo off
git add .
git commit -m "SkillBridge AI: Final Hackathon Submission"
git branch -M main
git remote remove origin
git remote add origin "https://github.com/sachinyaduvanshi553-debug/CAREER-SETU---AI.git"
git push -u origin main
