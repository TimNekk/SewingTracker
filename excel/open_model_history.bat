call cd %0\..\..
call "venv\Scripts\activate.bat"
call python app.py mode=model model=%1 market=%2