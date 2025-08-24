@echo off
echo =====================================
echo   CLASS TRACK SYSTEM - SETUP
echo =====================================
echo.
echo Installing Python dependencies...
pip install -r requirements.txt
echo.
echo Setting up Docker containers...
docker-compose up -d
echo.
echo Waiting for MySQL to initialize...
timeout /t 10 /nobreak > nul
echo.
echo Setup complete! You can now run start_app.bat
echo.
pause
