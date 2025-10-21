@echo off
echo Setting up Windows Task Scheduler for FitBUX News Curator...

REM Create a task that runs every 3 hours on weekdays
schtasks /create /tn "FitBUX News Curator" /tr "python C:\Users\JosephReinke\Desktop\ai-news-scrapper\run_agent.py" /sc hourly /mo 3 /sd 01/01/2025 /st 06:00 /f

echo Task created! The scheduler will now run automatically.
echo Check Windows Task Scheduler to see the task.
pause
