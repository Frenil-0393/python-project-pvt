# Scoreclub Django Main Project

This is the main learning project using basic Python + Django.

## Setup commands
```powershell
cd project_dev/django_project
"D:/DDU/SEM - 4/SP/Project - Scoreclub/.venv/Scripts/python.exe" -m pip install -r requirements.txt
"D:/DDU/SEM - 4/SP/Project - Scoreclub/.venv/Scripts/python.exe" manage.py makemigrations
"D:/DDU/SEM - 4/SP/Project - Scoreclub/.venv/Scripts/python.exe" manage.py migrate
"D:/DDU/SEM - 4/SP/Project - Scoreclub/.venv/Scripts/python.exe" manage.py runserver
```

## Role flows implemented
- Register user with role (fan/organizer/media)
- Login with role validation
- Role-based dashboard access

## Day 2 + Day 3 modules implemented
- Organizer: schedule, scores, players
- Fan: timetable, live scores, stats, highlights
- Media: broadcast, highlights, press room
