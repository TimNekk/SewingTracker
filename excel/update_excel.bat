call cd %0\..\..
call "venv\Scripts\activate.bat"
call python app.py mode=update_model market=%1
call "excel\input.xlsm"