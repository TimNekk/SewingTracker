call D:
call cd "D:\PyCharm Projects\sewing-tracker"
call "venv\Scripts\activate.bat"
call python app.py mode=update market=%1
call "excel\input.xlsm"