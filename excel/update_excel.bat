call cd /D %0\..\..
call "venv\Scripts\activate.bat"
call python app.py mode=update market=%1
call "excel\input.xlsm"