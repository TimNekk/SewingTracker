@echo off
echo Installing packages
pip install -r requirements.txt
cls
echo Done!
(
  echo python main.py
) > start.bat
echo start.bat was created (use it for running program)
pause