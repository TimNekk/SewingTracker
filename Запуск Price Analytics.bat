call cd /D %0\..
call venv\Scripts\activate.bat
call python %0\..\app.py mode=update
pause